# MentalHealth Shield — POC

POC mínima (FastAPI + regras simples) para triagem de mensagens de bem‑estar/saúde mental.

## O que vem pronto
- API HTTP com `POST /ingest/email` para processar uma “mensagem” (simulação de e‑mail/form).
- Extração simples (tópicos, pessoas citadas, sentimento).
- Classificação de prioridade (P1–P4) por regras + heurísticas.
- Geração de:
  - resposta empática ao funcionário (mock),
  - briefing técnico para RH (mock),
  - criação de “ticket” (mock) salvo em `data/tickets.jsonl`.
- Logs de auditoria em `data/audit.jsonl`.
- Amostras de teste em `tests/samples.jsonl`.
- Dockerfile e docker-compose (opcionais).
- GitHub Actions para rodar um lint/test simples.

> **Atenção:** Esta POC é *mockada* (não envia e‑mail real nem cria ticket real). Integrações reais podem ser ligadas depois.

---

## Rodando localmente (sem Docker)
Requisitos: Python 3.10+

```bash
# 1) criar venv e instalar deps
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) copiar variáveis de ambiente (opcional nesta POC)
cp .env.example .env

# 3) subir a API
uvicorn app.main:app --reload

# 4) testar (terminal 2)
curl -X POST http://127.0.0.1:8000/ingest/email \
  -H "Content-Type: application/json" \
  -d @tests/p1_exemplo.json
```

Abra http://127.0.0.1:8000/docs para ver o Swagger.

Para ver “tickets” e auditoria:
```bash
tail -f data/tickets.jsonl data/audit.jsonl
```

## Rodando com Docker
```bash
docker build -t mentalhealth-shield-poc .
docker run --rm -p 8000:8000 -v $(pwd)/data:/app/data mentalhealth-shield-poc
# (Windows PowerShell) use ${PWD}/data no lugar de $(pwd)/data
```

Ou com docker-compose:
```bash
docker compose up --build
```

## Workflow básico
1. Cliente envia JSON simulando e‑mail para `/ingest/email`.
2. Serviço extrai entidades → classifica prioridade → gera respostas.
3. Serviço grava ticket/briefing/auditoria e retorna o resultado completo (JSON).

## Estrutura
```
app/
  main.py
  models.py
  nlp.py
  classifier.py
  templates.py
  orchestrator.py
  storage.py
tests/
  samples.jsonl
  p1_exemplo.json
.github/workflows/
  ci.yml
requirements.txt
Dockerfile
docker-compose.yml
.env.example
Makefile
```

## Próximos passos (de POC para MVP)
- Substituir mocks por integrações reais (SMTP, Jira/ServiceNow/Slack).
- Adicionar autenticação/RBAC e logging estruturado.
- Adicionar modelo ML (BERTimbau) e telemetria de precisão.
- Adicionar fila (RabbitMQ/SQS) se houver volume/picos.


---

## Envio de e-mail real (SMTP genérico)

1. Edite `.env` (baseado no `.env.example`):

```
SMTP_HOST=smtp.seuprovedor.com
SMTP_PORT=587
SMTP_USER=seu_usuario
SMTP_PASS=sua_senha
SMTP_STARTTLS=true
SEND_EMAILS=true
REPLY_FROM_EMAIL=bem-estar@empresa.com
```

2. Suba a API novamente:

```bash
uvicorn app.main:app --reload
```

3. Faça um POST no `/ingest/email`. Se estiver `SEND_EMAILS=true`, a POC **envia o e-mail de confirmação** para o `sender` informado (use um endereço seu para testar).
