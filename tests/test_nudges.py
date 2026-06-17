from datetime import date

from commitment_decay_engine.models import Commitment
from commitment_decay_engine.nudges import evaluate_nudge


def test_nudge_after_two_days():
    item = Commitment(
        title="Fix Search",
        person="Ava",
        source="demo",
        date=date(2026, 1, 14),
        commitment="I will fix search.",
        keywords=["fix", "search"],
    )

    decision = evaluate_nudge(item, today=date(2026, 1, 17))

    assert decision.should_nudge is True
    assert "Hey Ava" in decision.message
