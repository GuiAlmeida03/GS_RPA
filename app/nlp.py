import re
from typing import List

TOPIC_PATTERNS = {
    "ansiedade": r"\bansiedad[ea]\b|\bcrise de p[âa]nico\b|\bansiedade\b",
    "sobrecarga": r"\bsobrecarga\b|\bmuita demanda\b|\bexaust[aã]o\b",
    "conflito": r"\bconflito\b|\bproblema com (gestor|colega|chefe)\b",
    "beneficios": r"\b(plano de sa[úu]de|benef[ií]cios|psic[oó]logo)\b",
}

PERSON_PATTERNS = [
    r"\bmeu gestor\b", r"\bminha gestora\b", r"\bmeu gerente\b",
    r"\bcolega\b", r"\bminha equipe\b", r"\btime\b"
]

def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[\r\n]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def extract_topics(text: str) -> List[str]:
    tn = normalize(text)
    hits = []
    for name, pat in TOPIC_PATTERNS.items():
        if re.search(pat, tn):
            hits.append(name)
    return list(dict.fromkeys(hits))

def extract_persons(text: str) -> List[str]:
    tn = normalize(text)
    hits = []
    for pat in PERSON_PATTERNS:
        if re.search(pat, tn):
            hits.append(re.sub(r"\b|\b", "", pat))
    return list(dict.fromkeys(hits))

def sentiment(text: str) -> str:
    tn = normalize(text)
    very_neg = [r"n[aã]o aguento mais", r"crise de p[âa]nico", r"desespero"]
    neg = [r"exaust[aã]o", r"sobrecarga", r"ansiedad[ea]"]
    if any(re.search(p, tn) for p in very_neg):
        return "muito_negativo"
    if any(re.search(p, tn) for p in neg):
        return "negativo"
    return "neutro"

def urgency_signals(text: str) -> List[str]:
    tn = normalize(text)
    candidates = ["urgente","hoje","agora","não aguento mais","crise de pânico"]
    return [p for p in candidates if re.search(re.escape(p), tn)]

def redact(text: str) -> str:
    text = re.sub(r"\b(\d{3}\.?\d{3}\.?\d{3}-?\d{2})\b", "[CPF]", text)
    text = re.sub(r"\b(\+?55\s?\(?\d{2}\)?\s?\d{4,5}-?\d{4})\b", "[TELEFONE]", text)
    return text
