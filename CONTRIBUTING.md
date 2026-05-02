# Contributing to Agrasandhani

Thanks for your interest in contributing! Agrasandhani is built in public, and
contributions — checks, fixes, docs, ideas — are welcome.

## Before you start

- Read the [DISCLAIMER.md](DISCLAIMER.md). Agrasandhani is a *detection* tool,
  not an exploitation framework. Contributions that add exploitation or
  harm-causing capability will not be accepted.
- Skim the [ROADMAP.md](ROADMAP.md) to see where things fit and what's already
  covered.
- By contributing, you agree that your contributions are licensed under the
  project's [MIT License](LICENSE).

## Development setup

```bash
# Clone your fork, then:
uv venv
source .venv/bin/activate
uv pip install -e .

# Dev tooling (pytest, mypy, ruff) is declared in pyproject.toml
uv pip install -e ".[dev]"   # or install the dev-dependencies group with uv
```

Requires **Python 3.11+** (see `pyproject.toml`).

## Quality bar

Before opening a pull request, make sure:

```bash
ruff check .        # lint
ruff format .       # format
mypy .              # strict type checking (configured in pyproject.toml)
pytest              # tests pass
```

- Type hints are required; the project runs `mypy --strict`.
- New behavior needs tests. Network calls in tests must be mocked — **tests must
  never hit real external targets.**

## Adding a new check

1. Create a class in `agrasandhani/checks/` that subclasses `BaseCheck`.
2. Set `name` and `category`, and implement `async def run(...)`.
3. Every finding should carry: `title`, `severity`, `description`,
   `remediation`, and its **OWASP Top 10** and **WSTG** mapping.
4. Register the check so the scanner runs it.
5. **Update both coverage tables in [ROADMAP.md](ROADMAP.md)** in the same PR, so
   the ledger stays in sync with reality.
6. Add tests with mocked HTTP responses.

## Commit & PR guidelines

- Keep pull requests focused; one logical change per PR.
- Write a clear description: what, why, and how you tested it.
- Reference any related issue.

## Reporting bugs & requesting features

Open an issue. For **security vulnerabilities in Agrasandhani itself**, follow
[SECURITY.md](SECURITY.md) instead of opening a public issue.

## Code of Conduct

Participation is governed by our [Code of Conduct](CODE_OF_CONDUCT.md).
