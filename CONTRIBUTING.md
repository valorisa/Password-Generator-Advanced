# Contributing to Password-Generator-Advanced

Thank you for your interest in contributing to **Password-Generator-Advanced**!

## Prerequisites

- Python 3.12 + Poetry

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feat/my-feature`
4. Make your changes
5. Run checks locally (see below)
6. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
7. Push and open a Pull Request

## Local Development

```bash
pip install poetry && poetry install
ruff check .
pytest tests/
poetry build
```

## Branch Naming

- `feat/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation only
- `refactor/*` - Code refactoring
- `test/*` - Adding or updating tests

## Commit Messages

We use [Conventional Commits 1.0.0](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `chore:` - Maintenance
- `refactor:` - Code refactoring
- `test:` - Tests

## Pull Request Process

1. Create branch following naming convention
2. Run all local checks
3. Commit using Conventional Commits
4. Open PR using the provided template
5. Wait for review from @valorisa

## Versioning

This project follows [SemVer 2.0.0](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).
