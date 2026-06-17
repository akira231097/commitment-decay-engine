from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .models import Commitment, CommitmentStatus, EvidenceItem


@dataclass(slots=True)
class ReconciliationResult:
    commitment: Commitment
    matched: bool
    evidence: EvidenceItem | None = None
    reason: str = ""


FULFILLMENT_HINTS = {
    "done", "completed", "merged", "shipped", "deployed", "closed",
    "fixed", "resolved", "published", "released",
}


def reconcile_commitment(
    commitment: Commitment,
    evidence_items: list[EvidenceItem],
    *,
    checked_on: date,
) -> ReconciliationResult:
    best = _best_match(commitment, evidence_items)
    commitment.last_checked = checked_on
    if not best:
        return ReconciliationResult(commitment, matched=False, reason="No related evidence found.")

    text = best.text.lower()
    if any(hint in text for hint in FULFILLMENT_HINTS):
        commitment.status = CommitmentStatus.FULFILLED
        commitment.fulfilled_date = best.date or checked_on
        commitment.fulfillment_evidence = _evidence_summary(best)
        return ReconciliationResult(
            commitment,
            matched=True,
            evidence=best,
            reason="Matched completion evidence.",
        )

    commitment.fulfillment_evidence = f"Progress evidence: {_evidence_summary(best)}"
    return ReconciliationResult(
        commitment,
        matched=True,
        evidence=best,
        reason="Matched progress evidence, but not enough to mark fulfilled.",
    )


def _best_match(commitment: Commitment, evidence_items: list[EvidenceItem]) -> EvidenceItem | None:
    terms = {term.lower() for term in commitment.keywords}
    terms.update(word.lower() for word in commitment.title.split() if len(word) > 2)
    best: tuple[int, EvidenceItem] | None = None
    for item in evidence_items:
        haystack = f"{item.text} {item.actor or ''}".lower()
        score = sum(1 for term in terms if term and term in haystack)
        if item.actor and item.actor.lower() == commitment.person.lower():
            score += 2
        if score >= 2 and (best is None or score > best[0]):
            best = (score, item)
    return best[1] if best else None


def _evidence_summary(item: EvidenceItem) -> str:
    actor = f"{item.actor}: " if item.actor else ""
    when = f" on {item.date.isoformat()}" if item.date else ""
    url = f" ({item.url})" if item.url else ""
    return f"{item.source}{when} - {actor}{item.text[:220]}{url}"
