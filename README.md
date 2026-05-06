
# Password-Generator-Advanced

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?logo=python&logoColor=white)
![Security: secrets](https://img.shields.io/badge/Security-secrets%20module-green.svg)

Generateur de mots de passe securises en ligne de commande avec des contraintes cryptographiques strictes. Chaque mot de passe genere contient obligatoirement des lettres minuscules, majuscules, chiffres et caracteres speciaux, avec un minimum garanti de 9 chiffres et 9 caracteres speciaux.

---

## Pourquoi ce projet ?

La plupart des generateurs de mots de passe ne garantissent pas la presence de chaque categorie de caracteres. Password-Generator-Advanced applique des **contraintes strictes et non-negociables** a chaque generation :

| Contrainte | Minimum garanti |
|------------|-----------------|
| Chiffres (0-9) | 9 |
| Caracteres speciaux (`!@#$%^&*`...) | 9 |
| Lettres minuscules (a-z) | 1 |
| Lettres majuscules (A-Z) | 1 |
| **Longueur minimale totale** | **20 caracteres** |

Le module Python `secrets` est utilise pour la generation (CSPRNG — Cryptographically Secure Pseudo-Random Number Generator), contrairement a `random` qui n'est pas adapte a un usage securitaire.

---

## Installation

### Prerequis

- Python 3.12 ou superieur
- Poetry (gestionnaire de dependances)

### Etapes

```bash
git clone https://github.com/valorisa/Password-Generator-Advanced.git
cd Password-Generator-Advanced
poetry install
```

---

## Utilisation

```bash
poetry run python -m password_generator_advanced
```

Le menu interactif s'affiche :

```
==================================================
   GENERATEUR DE MOTS DE PASSE SECURISES
==================================================

Contraintes appliquees :
  - Minimum 9 chiffres
  - Minimum 9 caracteres speciaux
  - Au moins 1 lettre minuscule
  - Au moins 1 lettre majuscule
  - Longueur minimale : 20 caracteres

--------------------------------------------------
  1 - Generer un mot de passe
  2 - Generer plusieurs mots de passe
  3 - Quitter
--------------------------------------------------

  Votre choix (1-3) :
```

### Generer un mot de passe unique

Choisissez `1`, puis indiquez la longueur souhaitee (minimum 20). Le mot de passe est affiche avec sa composition detaillee :

```
  Mot de passe genere :
  k7$2!mR9@4#8^1&5*3%6Qw
  Longueur : 23 caracteres

  Composition :
    Chiffres         : 9
    Speciaux         : 10
    Minuscules       : 2
    Majuscules       : 2
```

### Generer plusieurs mots de passe

Choisissez `2`, indiquez la longueur puis le nombre souhaite (1 a 50).

---

## Architecture du projet

```
Password-Generator-Advanced/
├── src/
│   └── password_generator_advanced/
│       ├── __init__.py          # Version du package
│       ├── main.py              # Menu interactif CLI
│       └── generator.py         # Algorithme de generation
├── tests/
├── pyproject.toml               # Configuration Poetry
├── LICENSE                      # MIT
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── CHANGELOG.md
```

### Algorithme de generation (`generator.py`)

1. **Placement garanti** : 9 chiffres + 9 caracteres speciaux + 1 minuscule + 1 majuscule sont places en premier
2. **Remplissage** : Les positions restantes sont remplies avec un melange aleatoire de toutes les categories
3. **Melange final** : L'ensemble est melange via `secrets.SystemRandom().shuffle()` pour eliminer tout pattern positionnel previsible

Cette approche garantit mathematiquement le respect des contraintes tout en maximisant l'entropie du resultat.

---

## Securite

- **Module `secrets`** : Utilise le generateur aleatoire cryptographiquement securise du systeme d'exploitation (`/dev/urandom` sur Linux/macOS, `CryptGenRandom` sur Windows)
- **Aucune dependance externe** : Uniquement la bibliotheque standard Python — pas de surface d'attaque tierce
- **Pas de stockage** : Les mots de passe generes ne sont jamais ecrits sur disque ni envoyes sur le reseau

Pour signaler une vulnerabilite, consultez [SECURITY.md](SECURITY.md).

---

## Developpement

```bash
# Lancer les tests
poetry run pytest tests/ -v

# Verifier le style
poetry run ruff check .

# Corriger automatiquement
poetry run ruff check . --fix
```

---

## Contribution

Les contributions sont bienvenues. Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour le processus detaille.

Ce projet respecte le [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

---

## Licence

[MIT](LICENSE) - Utilisation libre, commerciale et modification autorisees.

---

**Auteur** : [valorisa](https://github.com/valorisa)
