# Security Policy

## Supported Versions

This is an early public release. Use the latest version on `main`.

## Reporting a Vulnerability

Please open a GitHub issue for security concerns that do not include secrets or private data.

If a report requires sensitive detail, contact the repository owner privately through GitHub.

## Secret Handling

The demo does not require credentials.

If you add Slack, Linear, GitHub, Jira, or Notion adapters, use environment variables or a secret manager. Never commit `.env` files, tokens, transcripts, or real workspace exports.
