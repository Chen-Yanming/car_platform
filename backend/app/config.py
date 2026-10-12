import os
from functools import lru_cache
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
  value = os.getenv(name)
  if value is None:
    return default
  return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
  api_prefix: str = "/api"
  mock_mode: bool = _get_bool("IOT_MOCK_MODE", True)
  request_timeout: float = float(os.getenv("REQUEST_TIMEOUT", 5))
  # Modbus 网关配置
  gateway_ip: str = os.getenv("GATEWAY_IP", "192.168.3.88")
  gateway_port: int = int(os.getenv("GATEWAY_PORT", "502"))
  modbus_unit_id: int = int(os.getenv("MODBUS_UNIT_ID", "1"))  # Modbus 站号/单元ID

  @property
  def use_modbus(self) -> bool:
    return not self.mock_mode and bool(self.gateway_ip and self.gateway_port)


@lru_cache
def get_settings() -> Settings:
  return Settings()

