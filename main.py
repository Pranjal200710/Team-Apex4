from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from .models import LoginRequest, ChatRequest, ActionRequest, DecisionRequest
from .database import MockDatabase
from .intent_detector import IntentDetector
from .security_gateway import SecurityGateway

app=FastAPI(title="MediCare Assistant Prototype",version="1.0.0")
db=MockDatabase(); detector=IntentDetector(); gateway=SecurityGateway(db)
ROOT=Path(__file__).resolve().parent.parent
app.mount("/patient",StaticFiles(directory=ROOT/"frontend"/"chatbot",html=True),name="patient-ui")
app.mount("/caregiver",StaticFiles(directory=ROOT/"frontend"/"caregiver",html=True),name="caregiver-ui")
def patient_or_404(patient_id):
    patient=db.patient(patient_id)
    if not patient: raise HTTPException(404,"Mock patient not found")
    return patient
@app.get("/")
def root(): return {"patient_chat":"/patient/","caregiver_dashboard":"/caregiver/","docs":"/docs"}
@app.post("/api/login")
def login(body:LoginRequest):
    p=patient_or_404(body.patient_id); return {"patient":p,"auto_open_chatbot":p["age"]>=60}
@app.post("/api/chat")
def chat(body:ChatRequest):
    patient_or_404(body.patient_id); action=detector.detect(body.patient_id,body.message); return handle(action)
@app.post("/api/action")
def action(body:ActionRequest): patient_or_404(body.patient_id); return handle(body)
@app.post("/api/payment/request")
def payment(body:ActionRequest):
    if body.action!="MAKE_PAYMENT": raise HTTPException(422,"action must be MAKE_PAYMENT")
    patient_or_404(body.patient_id); return handle(body)
def handle(action):
    try:
        response=gateway.submit(action)
        if response["status"]=="PENDING_APPROVAL": return {"message":f"This {action.action.replace('_',' ').lower()} requires caregiver approval. Your request is pending.","action":action.action,"risk":response["risk"],"status":response["status"],"approval_request_id":response["approval"].id}
        return {"message":response["result"].get("message","Request completed."),"action":action.action,"risk":response["risk"],"status":response["status"],"data":response["result"]}
    except ValueError as e: raise HTTPException(400,str(e))
@app.get("/api/security/requests/{caregiver_id}")
def requests(caregiver_id:str): return gateway.approvals.for_caregiver(caregiver_id)
@app.post("/api/security/requests/{request_id}/approve")
def approve(request_id:str,body:DecisionRequest): return decide(request_id,body.caregiver_id,True)
@app.post("/api/security/requests/{request_id}/deny")
def deny(request_id:str,body:DecisionRequest): return decide(request_id,body.caregiver_id,False)
def decide(request_id,caregiver_id,approved):
    try: return gateway.decide(request_id,caregiver_id,approved)
    except ValueError as e: raise HTTPException(400,str(e))
@app.get("/api/patient/{patient_id}/reports")
def reports(patient_id:str): patient_or_404(patient_id); return {"reports":db.reports.get(patient_id,[])}
@app.get("/api/patient/{patient_id}/prescriptions")
def prescriptions(patient_id:str): patient_or_404(patient_id); return {"prescriptions":db.prescriptions.get(patient_id,[])}
@app.get("/api/patient/{patient_id}/appointments")
def appointments(patient_id:str): patient_or_404(patient_id); return {"appointments":db.appointments.get(patient_id,[])}
@app.get("/api/patient/{patient_id}/payments")
def payments(patient_id:str): patient_or_404(patient_id); return {"payments":db.payments.get(patient_id,[])}
@app.get("/api/audit")
def audit(): return gateway.audit.records
