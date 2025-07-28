from __future__ import annotations

import os

from .pdf_utils import extract_pages, simple_headings

def ingest_collection(input_dir: str):
    pdfs = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(".pdf")
    ]
    pdfs.sort()
    docs = []
    for p in pdfs:
        pages = extract_pages(p)
        heads = simple_headings(p)
        docs.append({"path": p, "pages": pages, "headings": heads})
    return docs
