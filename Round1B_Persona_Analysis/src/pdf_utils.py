from __future__ import annotations
import fitz
from typing import List, Dict

def extract_pages(pdf_path: str) -> List[str]:
    doc = fitz.open(pdf_path)
    texts = []
    for pno in range(len(doc)):
        texts.append(doc[pno].get_text("text"))
    doc.close()
    return texts

def simple_headings(pdf_path: str) -> Dict[int, List[str]]:
    doc = fitz.open(pdf_path)
    res = {}
    for pno in range(len(doc)):
        page = doc[pno]
        blocks = page.get_text("dict")["blocks"]
        cand = []
        for b in blocks:
            if b.get("type", 0) != 0: continue
            for l in b.get("lines", []):
                spans = l.get("spans", [])
                txt = "".join(s.get("text", "") for s in spans).strip()
                if not txt or len(txt) > 120: continue
                size_avg = sum(float(s.get("size", 0.0)) for s in spans) / max(1, len(spans))
                bold = any("Bold" in s.get("font", "") for s in spans)
                if size_avg >= 12.5 or bold:
                    cand.append(txt)
        res[pno+1] = cand[:30]
    doc.close()
    return res
