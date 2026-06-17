from __future__ import annotations

from collections import Counter, defaultdict

from .models import Commitment, CommitmentStatus


def summarize(commitments: list[Commitment]) -> dict[str, object]:
    by_status = Counter(item.status.value for item in commitments)
    by_person: dict[str, Counter[str]] = defaultdict(Counter)
    for item in commitments:
        by_person[item.person][item.status.value] += 1

    people = {}
    for person, counts in by_person.items():
        total = sum(counts.values())
        fulfilled = counts[CommitmentStatus.FULFILLED.value]
        people[person] = {
            "total": total,
            "fulfilled": fulfilled,
            "open": counts[CommitmentStatus.OPEN.value],
            "stale": counts[CommitmentStatus.STALE.value],
            "fulfillment_rate": round(fulfilled / total, 2) if total else 0,
        }

    return {
        "total": len(commitments),
        "by_status": dict(by_status),
        "by_person": people,
        "open_items": [
            {
                "person": item.person,
                "title": item.title,
                "date": item.date.isoformat(),
                "deadline": item.deadline,
            }
            for item in commitments
            if item.status is CommitmentStatus.OPEN
        ],
    }
