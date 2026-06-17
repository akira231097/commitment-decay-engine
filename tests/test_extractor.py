from datetime import date

from commitment_decay_engine.extractor import extract_commitments


def test_extracts_personal_commitments_only():
    text = "\n".join(
        [
            "Maya: I will rewrite the onboarding email copy by Friday.",
            "Noah: We should probably improve the dashboard someday.",
            "Ava: I can handle the API rate limit issue today.",
            "Maya: I already fixed the broken signup link yesterday.",
        ]
    )
    items = extract_commitments(text, source="test", meeting_date=date(2026, 1, 14))

    assert len(items) == 2
    assert {item.person for item in items} == {"Maya", "Ava"}
    assert items[0].deadline == "Friday"
    assert items[1].deadline == "today"
