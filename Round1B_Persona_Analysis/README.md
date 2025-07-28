# Round 1B — Persona‑Driven Document Intelligence

Offline, fast relevance ranking across multi‑PDF collections with SentenceTransformer MiniLM embeddings + keyword boosts and cross‑document linking.

## Build
```bash
docker build --platform linux/amd64 -t persona:local -f Dockerfile .
```

## Run
```bash
mkdir -p input output
docker run --rm   -v $(pwd)/input:/app/input   -v $(pwd)/output:/app/output   --network none persona:local
# outputs /app/output/results.json
```

## Tests
```bash
pip install -r requirements.txt -r ../Round1A_PDF_Outlines/requirements.txt
PYTHONPATH=Round1A_PDF_Outlines pytest Round1A_PDF_Outlines/tests -q
PYTHONPATH=Round1B_Persona_Analysis pytest Round1B_Persona_Analysis/tests -q
```