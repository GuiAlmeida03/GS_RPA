import re
from typing import Tuple, List
from .nlp import normalize

P1_TERMS = [
    (r"\bn[aã]o aguento mais\b", 0.99, "nao_ag_prio1"),
    (r"\bcrise de p[âa]nico\b", 0.99, "crise_panico_prio1"),
    (r"\bpersegui[cç][aã]o\b", 0.9, "perseguicao_prio1"),
    (r"\bauto(?:agress[aã]o|les[aã]o)\b", 0.99, "autoagressao_prio1"),
]

P2_TERMS = [
    (r"\bsobrecarga cr[oô]nica\b", 0.8, "sobrecarga_cronica"),
    (r"\bexaust[aã]o\b", 0.75, "exaustao"),
    (r"\bsem folga\b", 0.7, "sem_folga"),
]

P3_TERMS = [
    (r"\bcomo agendar psic[oó]logo\b", 0.7, "como_agendar_psicologo"),
    (r"\bplano de sa[úu]de\b", 0.6, "plano_saude"),
]

P4_TERMS = [
    (r"\bproblema com (gestor|colega|chefe)\b", 0.6, "conflito_pessoal"),
    (r"\bconflito\b", 0.6, "conflito"),
]

def classify(text: str) -> Tuple[str, float, List[str]]:
    tn = normalize(text)
    hits = []

    def scan(terms, label):
        for pat, score, code in terms:
            if re.search(pat, tn):
                return label, score, [code]
        return None

    for terms, label in [(P1_TERMS, "P1"), (P2_TERMS, "P2"), (P3_TERMS, "P3"), (P4_TERMS, "P4")]:
        res = scan(terms, label)
        if res:
            return res

    # fallback heurística
    if len(tn) > 0 and any(w in tn for w in ["ansiedade","sobrecarga","exaust", "conflito"]):
        return "P2", 0.55, ["fallback_heuristic"]

    return "P3", 0.5, ["default_p3"]
