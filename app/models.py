from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal, Dict

Priority = Literal["P1", "P2", "P3", "P4"]

class EmailIn(BaseModel):
    sender: EmailStr = Field(..., description="E-mail do funcionário")
    subject: str
    body: str

class Extracted(BaseModel):
    topics: List[str]
    persons: List[str]
    sentiment: Literal["positivo", "neutro", "negativo", "muito_negativo"]
    urgency_signals: List[str]

class Classified(BaseModel):
    priority: Priority
    score: float
    rule_hits: List[str]

class Briefing(BaseModel):
    priority: Priority
    employee_id: str
    topics: List[str]
    sentiment: str
    urgency_signals: List[str]
    summary: str
    suggestion: str
    score: float

class ProcessResult(BaseModel):
    priority: Priority
    employee_email: EmailStr
    response_email_preview: str
    briefing_preview: str
    ticket_id: str
    audit_id: str
    extracted: Extracted
    classified: Classified
    meta: Dict[str, str] = {}
