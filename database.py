"""Mock in-memory data only. Production code should use a protected database service."""
from datetime import datetime

class MockDatabase:
    def __init__(self):
        self.patients={"P001":{"patient_id":"P001","name":"John Doe","age":67,"caregiver_id":"C001"},"P002":{"patient_id":"P002","name":"Maya Patel","age":42,"caregiver_id":"C002"}}
        self.reports={"P001":[{"name":"MRI Report","date":"12 Aug 2026","summary":"No acute abnormality."},{"name":"Blood Test","date":"03 Aug 2026","summary":"Results within expected range."},{"name":"X-Ray","date":"21 Jul 2026","summary":"No fracture identified."}]}
        self.prescriptions={"P001":[{"medicine":"Metformin 500 mg","instructions":"Once daily after meals"},{"medicine":"Vitamin D3","instructions":"Once weekly"}]}
        self.appointments={"P001":[{"doctor":"Dr. Smith","date":"30 Aug 2026","time":"4:00 PM","purpose":"Follow-up consultation"}]}
        self.payments={"P001":[{"transaction_id":"TXN-1001","from":"Mock HDFC •••• 4921","to":"Green Valley Hospital","amount":"₹1,250.00","date":"12 Aug 2026","purpose":"Cardiology consultation"}]}
    def patient(self, patient_id): return self.patients.get(patient_id)
    def execute(self, request):
        p=request.patient_id; action=request.action
        if action=="VIEW_REPORT": return {"reports":self.reports.get(p,[])}
        if action=="VIEW_PRESCRIPTION": return {"prescriptions":self.prescriptions.get(p,[])}
        if action=="VIEW_PAYMENT": return {"payments":self.payments.get(p,[])}
        if action=="VIEW_DOCTOR": return {"doctor":{"name":"Dr. Smith","specialty":"Cardiology","phone":"+91 00000 00000 (mock)"}}
        if action=="DELETE_REPORT":
            before=len(self.reports.get(p,[])); self.reports[p]=[r for r in self.reports.get(p,[]) if r["name"].lower()!=request.resource.lower()]
            return {"message":f"{request.resource} deleted from mock records.","changed":len(self.reports[p])<before}
        if action=="MAKE_PAYMENT":
            transaction={"transaction_id":f"TXN-{1000+len(self.payments.get(p,[]))+1}","from":"Mock HDFC •••• 4921","to":"Green Valley Hospital","amount":f"₹{request.amount or 0:,.2f}","date":datetime.now().strftime("%d %b %Y"),"purpose":request.purpose or "Healthcare payment"}; self.payments.setdefault(p,[]).insert(0,transaction)
            return {"message":"Mock payment marked successful.","payment":transaction}
        if action=="BOOK_APPOINTMENT": return {"message":"Mock appointment booked with Dr. Smith."}
        if action=="EDIT_APPOINTMENT": return {"message":"Mock appointment change completed."}
        if action=="EDIT_REPORT": return {"message":"Mock report edit completed."}
        return {"message":"I can help you view reports, prescriptions, appointments, payments, or doctor details."}
