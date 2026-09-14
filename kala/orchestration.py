"""Sutra orchestration: deterministic facts first, then specialist narration.

- calc_core computes every position and date (compute_chart / dasha_at).
- kala.analysis derives house lords, dignities, aspects and per-dimension
  signals; kala.yogas detects classical yogas. All of this is factual.
- The narrator turns those facts into grounded, localized prose. With an
  OpenAI key, specialist agents narrate from the SAME facts (they may not
  invent numbers); without a key the deterministic local narrator runs, so the
  app is always fully usable.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

from .analysis import (
    DIMENSION_SPEC,
    dimension_signal,
    planet_strength,
)
from .chart import Chart, chart_dasha_at
from .constants import graha_name, nakshatra_name, rashi_name
from .i18n import t
from .validators import ConsistencyFlag
from .yogas import detect_yogas, yoga_effect, yoga_name

# Ordered life dimensions + the dasha timeline, each with an i18n title key.
DIMENSIONS_ORDER = ["personality", "career", "finance", "education", "romance", "health"]
DIM_TITLE_KEY = {
    "personality": "dim_personality",
    "career": "dim_career",
    "finance": "dim_finance",
    "education": "dim_education",
    "romance": "dim_romance",
    "health": "dim_health",
}


@dataclass
class Prediction:
    domain: str
    title: str
    body: str


@dataclass
class HoroscopeResult:
    mode: str  # "openai" | "local"
    language: str
    sections: list = field(default_factory=list)
    remedies: list = field(default_factory=list)
    validation: ConsistencyFlag | None = None
    yogas: list = field(default_factory=list)  # list[(name, effect)] localized


# ---------------------------------------------------------------------------
# Localized fragments for the local narrator
# ---------------------------------------------------------------------------

_DIM_THEME = {
    "personality": {"en": "self and temperament", "hi": "स्वयं व स्वभाव", "te": "స్వీయం, స్వభావం"},
    "career": {"en": "career and action", "hi": "कर्म व करियर", "te": "వృత్తి, కర్మ"},
    "finance": {"en": "wealth and income", "hi": "धन व आय", "te": "సంపద, ఆదాయం"},
    "education": {"en": "learning and intellect", "hi": "विद्या व बुद्धि", "te": "విద్య, బుద్ధి"},
    "romance": {"en": "love and partnership", "hi": "प्रेम व साझेदारी", "te": "ప్రేమ, భాగస్వామ్యం"},
    "health": {"en": "vitality and well-being", "hi": "जीवनशक्ति व स्वास्थ्य", "te": "ప్రాణశక్తి, ఆరోగ్యం"},
}

_DIGNITY = {
    "exalted": {"en": "exalted and very strong", "hi": "उच्च व अत्यंत बलवान", "te": "ఉచ్ఛస్థితిలో, చాలా బలం"},
    "moolatrikona": {"en": "in moolatrikona and strong", "hi": "मूलत्रिकोण में व बलवान", "te": "మూలత్రికోణంలో, బలం"},
    "own": {"en": "in its own sign and strong", "hi": "स्वराशि में व बलवान", "te": "స్వక్షేత్రంలో, బలం"},
    "debilitated": {"en": "debilitated and under pressure", "hi": "नीच व दबाव में", "te": "నీచస్థితిలో, ఒత్తిడిలో"},
    "neutral": {"en": "comfortably placed", "hi": "सामान्य स्थिति में", "te": "సాధారణ స్థితిలో"},
}

_PSTR = {
    "strong": {"en": "strong", "hi": "बलवान", "te": "బలం"},
    "moderate": {"en": "moderate", "hi": "मध्यम", "te": "మధ్యస్థం"},
    "weak": {"en": "tender", "hi": "कोमल", "te": "సున్నితం"},
}

_LABEL = {
    "strong": {"en": "strong and supportive", "hi": "बलवान व सहायक", "te": "బలంగా, అనుకూలంగా"},
    "moderate": {"en": "mixed — steady with effort", "hi": "मिश्रित — प्रयास से स्थिर", "te": "మిశ్రమం — కృషితో స్థిరం"},
    "weak": {"en": "tender — asks for patience and care", "hi": "कोमल — धैर्य व देखभाल आवश्यक", "te": "సున్నితం — ఓర్పు, శ్రద్ధ అవసరం"},
}

_GUIDE = {
    "strong": {"en": "Build on this and act with confidence.", "hi": "इस पर आगे बढ़ें और आत्मविश्वास से कार्य करें।", "te": "దీనిపై ముందుకు సాగండి, ఆత్మవిశ్వాసంతో వ్యవహరించండి."},
    "moderate": {"en": "Progress is steady; consistency and timing pay off.", "hi": "प्रगति स्थिर है; निरंतरता व सही समय लाभ देते हैं।", "te": "పురోగతి స్థిరం; స్థిరత్వం, సరైన సమయం ఫలితమిస్తాయి."},
    "weak": {"en": "Go gently; small disciplined steps help the most.", "hi": "धैर्य रखें; छोटे अनुशासित कदम सर्वाधिक सहायक हैं।", "te": "నెమ్మదిగా సాగండి; చిన్న క్రమశిక్షణ అడుగులే ఎక్కువ సహాయపడతాయి."},
}

_LEAD_TMPL = {
    "en": "The {house} of {theme} is ruled by {lord}, placed in {lord_sign} ({lord_house}) — {dignity}.",
    "hi": "{theme} का {house} {lord} द्वारा शासित है, जो {lord_sign} ({lord_house}) में स्थित है — {dignity}।",
    "te": "{theme} యొక్క {house}ను {lord} పాలిస్తాడు, {lord_sign} ({lord_house})లో ఉన్నాడు — {dignity}.",
}
_KARAKA_TMPL = {
    "en": "Its natural significator {karaka} is {kstr} in {karaka_sign}.",
    "hi": "इसका कारक {karaka} {karaka_sign} में {kstr} है।",
    "te": "దీని కారకుడు {karaka} {karaka_sign}లో {kstr}గా ఉన్నాడు.",
}
_OVERALL_TMPL = {
    "en": "Overall, this area of life is {label}. {guide}",
    "hi": "कुल मिलाकर जीवन का यह क्षेत्र {label} है। {guide}",
    "te": "మొత్తంగా జీవితంలో ఈ విభాగం {label}. {guide}",
}


def _house_label(h: int, lang: str) -> str:
    if lang == "en":
        ord_ = {1: "1st", 2: "2nd", 3: "3rd"}.get(h, f"{h}th")
        return f"{ord_} house"
    if lang == "hi":
        return f"{h}वें भाव"
    return f"{h}వ భావం"


def _frag(d: dict, key: str, lang: str) -> str:
    return d.get(key, d.get("neutral", {})).get(lang) if key in d else ""


# ---------------------------------------------------------------------------
# Facts payload (also handed to live agents so they never invent numbers)
# ---------------------------------------------------------------------------

def chart_facts(chart: Chart, epoch_iso: str) -> dict:
    hit = chart_dasha_at(chart, epoch_iso)
    md = hit["mahadasha"] if hit else None
    ad = hit["antardasha"] if hit else None
    pd = hit["pratyantardasha"] if hit else None
    dims = {}
    for k in DIMENSION_SPEC:
        d = dimension_signal(chart, k)
        dims[k] = {
            "strength": d.strength,
            "label": d.label,
            "houses": [
                {"house": h.house, "sign": h.sign, "lord": h.lord,
                 "lord_house": h.lord_house, "lord_sign": h.lord_sign,
                 "lord_dignity": h.lord_dignity, "occupants": h.occupants}
                for h in d.houses
            ],
            "karakas": [{"graha": ps.graha, "sign": ps.sign, "house": ps.house,
                         "dignity": ps.dignity, "label": ps.label} for ps in d.karakas],
        }
    return {
        "name": chart.native.name,
        "birth": f"{chart.native.date} {chart.native.time}",
        "place": chart.native.place,
        "moon_sidereal": round(chart.moon_sidereal, 4),
        "nakshatra": chart.nakshatra,
        "pada": chart.pada,
        "rashi": chart.rashi,
        "lagna_rashi": chart.lagna_rashi,
        "ayanamsa": round(chart.ayanamsa, 4),
        "birth_dasha_lord": chart.birth_lord,
        "balance": chart.balance_ymd.as_str(),
        "current_mahadasha": {"lord": md.lord, "start": md.start, "end": md.end} if md else None,
        "current_antardasha": {"lord": ad.lord, "start": ad.start, "end": ad.end} if ad else None,
        "current_pratyantardasha": {"lord": pd.lord, "start": pd.start, "end": pd.end} if pd else None,
        "placements": [
            {"graha": p.graha, "rashi": p.rashi, "house": p.house,
             "nakshatra": p.nakshatra, "pada": p.pada, "retrograde": p.retrograde}
            for p in chart.placements
        ],
        "dimensions": dims,
        "yogas": [y.key for y in detect_yogas(chart)],
    }


# ---------------------------------------------------------------------------
# Local narrator (no key). Grounded, localized, honest.
# ---------------------------------------------------------------------------

def _load_kb():
    try:
        from . import knowledge_base as kb  # type: ignore
        return kb
    except Exception:
        return None


def _kb_text(entry, lang: str) -> str:
    if not entry:
        return ""
    val = entry.get(lang) or entry.get("en") or ""
    return str(val).strip()


def _kb_extra(chart, key: str, dim, kb, lang: str) -> str:
    """A grounded enrichment sentence from the sourced knowledge base."""
    if kb is None:
        return ""
    try:
        if key == "personality":
            nak = getattr(kb, "NAKSHATRA_KB", {}).get(chart.nakshatra, {})
            ra = getattr(kb, "RASHI_KB", {}).get(chart.rashi, {})
            return " ".join(x for x in [_kb_text(nak.get("traits"), lang), _kb_text(ra.get("traits"), lang)] if x)
        if key == "career":
            nak = getattr(kb, "NAKSHATRA_KB", {}).get(chart.nakshatra, {})
            return _kb_text(nak.get("career"), lang)
        # finance/education/romance/health -> significations of the first karaka
        karaka = dim.karakas[0].graha
        g = getattr(kb, "GRAHA_KB", {}).get(karaka, {})
        return _kb_text(g.get("significations"), lang)
    except Exception:
        return ""


def _dimension_body(chart, key: str, lang: str, kb) -> str:
    dim = dimension_signal(chart, key)
    primary = dim.houses[0]
    lead = _LEAD_TMPL[lang].format(
        house=_house_label(primary.house, lang),
        theme=_DIM_THEME[key][lang],
        lord=graha_name(primary.lord, lang),
        lord_sign=rashi_name(primary.lord_sign, lang),
        lord_house=_house_label(primary.lord_house, lang),
        dignity=_DIGNITY[primary.lord_dignity][lang],
    )
    karaka = dim.karakas[0]
    kk = _KARAKA_TMPL[lang].format(
        karaka=graha_name(karaka.graha, lang),
        kstr=_PSTR[karaka.label][lang],
        karaka_sign=rashi_name(karaka.sign, lang),
    )
    extra = _kb_extra(chart, key, dim, kb, lang)
    overall = _OVERALL_TMPL[lang].format(label=_LABEL[dim.label][lang], guide=_GUIDE[dim.label][lang])
    parts = [lead, kk]
    if extra:
        parts.append(extra)
    parts.append(overall)
    return " ".join(parts)


_TIMELINE_TMPL = {
    "en": "You are in the {md} Mahadasha ({mds} – {mde}), with {ad} Antardasha now. {mdeff} This sub-period colours the theme of {adtheme}.",
    "hi": "आप {md} महादशा ({mds} – {mde}) में हैं, अभी {ad} अंतर्दशा। {mdeff} यह अंतर अवधि {adtheme} के भाव को रंग देती है।",
    "te": "మీరు {md} మహాదశ ({mds} – {mde})లో ఉన్నారు, ప్రస్తుతం {ad} అంతర్దశ. {mdeff} ఈ ఉపదశ {adtheme} భావాన్ని ప్రభావితం చేస్తుంది.",
}


def _timeline_body(chart, epoch_iso: str, lang: str, kb) -> str:
    hit = chart_dasha_at(chart, epoch_iso)
    md = hit["mahadasha"] if hit else None
    ad = hit["antardasha"] if hit else None
    if not md:
        return ""
    mdeff = ""
    if kb is not None:
        try:
            mdeff = _kb_text(getattr(kb, "DASHA_KB", {}).get(md.lord, {}).get("effect"), lang)
        except Exception:
            mdeff = ""
    adtheme = ""
    if kb is not None and ad is not None:
        try:
            adtheme = _kb_text(getattr(kb, "GRAHA_KB", {}).get(ad.lord, {}).get("significations"), lang)
        except Exception:
            adtheme = ""
    return _TIMELINE_TMPL[lang].format(
        md=graha_name(md.lord, lang), mds=md.start, mde=md.end,
        ad=graha_name(ad.lord, lang) if ad else graha_name(md.lord, lang),
        mdeff=mdeff, adtheme=adtheme or _DIM_THEME["career"][lang],
    ).replace("  ", " ").strip()


_REMEDY = {
    "en": [
        "Strengthen your Mahadasha lord {md} through its weekday practice, mantra and charity.",
        "Honour the deity of {nak} nakshatra and keep speech gentle in the current period.",
        "Support the tender areas of the chart with routine, gratitude and service rather than haste.",
    ],
    "hi": [
        "महादशा स्वामी {md} को उसके वार, मंत्र व दान से बल दें।",
        "{nak} नक्षत्र के देवता का सम्मान करें और वर्तमान काल में वाणी कोमल रखें।",
        "कुंडली के कोमल क्षेत्रों को शीघ्रता के बजाय नियमितता, कृतज्ञता व सेवा से सहारा दें।",
    ],
    "te": [
        "మహాదశ అధిపతి {md}ని ఆ వారం, మంత్రం, దానంతో బలపరచండి.",
        "{nak} నక్షత్ర దేవతను గౌరవించండి, ప్రస్తుత కాలంలో మాటను మృదువుగా ఉంచండి.",
        "జాతకంలోని సున్నిత విభాగాలను తొందరకు బదులు క్రమశిక్షణ, కృతజ్ఞత, సేవతో ఆదుకోండి.",
    ],
}


def local_horoscope(chart: Chart, epoch_iso: str, lang: str,
                    validation: ConsistencyFlag | None) -> HoroscopeResult:
    kb = _load_kb()
    sections: list[Prediction] = []
    for key in DIMENSIONS_ORDER:
        sections.append(Prediction(key, t(DIM_TITLE_KEY[key], lang), _dimension_body(chart, key, lang, kb)))
    tl = _timeline_body(chart, epoch_iso, lang, kb)
    if tl:
        sections.append(Prediction("timeline", t("dim_timeline", lang), tl))

    md_lord = chart.birth_lord
    hit = chart_dasha_at(chart, epoch_iso)
    if hit and hit["mahadasha"]:
        md_lord = hit["mahadasha"].lord
    remedies = [r.format(md=graha_name(md_lord, lang), nak=nakshatra_name(chart.nakshatra, lang))
                for r in _REMEDY[lang]]
    if kb is not None:
        try:
            kb_remedy = _kb_text(getattr(kb, "GRAHA_KB", {}).get(md_lord, {}).get("remedies"), lang)
            if kb_remedy:
                remedies.append(kb_remedy)
        except Exception:
            pass

    yogas = [(yoga_name(y, lang), yoga_effect(y, lang)) for y in detect_yogas(chart)]
    return HoroscopeResult("local", lang, sections, remedies, validation, yogas)


# ---------------------------------------------------------------------------
# OpenAI Agents SDK path
# ---------------------------------------------------------------------------

def openai_horoscope(chart: Chart, epoch_iso: str, lang: str,
                     validation: ConsistencyFlag | None, api_key: str) -> HoroscopeResult:
    from agents import Agent, Runner, function_tool

    os.environ["OPENAI_API_KEY"] = api_key
    facts = chart_facts(chart, epoch_iso)
    facts_json = json.dumps(facts, ensure_ascii=False)

    @function_tool
    def get_chart_facts() -> str:
        """Return the deterministic chart facts (positions, houses, dignities,
        per-dimension house lords/karakas, current dasha, detected yogas). The
        only source of numbers. Never compute astronomy yourself."""
        return facts_json

    lang_name = {"en": "English", "hi": "Hindi", "te": "Telugu"}[lang]
    sections: list[Prediction] = []

    for key in DIMENSIONS_ORDER:
        agent = Agent(
            name=f"{key} specialist",
            instructions=(
                f"You are a Vedic astrology specialist for the '{key}' area of life in the Kala "
                f"Chakra studio. Call get_chart_facts and base EVERYTHING on facts.dimensions['{key}'] "
                f"(its house lord placement, dignity and karaka strength) and the current dasha. Never "
                f"invent degrees, houses or dates. Write 3-4 sentences of grounded, specific, "
                f"empowering, non-fear-based guidance. Write ONLY in {lang_name}. No preamble, no markdown."
            ),
            tools=[get_chart_facts],
        )
        try:
            result = Runner.run_sync(agent, f"Give the {key} reading.")
            body = str(result.final_output).strip()
        except Exception:
            body = _dimension_body(chart, key, lang, _load_kb())
        sections.append(Prediction(key, t(DIM_TITLE_KEY[key], lang), body))

    # Timeline from the deterministic narrator (dates must stay exact).
    tl = _timeline_body(chart, epoch_iso, lang, _load_kb())
    if tl:
        sections.append(Prediction("timeline", t("dim_timeline", lang), tl))

    remedy_agent = Agent(
        name="remedy specialist",
        instructions=(
            "Call get_chart_facts. Suggest exactly 3 gentle, non-fear-based Vedic remedies tied to "
            f"the current Mahadasha lord and the Moon nakshatra. Write ONLY in {lang_name}. "
            "Return them as 3 short lines."
        ),
        tools=[get_chart_facts],
    )
    try:
        rr = Runner.run_sync(remedy_agent, "List the remedies.")
        remedies = [ln.strip("-• ").strip() for ln in str(rr.final_output).splitlines() if ln.strip()][:3]
    except Exception:
        remedies = []
    if not remedies:
        remedies = local_horoscope(chart, epoch_iso, lang, validation).remedies

    yogas = [(yoga_name(y, lang), yoga_effect(y, lang)) for y in detect_yogas(chart)]
    return HoroscopeResult("openai", lang, sections, remedies, validation, yogas)


def run_orchestration(chart: Chart, epoch_iso: str, lang: str,
                      validation: ConsistencyFlag | None,
                      api_key: str | None = None) -> HoroscopeResult:
    """Narrate the chart. Keys come from config (environment) only; the optional
    api_key argument exists for tests and is not sourced from any UI."""
    from .config import get_settings

    key = (api_key or get_settings().openai_api_key or "").strip()
    if key:
        try:
            return openai_horoscope(chart, epoch_iso, lang, validation, key)
        except Exception:
            pass
    return local_horoscope(chart, epoch_iso, lang, validation)
