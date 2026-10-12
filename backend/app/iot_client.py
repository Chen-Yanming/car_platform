import asyncio
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

from .config import Settings


class IoTClient:
  """向汇川物联网平台写寄存器的简单客户端。

  当前实现支持两种模式：
  1. mock 模式：仅把寄存器值缓存在内存，方便前后端联调。
  2. 实际模式：直接通过 Modbus 连接网关，读写寄存器。
  """

  def __init__(self, settings: Settings):
    self.settings = settings
    self._history: Dict[str, Dict[str, Any]] = {}
    # mock 模式下用于持久化调试寄存器值的文件
    logs_dir = Path(__file__).resolve().parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    self._mock_file = logs_dir / "mock_registers.json"
    self._mock_file_mtime = 0  # 记录文件最后修改时间，用于检测文件是否被外部修改
    # 启动时尝试从文件恢复历史值，便于调试时多次重启
    self._reload_mock_file()

  def _reload_mock_file(self) -> None:
    """从文件重新加载 mock 寄存器值"""
    if self._mock_file.exists():
      try:
        # 检查文件是否被修改
        current_mtime = self._mock_file.stat().st_mtime
        if current_mtime != self._mock_file_mtime:
          data = json.loads(self._mock_file.read_text(encoding="utf-8"))
          if isinstance(data, dict):
            # 更新内存缓存，保留文件中的所有值
            self._history.update(data)
            self._mock_file_mtime = current_mtime
      except Exception:
        # 文件内容异常时忽略，使用现有缓存
        pass

  def _record_cache(self, action: str, register: dict, value: Any) -> None:
    self._history[action] = {
      "action": action,
      "address": register["address"],
      "name": register.get("name"),
      "value": value,
    }

  async def write_register(self, action: str, register: dict, value: Any) -> Dict[str, Any]:
    register_key = register["address"]
    if not self.settings.use_modbus:
      self._record_cache(action, register, value)
      # 调试模式下，把模拟寄存器的当前值写入本地文件，便于排查
      try:
        self._mock_file.write_text(
          json.dumps(self._history, ensure_ascii=False, indent=2),
          encoding="utf-8",
        )
      except Exception:
        # 写文件失败不影响核心流程
        pass
      return {
        "mode": "mock",
        "address": register_key,
        "value": value,
      }

    addr_info = self._parse_modbus_address(register)

    def _write():
      unit_id = addr_info["unit_id"]  # 使用环境变量中配置的站号
      client = ModbusTcpClient(self.settings.gateway_ip, port=self.settings.gateway_port)
      try:
        client.connect()
        data_type = str(register.get("data_type", "")).lower()
        # 允许在寄存器配置中覆盖大小端；默认 BIG + LITTLE（现场确认大多数 Real 为此组合）
        byteorder = Endian[str(register.get("byteorder", "BIG")).upper()]
        wordorder = Endian[str(register.get("wordorder", "LITTLE")).upper()]
        if addr_info["mode"] == "coil":
          client.write_coil(addr_info["address"], bool(value), unit=unit_id)
        elif addr_info["mode"] == "holding_bit":
          current = client.read_holding_registers(addr_info["address"], 1, unit=unit_id).registers[0]
          mask = 1 << addr_info["bit"]
          if bool(value):
            current |= mask
          else:
            current &= ~mask
          client.write_register(addr_info["address"], current, unit=unit_id)
        elif addr_info["mode"] == "holding":
          if data_type in {"real", "float"}:
            builder = BinaryPayloadBuilder(byteorder=byteorder, wordorder=wordorder)
            builder.add_32bit_float(float(value))
            registers = builder.to_registers()
            client.write_registers(addr_info["address"], registers, unit=unit_id)
          else:
            client.write_register(addr_info["address"], int(float(value)) & 0xFFFF, unit=unit_id)
        else:
          raise ValueError(f"Unsupported modbus mode: {addr_info['mode']}")
      finally:
        client.close()

    await asyncio.to_thread(_write)
    self._record_cache(action, register, value)
    return {
      "mode": "modbus",
      "address": register_key,
      "modbus_address": addr_info["address"],
      "value": value,
    }

  async def pulse(self, action: str, register: dict, value: Any, duration_ms: int = 200) -> Dict[str, Any]:
    """写入一个脉冲值后再复位。"""
    result = await self.write_register(action, register, value)
    await asyncio.sleep(duration_ms / 1000)
    await self.write_register(
      action,
      register,
      0 if isinstance(value, (int, float)) else False,
    )
    return result

  def get_cache(self) -> List[Dict[str, Any]]:
    return list(self._history.values())

  def get_action_value(self, action: str) -> Any:
    record = self._history.get(action)
    return record["value"] if record else None

  async def read_register(self, action: str, register: dict) -> Any:
    """读取寄存器值，仅读取不修改。
    
    此方法仅从PLC读取寄存器值，不会修改任何寄存器的值。
    _record_cache 仅用于缓存读取的值到内存，不会写入PLC。
    """
    if not self.settings.use_modbus:
      # 在 mock 模式下，每次读取时检查文件是否被修改，如果是则重新加载
      self._reload_mock_file()
      cached = self._history.get(action)
      return cached["value"] if cached else 0

    addr_info = self._parse_modbus_address(register)

    def _read():
      unit_id = addr_info["unit_id"]  # 使用环境变量中配置的站号
      client = ModbusTcpClient(self.settings.gateway_ip, port=self.settings.gateway_port)
      try:
        client.connect()
        data_type = str(register.get("data_type", "")).lower()
        byteorder = Endian[str(register.get("byteorder", "BIG")).upper()]
        wordorder = Endian[str(register.get("wordorder", "LITTLE")).upper()]
        if data_type == "bool":
          if addr_info["mode"] == "coil":
            rr = client.read_coils(addr_info["address"], 1, unit=unit_id)
            return bool(rr.bits[0])
          rr = client.read_holding_registers(addr_info["address"], 1, unit=unit_id)
          value = rr.registers[0]
          return bool((value >> addr_info["bit"]) & 1)
        elif data_type in {"int", "int16"}:
          rr = client.read_holding_registers(addr_info["address"], 1, unit=unit_id)
          return self._to_signed(rr.registers[0], 16)
        elif data_type in {"int32"}:
          rr = client.read_holding_registers(addr_info["address"], 2, unit=unit_id)
          high, low = rr.registers
          value = (high << 16) | low
          return self._to_signed(value, 32)
        elif data_type in {"real", "float"}:
          rr = client.read_holding_registers(addr_info["address"], 2, unit=unit_id)
          decoder = BinaryPayloadDecoder.fromRegisters(rr.registers, byteorder=byteorder, wordorder=wordorder)
          return round(decoder.decode_32bit_float(), 6)
        else:
          rr = client.read_holding_registers(addr_info["address"], 1, unit=unit_id)
          return rr.registers[0]
      finally:
        client.close()

    # 仅读取，不写入
    value = await asyncio.to_thread(_read)
    # 仅缓存到内存，不写入PLC
    self._record_cache(action, register, value)
    return value

  def _parse_modbus_address(self, register: dict) -> Dict[str, Optional[int]]:
    """解析 Modbus 地址格式，支持：
    - "1 M 40" 或 "M 40" -> 线圈地址40（忽略站号，使用环境变量中的站号）
    - "D1895.2" -> 保持寄存器1895，位2
    - "1 D 100" 或 "D 100" -> 保持寄存器100（忽略站号，使用环境变量中的站号）
    
    注意：所有站号都使用环境变量 MODBUS_UNIT_ID 中配置的值，地址字符串中的站号会被忽略。
    """
    address_str = str(register.get("address", "0")).strip()
    upper = address_str.upper()
    
    # 统一使用环境变量中配置的站号
    unit_id = self.settings.modbus_unit_id
    
    # 处理 "1 M 40" 或 "M 40" 格式（忽略站号部分）
    if "M" in upper and " " in upper:
      parts = address_str.replace("  ", " ").split()
      # 如果第一个部分是数字，可能是站号，忽略它，取最后一个数字作为地址
      if len(parts) >= 3 and parts[0].isdigit():
        # "1 M 40" 格式，忽略站号，只提取地址
        addr = int(parts[-1])
      else:
        # "M 40" 格式，只提取地址
        addr = int(parts[-1])
      return {"mode": "coil", "address": addr, "bit": None, "unit_id": unit_id}

    # 处理 "D1895.2" 格式（保持寄存器，带位号）
    match = re.match(r"D(\d+)(?:\.(\d+))?", upper)
    if match:
      addr = int(match.group(1))
      bit = match.group(2)
      if bit is not None:
        return {"mode": "holding_bit", "address": addr, "bit": int(bit), "unit_id": unit_id}
      return {"mode": "holding", "address": addr, "bit": None, "unit_id": unit_id}

    # 处理 "1 D 100" 或 "D 100" 格式（忽略站号部分）
    if "D" in upper and " " in upper:
      parts = address_str.replace("  ", " ").split()
      # 如果第一个部分是数字，可能是站号，忽略它，取最后一个数字作为地址
      if len(parts) >= 3 and parts[0].isdigit():
        # "1 D 100" 格式，忽略站号，只提取地址
        addr = int(parts[-1])
      else:
        # "D 100" 格式，只提取地址
        addr = int(parts[-1])
      return {"mode": "holding", "address": addr, "bit": None, "unit_id": unit_id}

    raise ValueError(f"Unsupported address format: {register.get('address')}")

  @staticmethod
  def _to_signed(value: int, bits: int) -> int:
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

