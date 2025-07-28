import json, sys
from rapidfuzz import fuzz

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def match_score(pred, gt):
    used = set()
    tp = 0
    for i, p in enumerate(pred):
        for j, g in enumerate(gt):
            if j in used: continue
            if p["level"] != g["level"]: continue
            if abs(p["page"] - g["page"]) > 1: continue
            if fuzz.token_set_ratio(p["text"], g["text"]) >= 90:
                tp += 1
                used.add(j)
                break
    prec = tp / max(1, len(pred))
    rec = tp / max(1, len(gt))
    return prec, rec

if __name__ == "__main__":
    pred = load(sys.argv[1])
    gt = load(sys.argv[2])
    p, r = match_score(pred["outline"], gt["outline"])
    f1 = 0 if (p+r)==0 else 2*p*r/(p+r)
    print(json.dumps({"precision": p, "recall": r, "f1": f1}, indent=2))
