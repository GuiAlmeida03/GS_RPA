import os, json, uuid, datetime as dt

DATA_DIR = os.path.abspath(os.path.join(os.getcwd(), 'data'))
os.makedirs(DATA_DIR, exist_ok=True)

def _path(name): return os.path.join(DATA_DIR, name)

def append_jsonl(filename: str, obj: dict) -> str:
    fp = _path(filename)
    with open(fp, 'a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    return fp

def create_ticket(briefing_text: str, priority: str) -> str:
    ticket_id = f"TICK-{uuid.uuid4().hex[:8]}"
    append_jsonl("tickets.jsonl", {
        "ticket_id": ticket_id,
        "priority": priority,
        "briefing": briefing_text,
        "created_at": dt.datetime.utcnow().isoformat() + 'Z'
    })
    return ticket_id

def audit(event: str, payload: dict) -> str:
    audit_id = f"AUD-{uuid.uuid4().hex[:8]}"
    append_jsonl("audit.jsonl", {
        "audit_id": audit_id,
        "event": event,
        "payload": payload,
        "ts": dt.datetime.utcnow().isoformat() + 'Z'
    })
    return audit_id
