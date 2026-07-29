"""Tests for password_generator_advanced.generator."""

import string

from password_generator_advanced.generator import (
    DEFAULT_MIN_DIGITS,
    DEFAULT_MIN_SPECIAL,
    evaluate_password,
    generate_passphrase,
    generate_password,
    minimum_length,
)

MIN_LENGTH = minimum_length(DEFAULT_MIN_DIGITS, DEFAULT_MIN_SPECIAL)


def test_minimum_length_respected():
    password = generate_password(MIN_LENGTH)
    assert len(password) == MIN_LENGTH


def test_custom_length_respected():
    password = generate_password(30)
    assert len(password) == 30


def test_minimum_digits_guaranteed():
    password = generate_password(MIN_LENGTH)
    digit_count = sum(1 for c in password if c.isdigit())
    assert digit_count >= DEFAULT_MIN_DIGITS


def test_minimum_special_guaranteed():
    password = generate_password(MIN_LENGTH)
    special_count = sum(1 for c in password if c in string.punctuation)
    assert special_count >= DEFAULT_MIN_SPECIAL


def test_has_lowercase():
    password = generate_password(MIN_LENGTH)
    assert any(c.islower() for c in password)


def test_has_uppercase():
    password = generate_password(MIN_LENGTH)
    assert any(c.isupper() for c in password)


def test_raises_on_too_short():
    try:
        generate_password(5)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_uniqueness():
    passwords = {generate_password(25) for _ in range(20)}
    assert len(passwords) == 20


def test_custom_min_digits():
    password = generate_password(30, min_digits=5, min_special=5)
    digit_count = sum(1 for c in password if c.isdigit())
    assert digit_count >= 5


def test_custom_min_special():
    password = generate_password(30, min_digits=5, min_special=12)
    special_count = sum(1 for c in password if c in string.punctuation)
    assert special_count >= 12


def test_passphrase_word_count():
    passphrase = generate_passphrase(6)
    assert len(passphrase.split("-")) == 6


def test_passphrase_custom_separator():
    passphrase = generate_passphrase(4, separator=".")
    assert len(passphrase.split(".")) == 4


def test_passphrase_uniqueness():
    passphrases = {generate_passphrase(6) for _ in range(20)}
    assert len(passphrases) == 20


def test_passphrase_raises_on_zero_words():
    try:
        generate_passphrase(0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_evaluate_strong_password():
    result = evaluate_password("aB3!xY9@kL7#mN2$pQ5^")
    assert result["length"] == 20
    assert result["has_lower"] is True
    assert result["has_upper"] is True
    assert result["has_digits"] is True
    assert result["has_special"] is True
    assert result["charset_size"] == 94
    assert result["entropy"] > 100


def test_evaluate_weak_password():
    result = evaluate_password("abc")
    assert result["strength"] == "Très faible"
    assert result["charset_size"] == 26


def test_evaluate_digits_only():
    result = evaluate_password("1234567890")
    assert result["has_digits"] is True
    assert result["has_lower"] is False
    assert result["charset_size"] == 10


def test_evaluate_passphrase():
    result = evaluate_password("correct-horse-battery-staple")
    assert result["length"] == 28
    assert result["has_lower"] is True
    assert result["has_special"] is True
