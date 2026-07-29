"""Générateur de mots de passe sécurisés avec contraintes strictes."""

import math
import secrets
import string

from .wordlist import WORDLIST

DEFAULT_MIN_DIGITS = 9
DEFAULT_MIN_SPECIAL = 9


def minimum_length(min_digits: int, min_special: int) -> int:
    return min_digits + min_special + 2


def generate_password(
    length: int,
    min_digits: int = DEFAULT_MIN_DIGITS,
    min_special: int = DEFAULT_MIN_SPECIAL,
) -> str:
    min_len = minimum_length(min_digits, min_special)
    if length < min_len:
        raise ValueError(
            f"La longueur minimale est {min_len} "
            f"({min_digits} chiffres + {min_special} spéciaux + 1 min + 1 maj)"
        )

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation

    password_chars: list[str] = []

    password_chars.extend(secrets.choice(digits) for _ in range(min_digits))
    password_chars.extend(secrets.choice(special) for _ in range(min_special))
    password_chars.append(secrets.choice(lowercase))
    password_chars.append(secrets.choice(uppercase))

    all_chars = lowercase + uppercase + digits + special
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(all_chars) for _ in range(remaining))

    result = list(password_chars)
    secrets.SystemRandom().shuffle(result)

    return "".join(result)


def generate_passphrase(num_words: int = 6, separator: str = "-") -> str:
    if num_words < 1:
        raise ValueError("Le nombre de mots doit être au moins 1")
    words = [secrets.choice(WORDLIST) for _ in range(num_words)]
    return separator.join(words)


def evaluate_password(password: str) -> dict:
    length = len(password)
    charset_size = 0

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digits:
        charset_size += 10
    if has_special:
        charset_size += 32

    entropy = length * math.log2(charset_size) if charset_size > 0 else 0

    if entropy >= 128:
        strength = "Très fort"
    elif entropy >= 80:
        strength = "Fort"
    elif entropy >= 64:
        strength = "Moyen"
    elif entropy >= 48:
        strength = "Faible"
    else:
        strength = "Très faible"

    return {
        "length": length,
        "entropy": round(entropy, 1),
        "charset_size": charset_size,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digits": has_digits,
        "has_special": has_special,
        "strength": strength,
    }
