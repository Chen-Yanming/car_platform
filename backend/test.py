from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

# 网关配置
GATEWAY_IP = "192.168.3.88"
GATEWAY_PORT = 502
MODBUS_UNIT_ID = 1
# 测试寄存器：D1574 和 D1931（均为 Real，占用 2 个寄存器）
# 注意：有的设备/网关地址从 0 起始，有的从 1 起始，下面会分别尝试。
D1574_START_ADDRESS_ZERO_BASE = 1573
D1574_START_ADDRESS_ONE_BASE = 1574
D1931_START_ADDRESS_ZERO_BASE = 1930
D1931_START_ADDRESS_ONE_BASE = 1931

def read_real_type(label: str, addrs: list[int]):
    """读取指定寄存器（Real）并测试地址与大小端组合。"""
    client = ModbusTcpClient(GATEWAY_IP, port=GATEWAY_PORT)
    try:
        if not client.connect():
            print(f"❌ 连接失败：无法访问网关 {GATEWAY_IP}:{GATEWAY_PORT}")
            return
        for addr in addrs:
            response = client.read_holding_registers(address=addr, count=2, unit=MODBUS_UNIT_ID)
            print(f"\n=== [{label}] 读取地址 {addr}，count=2 ===")
            if response.isError():
                print(f"❌ 读取失败：{response}")
                continue
            print(f"原始寄存器: {response.registers}")
            for bo in (Endian.BIG, Endian.LITTLE):
                for wo in (Endian.BIG, Endian.LITTLE):
                    dec = BinaryPayloadDecoder.fromRegisters(
                        response.registers, byteorder=bo, wordorder=wo
                    )
                    val = dec.decode_32bit_float()
                    print(f"byteorder={bo.name:<6} wordorder={wo.name:<6} => {val}")

    except ModbusException as e:
        print(f"❌ Modbus通信错误：{e}")
    except Exception as e:
        print(f"❌ 脚本运行错误：{e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("=== Modbus D1574 (Real型) 只读测试脚本 ===")
    # 读取 D1574
    read_real_type("D1574", [D1574_START_ADDRESS_ZERO_BASE, D1574_START_ADDRESS_ONE_BASE])
    # 读取 D1931
    read_real_type("D1931", [D1931_START_ADDRESS_ZERO_BASE, D1931_START_ADDRESS_ONE_BASE])

    # 简单写入-读取验证（可按需取消注释）
    # def write_and_read(val: float):
    #     client = ModbusTcpClient(GATEWAY_IP, port=GATEWAY_PORT)
    #     try:
    #         if not client.connect():
    #             print("连接失败，写入未执行")
    #             return
    #         for addr in (D1574_START_ADDRESS_ZERO_BASE, D1574_START_ADDRESS_ONE_BASE,
    #                      D1931_START_ADDRESS_ZERO_BASE, D1931_START_ADDRESS_ONE_BASE):
    #             # 写入使用 BIG/LITTLE
    #             b = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    #             b.add_32bit_float(val)
    #             regs = b.to_registers()
    #             client.write_registers(addr, regs, unit=MODBUS_UNIT_ID)
    #             # 立即读回并用 BIG/LITTLE 解码
    #             resp = client.read_holding_registers(addr, 2, unit=MODBUS_UNIT_ID)
    #             d = BinaryPayloadDecoder.fromRegisters(
    #                 resp.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE
    #             )
    #             back = d.decode_32bit_float()
    #             print(f"[写后读回] addr={addr} 写入={val} 读回={back} regs={resp.registers}")
    #     finally:
    #         client.close()
    #
    # write_and_read(-0.1)