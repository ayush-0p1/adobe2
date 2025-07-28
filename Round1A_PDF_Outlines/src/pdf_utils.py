from __future__ import annotations
import fitz
from dataclasses import dataclass
from typing import List

@dataclass
class Span:
    text: str
    size: float
    font: str
    bold: bool
    page: int
    x0: float
    x1: float
    y0: float
    y1: float
    line_len: int

def extract_spans(pdf_path: str, max_pages: int | None = None) -> List[Span]:
    doc = fitz.open(pdf_path)
    spans: List[Span] = []
    pages = range(len(doc)) if max_pages is None else range(min(len(doc), max_pages))
    for pno in pages:
        page = doc[pno]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b.get("type", 0) != 0:
                continue
            for line in b.get("lines", []):
                line_text = "".join(s["text"] for s in (line.get("spans") or []))
                line_len = len(line_text.strip())
                for s in line.get("spans", []):
                    text = s.get("text", "").strip()
                    if not text:
                        continue
                    font = s.get("font", "")
                    bold = "Bold" in font or "Black" in font or "Heavy" in font
                    size = float(s.get("size", 0.0))
                    x0, y0, x1, y1 = s.get("bbox", [0,0,0,0])
                    spans.append(Span(text, size, font, bold, pno+1, x0, x1, y0, y1, line_len))
    doc.close()
    return spans
