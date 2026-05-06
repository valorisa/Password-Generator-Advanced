"""Générateur de mots de passe sécurisés avec contraintes strictes."""

import secrets
import string


MIN_DIGITS = 9
MIN_SPECIAL = 9
MIN_LENGTH = MIN_DIGITS + MIN_SPECIAL + 2  # au moins 1 minuscule + 1 majuscule


def generate_password(length: int) -> str:
    """Génère un mot de passe avec les contraintes :
    - Au moins 9 chiffres
    - Au moins 9 caractères spéciaux
    - Au moins 1 lettre minuscule
    - Au moins 1 lettre majuscule
    """
    if length < MIN_LENGTH:
        raise ValueError(
            f"La longueur minimale est {MIN_LENGTH} "
            f"(9 chiffres + 9 spéciaux + 1 min + 1 maj)"
        )

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation

    password_chars: list[str] = []

    # Garantir le minimum de chaque catégorie
    password_chars.extend(secrets.choice(digits) for _ in range(MIN_DIGITS))
    password_chars.extend(secrets.choice(special) for _ in range(MIN_SPECIAL))
    password_chars.append(secrets.choice(lowercase))
    password_chars.append(secrets.choice(uppercase))

    # Remplir le reste avec un mélange de toutes les catégories
    all_chars = lowercase + uppercase + digits + special
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(all_chars) for _ in range(remaining))

    # Mélanger pour éviter un pattern prévisible
    result = list(password_chars)
    secrets.SystemRandom().shuffle(result)

    return "".join(result)
