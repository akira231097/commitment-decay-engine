from datetime import date

from commitment_decay_engine.ledger import MarkdownLedger
from commitment_decay_engine.models import Commitment


def test_markdown_ledger_roundtrip(tmp_path):
    ledger = MarkdownLedger(tmp_path)
    item = Commitment(
        title="Fix Search",
        person="Ava",
        source="demo",
        date=date(2026, 1, 14),
        commitment="I will fix search today.",
        deadline="today",
        keywords=["fix", "search"],
        last_checked=date(2026, 1, 14),
    )
    ledger.save(item)

    loaded = ledger.all()

    assert len(loaded) == 1
    assert loaded[0].person == "Ava"
    assert loaded[0].keywords == ["fix", "search"]
