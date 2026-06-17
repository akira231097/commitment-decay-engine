from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

from .models import Commitment, CommitmentStatus


FIELD_PATTERNS = {
    "person": r"\*\*Person:\*\*\s*(.+)",
    "source": r"\*\*Source:\*\*\s*(.+)",
    "date": r"\*\*Date:\*\*\s*(.+)",
    "commitment": r"\*\*Commitment:\*\*\s*(.+)",
    "deadline": r"\*\*Deadline:\*\*\s*(.+)",
    "status": r"\*\*Status:\*\*\s*(.+)",
    "keywords": r"\*\*Keywords:\*\*\s*(.+)",
    "fulfillment_evidence": r"\*\*Fulfillment evidence:\*\*\s*(.+)",
    "last_checked": r"\*\*Last checked:\*\*\s*(.+)",
    "nudge_count": r"\*\*Nudge count:\*\*\s*(\d+)",
    "last_nudged": r"\*\*Last nudged:\*\*\s*(.+)",
    "fulfilled_date": r"\*\*Fulfilled date:\*\*\s*(.+)",
}


class MarkdownLedger:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, commitment: Commitment) -> Path:
        path = self.root / f"{commitment.slug}.md"
        path.write_text(render_commitment(commitment), encoding="utf-8")
        return path

    def all(self) -> list[Commitment]:
        items: list[Commitment] = []
        for path in sorted(self.root.glob("*.md")):
            items.append(parse_commitment(path))
        return items

    def overwrite(self, commitment: Commitment) -> Path:
        return self.save(commitment)


def render_commitment(item: Commitment) -> str:
    lines = [
        f"## Commitment: {item.title}",
        f"- **Person:** {item.person}",
        f"- **Source:** {item.source}",
        f"- **Date:** {item.date.isoformat()}",
        f"- **Commitment:** {item.commitment}",
        f"- **Deadline:** {item.deadline}",
        f"- **Status:** {item.status.value}",
        f"- **Keywords:** {', '.join(item.keywords)}",
        f"- **Fulfillment evidence:** {item.fulfillment_evidence}",
        f"- **Last checked:** {_date_or_empty(item.last_checked)}",
        f"- **Nudge count:** {item.nudge_count}",
    ]
    if item.last_nudged:
        lines.append(f"- **Last nudged:** {item.last_nudged.isoformat()}")
    if item.fulfilled_date:
        lines.append(f"- **Fulfilled date:** {item.fulfilled_date.isoformat()}")
    return "\n".join(lines) + "\n"


def parse_commitment(path: Path) -> Commitment:
    content = path.read_text(encoding="utf-8")
    title_match = re.search(r"^## Commitment:\s*(.+)", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem
    fields = {name: _match(pattern, content) for name, pattern in FIELD_PATTERNS.items()}
    return Commitment(
        title=title,
        person=fields["person"],
        source=fields["source"],
        date=_parse_date(fields["date"]) or date.today(),
        commitment=fields["commitment"],
        deadline=fields["deadline"] or "Not specified",
        status=CommitmentStatus(fields["status"] or CommitmentStatus.OPEN.value),
        keywords=[part.strip() for part in fields["keywords"].split(",") if part.strip()],
        fulfillment_evidence=fields["fulfillment_evidence"] or "None yet",
        last_checked=_parse_date(fields["last_checked"]),
        nudge_count=int(fields["nudge_count"] or 0),
        last_nudged=_parse_date(fields["last_nudged"]),
        fulfilled_date=_parse_date(fields["fulfilled_date"]),
    )


def _match(pattern: str, content: str) -> str:
    found = re.search(pattern, content)
    return found.group(1).strip() if found else ""


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


def _date_or_empty(value: date | None) -> str:
    return value.isoformat() if value else ""
