# Kala Chakra — Vedic Horoscope Studio

A Streamlit app that turns **anyone's** birth details into a full Vedic horoscope.
The deterministic engine computes; the agents only narrate.

> Standing rule (from the GR-001 handover): **the LLM narrates, it never calculates.**
> Every rashi, nakshatra, degree and dasha date comes from `calc_core`.

## What it does

1. **Input** — name, date of birth, time of birth (or "unknown → sunrise"), place
   (city picker or manual lat/lon), and language (English / हिन्दी / తెలుగు).
2. **Engine** — `calc_core` computes sidereal positions (astronomy-engine / Meeus +
   Lahiri ayanamsa), rashi, nakshatra + pada, lagna, D1/D9, and the full
   Vimsottari dasha ladder with the current Mahadasha / Antardasha / Pratyantardasha.
3. **Agents** — a Sutra-orchestrated set of specialist agents (Personality, Career,
   Relationships, Health, Dasha timeline, Remedies) narrate the chart. With an
   `OPENAI_API_KEY` they run through the **OpenAI Agents SDK** and are handed only
   the computed facts; without a key a grounded local narrator runs in the same
   language, so the app is always usable.
4. **Documents** — upload existing horoscopes (PDF / image / text, any language).
   They are parsed (images via OpenAI vision when a key is present) and
   **cross-validated** against the computed ladder at the correct hierarchy level.
   Genuine differences are shown, never silently overridden; illegible content is
   flagged, never guessed.
5. **PDF** — export the horoscope as a PDF in the language chosen from the dropdown,
   using bundled Noto fonts for Telugu / Devanagari / Latin.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py          # serves on 0.0.0.0:8520
```

## Configuration (API keys)

The app is fully usable with **no key**. A key only unlocks live OpenAI agent
narration and image (vision) OCR of uploaded sheets. Keys are read from the
**environment / secret store only — never from the UI**:

1. **Cursor Cloud secret** — Dashboard → Cloud Agents → Secrets → `OPENAI_API_KEY`
   (persists; injected into new agent runs).
2. **Local `.env`** — `cp .env.example .env` then set `OPENAI_API_KEY`.

The sidebar shows engine status only. Full details:
[docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Moving this to your own GitHub repo

Easiest: use the **Create repo** button in the Cursor agent view. To push to an
existing repo instead, add a `GITHUB_TOKEN` secret and run
`bash scripts/migrate_to_github.sh https://github.com/<you>/<repo>.git`.
Full steps (token-safe): [docs/MIGRATION.md](docs/MIGRATION.md).

## Test

```bash
python3 tests/test_gr001.py
```

The GR-001 golden case (Satya Anand, 25 Nov 1977, 01:55 IST, Kolkata) verifies:
Moon ≈ 29.27° · Krittika pada 1 · Mesha · Sun birth balance ≈ 4.83y · Jupiter/Saturn
ladder ending in 2033/2052 · Jupiter MD + Venus AD at the test epoch. A separate
test proves that when a document supplies the almanac's 4-6-02 balance, the ladder
anchors to it and reproduces the exact handwritten dates (2033-05-27 / 2052-05-27).

## Layout

```
app.py                     Streamlit UI (form, results, PDF)
kala/
  ephemeris.py             astronomy-engine wrapper + Lahiri ayanamsa
  nakshatra.py             rashi / nakshatra / navamsa / house
  vimsottari.py            dasha ladder + dasha_at (360-day civil scheme)
  chart.py                 compute_chart(native) — the one deterministic entry
  geo.py                   city table + timezonefinder + manual coords
  i18n.py                  UI strings en / hi / te
  parsing.py               PDF / image (vision) / text -> IngestedSource
  validators.py            level-aware cross-validation
  orchestration.py         Sutra + specialist agents (OpenAI SDK / local)
  pdf_report.py            fpdf2 PDF with Noto fonts
assets/fonts/              Noto Sans (Latin / Telugu / Devanagari)
tests/test_gr001.py        golden regression
docs/                      GR-001 handover PDF
```

The earlier Next.js prototype has been replaced by this Streamlit app.
