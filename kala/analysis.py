"""Deterministic chart analysis: dignities, house lords, aspects, strength.

Everything here is factual Jyotish bookkeeping derived from the already-computed
chart (signs, houses, navamsa). No astronomy is done here and nothing is
invented — this layer only *reads* what compute_chart produced so the narrator
and the yoga engine can speak from grounded facts.

Canonical tables (sign rulers, exaltation/debilitation/own/moolatrikona,
Parashari aspects) follow Brihat Parashara Hora Shastra (BPHS).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .constants import RASHIS

# Sign ruler (rashi -> graha). BPHS.
RASHI_LORD = {
    "Mesha": "Mars", "Vrishabha": "Venus", "Mithuna": "Mercury", "Karka": "Moon",
    "Simha": "Sun", "Kanya": "Mercury", "Tula": "Venus", "Vrischika": "Mars",
    "Dhanu": "Jupiter", "Makara": "Saturn", "Kumbha": "Saturn", "Meena": "Jupiter",
}

# Exaltation / debilitation sign per graha (7 classical grahas). BPHS.
EXALTATION = {
    "Sun": "Mesha", "Moon": "Vrishabha", "Mars": "Makara", "Mercury": "Kanya",
    "Jupiter": "Karka", "Venus": "Meena", "Saturn": "Tula",
}
DEBILITATION = {
    "Sun": "Tula", "Moon": "Vrischika", "Mars": "Karka", "Mercury": "Meena",
    "Jupiter": "Makara", "Venus": "Kanya", "Saturn": "Mesha",
}

# Own signs (rulership). Nodes have no undisputed own sign; omitted on purpose.
OWN_SIGNS = {
    "Sun": ["Simha"], "Moon": ["Karka"], "Mars": ["Mesha", "Vrischika"],
    "Mercury": ["Mithuna", "Kanya"], "Jupiter": ["Dhanu", "Meena"],
    "Venus": ["Vrishabha", "Tula"], "Saturn": ["Makara", "Kumbha"],
}

# Moolatrikona sign per graha (used only for a small strength bonus).
MOOLATRIKONA = {
    "Sun": "Simha", "Moon": "Vrishabha", "Mars": "Mesha", "Mercury": "Kanya",
    "Jupiter": "Dhanu", "Venus": "Tula", "Saturn": "Kumbha",
}

NATURAL_BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
NATURAL_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

# Parashari special aspects: house-offsets a graha aspects (1 = its own house).
# Everyone aspects the 7th; Mars 4/8, Jupiter 5/9, Saturn 3/10 in addition.
ASPECT_OFFSETS = {
    "Sun": [7], "Moon": [7], "Mercury": [7], "Venus": [7],
    "Mars": [4, 7, 8], "Jupiter": [5, 7, 9], "Saturn": [3, 7, 10],
    # Nodes: many schools give them Jupiter-like 5/7/9; kept for aspect checks.
    "Rahu": [5, 7, 9], "Ketu": [5, 7, 9],
}

KENDRAS = (1, 4, 7, 10)
TRIKONAS = (1, 5, 9)
DUSTHANAS = (6, 8, 12)


def _sidx(sign: str) -> int:
    return RASHIS.index(sign)


def sign_in_house(chart, house: int) -> str:
    """The rashi occupying a given house (whole-sign from lagna)."""
    lag = _sidx(chart.lagna_rashi)
    return RASHIS[(lag + house - 1) % 12]


def house_of_sign(chart, sign: str) -> int:
    lag = _sidx(chart.lagna_rashi)
    return ((_sidx(sign) - lag) % 12) + 1


def lord_of_house(chart, house: int) -> str:
    return RASHI_LORD[sign_in_house(chart, house)]


def placement_of(chart, graha: str):
    for p in chart.placements:
        if p.graha == graha:
            return p
    return None


def house_of(chart, graha: str) -> int:
    p = placement_of(chart, graha)
    return p.house if p else 0


def sign_of(chart, graha: str) -> str:
    p = placement_of(chart, graha)
    return p.rashi if p else ""


def dignity(graha: str, sign: str) -> str:
    """One of: exalted | debilitated | moolatrikona | own | neutral."""
    if EXALTATION.get(graha) == sign:
        return "exalted"
    if DEBILITATION.get(graha) == sign:
        return "debilitated"
    if MOOLATRIKONA.get(graha) == sign:
        return "moolatrikona"
    if sign in OWN_SIGNS.get(graha, []):
        return "own"
    return "neutral"


def houses_apart(from_house: int, to_house: int) -> int:
    """Count 1..12 of to_house counted from from_house (from_house itself = 1)."""
    return ((to_house - from_house) % 12) + 1


def aspects_house(chart, graha: str, target_house: int) -> bool:
    h = house_of(chart, graha)
    if not h:
        return False
    for off in ASPECT_OFFSETS.get(graha, [7]):
        if ((h - 1 + off - 1) % 12) + 1 == target_house:
            return True
    return False


def aspects_graha(chart, from_graha: str, to_graha: str) -> bool:
    return aspects_house(chart, from_graha, house_of(chart, to_graha))


def conjunct(chart, a: str, b: str) -> bool:
    return house_of(chart, a) == house_of(chart, b) and house_of(chart, a) != 0


def grahas_in_house(chart, house: int) -> list:
    return [p.graha for p in chart.placements if p.house == house]


# ---------------------------------------------------------------------------
# Per-planet strength (a light, transparent 0..10 heuristic; NOT Shadbala).
# ---------------------------------------------------------------------------

_DIGNITY_SCORE = {
    "exalted": 4.0, "moolatrikona": 3.0, "own": 3.0, "neutral": 1.0,
    "debilitated": -2.0,
}


@dataclass
class PlanetStrength:
    graha: str
    sign: str
    house: int
    dignity: str
    retrograde: bool
    score: float          # rough 0..10
    label: str            # strong | moderate | weak


def planet_strength(chart, graha: str) -> PlanetStrength:
    p = placement_of(chart, graha)
    dig = dignity(graha, p.rashi)
    score = 3.0 + _DIGNITY_SCORE.get(dig, 1.0)
    # Angular / trinal placement adds stability.
    if p.house in KENDRAS:
        score += 1.5
    elif p.house in TRIKONAS:
        score += 1.0
    elif p.house in DUSTHANAS:
        score -= 1.5
    # Benefic aspect onto the planet's own house helps a little.
    for b in ("Jupiter", "Venus", "Mercury"):
        if b != graha and aspects_graha(chart, b, graha):
            score += 0.5
    score = max(0.0, min(10.0, score))
    label = "strong" if score >= 6.5 else "weak" if score <= 3.0 else "moderate"
    return PlanetStrength(graha, p.rashi, p.house, dig, p.retrograde, round(score, 1), label)


# ---------------------------------------------------------------------------
# Life-dimension signal map. Language-neutral facts for the narrator.
# ---------------------------------------------------------------------------

# houses examined, and the natural significators (karakas) for each dimension.
DIMENSION_SPEC = {
    "personality": {"houses": [1], "karakas": ["Sun", "Moon"]},
    "career":      {"houses": [10], "karakas": ["Saturn", "Sun", "Mercury"]},
    "finance":     {"houses": [2, 11], "karakas": ["Jupiter", "Venus"]},
    "education":   {"houses": [4, 5], "karakas": ["Mercury", "Jupiter"]},
    "romance":     {"houses": [7, 5], "karakas": ["Venus"]},
    "health":      {"houses": [1, 6], "karakas": ["Sun", "Saturn"]},
}


@dataclass
class HouseSignal:
    house: int
    sign: str
    lord: str
    lord_house: int
    lord_sign: str
    lord_dignity: str
    occupants: list = field(default_factory=list)


@dataclass
class DimensionSignal:
    key: str
    houses: list = field(default_factory=list)          # list[HouseSignal]
    karakas: list = field(default_factory=list)         # list[PlanetStrength]
    strength: float = 0.0
    label: str = "moderate"


def dimension_signal(chart, key: str) -> DimensionSignal:
    spec = DIMENSION_SPEC[key]
    houses = []
    for h in spec["houses"]:
        sign = sign_in_house(chart, h)
        lord = RASHI_LORD[sign]
        lp = placement_of(chart, lord)
        houses.append(HouseSignal(
            house=h, sign=sign, lord=lord,
            lord_house=lp.house, lord_sign=lp.rashi,
            lord_dignity=dignity(lord, lp.rashi),
            occupants=grahas_in_house(chart, h),
        ))
    karakas = [planet_strength(chart, k) for k in spec["karakas"]]
    # Dimension strength = mean of (house-lord strengths + primary karaka).
    scores = [planet_strength(chart, hs.lord).score for hs in houses]
    scores.append(karakas[0].score)
    avg = sum(scores) / len(scores)
    label = "strong" if avg >= 6.0 else "weak" if avg <= 3.2 else "moderate"
    return DimensionSignal(key, houses, karakas, round(avg, 1), label)


def all_dimensions(chart) -> list:
    return [dimension_signal(chart, k) for k in DIMENSION_SPEC]
