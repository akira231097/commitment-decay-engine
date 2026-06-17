# Privacy and Safety

Commitment tracking can become invasive if it is designed carelessly. This project is built around supportive accountability.

## What Not To Store

Do not commit:

- real private transcripts
- Slack exports
- customer data
- phone numbers
- email lists
- API tokens
- OAuth credentials
- private ticket descriptions
- sensitive HR or legal context

Use fictional examples or anonymized fixtures only.

## Nudge Rules

Nudges should be:

- private
- kind
- specific
- rate-limited
- easy to dismiss
- framed as help, not blame

Bad:

> You still have not done the API task.

Better:

> Hey Ava - you mentioned the API task in the product sync. I have not seen related activity yet. Want me to create a ticket, or has it been handled somewhere I have not checked?

## Analytics Rules

Analytics should identify process problems:

- too many verbal commitments
- missing ticket creation
- unclear owners
- recurring blocked areas
- unrealistic deadlines

Avoid public leaderboards or individual shame metrics.

## Public Repo Scope

This repo intentionally uses fictional people and fake evidence links. Production deployments should keep private data in private storage and commit only code, schemas, and sanitized examples.
