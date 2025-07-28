from src.features import detect_number_depth

def test_number_depth():
    assert detect_number_depth("1. Introduction") >= 1
    assert detect_number_depth("1.1. Background") >= 1
    assert detect_number_depth("A. Methods") >= 1
    assert detect_number_depth("Introduction") == 0
