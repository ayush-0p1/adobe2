# Approach Explanation

The Round 1B solution analyses a collection of PDFs through the lens of predefined user personas. It is designed to run completely offline and to produce deterministic results using a lightweight pipeline.

**Ingestion and Chunking**

The tool first ingests every PDF from the provided directory. For each document, it extracts plain text pages and light‑weight heading candidates via `fitz` (PyMuPDF) in `pdf_utils.simple_headings`. Pages are then segmented into overlapping text chunks by `chunk_pages`, which uses a configurable sliding window. This approach keeps context intact while remaining memory‑efficient.

**Embedding and Persona Prompts**

Embeddings are generated with `sentence-transformers` in CPU mode. The `Embedder` class loads a local MiniLM model and normalises vectors for cosine similarity. Personas are defined in YAML via `Persona` dataclasses. For each persona, a text prompt is built from the persona’s role, expertise and keywords. This prompt is embedded once and reused for ranking all chunks.

**Scoring Mechanism**

`scoring.rank_chunks` combines multiple signals. Raw cosine similarity between the persona vector and each chunk forms the base score. Additional boosts are applied when persona keywords appear in the chunk or if the chunk is near an extracted heading. A simple page‑based decay biases the results toward earlier pages. The highest ranking chunks are returned and also aggregated into unique page‑level “sections” using `ranking.top_sections`.

**Cross‑Document Linking and Summaries**

To provide extra context, chunks are compared with each other through a similarity graph built by `crosslinker.build_graph`. Edges are added when the cosine score between chunk vectors exceeds a configurable threshold. The resulting network is exported as a simple edge list. Individual chunks are further distilled using `summary.top_sentences`, which selects the most representative sentences based on term frequency.

**Output Format and Execution**

`src.main` orchestrates the entire pipeline. After processing, it writes a single JSON file containing per‑persona sections, ranked subsections and the cross‑document graph. All operations are deterministic and the runtime is typically under a minute for small collections on eight CPU cores. The provided Dockerfile bundles the code with the necessary models so it can run without network access.