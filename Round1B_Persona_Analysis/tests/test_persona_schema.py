from src.persona_schema import load_personas
def test_load_personas(tmp_path):
    p = tmp_path / "p.yaml"
    p.write_text("""
personas:
  - id: a
    role: R
    expertise: [x]
    job: J
    keywords: [k]
""", encoding="utf-8")
    personas = load_personas(str(p))
    assert len(personas) == 1 and personas[0].id == "a"
