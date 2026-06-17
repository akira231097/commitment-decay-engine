# Commitment Decay Engine

Supportive accountability for fast-moving teams.

Commitment Decay Engine turns messy meeting notes and chat updates into a lightweight commitment ledger, then helps teams reconcile what was promised against evidence from follow-up notes, tickets, pull requests, and status updates.

The core idea is simple: commitments decay when nobody remembers them. The engine keeps track without turning follow-through into surveillance.

## Why This Exists

Most teams lose work in the gap between:

- "I'll take care of that"
- the ticket that never gets created
- the follow-up that happens in a different channel
- the teammate who forgot because priorities changed

This project models a safer workflow:

1. Extract commitments from transcripts or chat logs.
2. Store them as readable markdown files.
3. Reconcile them against evidence.
4. Mark clear completions as fulfilled.
5. Suggest private, empathetic nudges only when needed.
6. Generate weekly patterns without shaming individuals in public.

## What It Demonstrates

This repo is a public, sanitized implementation of a production-style operations agent pattern:

- transcript intake
- commitment extraction
- durable markdown ledger
- evidence matching
- nudge policy with rate limits
- stale-commitment handling
- weekly analytics
- CLI-first workflow
- demo mode without Slack, Linear, or private credentials

It is designed to be understandable in a few minutes and extensible in a few hours.

## Architecture

```text
meeting transcript / chat export
        |
        v
 commitment extractor
        |
        v
 markdown commitment ledger
        |
        v
 evidence reconciliation
        |
        v
 status update / private nudge suggestion / weekly report
```

The engine is deliberately adapter-friendly. The public repo ships with local-file inputs. Real deployments can add adapters for Slack, Linear, GitHub, Jira, Notion, or internal systems without changing the core policy logic.

## Quick Start

```bash
git clone https://github.com/akira231097/commitment-decay-engine.git
cd commitment-decay-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the demo:

```bash
cde demo
```

Extract commitments from the sample transcript:

```bash
cde extract examples/sample_transcript.txt --ledger .demo-ledger
```

List open commitments:

```bash
cde list --ledger .demo-ledger --status open
```

Reconcile against sample evidence:

```bash
cde reconcile --ledger .demo-ledger --evidence examples/sample_evidence.json
```

Generate a weekly report:

```bash
cde report --ledger .demo-ledger
```

## Example Commitment File

```markdown
## Commitment: Fix onboarding email copy
- **Person:** Maya
- **Source:** Weekly product sync
- **Date:** 2026-01-14
- **Commitment:** I will rewrite the onboarding email copy by Friday.
- **Deadline:** 2026-01-16
- **Status:** Open
- **Keywords:** onboarding, email, copy
- **Fulfillment evidence:** None yet
- **Last checked:** 2026-01-14
- **Nudge count:** 0
```

## Supportive Nudge Style

The engine does not send public reminders. It suggests private language like:

> Hey Maya - you mentioned rewriting the onboarding email copy in the product sync. I have not seen a related update yet. Want me to create a ticket for this, or has it been handled somewhere I have not checked?

The tone matters. The goal is to reduce dropped work, not create pressure theater.

## Repository Layout

```text
commitment_decay_engine/
  analytics.py      weekly summaries and follow-through patterns
  cli.py            command line interface
  extractor.py      transcript/chat commitment extraction
  ledger.py         markdown file persistence
  models.py         dataclasses and status enums
  nudges.py         rate limits and private reminder templates
  reconcile.py      evidence matching and status updates
examples/
  sample_transcript.txt
  sample_evidence.json
docs/
  architecture.md
  privacy.md
tests/
```

## Design Principles

- Supportive, not punitive.
- Private nudges only.
- Human-readable storage.
- Clear evidence before marking something fulfilled.
- Rate limits to avoid nagging.
- No secrets required for demo mode.
- Integrations are adapters, not core policy.

## Privacy

This public repo contains only fictional examples. Do not commit real transcripts, private Slack exports, customer data, tokens, phone numbers, or internal ticket data.

See [docs/privacy.md](docs/privacy.md).

## License

MIT
