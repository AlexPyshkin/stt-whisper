from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class GateWayDTO(BaseModel):
    serviceName: str
    jobName: str
    statusCode: int
    success: bool
    errorMessage: Optional[str]
    responseBodyBatch: List[str]
    job: Optional[Dict[str, Any]] = None
