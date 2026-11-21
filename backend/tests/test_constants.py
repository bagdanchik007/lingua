from app.core.constants import CEFR_LEVELS, EXERCISE_TYPES, SUPPORTED_LANGUAGE_CODES


def test_cefr_levels():
    assert "A1" in CEFR_LEVELS
    assert "C1" in CEFR_LEVELS


def test_exercise_types():
    assert "multiple_choice" in EXERCISE_TYPES
    assert "fill_blank" in EXERCISE_TYPES


def test_languages():
    assert "de" in SUPPORTED_LANGUAGE_CODES
    assert "en" in SUPPORTED_LANGUAGE_CODES
