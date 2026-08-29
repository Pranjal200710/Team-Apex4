from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field

class RiskLevel(str, Enum): LOW="LOW"; MEDIUM="MEDIUM"; HIGH="HIGH"; CRITICAL="CRITICAL"
class ApprovalStatus(str, Enum): NOT_REQUIRED="NOT_REQUIRED"; PENDING="PENDING"; APPROVED="APPROVED"; DENIED="DENIED"
class LoginRequest(BaseModel): patient_id: str
class ChatRequest(BaseModel): patient_id: str; message: str = Field(min_length=1, max_length=500)
class ActionRequest(BaseModel): patient_id: str; action: str; resource: str = "General request"; reason: str = "Requested through healthcare assistant"; amount: Optional[float] = Field(default=None, ge=0); purpose: Optional[str] = None; details: dict[str, Any] = Field(default_factory=dict)
class DecisionRequest(BaseModel): caregiver_id: str
class ApprovalRequest(BaseModel):
    id: str; patient_id: str; patient_name: str; caregiver_id: str; action: str; resource: str; reason: str; risk_level: RiskLevel; status: ApprovalStatus; created_at: datetime; amount: Optional[float] = None; purpose: Optional[str] = None; result: Optional[str] = None
class AuditRecord(BaseModel):
    timestamp: datetime; patient_id: str; caregiver_id: str; requested_action: str; resource: str; risk_level: RiskLevel; approval_status: ApprovalStatus; executed_status: bool
