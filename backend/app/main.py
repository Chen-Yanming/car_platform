from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .iot_client import IoTClient
from .register_map import REGISTER_MAP
from .schemas import (
  RegisterReadRequest,
  RegisterReadResponse,
  RegisterWriteRequest,
  RegisterWriteResponse,
)
from .logger import get_register_logger

settings = get_settings()
client = IoTClient(settings)
register_logger = get_register_logger()
app = FastAPI(title="智能钻孔车后端", version="0.1.0")

allow_origins = ["*"]
if settings.mock_mode:
  allow_origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=allow_origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/health")
async def health():
  return {"status": "ok", "mock_mode": settings.mock_mode}


@app.post("/api/registers/write", response_model=RegisterWriteResponse)
async def write_register(payload: RegisterWriteRequest):
  register = REGISTER_MAP.get(payload.action)
  if not register:
    # 记录未找到的 action，便于调试
    register_logger.warning(
      "未找到寄存器映射: action=%s, 可用actions=%s",
      payload.action,
      list(REGISTER_MAP.keys())[:10]  # 只显示前10个，避免日志过长
    )
    raise HTTPException(status_code=404, detail=f"未找到对应的寄存器映射: {payload.action}")

  # 先记录日志，确保即使写入失败也能记录操作
  register_logger.info(
    "action=%s name=%s address=%s value=%s mode=%s",
    payload.action,
    register["name"],
    register["address"],
    payload.value,
    "mock" if settings.mock_mode else "iot",
  )
  # 确保日志立即刷新到文件
  for handler in register_logger.handlers:
    if hasattr(handler, 'flush'):
      handler.flush()

  data = await client.write_register(payload.action, register, payload.value)

  return RegisterWriteResponse(
    action=payload.action,
    register_name=register["name"],
    value=payload.value,
    message="指令已下发",
    payload=data if isinstance(data, dict) else None,
  )


@app.post("/api/registers/read", response_model=RegisterReadResponse)
async def read_registers(payload: RegisterReadRequest):
  """读取寄存器值，仅读取不修改。
  
  此接口仅从PLC读取寄存器值，不会修改任何寄存器的值。
  用于读取状态寄存器（如模式、初始化状态、报警状态等）用于前端显示。
  """
  values: Dict[str, Any] = {}
  for action in payload.actions:
    register = REGISTER_MAP.get(action)
    if not register:
      raise HTTPException(status_code=404, detail=f"未找到寄存器映射：{action}")
    # 仅读取，不写入
    result = await client.read_register(action, register)
    values[action] = result
  return RegisterReadResponse(values=values)


@app.get("/api/registers/cache")
async def read_cache():
  return {"items": client.get_cache()}

