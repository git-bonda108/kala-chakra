"""Evaluation dataset.

Two kinds of cases:

1. EXTERNAL truth (GR-001): expected values come from the handover document /
   independent Meeus+Lahiri reference. These guard real astronomical accuracy.

2. SNAPSHOT baselines: expected values were produced by this engine and frozen.
   They guard against unintended regressions (a change that silently moves a
   nakshatra or dasha lord will fail the harness).

Each case lists the native plus assertions with tolerances.
"""

from __future__ import annotations

from kala.chart import Native

# ---- Case 1: external golden truth ----------------------------------------
GR001 = {
    "id": "GR-001",
    "kind": "external",
    "native": Native("Satya Anand Bonda", "1977-11-25", "01:55:00", 5.5, 22.5726, 88.3639, "Kolkata, India"),
    "expect": {
        "moon_sidereal": 29.27,
        "moon_tol": 0.30,
        "nakshatra": "Krittika",
        "pada": 1,
        "rashi": "Mesha",
        "birth_lord": "Sun",
        "balance_years": 4.83,
        "balance_tol": 0.10,
        "epoch": "2026-06-01",
        "epoch_md_lord": "Jupiter",
        "epoch_ad_lord": "Venus",
        "jupiter_end_year": "2033",
        "saturn_end_year": "2052",
    },
    # When a document supplies the almanac balance, exact handwritten dates.
    "seed": {"lord": "Sun", "ymd": (4, 6, 2), "jupiter_end": "2033-05-27", "saturn_end": "2052-05-27"},
}

# ---- Case 2+: regression snapshots (frozen from this engine) ---------------
SNAPSHOTS = [
    {
        "id": "snap-chennai-1992",
        "kind": "snapshot",
        "native": Native("Anita Rao", "1992-03-14", "09:20:00", 5.5, 13.0827, 80.2707, "Chennai, India"),
        "expect": {
            "nakshatra": "Punarvasu",
            "pada": 3,
            "rashi": "Mithuna",
            "lagna_rashi": "Tula",
            "birth_lord": "Jupiter",
            "epoch": "2026-06-01",
            "epoch_md_lord": "Mercury",
        },
    },
    {
        "id": "snap-delhi-1985",
        "kind": "snapshot",
        "native": Native("Rohan Mehta", "1985-08-20", "22:10:00", 5.5, 28.6139, 77.2090, "Delhi, India"),
        "expect": {},  # filled by `python -m eval.harness --freeze`
    },
    {
        "id": "snap-hyd-2013",
        "kind": "snapshot",
        "native": Native("2013 Friday sheet", "2013-11-08", "05:59:00", 5.5, 17.3850, 78.4867, "Hyderabad, India"),
        "expect": {},
    },
]


def all_cases():
    return [GR001] + SNAPSHOTS
