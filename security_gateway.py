"""The chatbot never calls MockDatabase directly; all actions enter through this gateway."""
from datetime import datetime, timezone
from uuid import uuid4
from .models import RiskLevel, ApprovalStatus, ApprovalRequest, AuditRecord

class RiskEngine:
    RISKS={"GENERAL_HELP":RiskLevel.LOW,"VIEW_DOCTOR":RiskLevel.LOW,"BOOK_APPOINTMENT":RiskLevel.MEDIUM,"VIEW_REPORT":RiskLevel.HIGH,"VIEW_PRESCRIPTION":RiskLevel.HIGH,"VIEW_PAYMENT":RiskLevel.HIGH,"EDIT_APPOINTMENT":RiskLevel.HIGH,"EDIT_REPORT":RiskLevel.CRITICAL,"DELETE_REPORT":RiskLevel.CRITICAL,"MAKE_PAYMENT":RiskLevel.CRITICAL}
    def assess(self, action): return self.RISKS.get(action, RiskLevel.HIGH)
class PolicyEngine:
    def __init__(self, approval_risks=None): self.approval_risks=approval_risks or {RiskLevel.HIGH,RiskLevel.CRITICAL}
    def requires_approval(self,risk): return risk in self.approval_risks
class AuditLogger:
    def __init__(self): self.records=[]
    def append(self, request, patient, risk, approval, executed): self.records.append(AuditRecord(timestamp=datetime.now(timezone.utc),patient_id=request.patient_id,caregiver_id=patient["caregiver_id"],requested_action=request.action,resource=request.resource,risk_level=risk,approval_status=approval,executed_status=executed))
class CaregiverApprovalService:
    def __init__(self): self.requests={}
    def create(self, action, patient, risk):
        item=ApprovalRequest(id=str(uuid4()),patient_id=action.patient_id,patient_name=patient["name"],caregiver_id=patient["caregiver_id"],action=action.action,resource=action.resource,reason=action.reason,risk_level=risk,status=ApprovalStatus.PENDING,created_at=datetime.now(timezone.utc),amount=action.amount,purpose=action.purpose); self.requests[item.id]={"approval":item,"action":action}; return item
    def for_caregiver(self, caregiver_id): return [x["approval"] for x in self.requests.values() if x["approval"].caregiver_id==caregiver_id]
class SecurityGateway:
    def __init__(self, database): self.database=database; self.risk=RiskEngine(); self.policy=PolicyEngine(); self.approvals=CaregiverApprovalService(); self.audit=AuditLogger()
    def submit(self, action):
        patient=self.database.patient(action.patient_id)
        if not patient: raise ValueError("Unknown patient ID")
        risk=self.risk.assess(action.action)
        if self.policy.requires_approval(risk):
            approval=self.approvals.create(action,patient,risk); self.audit.append(action,patient,risk,ApprovalStatus.PENDING,False); return {"status":"PENDING_APPROVAL","risk":risk,"approval":approval}
        result=self.database.execute(action); self.audit.append(action,patient,risk,ApprovalStatus.NOT_REQUIRED,True); return {"status":"EXECUTED","risk":risk,"result":result}
    def decide(self, request_id, caregiver_id, approved):
        entry=self.approvals.requests.get(request_id)
        if not entry: raise ValueError("Approval request not found")
        item,action=entry["approval"],entry["action"]
        if item.caregiver_id!=caregiver_id: raise ValueError("Caregiver is not authorized for this request")
        if item.status!=ApprovalStatus.PENDING: raise ValueError("This request has already been decided")
        patient=self.database.patient(action.patient_id); item.status=ApprovalStatus.APPROVED if approved else ApprovalStatus.DENIED
        if approved: item.result=self.database.execute(action).get("message","Operation completed"); self.audit.append(action,patient,item.risk_level,item.status,True)
        else: item.result="Operation denied; no records were changed."; self.audit.append(action,patient,item.risk_level,item.status,False)
        return item
