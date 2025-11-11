from .models import EmailIn, Extracted, Classified, ProcessResult
from . import nlp
from .classifier import classify
from . import templates
from . import storage
from .emailer import send_email
import hashlib, os

def _employee_id_from_email(email: str) -> str:
    return hashlib.sha256(email.encode()).hexdigest()[:10].upper()

def _split_subject_body(preview: str):
    lines = preview.splitlines()
    if not lines:
        return "Mensagem recebida", preview
    first = lines[0].strip()
    subject = first.replace("Assunto:", "").strip() if first.lower().startswith("assunto") else first
    body = "\n".join(lines[1:]).strip()
    return subject, body

def process_email(email: EmailIn) -> ProcessResult:
    # 1) Extração
    topics = nlp.extract_topics(email.body)
    persons = nlp.extract_persons(email.body)
    sent = nlp.sentiment(email.body)
    urg = nlp.urgency_signals(email.body)
    extracted = Extracted(topics=topics, persons=persons, sentiment=sent, urgency_signals=urg)

    # 2) Classificação
    prio, score, rule_hits = classify(email.body)
    classified = Classified(priority=prio, score=score, rule_hits=rule_hits)

    # 3) Geração de artefatos (PREPARA TUDO ANTES DE ENVIAR)
    first_name = email.sender.split('@')[0].split('.')[0].capitalize()
    topic_hint = topics[0] if topics else "bem-estar"
    resp_preview = templates.email_employee(prio, first_name, topic_hint)

    summary = nlp.redact(email.body[:400])
    suggestion = "Encaminhar para Saúde Ocupacional" if prio in ("P1", "P2") else "Encaminhar para equipe responsável"
    employee_id = _employee_id_from_email(email.sender)

    briefing_text = templates.briefing(prio, employee_id, topics, sent, urg, summary, suggestion, score)

    # 3.1) Envio real de e-mail (opcional)
    if os.getenv("SEND_EMAILS", "false").strip().lower() in ("1", "true", "yes", "on"):
        subject, body = _split_subject_body(resp_preview)
        try:
            send_email(to_addr=email.sender, subject=subject, body=body)
        except Exception as e:
            # registra falha mas NÃO derruba a API
            storage.audit("email_send_error", {"employee_id": employee_id, "error": str(e)})

    # 4) “Criar ticket” (mock)
    ticket_id = storage.create_ticket(briefing_text, prio)

    # 5) Auditoria
    audit_id = storage.audit("process_email", {
        "employee_id": employee_id,
        "priority": prio,
        "score": score,
        "rule_hits": rule_hits
    })

    return ProcessResult(
        priority=prio,
        employee_email=email.sender,
        response_email_preview=resp_preview,
        briefing_preview=briefing_text,
        ticket_id=ticket_id,
        audit_id=audit_id,
        extracted=extracted,
        classified=classified,
        meta={"ticket_store": "data/tickets.jsonl", "audit_store": "data/audit.jsonl"}
    )
