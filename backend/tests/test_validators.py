from app.utils.validators import is_strong_password, normalize_answer, is_valid_email


def test_strong_password():
    assert is_strong_password("secret12") is True
    assert is_strong_password("short") is False
    assert is_strong_password("nodigits") is False


def test_normalize_answer():
    assert normalize_answer("  Der Mann  ") == "der mann"


def test_email():
    assert is_valid_email("a@b.co") is True
    assert is_valid_email("nope") is False
