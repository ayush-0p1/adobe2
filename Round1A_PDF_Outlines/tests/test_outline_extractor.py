from pathlib import Path
import fitz
from src.outline_extractor import extract_outline

CFG_PATH = Path(__file__).resolve().parents[1] / "config" / "config.yaml"

def test_extract_outline(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Sample Document", fontsize=24, fontname="helv")
    page.insert_text((72, 100), "1. Introduction", fontsize=18, fontname="helv")
    page.insert_text((72, 130), "1.1 Background", fontsize=14, fontname="helv")
    page.insert_text((72, 160), "Regular paragraph text.", fontsize=11, fontname="helv")
    page.insert_text((72, 180), "Another body line.", fontsize=11, fontname="helv")
    doc.save(pdf_path)
    result = extract_outline(str(pdf_path), str(CFG_PATH))
    assert result["title"] == "1. Introduction"
    assert result["outline"] == [{"level": "H1", "text": "1. Introduction", "page": 1}]