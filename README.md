# Agrasandhani

**A focused CLI security scanner for web applications**, aligned with OWASP Top 10 and the OWASP Web Security Testing Guide (WSTG).

## Features (Current)

- Clean, modern CLI built with Typer + Rich
- Single URL scanning
- Basic reconnaissance
- Security Headers check (maps to Security Misconfiguration)
- JSON and Table output
- Extensible check architecture

## Installation (Development)

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e .

# Or using pip
pip install -e .
```

## Usage

```bash
# Basic scan
agrasandhani scan https://example.com

# With verbose output
agrasandhani scan https://example.com -v

# JSON output
agrasandhani scan https://example.com -o json
```

## Project Goals

- Provide practical, focused security testing mapped to real-world risks (OWASP Top 10)
- Maintain clean, extensible architecture
- Be useful for developers and security professionals
- Build in public with high code quality

## Roadmap

- Add more OWASP Top 10 checks
- Support for authenticated scanning
- HTML reporting
- Better crawling with Playwright
- Parallel checks execution

## License

MIT License
