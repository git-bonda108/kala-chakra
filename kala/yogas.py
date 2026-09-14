"""Deterministic yoga detection from a computed chart.

Each detector uses only facts already in the chart (sign, house, conjunction,
Parashari aspect, dignity) via kala.analysis. Formation rules follow the
classical texts (BPHS, Phaladeepika, Saravali). Effect text is a concise,
non-fear-based paraphrase and is provided in en / hi / te.

detect_yogas(chart) -> list[Yoga]  (only the yogas actually present).
"""

from __future__ import annotations

from dataclasses import dataclass

from .analysis import (
    DUSTHANAS,
    KENDRAS,
    TRIKONAS,
    aspects_graha,
    conjunct,
    dignity,
    house_of,
    houses_apart,
    lord_of_house,
    placement_of,
    sign_of,
)


@dataclass
class Yoga:
    key: str
    name: dict          # {en,hi,te}
    effect: dict        # {en,hi,te}
    strength: str = "present"   # present | strong
    source: str = ""


def _n(en, hi, te):
    return {"en": en, "hi": hi, "te": te}


# planet -> (yoga name trilingual) for Pancha Mahapurusha
_MAHAPURUSHA = {
    "Mars": _n("Ruchaka Yoga", "रुचक योग", "రుచక యోగం"),
    "Mercury": _n("Bhadra Yoga", "भद्र योग", "భద్ర యోగం"),
    "Jupiter": _n("Hamsa Yoga", "हंस योग", "హంస యోగం"),
    "Venus": _n("Malavya Yoga", "मालव्य योग", "మాళవ్య యోగం"),
    "Saturn": _n("Sasa Yoga", "शश योग", "శశ యోగం"),
}
_MAHAPURUSHA_EFFECT = {
    "Mars": _n(
        "A Panch Mahapurusha yoga of Mars — courage, leadership, discipline and physical vigour; strong drive to achieve.",
        "मंगल का पंच महापुरुष योग — साहस, नेतृत्व, अनुशासन और शारीरिक शक्ति; लक्ष्य पाने की प्रबल प्रेरणा।",
        "కుజుని పంచ మహాపురుష యోగం — ధైర్యం, నాయకత్వం, క్రమశిక్షణ, శారీరక శక్తి; లక్ష్యసాధనలో బలమైన పట్టుదల.",
    ),
    "Mercury": _n(
        "A Panch Mahapurusha yoga of Mercury — sharp intellect, eloquence, learning and success in communication or commerce.",
        "बुध का पंच महापुरुष योग — तीव्र बुद्धि, वाक्पटुता, विद्या और संचार या वाणिज्य में सफलता।",
        "బుధుని పంచ మహాపురుష యోగం — పదునైన బుద్ధి, వాక్చాతుర్యం, విద్య, సంభాషణ లేదా వాణిజ్యంలో విజయం.",
    ),
    "Jupiter": _n(
        "A Panch Mahapurusha yoga of Jupiter — wisdom, ethics, respect and good fortune; a natural teacher and guide.",
        "गुरु का पंच महापुरुष योग — ज्ञान, नैतिकता, सम्मान और सौभाग्य; स्वाभाविक गुरु व मार्गदर्शक।",
        "గురుని పంచ మహాపురుష యోగం — జ్ఞానం, నైతికత, గౌరవం, అదృష్టం; సహజ గురువు, మార్గదర్శి.",
    ),
    "Venus": _n(
        "A Panch Mahapurusha yoga of Venus — charm, artistic gifts, comfort, relationships and refined enjoyment.",
        "शुक्र का पंच महापुरुष योग — आकर्षण, कलात्मक प्रतिभा, सुख, संबंध और परिष्कृत आनंद।",
        "శుక్రుని పంచ మహాపురుష యోగం — ఆకర్షణ, కళా ప్రతిభ, సౌకర్యం, సంబంధాలు, శుద్ధ ఆనందం.",
    ),
    "Saturn": _n(
        "A Panch Mahapurusha yoga of Saturn — endurance, authority through patience, and lasting achievement over time.",
        "शनि का पंच महापुरुष योग — सहनशीलता, धैर्य से अधिकार और समय के साथ स्थायी उपलब्धि।",
        "శని పంచ మహాపురుష యోగం — ఓర్పు, సహనంతో అధికారం, కాలక్రమేణా శాశ్వత సాధన.",
    ),
}


def _mahapurusha(chart):
    out = []
    for graha in ("Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        p = placement_of(chart, graha)
        if not p:
            continue
        dig = dignity(graha, p.rashi)
        if dig in ("own", "exalted", "moolatrikona") and p.house in KENDRAS:
            out.append(Yoga(
                key=f"mahapurusha_{graha.lower()}",
                name=_MAHAPURUSHA[graha],
                effect=_MAHAPURUSHA_EFFECT[graha],
                strength="strong",
                source="BPHS / Phaladeepika",
            ))
    return out


def _gaja_kesari(chart):
    jup_h = house_of(chart, "Jupiter")
    moon_h = house_of(chart, "Moon")
    if not jup_h or not moon_h:
        return []
    if houses_apart(moon_h, jup_h) in KENDRAS:
        return [Yoga(
            key="gaja_kesari",
            name=_n("Gaja Kesari Yoga", "गजकेसरी योग", "గజకేసరి యోగం"),
            effect=_n(
                "Jupiter in an angle from the Moon — intelligence, good repute, influence and steady prosperity.",
                "चंद्र से केंद्र में गुरु — बुद्धि, यश, प्रभाव और स्थिर समृद्धि।",
                "చంద్రుని నుండి కేంద్రంలో గురుడు — బుద్ధి, కీర్తి, ప్రభావం, స్థిర సమృద్ధి.",
            ),
            source="Phaladeepika",
        )]
    return []


def _budha_aditya(chart):
    if conjunct(chart, "Sun", "Mercury"):
        return [Yoga(
            key="budha_aditya",
            name=_n("Budha-Aditya Yoga", "बुध-आदित्य योग", "బుధ-ఆదిత్య యోగం"),
            effect=_n(
                "Sun and Mercury together — intelligence, clarity of expression, learning and administrative skill.",
                "सूर्य और बुध साथ — बुद्धि, अभिव्यक्ति की स्पष्टता, विद्या और प्रशासनिक कौशल।",
                "సూర్యుడు, బుధుడు కలిసి — బుద్ధి, భావ వ్యక్తీకరణ స్పష్టత, విద్య, పరిపాలనా నైపుణ్యం.",
            ),
            source="Classical",
        )]
    return []


def _chandra_mangala(chart):
    if conjunct(chart, "Moon", "Mars"):
        return [Yoga(
            key="chandra_mangala",
            name=_n("Chandra-Mangala Yoga", "चंद्र-मंगल योग", "చంద్ర-మంగళ యోగం"),
            effect=_n(
                "Moon with Mars — drive to earn, enterprise and resourcefulness with money and property.",
                "चंद्र के साथ मंगल — अर्जन की प्रेरणा, उद्यम और धन-संपत्ति में कुशलता।",
                "చంద్రునితో కుజుడు — సంపాదన పట్ల పట్టుదల, వ్యాపార దక్షత, ధనం-ఆస్తిలో నేర్పు.",
            ),
            source="Phaladeepika",
        )]
    return []


def _dhana(chart):
    """A checkable Dhana (wealth) yoga: the 2nd and 11th lords are conjunct,
    in mutual aspect, or in exchange (each in the other's house)."""
    l2 = lord_of_house(chart, 2)
    l11 = lord_of_house(chart, 11)
    if l2 == l11:
        return []  # one planet rules both; not a two-lord connection
    linked = (
        conjunct(chart, l2, l11)
        or (aspects_graha(chart, l2, l11) and aspects_graha(chart, l11, l2))
        or (house_of(chart, l2) == 11 and house_of(chart, l11) == 2)
    )
    if linked:
        return [Yoga(
            key="dhana",
            name=_n("Dhana Yoga", "धन योग", "ధన యోగం"),
            effect=_n(
                "The lords of income (11th) and wealth (2nd) are connected — capacity to earn and to accumulate.",
                "आय (एकादश) व धन (द्वितीय) के स्वामियों का संबंध — कमाने और संचय करने की क्षमता।",
                "ఆదాయం (11వ), సంపద (2వ) అధిపతుల అనుసంధానం — సంపాదించే, కూడబెట్టే సామర్థ్యం.",
            ),
            source="BPHS",
        )]
    return []


def _raja(chart):
    """A checkable Raja yoga: a kendra lord and a trikona lord (distinct
    planets) are conjunct or in mutual aspect."""
    kendra_lords = {lord_of_house(chart, h) for h in KENDRAS}
    trikona_lords = {lord_of_house(chart, h) for h in TRIKONAS}
    for kl in kendra_lords:
        for tl in trikona_lords:
            if kl == tl:
                continue
            if conjunct(chart, kl, tl) or (
                aspects_graha(chart, kl, tl) and aspects_graha(chart, tl, kl)
            ):
                return [Yoga(
                    key="raja",
                    name=_n("Raja Yoga", "राज योग", "రాజ యోగం"),
                    effect=_n(
                        "An angle-lord and a trine-lord are joined — a classical Raja yoga bringing status, success and rise.",
                        "केंद्र व त्रिकोण स्वामियों का योग — प्रतिष्ठा, सफलता और उन्नति देने वाला राज योग।",
                        "కేంద్ర, త్రికోణ అధిపతుల కలయిక — హోదా, విజయం, ఉన్నతినిచ్చే రాజ యోగం.",
                    ),
                    strength="strong",
                    source="BPHS",
                )]
    return []


def _neecha_bhanga(chart):
    """Neecha Bhanga Raja Yoga: a debilitated planet whose debilitation is
    cancelled. Common cancellations checked here:
      (a) the lord of the debilitation sign is in a kendra from lagna, or
      (b) the planet exalted in that sign is in a kendra from lagna, or
      (c) the debilitated planet itself is in a kendra from lagna.
    """
    from .analysis import RASHI_LORD, EXALTATION
    out = []
    for graha in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        p = placement_of(chart, graha)
        if not p or dignity(graha, p.rashi) != "debilitated":
            continue
        deb_sign = p.rashi
        disp = RASHI_LORD[deb_sign]
        exalter = next((g for g, s in EXALTATION.items() if s == deb_sign), None)
        cancelled = (
            house_of(chart, disp) in KENDRAS
            or (exalter and house_of(chart, exalter) in KENDRAS)
            or p.house in KENDRAS
        )
        if cancelled:
            out.append(Yoga(
                key=f"neecha_bhanga_{graha.lower()}",
                name=_n("Neecha Bhanga Raja Yoga", "नीच भंग राज योग", "నీచ భంగ రాజ యోగం"),
                effect=_n(
                    f"{graha}'s debilitation is cancelled — an early struggle turns into notable rise and success.",
                    f"{graha} की नीचता का भंग — आरंभिक संघर्ष बाद में उल्लेखनीय उन्नति व सफलता में बदलता है।",
                    f"{graha} నీచత్వం రద్దు — తొలి కష్టం తర్వాత గణనీయమైన ఉన్నతి, విజయంగా మారుతుంది.",
                ),
                source="BPHS",
            ))
    return out


def _vipreet_raja(chart):
    """Vipreet Raja yoga: a lord of 6/8/12 placed in a 6/8/12 house."""
    names = {
        6: _n("Harsha Yoga", "हर्ष योग", "హర్ష యోగం"),
        8: _n("Sarala Yoga", "सरल योग", "సరళ యోగం"),
        12: _n("Vimala Yoga", "विमल योग", "విమల యోగం"),
    }
    out = []
    for h in DUSTHANAS:
        lord = lord_of_house(chart, h)
        if house_of(chart, lord) in DUSTHANAS:
            out.append(Yoga(
                key=f"vipreet_{h}",
                name=names[h],
                effect=_n(
                    "A Vipreet Raja yoga — difficulties transform into unexpected gains and resilience.",
                    "विपरीत राज योग — कठिनाइयाँ अप्रत्याशित लाभ व दृढ़ता में बदलती हैं।",
                    "విపరీత రాజ యోగం — కష్టాలు అనూహ్య లాభాలుగా, పట్టుదలగా మారతాయి.",
                ),
                source="Phaladeepika",
            ))
    return out


def _kemadruma(chart):
    """Kemadruma: no graha (excluding Sun and the nodes) in the 2nd or 12th
    from the Moon. Cancelled if any graha sits in a kendra from the Moon or is
    conjunct the Moon."""
    moon_h = house_of(chart, "Moon")
    if not moon_h:
        return []
    second = ((moon_h - 1 + 1) % 12) + 1
    twelfth = ((moon_h - 1 - 1) % 12) + 1
    neighbours = [
        p for p in chart.placements
        if p.graha not in ("Moon", "Sun", "Rahu", "Ketu") and p.house in (second, twelfth)
    ]
    if neighbours:
        return []
    # cancellations
    for p in chart.placements:
        if p.graha in ("Moon", "Rahu", "Ketu"):
            continue
        if houses_apart(moon_h, p.house) in KENDRAS or p.house == moon_h:
            return []
    return [Yoga(
        key="kemadruma",
        name=_n("Kemadruma Yoga", "केमद्रुम योग", "కేమద్రుమ యోగం"),
        effect=_n(
            "The Moon stands without close support — cultivate steady routines, good company and self-reliance to offset it.",
            "चंद्र सहायकों बिना — स्थिर दिनचर्या, अच्छे संग और आत्मनिर्भरता से इसे संतुलित करें।",
            "చంద్రునికి సమీప మద్దతు లేదు — స్థిర దినచర్య, మంచి సాంగత్యం, ఆత్మనిర్భరతతో సమతుల్యం చేసుకోండి.",
        ),
        source="BPHS",
    )]


_DETECTORS = (
    _mahapurusha, _gaja_kesari, _budha_aditya, _chandra_mangala,
    _dhana, _raja, _neecha_bhanga, _vipreet_raja, _kemadruma,
)


def detect_yogas(chart) -> list:
    found: list = []
    for det in _DETECTORS:
        try:
            found.extend(det(chart))
        except Exception:
            continue
    return found


def yoga_name(y: Yoga, lang: str) -> str:
    return y.name.get(lang) or y.name.get("en") or y.key


def yoga_effect(y: Yoga, lang: str) -> str:
    return y.effect.get(lang) or y.effect.get("en") or ""
