# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     TRANSFORMERS_OFFLINE=1     HF_HUB_DISABLE_TELEMETRY=1     SENTENCE_TRANSFORMERS_HOME=/app/models

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && apt-get install -y --no-install-recommends       build-essential git     && rm -rf /var/lib/apt/lists/*     && pip install --no-cache-dir -r requirements.txt

ENV MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
RUN python - <<'PY'
from sentence_transformers import SentenceTransformer
import os
model_dir = "/app/models/all-MiniLM-L6-v2"
SentenceTransformer(os.environ.get("MODEL_NAME"), cache_folder=model_dir)
print("Model cached at", model_dir)
PY

COPY config /app/config
COPY src /app/src
COPY scripts /app/scripts

CMD ["python", "-m", "src.main", "--input_dir", "/app/input", "--output", "/app/output/results.json", "--personas", "/app/config/personas.yaml", "--settings", "/app/config/settings.yaml", "--model_dir", "/app/models/all-MiniLM-L6-v2"]
