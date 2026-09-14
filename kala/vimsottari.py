"""Vimsottari dasha ladder on the Hindu 360-day civil scheme.

Validated against the handwritten Satya Anand ladder:
Sun balance 4-6-02 from 1977-11-25 -> Jupiter 2017-05-27..2033-05-27,
Saturn -> 2052-05-27.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .constants import VIM_ORDER, VIM_YEARS


@dataclass
class Ymd:
    years: int
    months: int
    days: int

    def as_str(self) -> str:
        return f"{self.years}-{self.months:02d}-{self.days:02d}"


@dataclass
class DashaSpan:
    level: str
    lord: str
    start: str  # ISO date
    end: str
    duration: Ymd


def days360_to_ymd(total_days: float) -> Ymd:
    rounded = round(total_days)
    y = rounded // 360
    rem = rounded - y * 360
    m = rem // 30
    rem -= m * 30
    return Ymd(int(y), int(m), int(rem))


def ymd_to_days360(ymd: Ymd) -> int:
    return ymd.years * 360 + ymd.months * 30 + ymd.days


def years_to_ymd(years: float) -> Ymd:
    return days360_to_ymd(years * 360.0)


def ymd_to_years(ymd: Ymd) -> float:
    return ymd.years + ymd.months / 12.0 + ymd.days / 360.0


def _add_ymd(start: date, ymd: Ymd) -> date:
    from calendar import monthrange

    y = start.year + ymd.years
    m = start.month + ymd.months
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    d = start.day + ymd.days
    # normalise overflowing days onto following months
    while True:
        dim = monthrange(y, m)[1]
        if d <= dim:
            break
        d -= dim
        m += 1
        if m > 12:
            m = 1
            y += 1
    return date(y, m, d)


def _rotate_from(lord: str):
    i = VIM_ORDER.index(lord)
    return VIM_ORDER[i:] + VIM_ORDER[:i]


def _walk(start: date, first_lord: str, first_years: float, parent_years, level: str):
    order = _rotate_from(first_lord)
    spans = []
    cum_days = 0
    for i, lord in enumerate(order):
        if i == 0:
            years = first_years
        elif parent_years is None:
            years = VIM_YEARS[lord]
        else:
            years = parent_years * VIM_YEARS[lord] / 120.0
        duration = years_to_ymd(years)
        start_date = _add_ymd(start, days360_to_ymd(cum_days))
        cum_days += ymd_to_days360(duration)
        end_date = _add_ymd(start, days360_to_ymd(cum_days))
        spans.append(
            DashaSpan(level, lord, start_date.isoformat(), end_date.isoformat(), duration)
        )
    return spans


def mahadasha_ladder(birth: date, birth_lord: str, remaining_years: float):
    return _walk(birth, birth_lord, remaining_years, None, "mahadasha")


def antardasha_ladder(md: DashaSpan):
    md_years = ymd_to_years(md.duration)
    first = md_years * VIM_YEARS[md.lord] / 120.0
    return _walk(date.fromisoformat(md.start), md.lord, first, md_years, "antardasha")


def pratyantardasha_ladder(ad: DashaSpan):
    ad_years = ymd_to_years(ad.duration)
    first = ad_years * VIM_YEARS[ad.lord] / 120.0
    return _walk(date.fromisoformat(ad.start), ad.lord, first, ad_years, "pratyantardasha")


def span_containing(spans, iso: str):
    for s in spans:
        if s.start <= iso < s.end:
            return s
    if spans and iso == spans[-1].end:
        return spans[-1]
    return None


def dasha_at(ladder, iso: str):
    md = span_containing(ladder, iso)
    if md is None:
        return None
    ad = span_containing(antardasha_ladder(md), iso)
    pd = span_containing(pratyantardasha_ladder(ad), iso) if ad else None
    return {"mahadasha": md, "antardasha": ad, "pratyantardasha": pd}
