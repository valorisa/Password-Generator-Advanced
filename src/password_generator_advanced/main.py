"""Menu interactif et CLI du générateur de mots de passe."""

import argparse
import os
import sys

if sys.platform == "win32":
    os.system("")
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

from .clipboard import copy_to_clipboard
from .generator import (
    DEFAULT_MIN_DIGITS,
    DEFAULT_MIN_SPECIAL,
    evaluate_password,
    generate_passphrase,
    generate_password,
    minimum_length,
)


def print_header(min_digits: int, min_special: int):
    min_len = minimum_length(min_digits, min_special)
    print("\n" + "=" * 50)
    print("   GÉNÉRATEUR DE MOTS DE PASSE SÉCURISÉS")
    print("=" * 50)
    print("\nContraintes appliquées :")
    print(f"  - Minimum {min_digits} chiffres")
    print(f"  - Minimum {min_special} caractères spéciaux")
    print("  - Au moins 1 lettre minuscule")
    print("  - Au moins 1 lettre majuscule")
    print(f"  - Longueur minimale : {min_len} caractères")
    print()


def print_menu():
    print("-" * 50)
    print("  1 - Générer un mot de passe")
    print("  2 - Générer plusieurs mots de passe")
    print("  3 - Générer une passphrase")
    print("  4 - Évaluer un mot de passe / passphrase")
    print("  5 - Quitter")
    print("-" * 50)


def get_length(min_len: int) -> int:
    while True:
        try:
            length = int(input(f"\nLongueur du mot de passe (min {min_len}) : "))
            if length < min_len:
                print(f"  Erreur : minimum {min_len} caractères requis.")
                continue
            return length
        except ValueError:
            print("  Erreur : veuillez entrer un nombre entier.")


def get_count() -> int:
    while True:
        try:
            count = int(input("\nCombien de mots de passe ? (1-50) : "))
            if count < 1 or count > 50:
                print("  Erreur : entre 1 et 50.")
                continue
            return count
        except ValueError:
            print("  Erreur : veuillez entrer un nombre entier.")


def get_num_words() -> int:
    while True:
        try:
            num = int(input("\nNombre de mots (4-12, défaut 6) : ") or "6")
            if num < 4 or num > 12:
                print("  Erreur : entre 4 et 12 mots.")
                continue
            return num
        except ValueError:
            print("  Erreur : veuillez entrer un nombre entier.")


def offer_clipboard(text: str):
    choice = input("\n  Copier dans le presse-papier ? (o/N) : ").strip().lower()
    if choice in ("o", "oui", "y", "yes"):
        if copy_to_clipboard(text):
            print("  ✓ Copié dans le presse-papier.")
        else:
            print("  ✗ Impossible de copier (outil clipboard non disponible).")


def display_password(password: str):
    print("\n  Mot de passe généré :")
    print(f"  {password}")
    print(f"  Longueur : {len(password)} caractères")

    digits = sum(1 for c in password if c.isdigit())
    special = sum(1 for c in password if not c.isalnum())
    lower = sum(1 for c in password if c.islower())
    upper = sum(1 for c in password if c.isupper())

    print("\n  Composition :")
    print(f"    Chiffres         : {digits}")
    print(f"    Spéciaux         : {special}")
    print(f"    Minuscules       : {lower}")
    print(f"    Majuscules       : {upper}")

    offer_clipboard(password)


def display_passphrase(passphrase: str, num_words: int):
    print("\n  Passphrase générée :")
    print(f"  {passphrase}")
    bits = num_words * 11
    print(f"  {num_words} mots — ~{bits} bits d'entropie")

    offer_clipboard(passphrase)


def display_evaluation(result: dict):
    print("\n  Entropie théorique maximale :")
    print(f"    Longueur         : {result['length']} caractères")
    print(f"    Entropie max.    : {result['entropy']} bits")
    print(f"    Niveau           : {result['strength']}")
    print(f"    Jeu de caractères: {result['charset_size']} symboles possibles")
    print("\n  Catégories détectées :")
    print(f"    Minuscules       : {'✓' if result['has_lower'] else '✗'}")
    print(f"    Majuscules       : {'✓' if result['has_upper'] else '✗'}")
    print(f"    Chiffres         : {'✓' if result['has_digits'] else '✗'}")
    print(f"    Spéciaux         : {'✓' if result['has_special'] else '✗'}")
    print("\n  ⚠ Ce calcul suppose un choix aléatoire par caractère.")
    print("    Un mot de passe basé sur des mots du dictionnaire ou des")
    print("    patterns prévisibles aura une entropie réelle inférieure.")


def interactive_mode(min_digits: int, min_special: int):
    min_len = minimum_length(min_digits, min_special)
    print_header(min_digits, min_special)

    while True:
        print_menu()
        choice = input("\n  Votre choix (1-5) : ").strip()

        if choice == "1":
            length = get_length(min_len)
            password = generate_password(length, min_digits, min_special)
            display_password(password)

        elif choice == "2":
            length = get_length(min_len)
            count = get_count()
            print(f"\n  {count} mot(s) de passe de {length} caractères :\n")
            for i in range(count):
                password = generate_password(length, min_digits, min_special)
                print(f"  {i + 1:2d}. {password}")

        elif choice == "3":
            num_words = get_num_words()
            passphrase = generate_passphrase(num_words)
            display_passphrase(passphrase, num_words)

        elif choice == "4":
            pwd = input("\n  Entrez le mot de passe à évaluer : ")
            if pwd:
                result = evaluate_password(pwd)
                display_evaluation(result)
            else:
                print("  Erreur : saisie vide.")

        elif choice == "5":
            print("\n  Au revoir !\n")
            break

        else:
            print("\n  Erreur : choix invalide (1-5).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password-generator-advanced",
        description="Générateur de mots de passe sécurisés avec contraintes strictes",
    )
    parser.add_argument(
        "--length", "-l",
        type=int,
        help="Longueur du mot de passe à générer",
    )
    parser.add_argument(
        "--min-digits",
        type=int,
        default=DEFAULT_MIN_DIGITS,
        help=f"Nombre minimum de chiffres (défaut: {DEFAULT_MIN_DIGITS})",
    )
    parser.add_argument(
        "--min-special",
        type=int,
        default=DEFAULT_MIN_SPECIAL,
        help=f"Nombre minimum de caractères spéciaux (défaut: {DEFAULT_MIN_SPECIAL})",
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=1,
        help="Nombre de mots de passe à générer (défaut: 1)",
    )
    parser.add_argument(
        "--passphrase", "-p",
        action="store_true",
        help="Générer une passphrase au lieu d'un mot de passe",
    )
    parser.add_argument(
        "--words", "-w",
        type=int,
        default=6,
        help="Nombre de mots pour la passphrase (défaut: 6)",
    )
    parser.add_argument(
        "--separator",
        type=str,
        default="-",
        help="Séparateur pour la passphrase (défaut: -)",
    )
    parser.add_argument(
        "--copy", "-c",
        action="store_true",
        help="Copier le résultat dans le presse-papier",
    )
    parser.add_argument(
        "--evaluate", "-e",
        type=str,
        help="Évaluer la force d'un mot de passe ou passphrase",
    )
    return parser


def cli_mode(args: argparse.Namespace):
    if args.evaluate:
        result = evaluate_password(args.evaluate)
        display_evaluation(result)
    elif args.passphrase:
        for _ in range(args.count):
            passphrase = generate_passphrase(args.words, args.separator)
            print(passphrase)
        if args.copy and args.count == 1:
            passphrase = generate_passphrase(args.words, args.separator)
            copy_to_clipboard(passphrase)
    else:
        min_len = minimum_length(args.min_digits, args.min_special)
        length = args.length if args.length else min_len
        passwords = []
        for _ in range(args.count):
            password = generate_password(length, args.min_digits, args.min_special)
            passwords.append(password)
            print(password)
        if args.copy and len(passwords) == 1:
            copy_to_clipboard(passwords[0])


def main():
    parser = build_parser()
    args = parser.parse_args()

    has_cli_args = (
        args.length is not None
        or args.passphrase
        or args.count > 1
        or args.copy
        or args.evaluate is not None
        or args.min_digits != DEFAULT_MIN_DIGITS
        or args.min_special != DEFAULT_MIN_SPECIAL
    )

    if has_cli_args:
        cli_mode(args)
    else:
        interactive_mode(args.min_digits, args.min_special)


if __name__ == "__main__":
    main()
