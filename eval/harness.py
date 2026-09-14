"""Accuracy & regression evaluation harness.

Run:
    python3 -m eval.harness            # evaluate, print report, write eval/report.json
    python3 -m eval.harness --freeze   # (re)freeze snapshot baselines into eval/snapshots.json

Metrics:
    - identity accuracy: nakshatra / pada / rashi / lagna exactness
    - dasha accuracy: birth lord + current MD/AD lord correctness
    - position accuracy: Moon within tolerance (external truth only)
    - seed reproduction: almanac-anchored ladder matches exact handwritten dates

Exit code is non-zero if any case fails, so CI can gate on it.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kala.chart import chart_dasha_at, compute_chart  # noqa: E402
from kala.vimsottari import Ymd  # noqa: E402
from eval.dataset import all_cases  # noqa: E402

SNAP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapshots.json")
REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.json")


def _chart_snapshot(chart) -> dict:
    hit = chart_dasha_at(chart, "2026-06-01")
    return {
        "moon_sidereal": round(chart.moon_sidereal, 4),
        "nakshatra": chart.nakshatra,
        "pada": chart.pada,
        "rashi": chart.rashi,
        "lagna_rashi": chart.lagna_rashi,
        "birth_lord": chart.birth_lord,
        "epoch_md_lord": hit["mahadasha"].lord if hit else None,
        "epoch_ad_lord": hit["antardasha"].lord if hit and hit["antardasha"] else None,
    }


def freeze():
    snaps = {}
    for case in all_cases():
        if case["kind"] != "snapshot":
            continue
        snaps[case["id"]] = _chart_snapshot(compute_chart(case["native"]))
    with open(SNAP_PATH, "w", encoding="utf-8") as fh:
        json.dump(snaps, fh, indent=2, ensure_ascii=False)
    print(f"Froze {len(snaps)} snapshots -> {SNAP_PATH}")


def _check(results: list, name: str, ok: bool, got=None, want=None):
    results.append({"check": name, "pass": bool(ok), "got": got, "want": want})


def evaluate() -> dict:
    frozen = {}
    if os.path.exists(SNAP_PATH):
        with open(SNAP_PATH, encoding="utf-8") as fh:
            frozen = json.load(fh)

    cases_report = []
    total = passed = 0

    for case in all_cases():
        chart = compute_chart(case["native"])
        hit = chart_dasha_at(chart, case["expect"].get("epoch", "2026-06-01"))
        checks: list = []
        exp = case["expect"]

        if case["kind"] == "external":
            _check(checks, "moon_within_tol",
                   abs(chart.moon_sidereal - exp["moon_sidereal"]) <= exp["moon_tol"],
                   round(chart.moon_sidereal, 4), f"{exp['moon_sidereal']}±{exp['moon_tol']}")
            _check(checks, "nakshatra", chart.nakshatra == exp["nakshatra"], chart.nakshatra, exp["nakshatra"])
            _check(checks, "pada", chart.pada == exp["pada"], chart.pada, exp["pada"])
            _check(checks, "rashi", chart.rashi == exp["rashi"], chart.rashi, exp["rashi"])
            _check(checks, "birth_lord", chart.birth_lord == exp["birth_lord"], chart.birth_lord, exp["birth_lord"])
            _check(checks, "balance_within_tol",
                   abs(chart.balance_years - exp["balance_years"]) <= exp["balance_tol"],
                   round(chart.balance_years, 3), f"{exp['balance_years']}±{exp['balance_tol']}")
            _check(checks, "epoch_md_lord", hit and hit["mahadasha"].lord == exp["epoch_md_lord"],
                   hit["mahadasha"].lord if hit else None, exp["epoch_md_lord"])
            _check(checks, "epoch_ad_lord", hit and hit["antardasha"].lord == exp["epoch_ad_lord"],
                   hit["antardasha"].lord if hit and hit["antardasha"] else None, exp["epoch_ad_lord"])
            jup = next((s for s in chart.ladder if s.lord == "Jupiter"), None)
            sat = next((s for s in chart.ladder if s.lord == "Saturn"), None)
            _check(checks, "jupiter_end_year", jup and jup.end.startswith(exp["jupiter_end_year"]),
                   jup.end if jup else None, exp["jupiter_end_year"])
            _check(checks, "saturn_end_year", sat and sat.end.startswith(exp["saturn_end_year"]),
                   sat.end if sat else None, exp["saturn_end_year"])
            # Seed reproduction
            seed = case.get("seed")
            if seed:
                sc = compute_chart(case["native"], seed_balance=Ymd(*seed["ymd"]), seed_lord=seed["lord"])
                jup2 = next((s for s in sc.ladder if s.lord == "Jupiter"), None)
                sat2 = next((s for s in sc.ladder if s.lord == "Saturn"), None)
                _check(checks, "seed_jupiter_exact", jup2 and jup2.end == seed["jupiter_end"],
                       jup2.end if jup2 else None, seed["jupiter_end"])
                _check(checks, "seed_saturn_exact", sat2 and sat2.end == seed["saturn_end"],
                       sat2.end if sat2 else None, seed["saturn_end"])
        else:
            snap = _chart_snapshot(chart)
            base = frozen.get(case["id"])
            # explicit expectations (from dataset) first
            for key, want in exp.items():
                if key == "epoch":
                    continue
                got = snap.get(key)
                _check(checks, f"expect_{key}", got == want, got, want)
            # frozen snapshot regression
            if base:
                for key, want in base.items():
                    got = snap.get(key)
                    tol_ok = got == want
                    if key == "moon_sidereal" and isinstance(got, (int, float)):
                        tol_ok = abs(got - want) < 0.02
                    _check(checks, f"snapshot_{key}", tol_ok, got, want)

        case_pass = all(c["pass"] for c in checks)
        total += len(checks)
        passed += sum(1 for c in checks if c["pass"])
        cases_report.append({
            "id": case["id"],
            "kind": case["kind"],
            "pass": case_pass,
            "checks": checks,
        })

    report = {
        "total_checks": total,
        "passed": passed,
        "accuracy": round(passed / total, 4) if total else 0.0,
        "all_pass": all(c["pass"] for c in cases_report),
        "cases": cases_report,
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    return report


def _print(report: dict):
    print(f"Accuracy: {report['passed']}/{report['total_checks']} = {report['accuracy']*100:.1f}%")
    for case in report["cases"]:
        flag = "PASS" if case["pass"] else "FAIL"
        print(f"  [{flag}] {case['id']} ({case['kind']})")
        for c in case["checks"]:
            if not c["pass"]:
                print(f"      x {c['check']}: got {c['got']!r} want {c['want']!r}")


if __name__ == "__main__":
    if "--freeze" in sys.argv:
        freeze()
    else:
        rep = evaluate()
        _print(rep)
        sys.exit(0 if rep["all_pass"] else 1)
