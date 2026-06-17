from __future__ import annotations

import argparse
import json
import shutil
from datetime import date
from pathlib import Path

from .analytics import summarize
from .extractor import extract_commitments
from .ledger import MarkdownLedger
from .models import CommitmentStatus, EvidenceItem
from .nudges import evaluate_nudge
from .reconcile import reconcile_commitment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cde", description="Commitment Decay Engine CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="Run a local end-to-end demo")
    demo.add_argument("--ledger", default=".demo-ledger")

    extract = sub.add_parser("extract", help="Extract commitments from a transcript")
    extract.add_argument("transcript")
    extract.add_argument("--ledger", default="commitments")
    extract.add_argument("--source", default="Demo meeting")
    extract.add_argument("--date", default=date.today().isoformat())

    list_cmd = sub.add_parser("list", help="List commitments")
    list_cmd.add_argument("--ledger", default="commitments")
    list_cmd.add_argument("--status", choices=[s.value.lower() for s in CommitmentStatus])

    reconcile = sub.add_parser("reconcile", help="Reconcile commitments against evidence JSON")
    reconcile.add_argument("--ledger", default="commitments")
    reconcile.add_argument("--evidence", required=True)
    reconcile.add_argument("--date", default=date.today().isoformat())

    report = sub.add_parser("report", help="Generate analytics report")
    report.add_argument("--ledger", default="commitments")

    args = parser.parse_args(argv)

    if args.command == "demo":
        return _demo(Path(args.ledger))
    if args.command == "extract":
        return _extract(args)
    if args.command == "list":
        return _list(args)
    if args.command == "reconcile":
        return _reconcile(args)
    if args.command == "report":
        return _report(args)
    return 1


def _demo(ledger_path: Path) -> int:
    if ledger_path.exists():
        shutil.rmtree(ledger_path)
    transcript = Path("examples/sample_transcript.txt")
    evidence = Path("examples/sample_evidence.json")
    _extract(
        argparse.Namespace(
            transcript=str(transcript),
            ledger=str(ledger_path),
            source="Demo product sync",
            date="2026-01-14",
        )
    )
    _reconcile(
        argparse.Namespace(
            ledger=str(ledger_path),
            evidence=str(evidence),
            date="2026-01-17",
        )
    )
    return _report(argparse.Namespace(ledger=str(ledger_path)))


def _extract(args: argparse.Namespace) -> int:
    transcript = Path(args.transcript).read_text(encoding="utf-8")
    ledger = MarkdownLedger(args.ledger)
    meeting_date = date.fromisoformat(args.date)
    commitments = extract_commitments(transcript, source=args.source, meeting_date=meeting_date)
    for item in commitments:
        ledger.save(item)
    print(json.dumps({"extracted": len(commitments), "ledger": str(ledger.root)}, indent=2))
    return 0


def _list(args: argparse.Namespace) -> int:
    ledger = MarkdownLedger(args.ledger)
    items = ledger.all()
    if args.status:
        items = [item for item in items if item.status.value.lower() == args.status]
    payload = [
        {
            "person": item.person,
            "title": item.title,
            "status": item.status.value,
            "date": item.date.isoformat(),
            "deadline": item.deadline,
            "nudge_count": item.nudge_count,
        }
        for item in items
    ]
    print(json.dumps(payload, indent=2))
    return 0


def _reconcile(args: argparse.Namespace) -> int:
    ledger = MarkdownLedger(args.ledger)
    evidence_payload = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    evidence = [EvidenceItem.from_dict(item) for item in evidence_payload]
    checked_on = date.fromisoformat(args.date)
    results = []
    for commitment in ledger.all():
        result = reconcile_commitment(commitment, evidence, checked_on=checked_on)
        ledger.overwrite(result.commitment)
        if not result.matched:
            decision = evaluate_nudge(result.commitment, today=checked_on)
            if decision.should_nudge:
                result.commitment.nudge_count += 1
                result.commitment.last_nudged = checked_on
                ledger.overwrite(result.commitment)
        results.append({"title": commitment.title, "reason": result.reason})
    print(json.dumps({"reconciled": len(results), "results": results}, indent=2))
    return 0


def _report(args: argparse.Namespace) -> int:
    ledger = MarkdownLedger(args.ledger)
    print(json.dumps(summarize(ledger.all()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
