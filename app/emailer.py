import os, smtplib, ssl
from email.message import EmailMessage
from typing import Optional

def _bool(env_value: Optional[str], default: bool=False) -> bool:
    if env_value is None:
        return default
    return env_value.strip().lower() in ("1","true","yes","on")

def send_email(to_addr: str, subject: str, body: str, from_addr: Optional[str]=None) -> dict:
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    use_starttls = _bool(os.getenv("SMTP_STARTTLS", "true"), True)
    from_addr = from_addr or os.getenv("REPLY_FROM_EMAIL", "no-reply@example.com")

    if not host:
        raise RuntimeError("SMTP_HOST não definido. Preencha seu .env")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=30) as server:
        server.ehlo()
        if use_starttls:
            server.starttls(context=context)
            server.ehlo()
        if user and password:
            server.login(user, password)
        server.send_message(msg)

    # Retornamos um dicionário simples; provedores SMTP genéricos não retornam message-id facilmente
    return {"status": "sent", "to": to_addr, "subject": subject}
