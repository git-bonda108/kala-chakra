from __future__ import annotations

from dataclasses import dataclass

from .constants import (
    NAKSHATRA_LORDS,
    NAKSHATRA_SPAN,
    NAKSHATRAS,
    PADA_SPAN,
    RASHIS,
)


@dataclass
class NakshatraInfo:
    name: str
    index: int
    pada: int
    lord: str
    rashi: str
    elapsed_frac: float
    remaining_frac: float


def norm(deg: float) -> float:
    return deg % 360.0


def rashi_at(sidereal_deg: float) -> str:
    return RASHIS[int(norm(sidereal_deg) // 30)]


def house_from_lagna(graha_deg: float, lagna_deg: float) -> int:
    g = int(norm(graha_deg) // 30)
    l = int(norm(lagna_deg) // 30)
    return ((g - l) % 12) + 1


def nakshatra_at(sidereal_deg: float) -> NakshatraInfo:
    lon = norm(sidereal_deg)
    index = min(26, int(lon // NAKSHATRA_SPAN))
    start = index * NAKSHATRA_SPAN
    into = lon - start
    pada = min(3, int(into // PADA_SPAN)) + 1
    return NakshatraInfo(
        name=NAKSHATRAS[index],
        index=index,
        pada=pada,
        lord=NAKSHATRA_LORDS[index],
        rashi=rashi_at(lon),
        elapsed_frac=into / NAKSHATRA_SPAN,
        remaining_frac=(NAKSHATRA_SPAN - into) / NAKSHATRA_SPAN,
    )


def navamsa_rashi(sidereal_deg: float) -> str:
    lon = norm(sidereal_deg)
    sign = int(lon // 30)
    part = min(8, int((lon % 30) // (30.0 / 9.0)))
    if sign % 3 == 0:
        start = sign
    elif sign % 3 == 1:
        start = (sign + 8) % 12
    else:
        start = (sign + 4) % 12
    return RASHIS[(start + part) % 12]
