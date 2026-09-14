"""Parse uploaded reference documents into IngestedSource records.

Formats:
  - .txt / .md            -> read text, regex for dasha/rashi tokens
  - .pdf                  -> pypdf text extraction, then same regex
  - .png/.jpg/.jpeg/.webp -> OpenAI vision (if key) returns structured tokens
                             with confidence; low-confidence stays flagged and
                             is NEVER guessed. Without a key, the image is
                             recorded as unparsed (honest), not fabricated.

Standing rule: illegible content is surfaced as low-confidence, never invented.
"""

from __future__ import annotations

import io
import json
import re

from .constants import GRAHAS, RASHIS
from .validators import IngestedPeriod, IngestedSource

_LORD_ALIASES = {
    "sun": "Sun", "ravi": "Sun", "surya": "Sun",
    "moon": "Moon", "chandra": "Moon", "chandu": "Moon",
    "mars": "Mars", "kuja": "Mars", "mangal": "Mars", "angaraka": "Mars",
    "mercury": "Mercury", "budha": "Mercury", "budh": "Mercury",
    "jupiter": "Jupiter", "guru": "Jupiter", "brihaspati": "Jupiter",
    "venus": "Venus", "shukra": "Venus", "sukra": "Venus",
    "saturn": "Saturn", "shani": "Saturn", "sani": "Saturn",
    "rahu": "Rahu",
    "ketu": "Ketu",
}

_DATE_RE = re.compile(r"(\d{4})[-./](\d{1,2})[-./](\d{1,2})")


def _norm_date(m: re.Match) -> str:
    y, mo, d = m.group(1), int(m.group(2)), int(m.group(3))
    return f"{y}-{mo:02d}-{d:02d}"


def _periods_from_text(text: str) -> list[IngestedPeriod]:
    periods: list[IngestedPeriod] = []
    low = text.lower()
    for alias, lord in _LORD_ALIASES.items():
        for m in re.finditer(rf"\b{alias}\b", low):
            window = low[m.start(): m.start() + 60]
            dates = list(_DATE_RE.finditer(window))
            start = _norm_date(dates[0]) if len(dates) >= 1 else None
            end = _norm_date(dates[1]) if len(dates) >= 2 else None
            level = "mahadasha"
            if any(w in window for w in ("antar", "bhukti", "/")):
                level = "antardasha"
            if start or end:
                periods.append(
                    IngestedPeriod(level=level, lord=lord, start=start, end=end, confidence="medium")
                )
    # dedupe
    seen = set()
    out = []
    for p in periods:
        key = (p.level, p.lord, p.start, p.end)
        if key not in seen:
            seen.add(key)
            out.append(p)
    return out


def _rashi_from_text(text: str) -> str | None:
    for r in RASHIS:
        if r.lower() in text.lower():
            return r
    return None


def parse_text(name: str, text: str) -> IngestedSource:
    return IngestedSource(
        source_id=name,
        label=f"Text document: {name}",
        periods=_periods_from_text(text),
        moon_rashi=_rashi_from_text(text),
        confidence="medium",
        illegible=[] if text.strip() else ["empty document"],
    )


def parse_pdf(name: str, data: bytes) -> IngestedSource:
    text = ""
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(data))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as exc:  # pragma: no cover
        return IngestedSource(name, f"PDF (unreadable): {name}", [], None, [f"pdf error: {exc}"], "low")
    src = parse_text(name, text)
    src.label = f"PDF document: {name}"
    if not text.strip():
        src.illegible.append("PDF had no extractable text (likely scanned) — needs vision OCR.")
    return src


def parse_image(name: str, data: bytes, api_key: str | None) -> IngestedSource:
    if not api_key:
        return IngestedSource(
            source_id=name,
            label=f"Image (unparsed): {name}",
            periods=[],
            moon_rashi=None,
            illegible=["Image OCR needs an OpenAI API key. Not guessed."],
            confidence="low",
        )
    try:
        import base64

        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        b64 = base64.b64encode(data).decode()
        prompt = (
            "You are reading a handwritten or printed Vedic astrology sheet, often in Telugu/Hindi. "
            "Extract ONLY what you can read with confidence. Return strict JSON: "
            '{"moon_rashi": <one of '
            + ", ".join(RASHIS)
            + " or null>, "
            '"periods": [{"level":"mahadasha|antardasha","lord":<one of '
            + ", ".join(GRAHAS)
            + '>, "start":"YYYY-MM-DD" or null, "end":"YYYY-MM-DD" or null, "confidence":"high|medium|low"}], '
            '"illegible": [<short notes on anything you could NOT read; do not guess>]}'
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    ],
                }
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        payload = json.loads(resp.choices[0].message.content or "{}")
        periods = [
            IngestedPeriod(
                level=p.get("level", "mahadasha"),
                lord=p.get("lord", ""),
                start=p.get("start"),
                end=p.get("end"),
                confidence=p.get("confidence", "low"),
            )
            for p in payload.get("periods", [])
            if p.get("lord") in GRAHAS
        ]
        return IngestedSource(
            source_id=name,
            label=f"Image (vision OCR): {name}",
            periods=periods,
            moon_rashi=payload.get("moon_rashi") if payload.get("moon_rashi") in RASHIS else None,
            illegible=payload.get("illegible", []),
            confidence="medium",
        )
    except Exception as exc:  # pragma: no cover
        return IngestedSource(name, f"Image (OCR failed): {name}", [], None, [f"vision error: {exc}"], "low")


def parse_upload(name: str, data: bytes, api_key: str | None) -> IngestedSource:
    lower = name.lower()
    if lower.endswith((".txt", ".md", ".csv")):
        return parse_text(name, data.decode("utf-8", errors="replace"))
    if lower.endswith(".pdf"):
        return parse_pdf(name, data)
    if lower.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
        return parse_image(name, data, api_key)
    return IngestedSource(name, f"Unsupported: {name}", [], None, ["unsupported file type"], "low")


def source_from_chart(chart) -> IngestedSource:
    """Turn the computed chart's mahadasha ladder into an IngestedSource so it
    can be cross-validated against uploaded documents."""
    periods = [
        IngestedPeriod("mahadasha", s.lord, s.start, s.end, "high")
        for s in chart.ladder
    ]
    return IngestedSource(
        source_id="calc_core",
        label="Computed chart (ephemeris)",
        periods=periods,
        moon_rashi=chart.rashi,
        nakshatra=chart.nakshatra,
        confidence="high",
    )
