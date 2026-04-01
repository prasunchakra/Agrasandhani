# Agrasandhani

**Forecasts where the next breach hits.**

Agrasandhani is a background model that listens to a broad range of open threat signals and predicts which sectors and regions are at elevated risk of a publicly disclosed breach in the next 48 to 72 hours.

The name comes from the ledger kept by Chitragupta, the record-keeper in Hindu mythology who logs every deed and uses the record to decide what happens next. Read literally, it means roughly *the one who looks ahead*. Both meanings describe the tool: it keeps the ledger, then it forecasts.

> **Status:** pre-alpha. The pipeline, data model and baseline model are being built in the open. Nothing here should be used for operational decisions yet.

---

## What it does

Every few hours, Agrasandhani:

1. **Ingests** public signals: ransomware leak-site postings, CISA KEV additions, EPSS score changes, NVD advisories, GDELT news events with cyber themes, vendor and CERT advisories, and threat-intel feeds via OpenCTI.
2. **Normalises** them into a single event ledger keyed by `(timestamp, sector, region, actor, technique)`, using STIX 2.1 vocabularies and MITRE ATT&CK mappings.
3. **Builds features** over a `sector × region × day` grid: recent breach tempo, active-group cadence, exploitation pressure on software that sector depends on, news volume and tone.
4. **Forecasts** the expected number of disclosed breaches per cell over the next 2 and 3 days, with calibrated prediction intervals.
5. **Publishes** the forecast as a ranked risk table, a geographic heat map and a JSON API.

The output is a probability, not a prophecy. The goal is to tell a defender in healthcare in Western Europe that this week looks worse than baseline and why, early enough to act on it.

## What it is not

- Not an attribution tool. It does not claim to know who is behind anything.
- Not a vulnerability scanner or an EDR. It does not look at your network.
- Not a replacement for a threat-intel team. It is a prior they can argue with.

---

## Architecture

```
            ┌────────────────────────────────────────────────────────────┐
            │                        Signals                             │
            │  ransomware.live · CISA KEV · EPSS · NVD · GDELT · OpenCTI │
            └───────────────┬────────────────────────────────────────────┘
                            │  Dagster assets
                            ▼
            ┌────────────────────────────────────────────────────────────┐
            │  Scribe  — ingestion & normalisation (STIX 2.1, ATT&CK)    │
            └───────────────┬────────────────────────────────────────────┘
                            ▼
            ┌────────────────────────────────────────────────────────────┐
            │  Ledger  — Postgres + TimescaleDB event store, pgvector    │
            └───────────────┬────────────────────────────────────────────┘
                            ▼
            ┌────────────────────────────────────────────────────────────┐
            │  Verdict — feature grid, forecast model, conformal bounds  │
            └───────────────┬────────────────────────────────────────────┘
                            ▼
            ┌────────────────────────────────────────────────────────────┐
            │  Surface — FastAPI · risk table · map · alerts             │
            └────────────────────────────────────────────────────────────┘
```

The three internal names map to the mythology and are used consistently in code: **Scribe** writes to the ledger, **Ledger** holds the record, **Verdict** reads it and decides.

## Built on

Agrasandhani deliberately composes existing open-source projects rather than reinventing them.

| Concern | Library / project |
|---|---|
| Orchestration | [Dagster](https://dagster.io) |
| Threat-intel graph & feed connectors | [OpenCTI](https://github.com/OpenCTI-Platform/opencti), [stix2](https://github.com/oasis-open/cti-python-stix2) |
| ATT&CK mappings | [mitreattack-python](https://github.com/mitre-attack/mitreattack-python) |
| Breach ground truth | [ransomware.live](https://www.ransomware.live), [ransomwatch](https://github.com/joshhighet/ransomwatch), HHS OCR breach portal, SEC EDGAR 8-K |
| Exploitation signals | [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog), [FIRST EPSS](https://www.first.org/epss/), NVD |
| News & event stream | [GDELT](https://www.gdeltproject.org), [trafilatura](https://github.com/adbar/trafilatura) |
| Text extraction | [spaCy](https://spacy.io), [GLiNER](https://github.com/urchade/GLiNER), [sentence-transformers](https://www.sbert.net) |
| Storage | PostgreSQL, [TimescaleDB](https://github.com/timescale/timescaledb), [pgvector](https://github.com/pgvector/pgvector), [DuckDB](https://duckdb.org) |
| Modelling | [LightGBM](https://github.com/microsoft/LightGBM), [tick](https://github.com/X-DataInitiative/tick) (Hawkes), [statsforecast](https://github.com/Nixtla/statsforecast) |
| Calibration | [MAPIE](https://github.com/scikit-learn-contrib/MAPIE) (conformal prediction) |
| Evaluation & ops | [MLflow](https://mlflow.org), [Evidently](https://github.com/evidentlyai/evidently), [Great Expectations](https://greatexpectations.io) |
| Serving & UI | [FastAPI](https://fastapi.tiangolo.com), [Streamlit](https://streamlit.io) (prototype), [kepler.gl](https://kepler.gl) |

## Repository layout

```
agrasandhani/
├── agra/                   # Python package (short handle used in code and CLI)
│   ├── scribe/             # ingestion assets, one module per source
│   ├── ledger/             # schema, migrations, event model
│   ├── verdict/            # features, models, calibration, backtests
│   └── surface/            # API, dashboard, alerting
├── dagster/                # Dagster definitions and schedules
├── notebooks/              # exploration and backtest reports
├── tests/
├── docs/
│   ├── data-model.md
│   ├── signals.md          # every source: licence, cadence, fields used
│   └── evaluation.md       # how we score forecasts
├── docker-compose.yml      # Postgres/Timescale, OpenCTI, Dagster, API
├── pyproject.toml
└── README.md
```

## Quick start

> Not yet runnable. This section describes the intended developer experience and will be kept honest as the code lands.

```bash
git clone https://github.com/<org>/agrasandhani.git
cd agrasandhani
uv sync                          # or: pip install -e ".[dev]"
cp .env.example .env             # API keys for sources that need them
docker compose up -d             # Postgres/Timescale, Dagster, OpenCTI
agra scribe backfill --days 365  # pull historical signals and labels
agra verdict train               # fit the baseline model
agra verdict forecast --horizon 72h
agra surface serve               # http://localhost:8000
```

## How forecasts are evaluated

The base rate of a disclosed breach in any single `(sector, region, day)` cell is tiny, so accuracy is meaningless. Forecasts are scored on:

- **Brier score** and **log loss** against realised disclosures, per horizon.
- **Precision and recall at top-k cells**, because a user only acts on the top of the list.
- **Interval coverage** from the conformal layer: a 90% interval should contain the truth about 90% of the time.
- **Lift over a seasonal-naive baseline** (same cell, same weekday, trailing 8-week mean). If the model does not beat that, it does not ship.

All evaluation uses strict time-based splits. No feature may use information published after the forecast timestamp. See `docs/evaluation.md`.

## Roadmap

**v0.1 — baseline ledger and forecast**
ransomware.live, KEV, EPSS and GDELT into Timescale via Dagster; LightGBM count model on the sector × region × day grid; MAPIE intervals; Streamlit risk table and map; backtest report.

**v0.2 — richer signals**
OpenCTI as the intel graph; NLP extraction of sector, region, actor and technique from advisories and news; ATT&CK group-to-sector priors.

**v0.3 — temporal structure**
Hawkes process per cell to capture self-exciting breach clusters; ensemble with the tree model; per-actor cadence features.

**v0.4 — surface**
FastAPI with versioned forecasts; alerting on cells crossing a threshold; forecast explanations (which signals moved the number).

## Contributing

Issues and pull requests are welcome once v0.1 lands. Until then the fastest way to help is to open an issue proposing a signal source, with its licence, update cadence and the fields you think matter.

Every source added to `scribe/` needs a matching entry in `docs/signals.md` covering licence and terms of use. Several upstream feeds have restrictions on redistribution; we respect them.

## License

Apache License 2.0. See [LICENSE](LICENSE).

Agrasandhani aggregates data from third-party sources, each under its own terms. The license above covers this project's code, not the upstream data.
