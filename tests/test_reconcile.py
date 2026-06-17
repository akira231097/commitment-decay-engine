from datetime import date

from commitment_decay_engine.models import Commitment, CommitmentStatus, EvidenceItem
from commitment_decay_engine.reconcile import reconcile_commitment


def test_reconcile_marks_clear_completion_fulfilled():
    item = Commitment(
        title="Rewrite Email Copy",
        person="Maya",
        source="demo",
        date=date(2026, 1, 14),
        commitment="I will rewrite the onboarding email copy.",
        keywords=["onboarding", "email", "copy"],
    )
    evidence = [
        EvidenceItem(
            source="issue tracker",
            actor="Maya",
            date=date(2026, 1, 16),
            text="Completed onboarding email copy rewrite.",
        )
    ]

    result = reconcile_commitment(item, evidence, checked_on=date(2026, 1, 17))

    assert result.matched is True
    assert result.commitment.status is CommitmentStatus.FULFILLED
    assert result.commitment.fulfilled_date == date(2026, 1, 16)


def test_reconcile_avoids_single_generic_word_false_match():
    item = Commitment(
        title="Investigate Search Staleness",
        person="Liam",
        source="demo",
        date=date(2026, 1, 14),
        commitment="Let me investigate why search is returning stale records.",
        keywords=["search", "stale", "records"],
    )
    evidence = [
        EvidenceItem(
            source="issue tracker",
            actor="Maya",
            date=date(2026, 1, 16),
            text="Completed onboarding email copy rewrite.",
        )
    ]

    result = reconcile_commitment(item, evidence, checked_on=date(2026, 1, 17))

    assert result.matched is False
    assert result.commitment.status is CommitmentStatus.OPEN
