# Architecture

Commitment Decay Engine is split into policy modules and integration adapters.

The public repo only includes local-file adapters so it can run without private credentials.

## Flow

```text
Transcript or chat export
  -> extractor
  -> markdown ledger
  -> evidence reconciler
  -> nudge policy
  -> analytics report
```

## Modules

### Extractor

`commitment_decay_engine.extractor` parses speaker-labeled text and extracts likely commitments. The public implementation is deterministic and conservative.

In a production system, this can be replaced with an LLM extractor that returns the same `Commitment` dataclass.

### Ledger

`commitment_decay_engine.ledger` stores each commitment as a markdown file. Markdown is intentionally boring:

- easy to audit
- easy to diff
- easy to edit manually
- friendly to git history

### Reconciler

`commitment_decay_engine.reconcile` compares open commitments against evidence items. Evidence can come from tickets, pull requests, team chat, meeting notes, or any adapter that produces `EvidenceItem`.

The engine only marks a commitment fulfilled when evidence includes completion-like language such as `done`, `merged`, `shipped`, `deployed`, or `resolved`.

### Nudge Policy

`commitment_decay_engine.nudges` decides whether a private reminder is appropriate.

The public policy includes:

- minimum age before nudging
- max nudges per commitment
- one nudge per day for a commitment
- empathetic templates

Real deployments should add channel-level rate limits and quiet hours.

### Analytics

`commitment_decay_engine.analytics` summarizes open, fulfilled, and stale work. Reports should be used to improve team systems, not to shame people.

## Adapter Boundary

Adapters should live outside the core policy. Examples:

- Slack adapter: fetch channel messages and send private DMs
- Linear/Jira adapter: fetch issues and status changes
- GitHub adapter: fetch merged PRs and issue closures
- Transcript adapter: ingest meeting transcripts

Each adapter should produce plain commitments or evidence items. The core engine should not know about vendor-specific APIs.
