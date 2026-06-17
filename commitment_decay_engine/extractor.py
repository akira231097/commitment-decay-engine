from __future__ import annotations

import re
from datetime import date

from .models import Commitment

SPEAKER_LINE = re.compile(r"^(?P<speaker>[A-Z][A-Za-z ._-]{1,40}):\s*(?P<text>.+)$")
COMMITMENT_PATTERNS = [
    re.compile(r"\bI(?:'ll| will| can| am going to)\b", re.IGNORECASE),
    re.compile(r"\bLet me\b", re.IGNORECASE),
    re.compile(r"\bI can take\b", re.IGNORECASE),
    re.compile(r"\bI'll handle\b", re.IGNORECASE),
]
NON_COMMITMENT_HINTS = [
    "i already",
    "i finished",
    "i fixed",
    "we should",
    "someone should",
    "it would be nice",
]


def extract_commitments(text: str, *, source: str, meeting_date: date) -> list[Commitment]:
    """Extract likely commitments from speaker-labeled transcript text.

    This public extractor is intentionally deterministic and conservative. In a
    production deployment, this layer can be replaced with an LLM extraction
    adapter while keeping the ledger, reconciliation, and policy modules.
    """
    commitments: list[Commitment] = []
    for line in text.splitlines():
        match = SPEAKER_LINE.match(line.strip())
        if not match:
            continue
        speaker = match.group("speaker").strip()
        utterance = match.group("text").strip()
        if not _looks_like_commitment(utterance):
            continue
        commitments.append(
            Commitment(
                title=_title_from_text(utterance),
                person=speaker,
                source=source,
                date=meeting_date,
                commitment=utterance,
                deadline=_extract_deadline(utterance),
                keywords=_keywords(utterance),
                last_checked=meeting_date,
            )
        )
    return commitments


def _looks_like_commitment(text: str) -> bool:
    lowered = text.lower()
    if any(hint in lowered for hint in NON_COMMITMENT_HINTS):
        return False
    return any(pattern.search(text) for pattern in COMMITMENT_PATTERNS)


def _title_from_text(text: str) -> str:
    cleaned = re.sub(r"\b(I'll|I will|I can|I am going to|Let me)\b", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^A-Za-z0-9 ]+", " ", cleaned)
    words = [w for w in cleaned.split() if len(w) > 2][:6]
    return " ".join(words).title() or "Follow Up"


def _extract_deadline(text: str) -> str:
    lowered = text.lower()
    if "today" in lowered:
        return "today"
    if "tomorrow" in lowered:
        return "tomorrow"
    weekday = re.search(r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", lowered)
    if weekday:
        return weekday.group(1).title()
    iso = re.search(r"\b20\d{2}-\d{2}-\d{2}\b", text)
    if iso:
        return iso.group(0)
    return "Not specified"


def _keywords(text: str) -> list[str]:
    stop = {
        "will", "with", "that", "this", "from", "have", "into", "today",
        "tomorrow", "going", "take", "handle", "look", "investigate",
        "the", "can", "let", "why", "and", "for", "you",
    }
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text.lower())
    unique: list[str] = []
    for word in words:
        if word in stop or word in unique:
            continue
        unique.append(word)
    return unique[:5]
