from typing import Dict, Optional, Any
from pydantic import BaseModel


class ReportModel(BaseModel):
    id: str
    report: Dict[str, Any]
    name: str
    description: str
    timestamp: str
    target_device: Dict[str, Any]


class ScanRequestModel(BaseModel):
    scope: str
    details: Dict[str, Any]
    name: Optional[str]
    description: Optional[str]
    timestamp: Optional[str]
    target_device: Optional[Dict[str, Any]]


class CredentialModel(BaseModel):
    credential: str
    credential_type: str  # ["Others", "Email", "Username", "Phone"]
    leaked: bool
    leaked_date: Optional[str]
