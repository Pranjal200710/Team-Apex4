# MediCare conversational healthcare assistant (prototype)

This is a safe, fully mock FastAPI demo. It contains no real patient information, payment connection, hospital system, or production authentication.

## What it demonstrates

- Backend age check: `P001` (John Doe, age 67) automatically opens the assistant after login.
- Rule-based intent detection; no API key or external LLM is used.
- Every chatbot request passes through `SecurityGateway`; the chatbot never calls the data layer.
- Deterministic risk engine and configurable policy: `HIGH` / `CRITICAL` actions need caregiver approval.
- Caregiver dashboard uses lightweight 3-second polling.
- Mock record deletion and mock payment only happen **after approval**.
- Append-only, in-memory audit records exposed at `/api/audit`.

## Run in GitHub Codespaces

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Forward port **8000**, then open these URLs:

- `https://<your-forwarded-url>/patient/` — patient chatbot
- `https://<your-forwarded-url>/caregiver/` — caregiver approval console
- `https://<your-forwarded-url>/docs` — interactive REST API documentation

## Demo credentials and flow

- Patient: `P001` — John Doe (67), caregiver: `C001`
- Caregiver console: C001 is already selected in this mock UI.

In the patient page, try:

```text
I want to delete my MRI report.
Pay ₹2500 for my consultation.
Show my prescription.
Show my payment history.
```

Open the caregiver page in another tab, approve or deny the pending request, then refresh/use the endpoints to see the outcome. `DELETE_REPORT` removes the mock report only after approval; a payment is added to mock payment history only after approval.

## Integration points

Your existing payments dashboard can call `GET /api/patient/P001/payments`. To submit a payment authorization, call `POST /api/payment/request` with `patient_id`, `action: "MAKE_PAYMENT"`, `amount`, and `purpose`. The caregiver dashboard uses `GET /api/security/requests/{caregiver_id}` and the approve/deny endpoints. In a real system, replace mock login, in-memory data and polling with authenticated backend services, a protected database, and WebSockets.
