import json, csv, sys
data = json.load(open(sys.argv[1], "r", encoding="utf-8"))
with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["persona_id","doc","page","importance_rank","score","type","title/refined"])
    for res in data.get("results", []):
        pid = res["persona"]["id"]
        for s in res.get("sections", []):
            w.writerow([pid, s["document"], s["page"], s["importance_rank"], s.get("score", 0.0), "section", s.get("section_title","")])
        for ss in res.get("subsections", []):
            w.writerow([pid, ss["document"], ss["page"], ss["importance_rank"], ss.get("score", 0.0), "subsection", ss.get("refined_text","")])
