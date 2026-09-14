"""Horoscope PDF in English / Hindi / Telugu using Noto Unicode fonts."""

from __future__ import annotations

import os

from fpdf import FPDF

from .chart import Chart, chart_dasha_at, format_dms
from .constants import graha_name, nakshatra_name, rashi_name
from .i18n import t
from .orchestration import HoroscopeResult

_FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts")

_FONT_FILES = {
    "en": ("NotoSans-Regular.ttf", "NotoSans-Bold.ttf"),
    "hi": ("NotoSansDevanagari-Regular.ttf", "NotoSansDevanagari-Bold.ttf"),
    "te": ("NotoSansTelugu-Regular.ttf", "NotoSansTelugu-Bold.ttf"),
}


class _PDF(FPDF):
    def __init__(self, lang: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.lang = lang
        reg, bold = _FONT_FILES.get(lang, _FONT_FILES["en"])
        # Primary (script-specific) family used for prose.
        self.add_font("body", "", os.path.join(_FONT_DIR, reg))
        self.add_font("body", "B", os.path.join(_FONT_DIR, bold))
        # Latin family for numbers, dates, degrees.
        self.add_font("latin", "", os.path.join(_FONT_DIR, "NotoSans-Regular.ttf"))
        self.add_font("latin", "B", os.path.join(_FONT_DIR, "NotoSans-Bold.ttf"))
        # Every script registered so glyphs fall back across languages
        # (Latin 'R'/'•' inside a Telugu font, native letters inside Latin).
        self.add_font("fb_noto", "", os.path.join(_FONT_DIR, "NotoSans-Regular.ttf"))
        self.add_font("fb_deva", "", os.path.join(_FONT_DIR, "NotoSansDevanagari-Regular.ttf"))
        self.add_font("fb_telugu", "", os.path.join(_FONT_DIR, "NotoSansTelugu-Regular.ttf"))
        self.set_fallback_fonts(["fb_noto", "fb_deva", "fb_telugu"])
        self.set_auto_page_break(auto=True, margin=16)


def build_pdf(chart: Chart, result: HoroscopeResult, epoch_iso: str, lang: str) -> bytes:
    pdf = _PDF(lang)
    pdf.add_page()

    pdf.set_font("body", "B", 20)
    pdf.cell(0, 12, t("title", lang), new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("latin", "", 11)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 7, f"{chart.native.name}  |  {chart.native.date} {chart.native.time}  |  {chart.native.place}",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Summary
    _heading(pdf, t("summary", lang))
    rows = [
        (t("moon", lang), f"{rashi_name(chart.rashi, lang)}  ({format_dms(chart.moon_sidereal)})"),
        (t("nakshatra", lang), f"{nakshatra_name(chart.nakshatra, lang)}  pada {chart.pada}"),
        (t("lagna", lang), rashi_name(chart.lagna_rashi, lang)),
        (t("ayanamsa", lang), f"{chart.ayanamsa:.4f}"),
    ]
    hit = chart_dasha_at(chart, epoch_iso)
    if hit and hit["mahadasha"]:
        md, ad = hit["mahadasha"], hit["antardasha"]
        cur = f"{graha_name(md.lord, lang)} ({md.start}–{md.end})"
        if ad:
            cur += f" / {graha_name(ad.lord, lang)}"
        rows.append((t("current_period", lang), cur))
    for label, value in rows:
        _kv(pdf, label, value)
    pdf.ln(2)

    # Planetary table
    _heading(pdf, t("grahas", lang))
    pdf.set_font("body", "B", 10)
    w = [40, 45, 22, 55]
    headers = [t("graha", lang), t("degree", lang), t("house", lang), t("nakshatra", lang)]
    for i, h in enumerate(headers):
        pdf.cell(w[i], 7, h, border="B")
    pdf.ln(7)
    pdf.set_font("body", "", 10)
    for p in chart.placements:
        pdf.cell(w[0], 6, graha_name(p.graha, lang) + (" (R)" if p.retrograde else ""))
        pdf.set_font("latin", "", 10)
        pdf.cell(w[1], 6, format_dms(p.sidereal))
        pdf.cell(w[2], 6, str(p.house))
        pdf.set_font("body", "", 10)
        pdf.cell(w[3], 6, f"{nakshatra_name(p.nakshatra, lang)} {p.pada}")
        pdf.ln(6)
    pdf.ln(2)

    # Dasha ladder
    _heading(pdf, t("dasha", lang))
    pdf.set_font("latin", "", 10)
    for s in chart.ladder[:9]:
        pdf.cell(0, 6, f"{graha_name(s.lord, lang)}   {s.start}  ->  {s.end}   ({s.duration.as_str()})",
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Predictions
    _heading(pdf, t("predictions", lang))
    for sec in result.sections:
        _para(pdf, sec.title, font="body", style="B", size=11)
        _para(pdf, sec.body, font="body", style="", size=10)
        pdf.ln(1)

    # Special yogas
    _heading(pdf, t("yogas", lang))
    if getattr(result, "yogas", None):
        for yname, yeff in result.yogas:
            _para(pdf, yname, font="body", style="B", size=10)
            _para(pdf, yeff, font="body", style="", size=10)
            pdf.ln(0.5)
    else:
        _para(pdf, t("no_yogas", lang), font="body", style="", size=10)
    pdf.ln(1)

    if result.remedies:
        _heading(pdf, t("remedies", lang))
        for r in result.remedies:
            _para(pdf, f"• {r}", font="body", style="", size=10)
        pdf.ln(1)

    if result.validation:
        _heading(pdf, t("validation", lang))
        pdf.set_text_color(90, 90, 90)
        _para(pdf, f"{result.validation.status}: {result.validation.message}", font="latin", style="", size=9, h=5)
        for d in result.validation.details[:8]:
            _para(pdf, f"- {d}", font="latin", style="", size=9, h=5)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(4)
    pdf.set_text_color(120, 120, 120)
    _para(pdf, t("footer_rule", lang), font="latin", style="", size=8, h=4)

    out = pdf.output()
    return bytes(out)


def _para(pdf: _PDF, text: str, font: str = "body", style: str = "", size: int = 10, h: float = 6):
    pdf.set_font(font, style, size)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, h, text, new_x="LMARGIN", new_y="NEXT")


def _heading(pdf: _PDF, text: str):
    pdf.set_font("body", "B", 13)
    pdf.set_text_color(150, 40, 40)
    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)


def _kv(pdf: _PDF, label: str, value: str):
    label_w = 55
    x0 = pdf.l_margin
    y0 = pdf.get_y()
    pdf.set_font("body", "B", 10)
    pdf.set_xy(x0, y0)
    pdf.cell(label_w, 6, label)
    pdf.set_font("body", "", 10)
    pdf.set_xy(x0 + label_w, y0)
    pdf.multi_cell(pdf.epw - label_w, 6, value, new_x="LMARGIN", new_y="NEXT")
