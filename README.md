# Document Intelligence Solutions

This repository contains two standalone Dockerized solutions for common PDF processing tasks. The projects were created as part of separate coding rounds and share a lightweight dependency stack so they can run fully offline.

- **[Round 1A – PDF Outline Extraction](Round1A_PDF_Outlines/README.md)** – Detects document titles and hierarchical headings (H1–H3) from PDFs. Outputs deterministic JSON with page numbers for downstream use.
- **[Round 1B – Persona‑Driven Document Intelligence](Round1B_Persona_Analysis/README.md)** – Ranks relevant sections across multiple PDFs based on user personas. Produces summaries and cross‑document links.

Both solutions are optimized for speed and small CPU‑only environments. See each subproject for full usage details.

## Quick Start

Clone the repository and build the Docker images:

```bash
# Outline extraction image
cd Round1A_PDF_Outlines
docker build --platform linux/amd64 -t outlines:local -f Dockerfile .

# Persona analysis image
cd ../Round1B_Persona_Analysis
docker build --platform linux/amd64 -t persona:local -f Dockerfile .
```

Run the containers on your PDFs. Each expects an `input/` directory with PDF files and writes results to `output/`.

```bash
# Run outline extraction
mkdir -p input output
# place PDFs into input/
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none outlines:local
# JSON outlines are written to output/

# Run persona-driven analysis
mkdir -p input output
# place PDFs into input/
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none persona:local
# results.json appears in output/
```

For additional configuration and advanced options, consult the README inside each round directory.