#!/usr/bin/env bash
set -euo pipefail
python -m src.main --input_dir "$1" --output_dir "$2" --config config/config.yaml
