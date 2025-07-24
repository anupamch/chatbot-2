from pydantic import BaseModel
from typing import Dict, Any
class PromptRequest(BaseModel):
    prompt: str

class GenerationResponse(BaseModel):
    response: str
    error: bool = False

class SystemStatus(BaseModel):
    device_info: Dict[str, str]
    memory_usage: Dict[str, float]
    uptime_seconds: float | None = None
    model_info: Dict[str, Any]