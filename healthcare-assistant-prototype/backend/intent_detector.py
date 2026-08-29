"""Replace this deterministic prototype detector with an audited LLM adapter in production."""
import re
from .models import ActionRequest

class IntentDetector:
    def detect(self, patient_id: str, message: str) -> ActionRequest:
        text = message.lower()
        amount_match = re.search(r"(?:₹|rs\.?|inr\s*)\s*(\d+(?:\.\d{1,2})?)", text)
        if any(word in text for word in ["pay", "payment", "make a payment"]):
            amount = float(amount_match.group(1)) if amount_match else None
            purpose = re.sub(r".*?(?:for)\s+", "", message, flags=re.I).strip(" .") or "healthcare payment"
            return ActionRequest(patient_id=patient_id, action="MAKE_PAYMENT", resource="MOCK_PAYMENT", reason=message, amount=amount, purpose=purpose)
        if "delete" in text and any(x in text for x in ["report", "mri", "blood", "x-ray", "xray"]): return ActionRequest(patient_id=patient_id, action="DELETE_REPORT", resource=self._report(text), reason=message)
        if any(x in text for x in ["edit", "change", "update"]) and "report" in text: return ActionRequest(patient_id=patient_id, action="EDIT_REPORT", resource=self._report(text), reason=message)
        if any(x in text for x in ["show", "view", "see"]) and any(x in text for x in ["report", "mri", "blood", "x-ray", "xray"]): return ActionRequest(patient_id=patient_id, action="VIEW_REPORT", resource=self._report(text), reason=message)
        if any(x in text for x in ["prescription", "medicine", "medication"]): return ActionRequest(patient_id=patient_id, action="VIEW_PRESCRIPTION", resource="PRESCRIPTIONS", reason=message)
        if any(x in text for x in ["change appointment", "reschedule", "move appointment"]): return ActionRequest(patient_id=patient_id, action="EDIT_APPOINTMENT", resource="APPOINTMENT", reason=message, details={"requested_change":message})
        if "appointment" in text and any(x in text for x in ["book", "schedule"]): return ActionRequest(patient_id=patient_id, action="BOOK_APPOINTMENT", resource="APPOINTMENT", reason=message)
        if any(x in text for x in ["payment history", "payments", "transactions"]): return ActionRequest(patient_id=patient_id, action="VIEW_PAYMENT", resource="PAYMENT_HISTORY", reason=message)
        if any(x in text for x in ["doctor", "dr."]): return ActionRequest(patient_id=patient_id, action="VIEW_DOCTOR", resource="DOCTOR_DETAILS", reason=message)
        return ActionRequest(patient_id=patient_id, action="GENERAL_HELP", resource="HELP", reason=message)
    @staticmethod
    def _report(text: str) -> str:
        if "mri" in text: return "MRI Report"
        if "blood" in text: return "Blood Test"
        if "x-ray" in text or "xray" in text: return "X-Ray"
        return "Medical Report"
