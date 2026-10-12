from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RegisterWriteRequest(BaseModel):
  action: str = Field(..., description="动作标识，对应 register_map 中的键")
  value: Any = Field(..., description="下发的目标值")


class RegisterWriteResponse(BaseModel):
  action: str
  register_name: str
  value: Any
  message: str
  payload: Optional[dict] = None


class RegisterReadRequest(BaseModel):
  actions: List[str] = Field(..., description="需要读取的动作标识列表")


class RegisterReadResponse(BaseModel):
  values: Dict[str, Any]

