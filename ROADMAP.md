# Agrasandhani Roadmap & Coverage Ledger

Agrasandhani is built by following two OWASP references as its source of truth:

- **OWASP Top 10 (2021)** — <https://github.com/OWASP/Top10> — *what* risks matter.
- **OWASP Web Security Testing Guide (WSTG v4.2)** — <https://github.com/OWASP/wstg> — *how* to test for them.

Every check maps to at least one **Top 10 category** and one **WSTG test ID** so that coverage is auditable rather than anecdotal. This document is the single place that tracks *what we plan to cover* (Roadmap) and *what is actually implemented* (Ledger).

> **Design principle:** default to **safe, passive, non-intrusive** checks. Anything active or intrusive (injection probes, brute force, fuzzing) is **opt-in**, gated behind an explicit flag and an authorization acknowledgement. See [DISCLAIMER.md](DISCLAIMER.md).

---

## Coverage Ledger

Legend: ✅ Done · 🟡 In progress / partial · ⬜ Planned

### OWASP Top 10 (2021) coverage

| ID  | Category                                   | Status | Notes |
|-----|--------------------------------------------|:------:|-------|
| A01 | Broken Access Control                      | ⬜ | Planned — Phase 4 (authorization/IDOR heuristics) |
| A02 | Cryptographic Failures                     | 🟡 | TLS/HSTS/cookie-security checks scoped for Phase 1 |
| A03 | Injection                                  | ⬜ | Planned — Phase 3 (opt-in active tests) |
| A04 | Insecure Design                            | ⬜ | Partially emergent from other checks; no direct test |
| A05 | Security Misconfiguration                  | 🟡 | Security-headers check built; wiring + value validation in Phase 1 |
| A06 | Vulnerable & Outdated Components           | ⬜ | Planned — Phase 5 (JS library version → advisory) |
| A07 | Identification & Authentication Failures   | ⬜ | Planned — Phase 4 |
| A08 | Software & Data Integrity Failures         | ⬜ | Planned — Phase 5 (SRI, integrity) |
| A09 | Security Logging & Monitoring Failures     | ⬜ | Out of scope for a black-box scanner; documentation only |
| A10 | Server-Side Request Forgery (SSRF)         | ⬜ | Planned — Phase 5 (surface detection only) |

### WSTG category coverage

| WSTG      | Category                                   | Status | Phase |
|-----------|--------------------------------------------|:------:|:-----:|
| WSTG-INFO | Information Gathering                       | 🟡 | 0–2 |
| WSTG-CONF | Configuration & Deployment Management       | 🟡 | 1 |
| WSTG-IDNT | Identity Management                         | ⬜ | 4 |
| WSTG-ATHN | Authentication                              | ⬜ | 4 |
| WSTG-ATHZ | Authorization                               | ⬜ | 4 |
| WSTG-SESS | Session Management                          | ⬜ | 4 |
| WSTG-INPV | Input Validation                            | ⬜ | 3 |
| WSTG-ERRH | Error Handling                              | ⬜ | 1 |
| WSTG-CRYP | Cryptography                                | ⬜ | 1 |
| WSTG-BUSL | Business Logic                              | ⬜ | — (manual; not automatable) |
| WSTG-CLNT | Client-side                                 | ⬜ | 3 |
| WSTG-APIT | API Testing                                 | ⬜ | future |

### Implemented checks (current build)

| Check                         | Category (Top 10 / WSTG)        | Status | Location |
|-------------------------------|---------------------------------|:------:|----------|
| Basic reconnaissance (homepage reachability) | WSTG-INFO       | ✅ | `core/scanner.py` |
| Security Headers (presence)   | A05 / WSTG-CONF-07              | 🟡 | `checks/security_headers.py` — *built but not yet wired into the scanner, and only tests presence, not values* |

---

## Roadmap

### Phase 0 — Foundation *(mostly complete)*
- ✅ CLI scaffold (Typer + Rich), `scan` / `version` commands
- ✅ Pydantic config with optional YAML loading
- ✅ Async HTTP client wrapper (httpx)
- ✅ Pluggable check architecture (`BaseCheck` ABC)
- ✅ Basic recon + JSON/table output
- 🟡 Register and execute checks through the plugin system (headers check is not yet invoked)

### Phase 1 — MVP: Passive configuration & crypto hygiene
*Focus: A02, A05 · WSTG-CONF, WSTG-CRYP, WSTG-ERRH*
- ⬜ Wire the check registry into `Scanner`; run checks concurrently
- ⬜ Security headers — **value validation** (weak CSP, permissive X-Frame-Options, etc.), not just presence
- ⬜ Cookie security attributes (`Secure`, `HttpOnly`, `SameSite`)
- ⬜ TLS / HTTPS enforcement, HTTP→HTTPS redirect, HSTS correctness
- ⬜ Server / framework fingerprinting & version disclosure (`Server`, `X-Powered-By`)
- ⬜ Information disclosure: verbose error pages, stack traces, HTML comments
- ⬜ Sensitive-file probing (`robots.txt`, `.git/`, `.env`, backups) — safe GETs only
- ⬜ Directory-listing detection
- ⬜ Structured finding model: severity, evidence, remediation, Top 10 + WSTG tags
- ⬜ HTML report output (Jinja2)

### Phase 2 — Crawling & content discovery
*Focus: WSTG-INFO*
- ⬜ Playwright-based crawler with scope control + depth limit
- ⬜ Link / form / endpoint enumeration
- ⬜ `sitemap.xml` / `robots.txt` parsing
- ⬜ Comment & metadata extraction, mixed-content detection

### Phase 3 — Active input validation *(opt-in, intrusive)*
*Focus: A03 · WSTG-INPV, WSTG-CLNT*
- ⬜ Reflected XSS probes (safe, non-destructive payloads)
- ⬜ Error-based SQL injection detection
- ⬜ Open redirect, host-header injection
- ⬜ CORS misconfiguration
- ⬜ Global safety guards: rate limiting, per-target authorization gate, `--aggressive` opt-in

### Phase 4 — Authentication, authorization & session
*Focus: A01, A07 · WSTG-ATHN, WSTG-ATHZ, WSTG-SESS, WSTG-IDNT*
- ⬜ Session cookie analysis and fixation checks
- ⬜ Authenticated scanning (inject session / credentials)
- ⬜ Login/logout flow handling, default-credential check (opt-in)
- ⬜ Access-control / IDOR heuristics

### Phase 5 — Components, integrity & SSRF surface
*Focus: A06, A08, A10*
- ⬜ Known-vulnerable JS library detection (version → advisory database)
- ⬜ Subresource Integrity (SRI) checks
- ⬜ SSRF surface identification (report only, no exploitation)

### Phase 6 — Reporting & ecosystem
- ⬜ SARIF output for CI / GitHub code scanning
- ⬜ HTML / PDF reports, baseline diffing between runs
- ⬜ Config profiles (`safe` / `aggressive`)
- ⬜ Docker image + GitHub Action

---

## Contributing to the roadmap

New checks should update **both** tables above in the same pull request that adds the check, so the ledger never drifts from reality. See [CONTRIBUTING.md](CONTRIBUTING.md).
