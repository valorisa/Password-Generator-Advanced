# Password-Generator-Advanced

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?logo=python&logoColor=white)
![Security: secrets](https://img.shields.io/badge/Security-secrets%20module-green.svg)

Générateur de mots de passe sécurisés en ligne de commande avec des contraintes cryptographiques strictes. Chaque mot de passe généré contient obligatoirement des lettres minuscules, majuscules, chiffres et caractères spéciaux, avec un minimum garanti de 9 chiffres et 9 caractères spéciaux.

---

## Pourquoi ce projet ?

La plupart des générateurs de mots de passe ne garantissent pas la présence de chaque catégorie de caractères. Password-Generator-Advanced applique des **contraintes strictes et non-négociables** à chaque génération :

| Contrainte | Minimum garanti |
|------------|-----------------|
| Chiffres (0-9) | 9 |
| Caractères spéciaux (`!@#$%^&*`...) | 9 |
| Lettres minuscules (a-z) | 1 |
| Lettres majuscules (A-Z) | 1 |
| **Longueur minimale totale** | **20 caractères** |

Le module Python `secrets` est utilisé pour la génération (CSPRNG — Cryptographically Secure Pseudo-Random Number Generator), contrairement à `random` qui n'est pas adapté à un usage sécuritaire.

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

```bash
poetry run python -m password_generator_advanced
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
  3 - Quitter
--------------------------------------------------

  Votre choix (1-3) :
```

### Générer un mot de passe unique

Choisissez `1`, puis indiquez la longueur souhaitée (minimum 20). Le mot de passe est affiché avec sa composition détaillée :

```
  Mot de passe généré :
  k7$2!mR9@4#8^1&5*3%6Qw
  Longueur : 23 caractères

  Composition :
    Chiffres         : 9
    Spéciaux         : 10
    Minuscules       : 2
    Majuscules       : 2
```

### Générer plusieurs mots de passe

Choisissez `2`, indiquez la longueur puis le nombre souhaité (1 à 50).

---

## Architecture du projet

```
Password-Generator-Advanced/
├── src/
│   └── password_generator_advanced/
│       ├── __init__.py          # Version du package
│       ├── main.py              # Menu interactif CLI
│       └── generator.py         # Algorithme de génération
├── tests/
├── pyproject.toml               # Configuration Poetry
├── LICENSE                      # MIT
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── CHANGELOG.md
```

### Algorithme de génération (`generator.py`)

1. **Placement garanti** : 9 chiffres + 9 caractères spéciaux + 1 minuscule + 1 majuscule sont placés en premier
2. **Remplissage** : Les positions restantes sont remplies avec un mélange aléatoire de toutes les catégories
3. **Mélange final** : L'ensemble est mélangé via `secrets.SystemRandom().shuffle()` pour éliminer tout pattern positionnel prévisible

Cette approche garantit mathématiquement le respect des contraintes tout en maximisant l'entropie du résultat.

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
