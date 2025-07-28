#!/usr/bin/env bash
set -euo pipefail
python -m src.main   --input_dir "$1"   --output "$2"   --personas config/personas.yaml   --settings config/settings.yaml   --model_dir /app/models/all-MiniLM-L6-v2
