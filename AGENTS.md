# Kala Chakra

Streamlit Vedic horoscope studio. Deterministic engine computes; agents narrate.

- `kala/chart.py` `compute_chart(native)` is the single source of positions/dates.
- Ephemeris: astronomy-engine (Meeus) + Lahiri ayanamsa. Dasha: Vimsottari, 360-day civil scheme.
- Agents (`kala/orchestration.py`) receive only computed facts. With `OPENAI_API_KEY` they use the OpenAI Agents SDK; otherwise a grounded local narrator runs. Either way they never compute astronomy.
- Uploaded documents are parsed (`kala/parsing.py`) and cross-validated at the correct dasha level (`kala/validators.py`). Illegible content is flagged, never guessed.
- Languages: en / hi / te via `kala/i18n.py`. PDF via `kala/pdf_report.py` with bundled Noto fonts.
- Golden test: `python3 tests/test_gr001.py`. Run it on any change to calc or validators.
- Dev server: `streamlit run app.py` on port 8520.
