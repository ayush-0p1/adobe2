from __future__ import annotations
import argparse, os, json
from .outline_extractor import extract_outline
from .logging_utils import get_logger
log = get_logger("main")

def process_dir(input_dir: str, output_dir: str, cfg: str):
    os.makedirs(output_dir, exist_ok=True)
    for name in os.listdir(input_dir):
        if not name.lower().endswith(".pdf"):
            continue
        in_path = os.path.join(input_dir, name)
        out_name = os.path.splitext(name)[0] + ".json"
        out_path = os.path.join(output_dir, out_name)
        log.info(f"Processing {name} …")
        result = extract_outline(in_path, cfg)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        log.info(f"→ {out_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", required=True)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    process_dir(args.input_dir, args.output_dir, args.config)

if __name__ == "__main__":
    main()
