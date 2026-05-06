# Password-Generator-Advanced

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?logo=python&logoColor=white)
![Security: secrets](https://img.shields.io/badge/Security-secrets%20module-green.svg)

Générateur de mots de passe sécurisés en ligne de commande avec des contraintes cryptographiques strictes. Chaque mot de passe généré contient obligatoirement des lettres minuscules, majuscules, chiffres et caractères spéciaux, avec des minimums configurables.

---

## Fonctionnalités

- Génération de mots de passe avec contraintes strictes (configurable)
- Génération de passphrases (style Diceware, 2048 mots, 11 bits d'entropie par mot)
- Évaluation de la force d'un mot de passe ou passphrase existant
- Copie dans le presse-papier (Windows, macOS, Linux)
- Mode interactif (menu) et mode CLI (arguments en ligne de commande)

---

## Contraintes par défaut

| Contrainte | Minimum garanti |
|------------|-----------------|
| Chiffres (0-9) | 9 |
| Caractères spéciaux (`!@#$%^&*`...) | 9 |
| Lettres minuscules (a-z) | 1 |
| Lettres majuscules (A-Z) | 1 |
| **Longueur minimale totale** | **20 caractères** |

Les contraintes de chiffres et caractères spéciaux sont paramétrables via `--min-digits` et `--min-special`.

Le module Python `secrets` est utilisé pour la génération (CSPRNG — Cryptographically Secure Pseudo-Random Number Generator).

---

## Installation

### Prérequis

- Python 3.12 ou supérieur
- Poetry (gestionnaire de dépendances)

### Étapes

```bash
git clone https://github.com/valorisa/Password-Generator-Advanced.git
cd Password-Generator-Advanced
poetry install
```

---

## Utilisation

### Mode interactif

```bash
python -m password_generator_advanced
```

Le menu interactif s'affiche :

```
==================================================
   GÉNÉRATEUR DE MOTS DE PASSE SÉCURISÉS
==================================================

Contraintes appliquées :
  - Minimum 9 chiffres
  - Minimum 9 caractères spéciaux
  - Au moins 1 lettre minuscule
  - Au moins 1 lettre majuscule
  - Longueur minimale : 20 caractères

--------------------------------------------------
  1 - Générer un mot de passe
  2 - Générer plusieurs mots de passe
  3 - Générer une passphrase
  4 - Évaluer un mot de passe / passphrase
  5 - Quitter
--------------------------------------------------
```

### Mode CLI

```bash
# Générer un mot de passe (longueur 30)
python -m password_generator_advanced --length 30

# Générer 5 mots de passe
python -m password_generator_advanced --length 25 --count 5

# Contraintes personnalisées
python -m password_generator_advanced --length 20 --min-digits 3 --min-special 5

# Générer une passphrase (6 mots par défaut)
python -m password_generator_advanced --passphrase

# Passphrase avec options
python -m password_generator_advanced --passphrase --words 8 --separator "."

# Évaluer un mot de passe existant
python -m password_generator_advanced --evaluate "mon-super-mot-de-passe!"

# Copier le résultat dans le presse-papier
python -m password_generator_advanced --length 25 --copy
```

### Options CLI complètes

| Option | Court | Description |
|--------|-------|-------------|
| `--length` | `-l` | Longueur du mot de passe |
| `--min-digits` | | Nombre minimum de chiffres (défaut: 9) |
| `--min-special` | | Nombre minimum de caractères spéciaux (défaut: 9) |
| `--count` | `-n` | Nombre de mots de passe à générer |
| `--passphrase` | `-p` | Générer une passphrase |
| `--words` | `-w` | Nombre de mots pour la passphrase (défaut: 6) |
| `--separator` | | Séparateur pour la passphrase (défaut: `-`) |
| `--evaluate` | `-e` | Évaluer la force d'un mot de passe |
| `--copy` | `-c` | Copier dans le presse-papier |

---

## Évaluation de mot de passe

L'outil peut évaluer la force d'un mot de passe ou passphrase existant :

```
  Évaluation :
    Longueur         : 28 caractères
    Entropie         : 164.0 bits
    Force            : Très fort
    Jeu de caractères: 58 symboles possibles

  Catégories détectées :
    Minuscules       : ✓
    Majuscules       : ✗
    Chiffres         : ✗
    Spéciaux         : ✓
```

Échelle de force :

| Entropie | Force |
|----------|-------|
| < 40 bits | Très faible |
| 40-59 bits | Faible |
| 60-79 bits | Moyen |
| 80-127 bits | Fort |
| ≥ 128 bits | Très fort |

---

## Architecture du projet

```
Password-Generator-Advanced/
├── src/
│   └── password_generator_advanced/
│       ├── __init__.py          # Version du package
│       ├── __main__.py          # Point d'entrée python -m
│       ├── main.py              # Menu interactif + CLI argparse
│       ├── generator.py         # Algorithme de génération + évaluation
│       ├── wordlist.py          # Liste de 2048 mots pour passphrases
│       └── clipboard.py         # Copie presse-papier cross-platform
├── tests/
│   └── test_generator.py       # 18 tests
├── pyproject.toml               # Configuration Poetry
├── LICENSE                      # MIT
├── SECURITY.md
├── CONTRIBUTING.md
└── CODE_OF_CONDUCT.md
```

### Algorithme de génération (`generator.py`)

1. **Placement garanti** : N chiffres + N caractères spéciaux + 1 minuscule + 1 majuscule sont placés en premier
2. **Remplissage** : Les positions restantes sont remplies avec un mélange aléatoire de toutes les catégories
3. **Mélange final** : L'ensemble est mélangé via `secrets.SystemRandom().shuffle()` pour éliminer tout pattern positionnel prévisible

### Génération de passphrases

Sélection aléatoire de mots depuis une liste de 2048 mots (11 bits d'entropie par mot). Une passphrase de 6 mots offre ~66 bits d'entropie.

---

## Sécurité

- **Module `secrets`** : Utilise le générateur aléatoire cryptographiquement sécurisé du système d'exploitation (`/dev/urandom` sur Linux/macOS, `CryptGenRandom` sur Windows)
- **Aucune dépendance externe** : Uniquement la bibliothèque standard Python — pas de surface d'attaque tierce
- **Pas de stockage** : Les mots de passe générés ne sont jamais écrits sur disque ni envoyés sur le réseau

Pour signaler une vulnérabilité, consultez [SECURITY.md](SECURITY.md).

---

## Développement

```bash
# Lancer les tests
poetry run pytest tests/ -v

# Vérifier le style
poetry run ruff check .

# Corriger automatiquement
poetry run ruff check . --fix
```

---

## Contribution

Les contributions sont bienvenues. Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour le processus détaillé.

Ce projet respecte le [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

---

## Licence

[MIT](LICENSE) - Utilisation libre, commerciale et modification autorisées.

---

**Auteur** : [valorisa](https://github.com/valorisa)
