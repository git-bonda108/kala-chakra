"""Level-aware cross-validation of ingested sources vs the computed chart.

Core rule from GR-001: a sub-period label in one source must NOT be compared
against a major-period label in another. Only flag a genuine, same-level
disagreement — and when flagged, surface both readings, never guess.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class IngestedPeriod:
    level: str            # mahadasha | antardasha | pratyantardasha
    lord: str
    start: str | None = None
    end: str | None = None
    confidence: str = "medium"
    note: str = ""


@dataclass
class IngestedSource:
    source_id: str
    label: str
    periods: list = field(default_factory=list)
    moon_rashi: str | None = None
    nakshatra: str | None = None
    illegible: list = field(default_factory=list)
    confidence: str = "medium"


@dataclass
class ConsistencyFlag:
    status: str           # CONSISTENT | CONFLICT | INCOMPLETE
    message: str
    candidates: list = field(default_factory=list)
    surfaced_to_judge: bool = False
    details: list = field(default_factory=list)


def _days_apart(a: str | None, b: str | None) -> float | None:
    if not a or not b:
        return None
    try:
        return abs((date.fromisoformat(a) - date.fromisoformat(b)).days)
    except ValueError:
        return None


def _overlap_days(a: IngestedPeriod, b: IngestedPeriod) -> float | None:
    if not (a.start and a.end and b.start and b.end):
        return None
    try:
        start = max(date.fromisoformat(a.start), date.fromisoformat(b.start))
        end = min(date.fromisoformat(a.end), date.fromisoformat(b.end))
        return (end - start).days
    except ValueError:
        return None


def cross_validate(
    left: IngestedSource,
    right: IngestedSource,
    md_tol_days: int = 60,
    ad_tol_days: int = 30,
) -> ConsistencyFlag:
    details: list[str] = []
    candidates: set[str] = set()
    compared = 0
    conflicts = 0

    for level in ("mahadasha", "antardasha", "pratyantardasha"):
        la = [p for p in left.periods if p.level == level]
        rb = [p for p in right.periods if p.level == level]
        if not la or not rb:
            if bool(la) != bool(rb):
                details.append(f"{level}: only one source has data — incomplete, not a conflict.")
            continue
        tol = md_tol_days if level == "mahadasha" else ad_tol_days
        for pa in la:
            peers = [pb for pb in rb if (_overlap_days(pa, pb) or 0) > tol or (pa.start is None or pb.start is None)]
            if not peers:
                details.append(f"{level}: {pa.lord} {pa.start}–{pa.end} has no overlapping peer.")
                continue
            for pb in peers:
                compared += 1
                if pa.lord != pb.lord:
                    conflicts += 1
                    candidates.update([pa.lord, pb.lord])
                    details.append(
                        f"{level} lord mismatch: {left.source_id} {pa.lord} vs {right.source_id} {pb.lord}."
                    )
                    continue
                sd = _days_apart(pa.start, pb.start)
                ed = _days_apart(pa.end, pb.end)
                if sd is not None and sd > tol:
                    conflicts += 1
                    candidates.add(pa.lord)
                    details.append(f"{level} {pa.lord}: start differs by {sd} days (> {tol}).")
                elif ed is not None and ed > tol:
                    conflicts += 1
                    candidates.add(pa.lord)
                    details.append(f"{level} {pa.lord}: end differs by {ed} days (> {tol}).")
                else:
                    details.append(f"{level} {pa.lord}: agrees within tolerance.")

    if left.moon_rashi and right.moon_rashi and left.moon_rashi != right.moon_rashi:
        conflicts += 1
        details.append(f"Moon rashi differs: {left.moon_rashi} vs {right.moon_rashi}.")

    if compared == 0 and conflicts == 0:
        return ConsistencyFlag("INCOMPLETE", "Not enough overlapping same-level data to compare.", [], False, details)
    if conflicts > 0:
        return ConsistencyFlag(
            "CONFLICT",
            "After aligning Mahadasha/Antardasha levels, the sources still differ. Both readings are shown.",
            sorted(candidates),
            True,
            details,
        )
    return ConsistencyFlag(
        "CONSISTENT",
        "The computed chart agrees with your document once periods are compared at the same level.",
        [],
        False,
        details,
    )
