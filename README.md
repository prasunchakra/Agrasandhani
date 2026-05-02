# Agrasandhani

**A focused CLI security scanner for web applications**, aligned with the
[OWASP Top 10](https://github.com/OWASP/Top10) and the
[OWASP Web Security Testing Guide (WSTG)](https://github.com/OWASP/wstg).

> *Agrasandhani* (अग्रसन्धानी) is, in Hindu tradition, the ledger in which every
> deed is meticulously recorded — a fitting name for a tool that audits and keeps
> account of a web application's security posture.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Status: pre-1.0](https://img.shields.io/badge/status-pre--1.0-orange.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)

---

## ⚠️ Legal notice — read first

Agrasandhani is a security testing tool. Use it **only** against systems you own
or are **explicitly authorized in writing** to test. Unauthorized scanning is
illegal in most jurisdictions. The software is provided "as is", with **no
warranty** and **no liability** for misuse.

**Full terms: [DISCLAIMER.md](DISCLAIMER.md).** If you don't agree, don't use it.

---

## Features (current)

- Clean, modern CLI built with Typer + Rich
- Single-URL scanning with basic reconnaissance
- Security Headers check (maps to *Security Misconfiguration*) — *being wired in*
- JSON and table output
- Extensible, plugin-based check architecture

> This project is **pre-1.0 and built in public.** Expect rapid change. See the
> [Roadmap & Coverage Ledger](ROADMAP.md) for exactly what is and isn't done.

## Installation (development)

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e .

# Or using pip
pip install -e .
```

Requires **Python 3.11+**.

## Usage

```bash
# Basic scan
agrasandhani scan https://example.com

# Verbose output
agrasandhani scan https://example.com -v

# JSON output
agrasandhani scan https://example.com -o json
```

## How coverage is tracked

Every check maps to at least one **OWASP Top 10** category and one **WSTG** test
ID, so coverage is auditable. The authoritative, always-updated status lives in
**[ROADMAP.md](ROADMAP.md)**. A snapshot:

### Coverage at a glance

Legend: ✅ Done · 🟡 Partial · ⬜ Planned

| OWASP Top 10 (2021)                       | Status |
|-------------------------------------------|:------:|
| A02 Cryptographic Failures                | 🟡 |
| A05 Security Misconfiguration             | 🟡 |
| A01 · A03 · A06 · A07 · A08 · A10         | ⬜ |

### Roadmap glimpse

| Phase | Theme | Focus |
|:-----:|-------|-------|
| **0** | Foundation *(mostly done)* | CLI, config, async HTTP, plugin architecture |
| **1** | **MVP** — passive config & crypto hygiene | Headers, cookies, TLS/HSTS, info disclosure, HTML report |
| **2** | Crawling & content discovery | Playwright crawler, endpoint/form enumeration |
| **3** | Active input validation *(opt-in)* | XSS/SQLi/redirect probes with safety guards |
| **4** | AuthN / AuthZ / Session | Authenticated scans, IDOR heuristics |
| **5** | Components, integrity & SSRF surface | Vulnerable JS libs, SRI, SSRF detection |
| **6** | Reporting & ecosystem | SARIF/CI, Docker, GitHub Action |

## Project goals

- Practical, focused testing mapped to real-world risk (OWASP Top 10 / WSTG)
- Safe-by-default: intrusive checks are always opt-in
- Clean, extensible architecture
- High code quality, built in public

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and our
[Code of Conduct](CODE_OF_CONDUCT.md). To report a vulnerability **in
Agrasandhani itself**, follow [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE) © 2026 Prasun Chakraborty
