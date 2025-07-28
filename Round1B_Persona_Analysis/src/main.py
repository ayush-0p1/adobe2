from __future__ import annotations
import argparse, os, time, yaml
from typing import List, Dict, Any
from .logging_utils import get_logger
from .ingest import ingest_collection
from .chunking import chunk_pages
from .embedding import Embedder
from .persona_schema import load_personas
from .scoring import rank_chunks
from .ranking import top_sections
from .crosslinker import build_graph
from .graph_builder import export_graph
from .summary import top_sentences
from .io_utils import save_json

log = get_logger("persona")

def build_chunks(docs: List[Dict[str, Any]], cfg: Dict[str, Any]):
    chunks: List[Dict[str, Any]] = []
    for d in docs:
        doc_path = d["path"]
        pages = d["pages"]
        headings = d["headings"]
        cks = chunk_pages(pages, cfg["chunk"]["max_chars"], cfg["chunk"]["stride_chars"], cfg["chunk"]["min_chars"])
        for c in cks:
            heads = headings.get(c["page"], [])
            c["heading"] = heads[0] if heads else ""
            c["doc"] = os.path.basename(doc_path)
        chunks.extend(cks)
    return chunks

def process(input_dir: str, output_path: str, personas_path: str, settings_path: str, model_dir: str):
    t0 = time.time()
    cfg = yaml.safe_load(open(settings_path, "r", encoding="utf-8"))
    personas = load_personas(personas_path)
    docs = ingest_collection(input_dir)
    chunks = build_chunks(docs, cfg)

    embed = Embedder(model_dir)
    chunk_vecs = embed.encode([c["text"] for c in chunks])

    results = []
    for p in personas:
        p_vec = embed.encode([p.prompt()])[0]
        ranked = rank_chunks(p_vec, chunk_vecs, chunks, cfg, headings={}, keywords=p.keywords)
        sections = top_sections(chunks, ranked, cfg["rank"]["section_top_k"])
        subsections = []
        for rank_idx, (idx, score) in enumerate(ranked, start=1):
            ch = chunks[idx]
            refined = top_sentences(ch["text"], cfg["summary"]["max_sentences"])
            subsections.append({
                "document": ch["doc"],
                "page": ch["page"],
                "refined_text": refined,
                "importance_rank": rank_idx,
                "score": float(score),
            })
        G = build_graph(chunk_vecs, chunks, cfg["similarity"]["min_sim"])
        graph = export_graph(G)
        results.append({
            "persona": {"id": p.id, "role": p.role, "job": p.job},
            "sections": sections,
            "subsections": subsections,
            "links": graph,
        })

    meta = {
        "input_documents": [os.path.basename(d["path"]) for d in docs],
        "personas_count": len(personas),
        "processed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runtime_seconds": round(time.time() - t0, 3),
    }
    final = {"metadata": meta, "results": results}
    save_json(final, output_path)
    log.info(f"Saved results to {output_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--personas", required=True)
    ap.add_argument("--settings", required=True)
    ap.add_argument("--model_dir", required=True)
    args = ap.parse_args()
    process(args.input_dir, args.output, args.personas, args.settings, args.model_dir)

if __name__ == "__main__":
    main()
