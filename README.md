# Password-Generator-Advanced

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?logo=python&logoColor=white)
![Security: secrets](https://img.shields.io/badge/Security-secrets%20module-green.svg)

Générateur de mots de passe sécurisés en ligne de commande avec des contraintes cryptographiques strictes. Chaque mot de passe généré contient obligatoirement des lettres minuscules, majuscules, chiffres et caractères spéciaux, avec des minimums configurables.

---

## Installation Rapide

**Password-Generator-Advanced est disponible sur PyPI !** N'importe qui peut l'installer directement avec pip :

```bash
pip install Password-Generator-Advanced
```

Une fois installé, lancez simplement :

```bash
password-generator-advanced
```

Le package est compatible avec **Python 3.12+** et fonctionne sur Linux, macOS et Windows.

**Que fait cette commande ?**
- Télécharge automatiquement la dernière version stable depuis PyPI
- Installe le package dans votre environnement Python
- Rend la commande `password-generator-advanced` disponible globalement

**Mise à jour vers la dernière version :**

```bash
pip install --upgrade Password-Generator-Advanced
```

**Installation dans un environnement virtuel (recommandé) :**

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Linux/macOS :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate

# Installer le package
pip install Password-Generator-Advanced
```

### Alternative : Installation depuis les sources

Si vous souhaitez contribuer au projet ou utiliser la version de développement :

```bash
git clone https://github.com/valorisa/Password-Generator-Advanced.git
cd Password-Generator-Advanced
poetry install
```

**Prérequis pour l'installation depuis les sources :**
- Python 3.12 ou supérieur
- Poetry (gestionnaire de dépendances)

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

## Utilisation

### Mode interactif

**Si vous avez installé via pip depuis PyPI :**

```bash
password-generator-advanced
```

**Si vous utilisez l'installation depuis les sources (avec Poetry) :**

```bash
python -m password_generator_advanced
```

*Note : Les deux commandes sont équivalentes et lancent le même programme.*

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
| `--evaluate` | `-e` | Évaluer l'entropie théorique d'un mot de passe |
| `--copy` | `-c` | Copier dans le presse-papier |

---

## Évaluation de mot de passe

L'outil peut évaluer l'entropie théorique maximale d'un mot de passe ou passphrase existant :

```
  Entropie théorique maximale :
    Longueur         : 28 caractères
    Entropie max.    : 164.0 bits
    Niveau           : Très fort
    Jeu de caractères: 58 symboles possibles

  Catégories détectées :
    Minuscules       : ✓
    Majuscules       : ✗
    Chiffres         : ✗
    Spéciaux         : ✓

  ⚠ Ce calcul suppose un choix aléatoire par caractère.
    Un mot de passe basé sur des mots du dictionnaire ou des
    patterns prévisibles aura une entropie réelle inférieure.
```

Seuils (alignés sur les recommandations ANSSI) :

| Entropie | Niveau |
|----------|--------|
| < 48 bits | Très faible |
| 48-63 bits | Faible |
| 64-79 bits | Moyen |
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
