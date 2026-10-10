"""Balanced, evidence-supported correct decisions; abstentions receive no credit."""
from .fixtures import REQUIREMENTS


def validate_report(report, last_frame):
    if not isinstance(report, dict) or set(report) != set(REQUIREMENTS):
        raise ValueError("Final report must contain exactly both requirements")
    for row in report.values():
        if not isinstance(row, dict) or set(row) != {"status", "frames"}:
            raise ValueError("Each judgment requires status and frames")
        if not isinstance(row["status"], str) or row["status"] not in {"passed", "failed", "unverified"}:
            raise ValueError("Unknown judgment state")
        frames = row["frames"]
        if not isinstance(frames, list) or len(frames) > 80 or any(type(f) is not int or not 0 <= f <= last_frame for f in frames):
            raise ValueError("Invalid evidence frame reference")
        if row["status"] != "unverified" and len(set(frames)) < 2:
            raise ValueError("A decision requires at least two distinct observed frames")


def decisions(report, gold, certificates):
    rows = []
    for requirement in REQUIREMENTS:
        if gold[requirement] is None:
            continue
        judgment = report[requirement]
        frames = set(judgment["frames"])
        supported = any(f in frames and f - 1 in frames and
                        cert.get(requirement) == judgment["status"]
                        for f, cert in certificates.items())
        rows.append({"gold": gold[requirement], "status": judgment["status"],
                     "correct": judgment["status"] == gold[requirement] and supported,
                     "supported": supported})
    return rows


def aggregate(rows):
    counts = {s: sum(r["gold"] == s for r in rows) for s in ("passed", "failed")}
    if not all(counts.values()):
        raise ValueError("Scoring requires positive and negative denominators")
    correct = {s: sum(r["gold"] == s and r["correct"] for r in rows) for s in counts}
    return {"status": "scored", "score": sum(correct[s] / counts[s] for s in counts) / 2,
            "eligible_judgments": len(rows), "class_counts": counts, "correct_counts": correct,
            "abstentions": sum(r["status"] == "unverified" for r in rows),
            "unsupported_decisions": sum(r["status"] != "unverified" and not r["supported"] for r in rows)}
