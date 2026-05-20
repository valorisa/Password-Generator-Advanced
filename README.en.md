# Password-Generator-Advanced

> 🇺🇸 English version | 🇫🇷 [Version française](README.md)

[![CI](https://github.com/valorisa/Password-Generator-Advanced/actions/workflows/ci.yml/badge.svg)](https://github.com/valorisa/Password-Generator-Advanced/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/Password-Generator-Advanced.svg)](https://pypi.org/project/Password-Generator-Advanced/)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?logo=python&logoColor=white)
![Security: secrets](https://img.shields.io/badge/Security-secrets%20module-green.svg)

Secure command-line password generator with strict cryptographic constraints. Every generated password mandatorily contains lowercase letters, uppercase letters, digits, and special characters, with configurable minimums.

---

## Quick Installation

**Password-Generator-Advanced is available on PyPI!** Anyone can install it directly with pip:

```bash
pip install Password-Generator-Advanced
```

Once installed, simply run:

```bash
password-generator-advanced
```

The package is compatible with **Python 3.12+** and works on Linux, macOS, and Windows.

**What does this command do?**
- Automatically downloads the latest stable version from PyPI
- Installs the package in your Python environment
- Makes the `password-generator-advanced` command available globally

**Upgrade to the latest version:**

```bash
pip install --upgrade Password-Generator-Advanced
```

**Installation in a virtual environment (recommended):**

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install the package
pip install Password-Generator-Advanced
```

### Alternative: Installation from Source

If you want to contribute to the project or use the development version:

```bash
git clone https://github.com/valorisa/Password-Generator-Advanced.git
cd Password-Generator-Advanced
poetry install
```

**Prerequisites for source installation:**
- Python 3.12 or higher
- Poetry (dependency manager)

---

## Features

- Password generation with strict constraints (configurable)
- Passphrase generation (Diceware-style, 2048 words, 11 bits of entropy per word)
- Strength evaluation of existing passwords or passphrases
- Clipboard copy (Windows, macOS, Linux)
- Interactive mode (menu) and CLI mode (command-line arguments)

---

## Default Constraints

| Constraint | Guaranteed Minimum |
|------------|-------------------|
| Digits (0-9) | 9 |
| Special characters (`!@#$%^&*`...) | 9 |
| Lowercase letters (a-z) | 1 |
| Uppercase letters (A-Z) | 1 |
| **Total minimum length** | **20 characters** |

Digit and special character constraints are configurable via `--min-digits` and `--min-special`.

Python's `secrets` module is used for generation (CSPRNG — Cryptographically Secure Pseudo-Random Number Generator).

---

## Usage

### Interactive Mode

**If you installed via pip from PyPI:**

```bash
password-generator-advanced
```

**If you're using the source installation (with Poetry):**

```bash
python -m password_generator_advanced
```

*Note: Both commands are equivalent and launch the same program.*

The interactive menu displays:

```
==================================================
   SECURE PASSWORD GENERATOR
==================================================

Applied constraints:
  - Minimum 9 digits
  - Minimum 9 special characters
  - At least 1 lowercase letter
  - At least 1 uppercase letter
  - Minimum length: 20 characters

--------------------------------------------------
  1 - Generate a password
  2 - Generate multiple passwords
  3 - Generate a passphrase
  4 - Evaluate a password / passphrase
  5 - Quit
--------------------------------------------------
```

### CLI Mode

```bash
# Generate a password (length 30)
python -m password_generator_advanced --length 30

# Generate 5 passwords
python -m password_generator_advanced --length 25 --count 5

# Custom constraints
python -m password_generator_advanced --length 20 --min-digits 3 --min-special 5

# Generate a passphrase (6 words by default)
python -m password_generator_advanced --passphrase

# Passphrase with options
python -m password_generator_advanced --passphrase --words 8 --separator "."

# Evaluate an existing password
python -m password_generator_advanced --evaluate "my-super-password!"

# Copy the result to clipboard
python -m password_generator_advanced --length 25 --copy
```

### Complete CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--length` | `-l` | Password length |
| `--min-digits` | | Minimum number of digits (default: 9) |
| `--min-special` | | Minimum number of special characters (default: 9) |
| `--count` | `-n` | Number of passwords to generate |
| `--passphrase` | `-p` | Generate a passphrase |
| `--words` | `-w` | Number of words for the passphrase (default: 6) |
| `--separator` | | Separator for the passphrase (default: `-`) |
| `--evaluate` | `-e` | Evaluate the theoretical entropy of a password |
| `--copy` | `-c` | Copy to clipboard |

---

## Password Evaluation

The tool can evaluate the maximum theoretical entropy of an existing password or passphrase:

```
  Maximum theoretical entropy:
    Length           : 28 characters
    Max. entropy     : 164.0 bits
    Level            : Very strong
    Character set    : 58 possible symbols

  Detected categories:
    Lowercase        : ✓
    Uppercase        : ✗
    Digits           : ✗
    Special chars    : ✓

  ⚠ This calculation assumes random choice per character.
    A password based on dictionary words or predictable
    patterns will have lower actual entropy.
```

Thresholds (aligned with ANSSI recommendations):

| Entropy | Level |
|---------|-------|
| < 48 bits | Very weak |
| 48-63 bits | Weak |
| 64-79 bits | Medium |
| 80-127 bits | Strong |
| ≥ 128 bits | Very strong |

---

## Project Architecture

```
Password-Generator-Advanced/
├── src/
│   └── password_generator_advanced/
│       ├── __init__.py          # Package version
│       ├── __main__.py          # python -m entry point
│       ├── main.py              # Interactive menu + CLI argparse
│       ├── generator.py         # Generation algorithm + evaluation
│       ├── wordlist.py          # List of 2048 words for passphrases
│       └── clipboard.py         # Cross-platform clipboard copy
├── tests/
│   └── test_generator.py       # 18 tests
├── pyproject.toml               # Poetry configuration
├── LICENSE                      # MIT
├── SECURITY.md
├── CONTRIBUTING.md
└── CODE_OF_CONDUCT.md
```

### Generation Algorithm (`generator.py`)

1. **Guaranteed placement**: N digits + N special characters + 1 lowercase + 1 uppercase are placed first
2. **Filling**: Remaining positions are filled with a random mix of all categories
3. **Final shuffle**: The whole set is shuffled via `secrets.SystemRandom().shuffle()` to eliminate any predictable positional pattern

### Passphrase Generation

Random selection of words from a list of 2048 words (11 bits of entropy per word). A 6-word passphrase offers ~66 bits of entropy.

---

## Security

- **`secrets` module**: Uses the operating system's cryptographically secure random generator (`/dev/urandom` on Linux/macOS, `CryptGenRandom` on Windows)
- **No external dependencies**: Only Python standard library — no third-party attack surface
- **No storage**: Generated passwords are never written to disk or sent over the network

To report a vulnerability, consult [SECURITY.md](SECURITY.md).

---

## Development

```bash
# Run tests
poetry run pytest tests/ -v

# Check style
poetry run ruff check .

# Auto-fix
poetry run ruff check . --fix
```

---

## Contributing

Contributions are welcome. Consult [CONTRIBUTING.md](CONTRIBUTING.md) for the detailed process.

This project adheres to the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

---

## License

[MIT](LICENSE) - Free use, commercial use, and modifications allowed.

---

**Author**: [valorisa](https://github.com/valorisa)
