"""Names and Vimsottari data with en / hi / te labels."""

from __future__ import annotations

GRAHAS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
]

RASHIS = [
    "Mesha",
    "Vrishabha",
    "Mithuna",
    "Karka",
    "Simha",
    "Kanya",
    "Tula",
    "Vrischika",
    "Dhanu",
    "Makara",
    "Kumbha",
    "Meena",
]

NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

# Vimsottari lord per nakshatra (Ashwini = Ketu), repeating every 9.
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
] * 3

VIM_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

VIM_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

NAKSHATRA_SPAN = 360.0 / 27.0
PADA_SPAN = NAKSHATRA_SPAN / 4.0

# South Indian square layout (row-major, 4x4). Inner cells are None.
SOUTH_INDIAN_CELLS = [
    ["Meena", "Mesha", "Vrishabha", "Mithuna"],
    ["Kumbha", None, None, "Karka"],
    ["Makara", None, None, "Simha"],
    ["Dhanu", "Vrischika", "Tula", "Kanya"],
]

# ---- Localised names -------------------------------------------------------

RASHI_NAMES = {
    "en": {r: n for r, n in zip(RASHIS, [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    ])},
    "hi": {r: n for r, n in zip(RASHIS, [
        "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
        "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन",
    ])},
    "te": {r: n for r, n in zip(RASHIS, [
        "మేష", "వృషభ", "మిథున", "కర్కాటక", "సింహ", "కన్య",
        "తుల", "వృశ్చిక", "ధనుస్సు", "మకర", "కుంభ", "మీన",
    ])},
}

GRAHA_NAMES = {
    "en": {g: g for g in GRAHAS},
    "hi": {g: n for g, n in zip(GRAHAS, [
        "सूर्य", "चंद्र", "मंगल", "बुध", "गुरु", "शुक्र", "शनि", "राहु", "केतु",
    ])},
    "te": {g: n for g, n in zip(GRAHAS, [
        "రవి", "చంద్ర", "కుజ", "బుధ", "గురు", "శుక్ర", "శని", "రాహు", "కేతు",
    ])},
}

NAKSHATRA_NAMES = {
    "en": {n: n for n in NAKSHATRAS},
    "hi": {n: h for n, h in zip(NAKSHATRAS, [
        "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु",
        "पुष्य", "आश्लेषा", "मघा", "पूर्व फाल्गुनी", "उत्तर फाल्गुनी", "हस्त",
        "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा",
        "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्व भाद्रपद",
        "उत्तर भाद्रपद", "रेवती",
    ])},
    "te": {n: t for n, t in zip(NAKSHATRAS, [
        "అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆర్ద్ర", "పునర్వసు",
        "పుష్యమి", "ఆశ్లేష", "మఘ", "పూర్వ ఫల్గుణి", "ఉత్తర ఫల్గుణి", "హస్త",
        "చిత్త", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ఠ", "మూల", "పూర్వాషాఢ",
        "ఉత్తరాషాఢ", "శ్రవణ", "ధనిష్ఠ", "శతభిష", "పూర్వ భాద్ర",
        "ఉత్తర భాద్ర", "రేవతి",
    ])},
}


def graha_name(graha: str, lang: str) -> str:
    return GRAHA_NAMES.get(lang, GRAHA_NAMES["en"]).get(graha, graha)


def rashi_name(rashi: str, lang: str) -> str:
    return RASHI_NAMES.get(lang, RASHI_NAMES["en"]).get(rashi, rashi)


def nakshatra_name(nak: str, lang: str) -> str:
    return NAKSHATRA_NAMES.get(lang, NAKSHATRA_NAMES["en"]).get(nak, nak)
