from app.utils.validators import is_strong_password, normalize_answer


def test_password_requires_digit_and_letter():
    assert is_strong_password("abcdefgh") is False
    assert is_strong_password("12345678") is False
    assert is_strong_password("abcd1234") is True


def test_normalize_collapses_spaces():
    assert normalize_answer("  a   b  ") == "a b"
