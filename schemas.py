from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class JobDTO(BaseModel):
    id: Optional[int] = None
    jobTitle: Optional[str] = None
    countryCode: Optional[str] = None
    city: Optional[str] = None
    jobLocation: Optional[str] = None
    salary: Optional[str] = None
    jobUrl: Optional[str] = None
    totalCount: Optional[int] = None


class GateWayDTO(BaseModel):
    serviceName: str
    jobName: str
    statusCode: int
    success: bool
    errorMessage: Optional[str]
    responseBodyBatch: List[JobDTO]
    job: Optional[Dict[str, Any]] = None
