# Sources & Bibliography — Jyotish Knowledge Base

This document lists the references used to compile `kala/knowledge_base.py`
(the 27 nakshatras, 12 rashis, 9 grahas, 12 bhavas, and the 9 Vimsottari
mahadasha lords). It records what each source was used for and an honest note
on confidence.

**Guiding principle:** No citations were fabricated. Core classical attributes
(nakshatra deity/symbol/gana, sign lord/element/quality, planetary karakatva,
house significations, Vimsottari periods) are long-standing and near-universally
agreed across the classical literature. The human-readable English/Hindi/Telugu
summaries are concise, non-fear-based *paraphrases*, not verbatim translations of
the Sanskrit originals.

---

## Classical Sanskrit texts (primary sources)

- **Brihat Parashara Hora Shastra (BPHS)** — attributed to Sage Parashara.
  The foundational text of Vedic astrology. Used for: planetary significations
  (karakatva), house (bhava) meanings, the Vimsottari dasha system and its
  period lengths, and nakshatra rulerships.
  Confidence: **HIGH** for structure and core assignments.

- **Phaladeepika** — by Mantreswara.
  A classic on predictive astrology. Used for: house significations, planetary
  results, and sign/planet characteristics that cross-check BPHS.
  Confidence: **HIGH**.

- **Saravali** — by Kalyana Varma.
  Classic compendium. Used for: planetary and sign traits, and nakshatra/rashi
  characteristics.
  Confidence: **HIGH** for the attributes drawn.

- **Brihat Jataka** — by Varahamihira.
  Early authoritative natal-astrology text. Used as a cross-check for sign
  (rashi) qualities (movable/fixed/dual), elements, and planetary natures.
  Confidence: **HIGH** for the specific attributes used.

Note on nakshatra deities and symbols: the presiding deities (devatas) trace to
Vedic sources (e.g. the Taittiriya Brahmana) and are reproduced consistently
across the classical Jyotish tradition. The deity, symbol, gana (Deva /
Manushya / Rakshasa), and Vimsottari ruling planet for each of the 27 nakshatras
are standard, well-attested assignments. Confidence: **HIGH**.

---

## Reputable modern references (corroboration & wording)

These were used to corroborate the classical attributes and to shape concise,
modern, non-fear-based summaries. They are secondary, not authoritative over the
classical texts.

- **AstroSage** — https://www.astrosage.com/
  Used for: cross-checking nakshatra characteristics, career tendencies, planet
  significations and remedies. Widely-used English/Hindi reference site.
  Confidence: **MEDIUM-HIGH** (popular reference; corroborated against classics).

- **Drik Panchang** — https://www.drikpanchang.com/
  Used for: nakshatra deity/symbol/gana confirmation and panchang conventions.
  Confidence: **HIGH** for factual almanac data (deities, symbols, lords).

- **Prokerala** — https://www.prokerala.com/astrology/
  Used for: nakshatra and rashi trait summaries and career associations.
  Confidence: **MEDIUM** (popular reference; used only where consistent with classics).

- **Wikipedia** — Nakshatra, Rashi (Hindu astrology), and Navagraha articles
  (e.g. https://en.wikipedia.org/wiki/Nakshatra ,
  https://en.wikipedia.org/wiki/Navagraha ).
  Used for: a neutral cross-check of deity names, symbols, ruling planets, and
  the Vimsottari dasha year values. Well-referenced for these tabular facts.
  Confidence: **HIGH** for the tabular attributes used.

---

## Hindi and Telugu language sources / channels

Hindi (Devanagari) and Telugu translations in the knowledge base are original,
concise summaries written to match the English trait text, cross-referenced with
these reputable language resources for terminology and spelling. They are
faithful paraphrases, not quotations.

- **AstroSage Hindi** — https://hindi.astrosage.com/
  Reference for standard Hindi Jyotish terminology (ग्रह, राशि, नक्षत्र, भाव, दशा).
  Confidence: **MEDIUM-HIGH**.

- **Telugu Panchangam / Jyotish references** — e.g. Prokerala Telugu
  (https://www.prokerala.com/astrology/telugu/) and Mulugu Panchangam
  (https://www.mulugu.com/), widely used Telugu almanac/astrology resources.
  Reference for standard Telugu terms (గ్రహం, రాశి, నక్షత్రం, భావం, దశ) and
  nakshatra/rashi names.
  Confidence: **MEDIUM** for terminology; translations here are editorial.

- **Well-known Hindi Jyotish YouTube channels** (e.g. Astro Arun Pandit,
  Astrologer Acharya types) and **Telugu channels** are part of the broader
  popular ecosystem. They were treated as general background only and were **not**
  relied upon for any specific factual claim in the knowledge base, to avoid
  citing content that cannot be verified. Confidence: **LOW** — background context only.

---

## Confidence summary

| Attribute category | Confidence | Notes |
| --- | --- | --- |
| Nakshatra deity / symbol / gana / ruling planet | HIGH | Classical, cross-checked; ruling planets match Vimsottari lords in `kala/constants.py`. |
| Rashi lord / element / quality | HIGH | Classical, universally agreed. |
| Graha karaka / significations | HIGH | Core BPHS karakatva. |
| Graha remedies | MEDIUM-HIGH | Traditional, non-fear-based practices; presented as general guidance, not prescriptions. |
| Bhava names / themes | HIGH | Standard classical house significations. |
| Vimsottari dasha periods & general effects | HIGH (periods) / MEDIUM (effects) | Period lengths are exact; general effects are broad tendencies that depend on chart specifics. |
| Hindi (hi) translations | MEDIUM-HIGH | Faithful summaries, not verbatim Sanskrit. |
| Telugu (te) translations | MEDIUM | Faithful summaries; terminology cross-checked. |

**Disclaimer:** These summaries are for educational and cultural reference. Dasha
effects and predictions in real charts depend on planetary strength, dignity,
house placement, and aspects — the knowledge base gives only general tendencies.
