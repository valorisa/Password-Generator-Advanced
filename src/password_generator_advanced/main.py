"""Menu interactif du générateur de mots de passe."""

import sys
import os

if sys.platform == "win32":
    os.system("")
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

from .generator import generate_password, MIN_LENGTH


def print_header():
    print("\n" + "=" * 50)
    print("   GÉNÉRATEUR DE MOTS DE PASSE SÉCURISÉS")
    print("=" * 50)
    print("\nContraintes appliquées :")
    print("  - Minimum 9 chiffres")
    print("  - Minimum 9 caractères spéciaux")
    print("  - Au moins 1 lettre minuscule")
    print("  - Au moins 1 lettre majuscule")
    print(f"  - Longueur minimale : {MIN_LENGTH} caractères")
    print()


def print_menu():
    print("-" * 50)
    print("  1 - Générer un mot de passe")
    print("  2 - Générer plusieurs mots de passe")
    print("  3 - Quitter")
    print("-" * 50)


def get_length() -> int:
    while True:
        try:
            length = int(input(f"\nLongueur du mot de passe (min {MIN_LENGTH}) : "))
            if length < MIN_LENGTH:
                print(f"  Erreur : minimum {MIN_LENGTH} caractères requis.")
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


def main():
    print_header()

    while True:
        print_menu()
        choice = input("\n  Votre choix (1-3) : ").strip()

        if choice == "1":
            length = get_length()
            password = generate_password(length)
            display_password(password)

        elif choice == "2":
            length = get_length()
            count = get_count()
            print(f"\n  {count} mot(s) de passe de {length} caractères :\n")
            for i in range(count):
                password = generate_password(length)
                print(f"  {i + 1:2d}. {password}")

        elif choice == "3":
            print("\n  Au revoir !\n")
            break

        else:
            print("\n  Erreur : choix invalide (1-3).")


if __name__ == "__main__":
    main()
