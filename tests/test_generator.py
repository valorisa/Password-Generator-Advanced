"""Tests for password_generator_advanced.generator."""

import string

from password_generator_advanced.generator import generate_password, MIN_LENGTH, MIN_DIGITS, MIN_SPECIAL


def test_minimum_length_respected():
    password = generate_password(MIN_LENGTH)
    assert len(password) == MIN_LENGTH


def test_custom_length_respected():
    password = generate_password(30)
    assert len(password) == 30


def test_minimum_digits_guaranteed():
    password = generate_password(MIN_LENGTH)
    digit_count = sum(1 for c in password if c.isdigit())
    assert digit_count >= MIN_DIGITS


def test_minimum_special_guaranteed():
    password = generate_password(MIN_LENGTH)
    special_count = sum(1 for c in password if c in string.punctuation)
    assert special_count >= MIN_SPECIAL


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
