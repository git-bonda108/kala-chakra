"""Sidereal positions from astronomy-engine (Meeus) + Lahiri ayanamsa.

This is the same math validated against the GR-001 golden case:
Moon sidereal ~= 29.27 deg for Satya Anand (25 Nov 1977, 01:55 IST, Kolkata).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone

import astronomy

from .constants import GRAHAS


def lahiri_ayanamsa(jd_tt: float) -> float:
    """Lahiri (Chitrapaksha). Linear term tuned to the Swiss-style J2000 value."""
    t = (jd_tt - 2451545.0) / 36525.0
    return 23.852431 + 1.396971536 * t - 0.000000348 * t * t


def trop_to_sid(tropical_deg: float, ayanamsa: float) -> float:
    return (tropical_deg - ayanamsa) % 360.0


def _mean_node_tropical(jd_tt: float) -> float:
    t = (jd_tt - 2451545.0) / 36525.0
    ome = (
        125.0445479
        - 1934.1362891 * t
        + 0.0020754 * t * t
        + (t ** 3) / 467441.0
        - (t ** 4) / 60616000.0
    )
    return ome % 360.0


def _true_obliquity(jd_tt: float) -> float:
    t = (jd_tt - 2451545.0) / 36525.0
    return 23.4392911 - 0.0130042 * t


def _tropical_ascendant(ramc_deg: float, lat_deg: float, eps_deg: float) -> float:
    ramc = math.radians(ramc_deg)
    lat = math.radians(lat_deg)
    eps = math.radians(eps_deg)
    y = -math.cos(ramc)
    x = math.sin(ramc) * math.cos(eps) + math.tan(lat) * math.sin(eps)
    return (math.degrees(math.atan2(y, x)) + 360.0) % 360.0


@dataclass
class GrahaPosition:
    graha: str
    tropical: float
    sidereal: float
    latitude: float
    retrograde: bool


@dataclass
class Sky:
    jd_ut: float
    jd_tt: float
    ayanamsa: float
    grahas: dict
    lagna_tropical: float
    lagna_sidereal: float


_PLANET_BODIES = {
    "Sun": astronomy.Body.Sun,
    "Mercury": astronomy.Body.Mercury,
    "Venus": astronomy.Body.Venus,
    "Mars": astronomy.Body.Mars,
    "Jupiter": astronomy.Body.Jupiter,
    "Saturn": astronomy.Body.Saturn,
}


def compute_sky(ut: datetime, lat: float, lon: float) -> Sky:
    if ut.tzinfo is None:
        ut = ut.replace(tzinfo=timezone.utc)
    time = astronomy.Time.Make(
        ut.year, ut.month, ut.day, ut.hour, ut.minute, ut.second + ut.microsecond / 1e6
    )
    jd_ut = time.ut + 2451545.0
    jd_tt = time.tt + 2451545.0
    ayan = lahiri_ayanamsa(jd_tt)

    grahas: dict[str, GrahaPosition] = {}

    moon = astronomy.EclipticGeoMoon(time)
    grahas["Moon"] = GrahaPosition("Moon", moon.lon % 360, trop_to_sid(moon.lon, ayan), moon.lat, False)

    for name, body in _PLANET_BODIES.items():
        vec = astronomy.GeoVector(body, time, True)
        ecl = astronomy.Ecliptic(vec)
        retro = _is_retrograde(body, time)
        grahas[name] = GrahaPosition(
            name, ecl.elon % 360, trop_to_sid(ecl.elon, ayan), ecl.elat, retro
        )

    rahu_trop = _mean_node_tropical(jd_tt)
    grahas["Rahu"] = GrahaPosition("Rahu", rahu_trop, trop_to_sid(rahu_trop, ayan), 0.0, True)
    grahas["Ketu"] = GrahaPosition(
        "Ketu", (rahu_trop + 180) % 360, trop_to_sid(rahu_trop + 180, ayan), 0.0, True
    )

    gast_hours = astronomy.SiderealTime(time)
    lst_hours = (gast_hours + lon / 15.0) % 24.0
    ramc = lst_hours * 15.0
    lagna_trop = _tropical_ascendant(ramc, lat, _true_obliquity(jd_tt))
    lagna_sid = trop_to_sid(lagna_trop, ayan)

    for g in GRAHAS:
        if g not in grahas:
            raise RuntimeError(f"missing graha {g}")

    return Sky(jd_ut, jd_tt, ayan, grahas, lagna_trop, lagna_sid)


def _is_retrograde(body, time) -> bool:
    try:
        before = astronomy.Ecliptic(astronomy.GeoVector(body, time.AddDays(-1), True)).elon
        after = astronomy.Ecliptic(astronomy.GeoVector(body, time.AddDays(1), True)).elon
        diff = (after - before + 540) % 360 - 180
        return diff < 0
    except Exception:
        return False
