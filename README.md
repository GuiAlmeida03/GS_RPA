# 🧠 MentalHealth Shield — POC
### Automação Inteligente para Triagem de Solicitações de Saúde Mental

**Autores:**
- Guilherme Almeida  
- Vitor Adauto  
- Matheus Barbosa

**Trabalho:** FIAP — Global Solution (Graduação)

---

## 📌 Objetivo da POC

Criar uma automação inteligente que:
- recebe e-mails de colaboradores
- analisa texto com NLP (regex — versão simplificada)
- classifica urgência (P1 → P4)
- gera resposta empática automática
- cria ticket local
- envia e-mail real via SMTP (Gmail)

---

## 🏗️ Arquitetura

```mermaid
flowchart LR
A[POST /ingest/email] --> B[NLP Extract]
B --> C[Classificação P1/P2/P3/P4]
C --> D[Gera e-mail para Funcionário]
C --> E[Gera Briefing Interno]
D --> F[SMTP SEND REAL]
E --> G[Audit + Ticket JSONL]
✅ Status da POC
Etapa	Resultado
FastAPI rodando local	✅
NLP básico funcionando	✅
Classificação P1–P4	✅
Geração de texto de resposta	✅
Envio real via SMTP Gmail	✅
Audit + Tickets em JSONL	✅

🔧 Como rodar
1) instalar dependências
bash
Copiar código
pip install -r requirements.txt
pip install email-validator
2) configurar .env
use .env.example como modelo

PARA GMAIL:

ativar 2FA

gerar App Password em: https://myaccount.google.com/apppasswords

usar essa senha no campo SMTP_PASS

IMPORTANTE:
NÃO subir .env no GitHub.

3) iniciar API
bash
Copiar código
uvicorn app.main:app --reload
4) testar no navegador
http://127.0.0.1:8000/docs
→ usar POST /ingest/email

📂 Saídas geradas
Local	Descrição
data/tickets.jsonl	tickets internos simulados
data/audit.jsonl	logs + erros SMTP
retorno do endpoint	exibe preview do e-mail e prioridade



