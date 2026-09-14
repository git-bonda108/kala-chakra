"""GR-001 golden regression, ported to the Python calc_core."""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kala.chart import Native, chart_dasha_at, compute_chart  # noqa: E402
from kala.vimsottari import span_containing  # noqa: E402

SATYA = Native(
    name="Satya Anand Bonda",
    date="1977-11-25",
    time="01:55:00",
    tz_offset_hours=5.5,
    lat=22.5726,
    lon=88.3639,
    place="Kolkata, India",
)


def test_identity_moon_krittika_mesha():
    c = compute_chart(SATYA)
    assert abs(c.moon_sidereal - 29.27) < 0.30
    assert c.nakshatra == "Krittika"
    assert c.pada == 1
    assert c.rashi == "Mesha"


def test_birth_lord_and_balance():
    c = compute_chart(SATYA)
    assert c.birth_lord == "Sun"
    assert abs(c.balance_years - 4.83) < 0.1


def test_ladder_ends_year_match():
    """Pure ephemeris recompute: lords + end YEARS match the handwritten ladder.
    (Exact days differ ~4 months because the almanac used a 4-6-02 balance;
    that difference is what the validator surfaces, not what we silently fix.)"""
    c = compute_chart(SATYA)
    jupiter = next(s for s in c.ladder if s.lord == "Jupiter")
    saturn = next(s for s in c.ladder if s.lord == "Saturn")
    assert jupiter.end.startswith("2033")
    assert saturn.end.startswith("2052")


def test_dasha_at_epoch():
    c = compute_chart(SATYA)
    hit = chart_dasha_at(c, "2026-06-01")
    assert hit["mahadasha"].lord == "Jupiter"
    assert hit["antardasha"].lord == "Venus"
    assert hit["mahadasha"].end.startswith("2033")


def test_seed_balance_anchors_to_almanac():
    """When a document supplies the 4-6-02 Sun balance, the ladder anchors to it
    and reproduces the exact handwritten dates."""
    from kala.vimsottari import Ymd
    c = compute_chart(SATYA, seed_balance=Ymd(4, 6, 2), seed_lord="Sun")
    jupiter = next(s for s in c.ladder if s.lord == "Jupiter")
    saturn = next(s for s in c.ladder if s.lord == "Saturn")
    assert jupiter.end == "2033-05-27"
    assert saturn.end == "2052-05-27"


if __name__ == "__main__":
    for fn in [
        test_identity_moon_krittika_mesha,
        test_birth_lord_and_balance,
        test_ladder_ends_year_match,
        test_dasha_at_epoch,
        test_seed_balance_anchors_to_almanac,
    ]:
        fn()
        print("PASS", fn.__name__)
    c = compute_chart(SATYA)
    print("moon", round(c.moon_sidereal, 4), c.nakshatra, c.pada, c.rashi)
    print("balance", c.balance_ymd.as_str(), "lord", c.birth_lord)
    print("lagna", c.lagna_rashi)
