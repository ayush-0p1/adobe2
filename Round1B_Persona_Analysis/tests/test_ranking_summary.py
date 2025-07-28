from src.scoring import make_keyword_set, keyword_boost, heading_boost_fn, page_prior
from src.ranking import top_sections
from src.summary import top_sentences


def test_keyword_boost():
    kw = make_keyword_set(["apple orange"])
    assert kw == {"apple", "orange"}
    assert keyword_boost("I like apple", kw, 0.2) == 0.2
    assert keyword_boost("nothing here", kw, 0.2) == 0.0


def test_top_sections_and_prior():
    chunks = [
        {"doc": "d", "page": 1, "heading": "A"},
        {"doc": "d", "page": 1, "heading": "B"},
        {"doc": "d", "page": 2, "heading": "C"},
    ]
    ranked = [(0, 0.1), (1, 0.5), (2, 0.6)]
    sections = top_sections(chunks, ranked, section_top_k=2)
    assert sections[0]["page"] == 2 and sections[0]["section_title"] == "C"
    assert sections[1]["page"] == 1 and sections[1]["section_title"] == "B"
    assert page_prior(1, 0.1) == 1.0
    assert page_prior(3, 0.1) == 0.8


def test_heading_boost_and_summary():
    hb = heading_boost_fn(1, {1: ["Intro heading"]}, "Intro heading text", 0.1)
    assert hb > 0.05
    text = "A A A. B B. C."
    assert top_sentences(text, k=2) == "A A A. B B."