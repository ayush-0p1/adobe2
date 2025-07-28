from __future__ import annotations
import re
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

def top_sentences(text: str, k: int = 3) -> str:
    sents = [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    if len(sents) <= k: return " ".join(sents)
    from collections import Counter
    words = re.findall(r"\w+", text.lower())
    freq = Counter(words)
    def score(sent):
        ws = re.findall(r"\w+", sent.lower())
        return sum(freq[w] for w in ws) / (len(ws)+1e-6)
    ranked = sorted(sents, key=score, reverse=True)[:k]
    return " ".join(ranked)
