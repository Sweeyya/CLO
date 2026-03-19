from pydantic import BaseModel
from typing import Optional, Literal

Priority = Literal["P0","P1","P2","P3"]

class InferRequest(BaseModel):
    prompt: str
    priority: Priority = "P1"
    slaSeconds: int = 0
    allowDefer: bool = True
    maxTokensCap: Optional[int] = None
    region: Optional[str] = None

class InferQueued(BaseModel):
    requestId: str
    status: Literal["queued"] = "queued"
    etaUtc: Optional[str] = None

class InferResponse(BaseModel):
    requestId: str
    model_used: str
    output: str
    tokens_out: int
    ran_when_utc: str
    ran_where_region: str
    carbon_intensity_g_per_kwh: int
    baseline_model: str = "LARGE_NOW"
