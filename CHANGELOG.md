# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-17

Initial public release of the Commitment Decay Engine — a supportive,
offline-first commitment tracking pipeline for fast-moving teams.

### Added

- **Deterministic commitment extraction** (`extractor.py`): a conservative
  regex parser that reads speaker-labeled transcript lines (`Name: utterance`)
  and keeps only first-person future-intent promises (`I'll`, `I will`, `I can`,
  `I am going to`, `Let me`), filtering out non-commitments via a blocklist
  (`we should`, `i already`, `i fixed`, ...). Derives a title, a coarse deadline
  (today / tomorrow / weekday / ISO date), and up to five keywords per
  commitment. Documented as a drop-in seam for an LLM-based extractor.
- **Lossless markdown ledger** (`ledger.py`): each commitment is persisted as a
  single git-diffable, hand-editable `.md` file keyed by a slugified
  `date-person-title`, with a render/parse round-trip driven by a regex field
  table. No database required.
- **Evidence reconciliation** (`reconcile.py`): keyword- and actor-based scoring
  matches commitments to JSON evidence items, with a `+2` actor-match boost and a
  minimum score of 2 to prevent false matches. Marks a commitment **Fulfilled**
  only when the best evidence contains completion language (`done`, `merged`,
  `shipped`, `deployed`, `resolved`, ...); weaker matches are recorded as
  progress and left **Open**.
- **Empathy-as-policy nudges** (`nudges.py`): `evaluate_nudge` is a pure function
  gated by minimum age (default 2 days), a max-nudge cap (default 3), and a
  one-nudge-per-day limit. Private message templates escalate gently with nudge
  count, ending with "No judgment - priorities shift."
- **Weekly analytics** (`analytics.py`): `summarize` aggregates the ledger into
  status counts, per-person fulfillment rates, and a list of open items, framed
  to surface process problems rather than rank individuals.
- **Typed data model** (`models.py`): slotted `Commitment` and `EvidenceItem`
  dataclasses, a `CommitmentStatus` `StrEnum` (Open / Fulfilled / Stale), and an
  `EvidenceItem.from_dict` JSON loader.
- **CLI** (`cli.py`): `argparse`-based `cde` entrypoint with `demo`, `extract`,
  `list`, `reconcile`, and `report` subcommands, including an end-to-end `demo`
  that runs the full pipeline against bundled fixtures.
- **Bundled fixtures**: `examples/sample_transcript.txt` and
  `examples/sample_evidence.json` containing only fictional people and fake
  evidence links, enabling fully offline demo runs with no credentials.
- **Documentation**: `README.md`, `docs/architecture.md`, `docs/privacy.md`, and
  `SECURITY.md` covering the design, adapter boundary, and data-handling stance.
- **Tests**: `pytest` suites for the extractor, ledger, reconciler, and nudge
  policy (`tests/`).
- **Tooling**: `pyproject.toml` (setuptools) packaging, an optional `dev`
  dependency group, a GitHub Actions CI workflow running the test suite on
  Python 3.11, and an `.env.example` listing optional (empty) adapter
  credentials for future integrations.

[1.0.0]: https://github.com/akira231097/commitment-decay-engine/releases/tag/v1.0.0
