# Round 1A — PDF Outline Extraction (Title, H1/H2/H3)

Fast, fully offline heading detection using PyMuPDF span metrics + robust heuristics.

## Highlights
- **≤10s on 50 pages** on 8‑CPU machines (vectorised scoring, single pass parsing).
- **No internet**. No ML downloads at runtime.
- Handles **mixed fonts, numbering patterns, multilingual scripts** (basic CJK/Japanese bonus).
- Outputs deterministic, schema‑validated JSON.

## Input & Output
- Input: PDF up to 50 pages.
- Output JSON schema:
```json
{
  "title": "...",
  "outline": [
    {"level": "H1", "text": "...", "page": 1},
    {"level": "H2", "text": "...", "page": 2}
  ]
}
```

## Build (AMD64)
```bash
docker build --platform linux/amd64 -t outlines:local -f Dockerfile .
```

## Run (evaluator style)
```bash
mkdir -p input output
# put PDFs in input/
docker run --rm   -v $(pwd)/input:/app/input   -v $(pwd)/output:/app/output   --network none outlines:local
# output/<file>.json produced
```

## Tests
```bash
pytest -q
```
