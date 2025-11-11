from textwrap import dedent

def email_employee(priority: str, first_name: str, topic_hint: str = "") -> str:
    if priority == "P1":
        return dedent(f"""
        Assunto: Recebemos sua mensagem – estamos com você
        Olá, {first_name}.
        Recebemos sua mensagem e entendemos que este é um momento difícil.
        Seu caso foi marcado como prioridade máxima e encaminhado, de forma estritamente restrita,
        à nossa equipe de Saúde Ocupacional.
        Se precisar de apoio imediato, você pode contatar nosso canal 24h: (XX) XXXX-XXXX.
        Em breve, um(a) profissional entrará em contato.
        Abraço,
        Equipe de Bem-Estar
        """).strip()
    if priority == "P3":
        return dedent(f"""
        Assunto: Sua dúvida sobre {topic_hint or 'bem-estar'}
        Olá, {first_name}!
        Recebemos sua dúvida e encaminhamos para a equipe responsável.
        Responderemos em até 48 horas.
        Conte conosco,
        Equipe de Benefícios
        """).strip()
    # P2/P4 genéricos
    return dedent(f"""
    Assunto: Recebemos sua mensagem
    Olá, {first_name}.
    Recebemos sua mensagem e direcionamos internamente para acompanhamento.
    Em breve retornaremos com próximos passos.
    Abraço,
    Equipe de Bem-Estar
    """).strip()

def briefing(priority: str, employee_id: str, topics, sentiment, urgency, summary, suggestion, score: float) -> str:
    return dedent(f"""
    Alerta {priority}
    Remetente (ID): {employee_id}
    Tópicos: {', '.join(topics) or '—'}
    Sentimento: {sentiment}
    Sinais de urgência: {', '.join(urgency) or '—'}
    Resumo do caso (sem PII desnecessária): {summary}
    Sugestão de próxima ação: {suggestion}
    Confiança do classificador: {score:.2f}
    """).strip()
