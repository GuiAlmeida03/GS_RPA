from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .models import EmailIn
from .orchestrator import process_email

app = FastAPI(title="MentalHealth Shield — POC", version="0.1.0")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/ingest/email")
def ingest_email(payload: EmailIn):
    result = process_email(payload)
    return JSONResponse(content=result.model_dump(), status_code=200)
