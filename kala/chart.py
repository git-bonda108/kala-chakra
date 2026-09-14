"""compute_chart: the single deterministic entry point for a native."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

from .constants import GRAHAS, VIM_YEARS
from .ephemeris import compute_sky
from .nakshatra import house_from_lagna, nakshatra_at, navamsa_rashi, rashi_at
from .vimsottari import (
    DashaSpan,
    Ymd,
    dasha_at,
    mahadasha_ladder,
    ymd_to_years,
)


@dataclass
class Native:
    name: str
    date: str        # YYYY-MM-DD (local civil date)
    time: str        # HH:MM[:SS] (local civil time)
    tz_offset_hours: float
    lat: float
    lon: float
    place: str


@dataclass
class Placement:
    graha: str
    sidereal: float
    rashi: str
    house: int
    nakshatra: str
    pada: int
    navamsa: str
    retrograde: bool


@dataclass
class Chart:
    native: Native
    ut_iso: str
    ayanamsa: float
    moon_sidereal: float
    nakshatra: str
    pada: int
    rashi: str
    lagna_sidereal: float
    lagna_rashi: str
    placements: list = field(default_factory=list)
    birth_lord: str = ""
    balance_years: float = 0.0
    balance_ymd: Ymd = None
    ladder: list = field(default_factory=list)


def _local_to_ut(date_str: str, time_str: str, tz_offset_hours: float) -> datetime:
    parts = [int(x) for x in time_str.split(":")]
    while len(parts) < 3:
        parts.append(0)
    hh, mm, ss = parts[0], parts[1], parts[2]
    y, mo, d = [int(x) for x in date_str.split("-")]
    local = datetime(y, mo, d, hh, mm, ss, tzinfo=timezone.utc)
    return local - timedelta(hours=tz_offset_hours)


def compute_chart(native: Native, seed_balance: "Ymd | None" = None,
                  seed_lord: "str | None" = None) -> Chart:
    """Compute the full chart.

    seed_balance / seed_lord: OPTIONAL opening Mahadasha remainder taken from a
    parsed document / almanac. When provided AND the seed lord matches the
    computed birth lord, the ladder is anchored to it (this is data-driven, not
    hardcoded). Otherwise the pure ephemeris balance is used.
    """
    ut = _local_to_ut(native.date, native.time, native.tz_offset_hours)
    sky = compute_sky(ut, native.lat, native.lon)

    moon = sky.grahas["Moon"].sidereal
    nak = nakshatra_at(moon)
    rashi = rashi_at(moon)
    lagna_rashi = rashi_at(sky.lagna_sidereal)

    placements = []
    for g in GRAHAS:
        pos = sky.grahas[g]
        info = nakshatra_at(pos.sidereal)
        placements.append(
            Placement(
                graha=g,
                sidereal=pos.sidereal,
                rashi=rashi_at(pos.sidereal),
                house=house_from_lagna(pos.sidereal, sky.lagna_sidereal),
                nakshatra=info.name,
                pada=info.pada,
                navamsa=navamsa_rashi(pos.sidereal),
                retrograde=pos.retrograde,
            )
        )

    balance_years = nak.remaining_frac * VIM_YEARS[nak.lord]
    if seed_balance is not None and (seed_lord is None or seed_lord == nak.lord):
        balance_years = ymd_to_years(seed_balance)
    birth_civil = date(*[int(x) for x in native.date.split("-")])
    ladder = mahadasha_ladder(birth_civil, nak.lord, balance_years)

    return Chart(
        native=native,
        ut_iso=ut.isoformat(),
        ayanamsa=sky.ayanamsa,
        moon_sidereal=moon,
        nakshatra=nak.name,
        pada=nak.pada,
        rashi=rashi,
        lagna_sidereal=sky.lagna_sidereal,
        lagna_rashi=lagna_rashi,
        placements=placements,
        birth_lord=nak.lord,
        balance_years=balance_years,
        balance_ymd=ladder[0].duration if ladder else Ymd(0, 0, 0),
        ladder=ladder,
    )


def chart_dasha_at(chart: Chart, iso: str):
    return dasha_at(chart.ladder, iso)


def format_dms(deg: float) -> str:
    d = int(deg)
    mf = (deg - d) * 60
    m = int(mf)
    s = round((mf - m) * 60)
    if s == 60:
        s = 0
        m += 1
    return f"{d}\u00b0 {m:02d}\u2032 {s:02d}\u2033"
