from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum
from typing import Any


class CommitmentStatus(StrEnum):
    OPEN = "Open"
    FULFILLED = "Fulfilled"
    STALE = "Stale"


@dataclass(slots=True)
class Commitment:
    title: str
    person: str
    source: str
    date: date
    commitment: str
    deadline: str = "Not specified"
    status: CommitmentStatus = CommitmentStatus.OPEN
    keywords: list[str] = field(default_factory=list)
    fulfillment_evidence: str = "None yet"
    last_checked: date | None = None
    nudge_count: int = 0
    last_nudged: date | None = None
    fulfilled_date: date | None = None

    @property
    def slug(self) -> str:
        raw = f"{self.date.isoformat()}-{self.person}-{self.title}".lower()
        chars = [c if c.isalnum() else "-" for c in raw]
        collapsed = "-".join(part for part in "".join(chars).split("-") if part)
        return collapsed[:90]


@dataclass(slots=True)
class EvidenceItem:
    source: str
    text: str
    actor: str | None = None
    date: date | None = None
    url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EvidenceItem":
        raw_date = payload.get("date")
        parsed_date = None
        if raw_date:
            parsed_date = datetime.fromisoformat(str(raw_date)).date()
        return cls(
            source=str(payload.get("source", "unknown")),
            text=str(payload.get("text", "")),
            actor=payload.get("actor"),
            date=parsed_date,
            url=payload.get("url"),
            metadata=dict(payload.get("metadata") or {}),
        )
