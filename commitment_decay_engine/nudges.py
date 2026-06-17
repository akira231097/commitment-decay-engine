from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .models import Commitment, CommitmentStatus


@dataclass(slots=True)
class NudgeDecision:
    should_nudge: bool
    message: str = ""
    reason: str = ""


def evaluate_nudge(
    commitment: Commitment,
    *,
    today: date,
    max_nudges: int = 3,
    min_age_days: int = 2,
) -> NudgeDecision:
    if commitment.status is not CommitmentStatus.OPEN:
        return NudgeDecision(False, reason="Commitment is not open.")
    age = (today - commitment.date).days
    if age < min_age_days:
        return NudgeDecision(False, reason=f"Only {age} days old.")
    if commitment.nudge_count >= max_nudges:
        return NudgeDecision(False, reason="Maximum nudges reached; mark stale instead.")
    if commitment.last_nudged == today:
        return NudgeDecision(False, reason="Already nudged today.")
    return NudgeDecision(True, message=render_nudge(commitment), reason="Eligible for private nudge.")


def render_nudge(commitment: Commitment) -> str:
    if commitment.nudge_count == 0:
        return (
            f"Hey {commitment.person} - you mentioned {commitment.commitment!r} "
            f"in {commitment.source}. I have not seen related activity yet. "
            "Want me to create a ticket for this, or has it been handled somewhere I have not checked?"
        )
    if commitment.nudge_count == 1:
        return (
            f"Quick follow-up on {commitment.title}. Still on your radar? "
            "Happy to close it out if priorities changed."
        )
    return (
        f"Last check-in on {commitment.title}. If this is no longer relevant, "
        "just say the word and I will mark it closed. No judgment - priorities shift."
    )
