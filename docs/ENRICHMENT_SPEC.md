# Kala Chakra — Enrichment SPEC: Life Dimensions, Yogas & Report Presentation

**Status:** Implementation-ready specification (domain research, not code).
**Scope:** Interpretive enrichment layer on top of the existing deterministic engine.
**Non-goal:** Re-deriving astronomy. All positions, dignities, houses, D9, and the
Vimsottari ladder come from `kala/chart.py::compute_chart`. This document tells the
narrator *what to say* and the engine *what boolean/derived facts to compute from
already-available data*.

---

## 0. Engine contract & shared primitives

Everything below is expressed in terms the engine already has, so no new astronomy
is required. The relevant fields (see `kala/chart.py`):

- `Placement.graha` — one of `Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu`.
- `Placement.rashi` — one of the 12 Sanskrit signs (`Mesha … Meena`).
- `Placement.house` — integer 1–12, whole-sign house counted **from lagna**.
- `Placement.sidereal` — sidereal ecliptic longitude in degrees (0–360).
- `Placement.navamsa` — D9 sign.
- `Placement.retrograde` — bool.
- `Chart.lagna_rashi`, `Chart.rashi` (Moon sign), `Chart.nakshatra`, `Chart.pada`.
- `Chart.ladder` — Vimsottari Maha→Antar→Pratyantar spans; `chart_dasha_at(chart, iso)`
  yields the currently running lords.

### 0.1 Derived helpers the engine should expose

These are pure functions over the fields above. Implement once; reuse everywhere.

```
SIGN_INDEX = {Mesha:0, Vrishabha:1, Mithuna:2, Karka:3, Simha:4, Kanya:5,
              Tula:6, Vrischika:7, Dhanu:8, Makara:9, Kumbha:10, Meena:11}

deg_in_sign(p)      = p.sidereal mod 30.0                # 0..30, for karaka ranking / exact dignity
house_of(graha)     = placement[graha].house             # 1..12 from lagna
sign_of(graha)      = placement[graha].rashi
lord_of_sign(sign)  = SIGN_LORD[sign]                    # table §2.9
lord_of_house(h)    = lord_of_sign( sign at house h )    # whole-sign: sign = lagna_rashi rotated by (h-1)
house_from(a, b)    = ((SIGN_INDEX[sign_of(a)] - SIGN_INDEX[sign_of(b)]) mod 12) + 1   # count of a's sign from b's sign, 1..12
conjunct(a, b)      = house_of(a) == house_of(b)         # same whole-sign house = same rashi
same_sign(a, b)     = sign_of(a) == sign_of(b)
```

**Whole-sign houses.** This app counts houses as whole signs from lagna
(`house_from_lagna`). Therefore *house lord of H* = lord of the sign that sits H
signs from the lagna sign, and "planet in house H" ⇔ "planet in that sign." Every
rule below assumes whole-sign; do not mix in bhava-chalit cusps.

### 0.2 House classes (from lagna, 1-indexed)

| Class | Houses | Meaning |
| --- | --- | --- |
| Kendra (angular / quadrant) | 1, 4, 7, 10 | Pillars of the chart; strong placement |
| Trikona (trine) | 1, 5, 9 | Dharma/fortune; most auspicious |
| Dusthana / Trik (evil) | 6, 8, 12 | Difficulty, loss, obstruction |
| Upachaya (growing) | 3, 6, 10, 11 | Improve over time; good for malefics |
| Maraka (killer) | 2, 7 | Health-limiting houses |
| Panapara | 2, 5, 8, 11 | Succedent |
| Apoklima | 3, 6, 9, 12 | Cadent |

*Source: BPHS ch. on Bhava-viveka; Phaladeepika ch. 2. Confidence: HIGH.*

### 0.3 Vedic full-aspect (graha drishti) rules — canonical

Every planet aspects the **7th** house/sign from itself (full). Additionally:

| Planet | Special full aspects (houses from itself) |
| --- | --- |
| Mars | 4th, 7th, 8th |
| Jupiter | 5th, 7th, 9th |
| Saturn | 3rd, 7th, 10th |
| Sun, Moon, Mercury, Venus | 7th only |
| Rahu, Ketu | 7th only (**MEDIUM**: some schools also grant 5th/9th like Jupiter — treat as optional, off by default) |

Engine check: `aspects(a, b)` is true when `house_from(b, a)` ∈ the aspect set of `a`
(always includes 7; plus the special offsets for Mars/Jupiter/Saturn).
`mutual_aspect(a,b) = aspects(a,b) and aspects(b,a)`.

*Source: BPHS "Graha Drishti"; Phaladeepika 2.13–2.15. Confidence: HIGH for the classical planets; nodal aspects MEDIUM.*

### 0.4 Natural benefics / malefics (for "benefic vs malefic aspect/conjunction")

- **Natural benefics (saumya):** Jupiter, Venus, waxing Moon, unafflicted Mercury.
- **Natural malefics (krura/papi):** Saturn, Mars, Sun, Rahu, Ketu, waning Moon,
  Mercury when conjoined only with malefics.
- **Moon waxing test** (engine, from longitudes): `angular_sep(Moon, Sun) between 72° and 288°`
  ⇒ treat Moon as benefic (bright); otherwise weak/malefic-leaning. (`angular_sep`
  = smallest circular difference of `sidereal` values.) *Confidence: HIGH; the exact
  72°/108° thresholds vary by author — MEDIUM on the cutoff.*
- **Mercury:** benefic if not conjunct (same house) with any natural malefic; else neutral/malefic.

*Source: BPHS "Graha-bheda"; Phaladeepika 2. Confidence: HIGH.*

### 0.5 Dignity states (used throughout; full table in §2.9)

For a planet P in sign S with `d = deg_in_sign(P)`:

- **Exalted (uccha):** S == exaltation sign of P. "Deep/exact exaltation" when `d`
  near the exaltation degree (± a few degrees).
- **Debilitated (neecha):** S == debilitation sign of P.
- **Own sign (swakshetra):** S ∈ own signs of P.
- **Mulatrikona:** S == mulatrikona sign of P and `d` within its mulatrikona arc.
- **Friend/enemy sign:** optional refinement via natural relationships table (MEDIUM
  priority; not required for the core rules here).

---

## 1. Life dimensions → computable signal map

Format per dimension: **primary house(s)** · **house lord to inspect** · **natural
karaka** · **D9 / dasha considerations** · **interpretive rules** (driven only by:
(a) sign of the house lord, (b) house the karaka occupies, (c) benefic/malefic
aspect/conjunction, (d) running Maha/Antar lord) · **phrasing guide** (strength vs
challenge).

> Global phrasing rule (all dimensions): describe **tendencies and timing**, never
> fixed fate. Prefer "supports / favours / a period to…" over "will." Always pair a
> challenge with a constructive lever (effort, timing, remedy). Never predict death,
> disease diagnosis, divorce, or financial ruin.

### 1.1 Personality & temperament

- **Primary houses:** 1st (Tanu — body, self, disposition).
- **House lord:** Lagna lord (lord of `lagna_rashi`) — its sign and house show how
  the self expresses and where life-energy flows.
- **Natural karakas:** Sun (soul/ego/vitality), Moon (mind/emotions). Also the
  **Moon's nakshatra** (temperament/gana) and its lord.
- **Cross-checks:** Sun sign (public/willful self), Moon sign (`Chart.rashi`, the
  emotional core — in Vedic práctice the Moon sign is the dominant "personality"
  read), Moon-nakshatra gana (Deva/Manushya/Rakshasa) from `knowledge_base.py`.
- **D9/dasha:** Lagna lord's navamsa dignity refines resilience of character; the
  running Mahadasha lord colours the current life-phase persona.

Interpretive rules:
1. **Lagna lord's sign** → element/quality of self-expression (Fire=assertive,
   Earth=grounded, Air=intellectual/social, Water=sensitive). Use `RASHI_KB` traits.
2. **Lagna lord's house** → the life arena the person identifies with (e.g. lagna
   lord in 10 → identity via career/status; in 12 → private/spiritual/abroad).
3. **Benefic (Jupiter/Venus) aspect on lagna or lagna lord** → refined, likeable,
   balanced temperament; **malefic (Saturn/Mars/Rahu) conjunction/aspect on lagna**
   → intense, hardened, or restless edge that maturity tempers.
4. **Moon sign + nakshatra gana** → emotional style (e.g. Karka Moon = nurturing;
   Rakshasa-gana nakshatra = strong-willed/blunt). If Moon is bright (§0.4) and
   unafflicted → steady mind; if waning + malefic-conjunct → mood sensitivity.

Phrasing guide — strength: "Your ascendant lord {L} in {sign} gives a {trait}
disposition; with {benefic} support you come across as {positive adjective}."
challenge: "A {malefic} influence on your ascendant can make you {intense/guarded};
channelled well this becomes {discipline/depth}." Keep it about *style*, not worth.

### 1.2 Career & profession

- **Primary house:** 10th (Karma — profession, status, public action).
- **House lord:** 10th lord — its sign shows the *field flavour*, its house shows
  *where career energy is spent*.
- **Natural karakas:** Sun (authority/government), Saturn (service/labour/industry),
  Mercury (commerce/communication/analysis); also **Jupiter** (advisory/teaching)
  as a general karaka of livelihood.
- **Amatyakaraka (Jaimini):** the Chara karaka with the **2nd-highest** `deg_in_sign`
  among the 7 planets Sun–Saturn (see §1.7). The AmK planet and the house/sign it
  sits in are a strong secondary indicator of profession and mentors.
- **Cross-checks:** 10th house **from the Moon** (career as felt/experienced), and
  the strongest planet in a kendra. Planets *in* the 10th strongly flavour vocation.
- **D9/dasha:** 10th lord's navamsa dignity = staying power of career; a Mahadasha
  of the 10th lord, AmK, or a planet in/aspecting the 10th typically times
  professional rises.

Interpretive rules:
1. **Sign of 10th lord** → career element/mode (Fire=leadership/enterprise,
   Earth=structure/finance/land, Air=communication/trade/tech, Water=care/creative/
   fluids). Combine with the karaka closest to the 10th.
2. **House of the strongest career karaka** (Sun/Saturn/Mercury) → domain: Sun in 10
   → authority roles; Saturn in 6 → service/labour/operations; Mercury in 3/5 →
   media/writing/markets.
3. **Benefic on 10th/10th lord** → recognition, ethical advancement; **malefic
   affliction** → friction, job changes, need for grit (frame as resilience).
4. **Running Maha/Antar lord = 10th lord / AmK / 10th-occupant** → a career-defining
   window (promotion, new role, visibility). Otherwise read the current lord's
   natural karaka to describe the *theme* of the present work-phase.

Phrasing guide — strength: name the field flavour concretely ("structure- and
service-oriented work — administration, operations, or engineering") and tie the
current dasha to timing. challenge: "career may progress in steps rather than leaps;
steady, accountable effort (Saturn's way) converts pressure into standing."

### 1.3 Finance & wealth

- **Primary houses:** 2nd (Dhana — accumulated wealth, savings, family money,
  speech) and 11th (Labha — income, gains, fulfilment of desires). 5th & 9th
  (Lakshmi-sthanas / trikonas) support sustained prosperity.
- **House lords:** 2nd lord and 11th lord — their mutual relationship is the crux of
  wealth (see Dhana yogas §2.5).
- **Natural karakas:** Jupiter (wealth/expansion/dhana-karaka), Venus (luxury,
  assets); Mercury for trade/commerce income.
- **Cross-checks:** connection among lords of **1, 2, 5, 9, 11** (the wealth-giving
  set). Planets in 2/11. 2nd/11th from the Moon (perceived earning).
- **D9/dasha:** dignity of 2nd/11th lords in navamsa = durability of wealth; dasha
  of a Dhana-yoga participant times income surges. Jupiter/Venus dasha generally
  supports finances if they are well-placed.

Interpretive rules:
1. **2nd lord in 11 / 11th lord in 2 / their conjunction or mutual aspect** →
   classic Dhana yoga: capacity to earn and retain (frame as strength).
2. **Jupiter or Venus in 2/5/11, or aspecting the 2nd/11th** → benefic support to
   savings and gains.
3. **2nd or 11th lord in a dusthana (6/8/12), or malefic affliction to 2/11 without
   benefic help** → money requires discipline, avoid over-leverage (frame as prudent
   caution, not poverty).
4. **Running dasha of 2nd/11th/5th/9th lord or a Dhana-yoga planet** → a period
   favourable for income, investments, or asset growth.

Phrasing guide — strength: "the link between your wealth (2nd) and gains (11th)
lords supports building and keeping resources, especially during {dasha}." challenge:
"finances reward planning and patience over speculation; a portion set aside steadily
outperforms quick bets." Always non-fatalistic; never promise specific sums.

### 1.4 Education & intellect

- **Primary houses:** 4th (foundational schooling, Bandhu), 5th (intelligence,
  learning capacity, Putra), 2nd (accumulated knowledge & memory, "vidya-dhana").
  9th supports higher/advanced learning.
- **House lords:** 4th & 5th lords for schooling/intellect; 2nd lord for retained
  knowledge.
- **Natural karakas:** Mercury (analytical intellect, articulation, buddhi) and
  Jupiter (wisdom, higher knowledge, jnana-karaka).
- **Cross-checks:** condition of Mercury & Jupiter (dignity, house, afflictions);
  the **Moon's nakshatra** (learning style/temperament — use `knowledge_base.py`).
- **D9/dasha:** Mercury/Jupiter navamsa dignity = depth of intellect; dasha of 4th/
  5th lord, Mercury, or Jupiter times educational milestones.

Interpretive rules:
1. **Mercury strong (own/exalted, kendra/trikona, benefic-aspected)** → sharp,
   articulate, quick-learning mind. **Jupiter strong** → wisdom, ethics, higher study.
2. **Budha-Aditya (Sun+Mercury same sign, §2.4)** → intelligence and analytical
   clarity (note: mild burn if very close to Sun).
3. **5th lord well-placed / benefic on 5th** → good grasping power and creative
   intellect; **malefic affliction to 5th/Mercury** → distractible or non-linear
   learning that suits hands-on/unconventional paths (frame constructively).
4. **Running Mercury/Jupiter/4th/5th-lord dasha** → strong window for study,
   exams, certifications, or teaching.

Phrasing guide — strength: connect Mercury/Jupiter dignity to concrete aptitudes
(analysis, languages, philosophy, sciences). challenge: reframe an afflicted 5th/
Mercury as a *different* learning mode (experiential, visual, applied), never as low
intelligence.

### 1.5 Romance, marriage & relationships

- **Primary house:** 7th (Yuvati/Kalatra — spouse, partnerships, marriage). 5th for
  romance/love affairs; 2nd (family) and 11th (fulfilment of desire, social bonds)
  support relationship life.
- **House lord:** 7th lord — its sign and house describe the partner and partnership
  arena.
- **Natural karakas:** **Venus** for a man's chart (wife/relationships), **Jupiter**
  for a woman's chart (husband). Venus is the universal relationship karaka; use the
  gendered karaka as a *secondary* refinement only when native gender is known,
  otherwise default to Venus + 7th.
- **Darakaraka (Jaimini):** the Chara karaka with the **lowest** `deg_in_sign` among
  the 7 planets (§1.7). The DK planet, its sign and house, signify the spouse and the
  nature of the bond.
- **D9/navamsa:** the **navamsa is the primary marriage chart**. Inspect: the
  **navamsa lord of the 7th** and the D9 sign of Venus/7th lord/Darakaraka. A planet
  weak in D1 but strong in D9 (vargottama or exalted in navamsa) strengthens marriage.
- **Dasha:** marriage/relationship events tend to time under dasha of the 7th lord,
  Venus, the Darakaraka, or a planet in/aspecting the 7th.

Interpretive rules:
1. **7th lord's sign** → partner's temperament flavour; **7th lord's house** → how/
   where partnership manifests (e.g. 7th lord in 10 → partner tied to career/status).
2. **Benefic (Jupiter/Venus) in or aspecting the 7th** → harmony, supportive union;
   **malefic (Saturn/Mars/Rahu/Ketu) in/aspecting 7th** → delays, effort, or
   friction that maturity and timing ease (frame as "commitment tested and deepened,"
   not doom). Mars affliction to 7th/Venus/Moon is the classic "Mangal" signal —
   present it as needing patience and matched partners, not as a curse.
3. **Venus's dignity & house** → quality of romantic/aesthetic life; Venus with
   malefics or in dusthana → relationships need conscious care.
4. **Running dasha of 7th lord / Venus / Darakaraka** → a period highlighting
   partnership, commitment, or significant relationship developments.

Phrasing guide — strength: describe partner qualities and harmony warmly and
specifically via 7th-lord sign + Venus condition. challenge: frame delays/tension as
timing and growth ("relationships mature later or after effort; a grounded, patient
partner suits you best"). Never state that marriage will fail or must be delayed by a
fixed age; avoid alarming "dosha" language — describe the pattern and the remedy.

### 1.6 Health & vitality

- **Primary houses:** 1st (body/constitution/vitality), 6th (illness, recovery,
  daily regimen), 8th (chronic/acute crises, longevity, Ayu). 12th (hospitalisation/
  rest) as secondary.
- **House lords:** lagna lord (overall vitality), 6th lord (nature of ailments),
  8th lord (longevity/chronic).
- **Natural karakas:** Sun (vitality, bones/heart, general health), Saturn
  (chronic/longevity/aging), Moon (mind/fluids/emotional health), Mars (accidents/
  inflammation/blood).
- **Cross-checks:** afflictions to lagna, lagna lord, and Moon; malefics in 1/8;
  benefic protection (Jupiter/Venus aspecting lagna is a strong shield).
- **D9/dasha:** lagna-lord navamsa dignity = constitutional reserve; dasha of 6th/
  8th lord or a malefic afflicting the lagna can mark health-attention periods
  (frame as "prioritise wellbeing," never as diagnosis).

Interpretive rules:
1. **Strong, unafflicted lagna + lagna lord + benefic aspect** → robust constitution
   and recuperative power.
2. **Malefic in 1st or heavy malefic aspect to lagna/Moon** → sensitive area
   (Mars=inflammation/injury, Saturn=chronic/joints, Rahu=hard-to-diagnose/anxiety);
   present as *tendencies to manage with lifestyle*, not predictions.
3. **6th/8th lord placement & strength** → resilience vs recurring issues; a strong
   6th lord actually helps *overcome* illness.
4. **Running dasha of 6th/8th lord or an afflicting malefic** → a window to invest in
   health, routine, and preventive care.

Phrasing guide — strength: "a resilient constitution with good recovery; maintain it
with regular routine." challenge: "a period to prioritise {area} through rest, diet,
and check-ups." **Never** name a specific disease, prognosis, or lifespan. Always
recommend qualified medical care alongside any lifestyle/remedy note.

### 1.7 Jaimini Chara Karakas (Atmakaraka / Amatyakaraka / Darakaraka) — computable

Fully derivable from `deg_in_sign` (= `sidereal mod 30`). Use the **7-karaka scheme**
(planets Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn — nodes excluded).

```
rank planets by deg_in_sign descending:
  Atmakaraka  (AK)  = highest  degrees  -> the soul's chief significator (self)
  Amatyakaraka(AmK) = 2nd highest        -> career, mentors, minister-of-self
  ...
  Darakaraka  (DK)  = lowest  degrees    -> spouse / partnerships
```

*Note (Rahu handling):* in the 8-karaka scheme Rahu is included using `30 − deg_in_sign(Rahu)`
(it moves retrograde). Default to the 7-karaka scheme for simplicity and label the
8-karaka variant **MEDIUM confidence / optional**. *Source: Jaimini Sutras 1.1; modern:
K.N. Rao, Sanjay Rath. Confidence: HIGH for the ranking method; scheme choice MEDIUM.*

---

## 2. Yogas — exact formation rules + effects

Priority ordering below is roughly by **frequency of presence + interpretive weight**:
conjunction/aspect yogas that appear in many charts come first; rarer, high-impact
yogas follow. Each yoga: **name (Sanskrit)** · **strict formation condition** (engine
terms) · **effect (1–2 sentences, display-ready)** · **source** · **confidence**.

All conditions use §0 helpers. "In kendra" = house ∈ {1,4,7,10}; "in trikona" =
{1,5,9}; "dusthana" = {6,8,12}. "Conjunct" = same whole-sign house. "Own/exalted/
debilitated" per §2.9.

---

### 2.1 Budha-Aditya yoga (बुध-आदित्य) — very common
- **Condition:** `same_sign(Sun, Mercury)` (Sun and Mercury in the same rashi).
  Optional refinement: not an exact combustion overlap (|sep| within a couple degrees)
  for the "clean" version — but classical rule only needs same-sign conjunction.
- **Effect:** Sharpens intelligence, communication, and analytical skill; supports
  scholarship, administration, and articulate expression.
- **Source:** Phaladeepika; BPHS conjunction yogas. **Confidence: HIGH** (formation);
  MEDIUM on combustion nuance.

### 2.2 Chandra-Mangala yoga (चन्द्र-मंगल) — common
- **Condition:** `conjunct(Moon, Mars)` (same house). Optional broaden:
  `mutual_aspect(Moon, Mars)`.
- **Effect:** Drive to earn and act; associated with financial enterprise and
  resourcefulness. Temper with balance, as it can add emotional intensity.
- **Source:** BPHS; Phaladeepika. **Confidence: HIGH** (conjunction); mutual-aspect
  variant MEDIUM.

### 2.3 Gaja Kesari yoga (गजकेसरी) — common, auspicious
- **Condition:** Jupiter is in a **kendra from the Moon**:
  `house_from(Jupiter, Moon) ∈ {1,4,7,10}`. (Stronger if Jupiter is also dignified
  and not combust/debilitated.)
- **Effect:** Confers intelligence, good reputation, and lasting respect; a
  fortifying, benevolent influence on the mind and status.
- **Source:** BPHS; Phaladeepika. **Confidence: HIGH.**

### 2.4 Pancha Mahapurusha yogas (पंच महापुरुष) — moderately common, high weight
General rule: a **non-luminary** (Mars/Mercury/Jupiter/Venus/Saturn) is in its **own
sign or exaltation** AND placed in a **kendra from lagna** (`house ∈ {1,4,7,10}`).
(Some schools also allow kendra from the Moon — treat as **MEDIUM/optional variant**.)

| Yoga | Planet | Qualifying sign (own **or** exalted) | Kendra from lagna |
| --- | --- | --- | --- |
| **Ruchaka** (रुचक) | Mars | Mesha **or** Vrischika (own) / Makara (exalt) | house ∈ {1,4,7,10} |
| **Bhadra** (भद्र) | Mercury | Mithuna (own) / Kanya (own **&** exalt) | house ∈ {1,4,7,10} |
| **Hamsa** (हंस) | Jupiter | Dhanu **or** Meena (own) / Karka (exalt) | house ∈ {1,4,7,10} |
| **Malavya** (मालव्य) | Venus | Vrishabha **or** Tula (own) / Meena (exalt) | house ∈ {1,4,7,10} |
| **Sasa / Shasha** (शश) | Saturn | Makara **or** Kumbha (own) / Tula (exalt) | house ∈ {1,4,7,10} |

- **Effect (per planet, one line each):**
  - Ruchaka — courage, leadership, physical vigour, command; a warrior/executive nature.
  - Bhadra — intellect, eloquence, business acumen, youthful sharpness.
  - Hamsa — wisdom, ethics, respect, spiritual and teaching gifts.
  - Malavya — charm, comfort, artistic taste, refined and pleasant life.
  - Sasa — discipline, authority over others, endurance, organisational power.
- **Source:** BPHS; Phaladeepika ch. 6; Saravali. **Confidence: HIGH** (own/exalt-in-
  kendra rule); the "kendra from Moon" extension MEDIUM.

### 2.5 Dhana yogas (धन योग) — wealth combinations (concrete checkable variants)
Let `L2 = lord_of_house(2)`, `L11 = lord_of_house(11)`, `L5`, `L9`, `L1` similarly.

- **Variant A — 2nd/11th link:** any of
  - `conjunct(L2, L11)`, or
  - `mutual_aspect(L2, L11)`, or
  - `house_of(L2) == 11 and house_of(L11) == 2` (exchange / parivartana).
- **Variant B — trikona-to-dhana link:** a lord of a wealth house {2, 11} is
  conjunct or in mutual aspect with a lord of a trikona {5, 9} (or the 1st):
  e.g. `conjunct(L11, L5)` or `conjunct(L2, L9)` or `conjunct(L1, L2)`.
- **Effect:** Supports earning capacity and the ability to accumulate and retain
  wealth; strongest during the dasha/antardasha of the participating lords.
- **Source:** BPHS "Dhana yoga adhyaya"; Phaladeepika. **Confidence: HIGH** for the
  lord-linkage principle; specific variant weighting MEDIUM.

### 2.6 Raja yogas (राज योग) — power/success (concrete checkable variant)
Let `KENDRA_LORDS = { lord_of_house(h) for h in [1,4,7,10] }` and
`TRIKONA_LORDS = { lord_of_house(h) for h in [1,5,9] }`.

- **Condition (core variant):** there exists a kendra lord `K` and a trikona lord `T`
  with `K != T` such that any of:
  - `conjunct(K, T)`, or
  - `mutual_aspect(K, T)`, or
  - exchange: `house_of(K) == (house governed by T)` **and** `house_of(T) == (house governed by K)`.
  (Because the 1st is both a kendra and a trikona, its lord participating with a
  9th/5th or 4th/7th/10th lord is a valid, common Raja yoga.)
- **Effect:** Elevates status, authority, and success; a signature of achievement and
  recognition, activated in the dasha of the yoga-forming planets.
- **Source:** BPHS "Raja yoga adhyaya"; Phaladeepika ch. 7. **Confidence: HIGH.**

### 2.7 Neecha Bhanga Raja yoga (नीचभंग राज योग) — cancellation of debilitation
Let `P` be a **debilitated** planet (sign == its debilitation sign, §2.9). Let
`DispDeb = lord_of_sign( debilitation_sign(P) )` (dispositor of the debilitated planet)
and `ExaltRuler = the planet exalted in that same sign`. Declare NBRY if **any** of
the common, checkable conditions hold:

1. **Dispositor in kendra:** `house_of(DispDeb) ∈ {1,4,7,10}` from lagna
   (**or** kendra from the Moon — optional).
2. **Exalt-ruler in kendra:** `house_of(ExaltRuler) ∈ {1,4,7,10}` from lagna (or Moon).
3. **Aspect by dispositor or exalt-ruler:** `aspects(DispDeb, P)` or `aspects(ExaltRuler, P)`.
4. **Mutual kendra of the two rulers:** `house_from(DispDeb, ExaltRuler) ∈ {1,4,7,10}`.
5. **Exalted in navamsa:** `P.navamsa == exaltation_sign(P)` (or `P` is vargottama —
   same sign in D1 and D9). *(This is the strongest single cancellation.)*

- **Effect:** A debilitated planet's weakness is neutralised — and can convert to
  notable rise and success — when the cancellation is strong; frame the native's
  early limitation transforming into later strength.
- **Source:** BPHS; Phaladeepika 3; modern: cancellation set per Mantreswara/PVR Rao.
  **Confidence: HIGH** that these are the recognised rules; exactly *which* apply in a
  chart and the resulting strength is MEDIUM — present as "supportive" not guaranteed.

### 2.8 Vipreet (Viparita) Raja yoga (विपरीत राज योग) — reversal of misfortune
Let `L6, L8, L12 = lords of houses 6, 8, 12`.
- **Condition:** a dusthana lord occupies a dusthana. Named sub-yogas:
  - **Harsha (हर्ष):** `house_of(L6) ∈ {6,8,12}`.
  - **Sarala (सरल):** `house_of(L8) ∈ {6,8,12}`.
  - **Vimala (विमल):** `house_of(L12) ∈ {6,8,12}`.
  (Classically strongest when the lord is in another dusthana than its own and not
  tightly tied to benefic kendra/trikona lords.)
- **Effect:** Adversity turns to advantage — obstacles, rivals, or losses ultimately
  produce gain, resilience, and unexpected rise.
- **Source:** BPHS; Phaladeepika. **Confidence: HIGH** (formation); interpretive
  strength MEDIUM.

### 2.9 Exaltation / Debilitation / Own-sign reference table (canonical engine data)

| Graha | Own sign(s) | Mulatrikona (sign · arc) | Exaltation (sign · deep degree) | Debilitation (sign) |
| --- | --- | --- | --- | --- |
| **Sun** | Simha | Simha 0°–20° | **Mesha** · 10° | Tula |
| **Moon** | Karka | Vrishabha 3°–30° | **Vrishabha** · 3° | Vrischika |
| **Mars** | Mesha, Vrischika | Mesha 0°–12° | **Makara** · 28° | Karka |
| **Mercury** | Mithuna, Kanya | Kanya 15°–20° | **Kanya** · 15° | Meena |
| **Jupiter** | Dhanu, Meena | Dhanu 0°–10° | **Karka** · 5° | Makara |
| **Venus** | Vrishabha, Tula | Tula 0°–15° | **Meena** · 27° | Kanya |
| **Saturn** | Makara, Kumbha | Kumbha 0°–20° | **Tula** · 20° | Mesha |
| **Rahu** | — (no rulership) | — | **Vrishabha** (some: Mithuna) | Vrischika (some: Dhanu) |
| **Ketu** | — (no rulership) | — | **Vrischika** (some: Dhanu) | Vrishabha (some: Mithuna) |

**Rahu/Ketu handling.** The nodes are shadow points with **no sign rulership**; they
never "own" or lord a house for lordship-based yogas — always use the sign's classical
ruler (e.g. use Mars for Vrischika even if Rahu sits there). Their exaltation/
debilitation signs are **not universally agreed**: the table gives the most common
assignment (Rahu exalts in Vrishabha, debilitates in Vrischika; Ketu opposite) with
the widely-cited alternative in parentheses (Rahu exalt Mithuna / debil Dhanu).
**Mark all node dignity as MEDIUM confidence** and prefer to *not* trigger
Mahapurusha/own-sign yogas from nodes.

*Sources: BPHS "Graha-uccha-neecha"; Phaladeepika 1.9–1.12; Saravali. Exaltation
signs & deep degrees are **HIGH** confidence for the seven planets and near-universal;
mulatrikona arcs HIGH; nodal dignities MEDIUM.*

### 2.10 Kemadruma yoga (केमद्रुम) — Moon isolation (place LAST: many cancellations)
- **Condition (formation):** the Moon is "unsupported":
  1. **No planet in 2nd or 12th from the Moon** — i.e. for all planets `X` in
     {Mars, Mercury, Jupiter, Venus, Saturn} (classically **excluding the Sun** and
     usually excluding **Rahu/Ketu**), `house_from(X, Moon) ∉ {2, 12}`; **and**
  2. **No planet conjunct the Moon** (`house_from(X, Moon) != 1`); **and**
  3. (stricter variant) **no planet in a kendra from the Moon**
     (`house_from(X, Moon) ∉ {1,4,7,10}`).
  Use conditions 1–2 as the core definition; treat 3 as the strict form. *Confidence
  on scope of "planets counted" is MEDIUM — document the choice (recommend excluding
  Sun + nodes).*
- **Effect (if uncancelled):** Can indicate emotional isolation, fluctuating support,
  or ups-and-downs of fortune; frame gently as a call to build stable inner and social
  foundations — **never** as inevitable hardship.
- **Cancellations (Kemadruma Bhanga) — declare cancelled if ANY hold:**
  - a planet occupies a **kendra from the Moon** (`house_from(X, Moon) ∈ {4,7,10}`), or
  - a planet occupies a **kendra from the lagna** while related to the Moon, or
  - the Moon is **conjunct or aspected by a benefic** (Jupiter/Venus; §0.4), or
  - the Moon is in **own sign/exaltation** (Karka/Vrishabha) or **vargottama**, or
  - **all planets aspect the Moon** (rare), or the Moon is in a kendra from lagna.
  A cancelled Kemadruma should **not** be reported as a negative yoga.
- **Source:** BPHS "Chandra yoga"; Phaladeepika; Saravali (cancellations). **Confidence:
  HIGH** for the isolation principle; MEDIUM for the exact planet-set and cancellation
  list — err toward cancellation and gentle phrasing.

### 2.11 Implementation notes for the yoga engine
- Compute all lordships from `lagna_rashi` + §2.9 SIGN_LORD; compute all "from Moon"
  offsets with `house_from(X, Moon)`.
- Evaluate yogas as pure booleans returning `{present, participants, strength_hint,
  confidence}`; keep effect text in `i18n`/`knowledge_base` keyed by yoga id.
- **Strength hint** (optional): raise it when participants are dignified (own/exalt,
  kendra/trikona), lower it when combust, debilitated (and uncancelled), or in
  dusthana. Do not let a low hint delete the yoga — it modulates wording only.
- **De-duplicate & prioritise for display:** cap the report to the top N yogas by
  (weight × strength); always surface Mahapurusha, Raja, and Dhana yogas first, then
  Gaja Kesari / Budha-Aditya / Chandra-Mangala, then Vipreet/NBRY, then Kemadruma
  (only if uncancelled).
- **Never fabricate.** If data is insufficient (e.g. unknown gender for gendered
  karaka), fall back to the gender-neutral rule and tag confidence.

---

## 3. Report presentation best practices

Survey of how highly-rated Vedic report products (e.g. AstroSage, Astro-Vision/
LifeSign, GaneshaSpeaks, Cafe Astrology's Vedic reports, and premium astrologer PDFs)
structure a premium reading, distilled into a concrete section order. Common
threads: a clean birth-details header, a factual chart snapshot before interpretation,
a **dasha timeline with the current period highlighted**, dimension-by-dimension life
readings, a yogas section, remedies tied to specific planets, and a clear disclaimer.

### 3.1 Recommended section ORDER and contents

1. **Cover / Birth-details header.** Name, date, exact time, place (lat/lon), timezone,
   ayanamsa used (Lahiri), and the report generation date. Establishes trust and
   reproducibility. *(App already has all of this in `Native` + `Chart`.)*
2. **Chart snapshot (facts before interpretation).**
   - **Rashi/Nakshatra summary:** Lagna (ascendant) sign, Moon sign (Rashi), and
     birth Nakshatra + pada, with one-line meanings.
   - **Planetary table:** each graha → sign, degrees (`format_dms`), house, nakshatra+
     pada, navamsa sign, retrograde flag, and dignity tag (exalted/own/debilitated).
   - **Bhava (house) table:** house → sign → house lord → planets tenanting it.
   - Optional: North/South-Indian chart diagram (South-Indian layout data already in
     `constants.py`).
3. **Vimsottari Dasha timeline.** The full Maha ladder with dates; **the currently
   running Maha→Antar (→Pratyantar) clearly highlighted**, plus a short "what this
   period emphasises" line from `DASHA_KB`. This is the most-valued dynamic section —
   put it early and make "where am I now" obvious.
4. **Personality & temperament** (dimension §1.1).
5. **Career & profession** (§1.2).
6. **Finance & wealth** (§1.3).
7. **Education & intellect** (§1.4).
8. **Romance, marriage & relationships** (§1.5).
9. **Health & vitality** (§1.6).
   *(Each dimension section: 1 strength paragraph + 1 challenge/growth paragraph +
   a "timing" note tied to the current or upcoming dasha.)*
10. **Yogas in your chart.** Only yogas detected as present (§2), ordered by weight;
    each with a plain-language name, one-line effect, and (optionally) the timing
    dasha. Cancelled/negated yogas either omitted or shown as "neutralised."
11. **Remedies (upaya).** Grouped by the relevant planet, drawn from `GRAHA_KB`
    remedies: gemstone (with a "consult before wearing" caveat), mantra, charity
    (daana), and lifestyle/behaviour. Tie each remedy to the planet driving the
    relevant dimension or affliction. Keep practical and optional.
12. **Summary / key takeaways.** 3–5 empowering bullets.
13. **Disclaimer.** Educational/cultural guidance; not a substitute for medical,
    legal, or financial advice; outcomes depend on effort and free will.

### 3.2 Tone & style rules (apply to every generated line)
- **Empowering & specific:** name the actual planet/house/sign driving each statement;
  avoid vague fortune-cookie lines.
- **Non-deterministic:** "supports / favours / a period to…"; never "you will."
  Free-will framing throughout.
- **Balanced:** pair each challenge with a constructive lever and, where relevant, a
  remedy tied to the responsible planet.
- **Safe boundaries:** no medical diagnoses/prognoses, no death/lifespan predictions,
  no guaranteed money amounts, no "your marriage will fail." Reframe classical
  "doshas" as patterns to manage.
- **Remedies as options:** present gemstone/mantra/charity/lifestyle as traditional,
  optional practices — recommend consulting a qualified astrologer before gemstones.

---

## 4. Trilingual note (English / Hindi / Telugu)

Canonical terms for the six dimensions, the dasha/yoga/remedy vocabulary, and the
common yoga names. (App language codes: `en`, `hi`, `te`.)

### 4.1 Life dimensions

| Dimension (en) | Hindi (hi) | Telugu (te) |
| --- | --- | --- |
| Personality & temperament | व्यक्तित्व / स्वभाव | వ్యక్తిత్వం / స్వభావం |
| Career & profession | करियर / व्यवसाय | వృత్తి / ఉద్యోగం |
| Finance & wealth | धन / संपत्ति | ధనం / సంపద |
| Education & intellect | शिक्षा / बुद्धि | విద్య / బుద్ధి |
| Romance, marriage & relationships | प्रेम / विवाह / संबंध | ప్రేమ / వివాహం / సంబంధాలు |
| Health & vitality | स्वास्थ्य / जीवनशक्ति | ఆరోగ్యం / ప్రాణశక్తి |

### 4.2 Core vocabulary

| Term (en) | Hindi (hi) | Telugu (te) |
| --- | --- | --- |
| Mahadasha | महादशा | మహాదశ |
| Antardasha | अंतर्दशा (भुक्ति) | అంతర్దశ (భుక్తి) |
| Yoga | योग | యోగం |
| Remedies (upaya) | उपाय | పరిహారాలు / ఉపాయాలు |
| Ascendant (Lagna) | लग्न | లగ్నం |
| Sign (Rashi) | राशि | రాశి |
| Nakshatra | नक्षत्र | నక్షత్రం |
| House (Bhava) | भाव / घर | భావం / గృహం |
| Planet (Graha) | ग्रह | గ్రహం |

### 4.3 Yoga names (where a common Hindi/Telugu term exists)

| Yoga (en/Sanskrit) | Hindi (hi) | Telugu (te) |
| --- | --- | --- |
| Raja yoga | राज योग | రాజ యోగం |
| Dhana yoga | धन योग | ధన యోగం |
| Gaja Kesari yoga | गजकेसरी योग | గజకేసరి యోగం |
| Budha-Aditya yoga | बुध-आदित्य योग | బుధ-ఆదిత్య యోగం |
| Chandra-Mangala yoga | चन्द्र-मंगल योग | చంద్ర-మంగళ యోగం |
| Pancha Mahapurusha yoga | पंच महापुरुष योग | పంచ మహాపురుష యోగం |
| — Ruchaka | रुचक योग | రుచక యోగం |
| — Bhadra | भद्र योग | భద్ర యోగం |
| — Hamsa | हंस योग | హంస యోగం |
| — Malavya | मालव्य योग | మాలవ్య యోగం |
| — Sasa/Shasha | शश योग | శశ యోగం |
| Neecha Bhanga Raja yoga | नीचभंग राज योग | నీచభంగ రాజ యోగం |
| Vipreet Raja yoga | विपरीत राज योग | విపరీత రాజ యోగం |
| Kemadruma yoga | केमद्रुम योग | కేమద్రుమ యోగం |

*Note: yoga names are Sanskrit and are typically transliterated (not translated) in
Hindi and Telugu; the columns give the standard Devanagari and Telugu-script
transliterations. Confidence: HIGH for the well-known yogas above; MEDIUM only on
minor spelling variants.*

---

## 5. Sources & confidence summary

**Classical (primary):** Brihat Parashara Hora Shastra (BPHS); Phaladeepika
(Mantreswara); Saravali (Kalyana Varma); Brihat Jataka (Varahamihira); Jaimini Sutras
(for chara karakas). **Modern (corroboration/wording):** K.N. Rao, P.V.R. Narasimha
Rao, and widely-used references (AstroSage, Drik Panchang) — used only where consistent
with the classics. See `docs/SOURCES.md` for the existing knowledge-base bibliography.

| Area | Confidence | Note |
| --- | --- | --- |
| House classes, karakas, house significations | HIGH | Universal classical assignment. |
| Aspect rules (7th all; Mars 4/7/8; Jup 5/7/9; Sat 3/7/10) | HIGH | Standard graha drishti; nodal aspects MEDIUM. |
| Exalt/debil/own/mulatrikona (7 planets) | HIGH | Near-universal; deep degrees standard. |
| Rahu/Ketu dignity | MEDIUM | Not universally agreed; alternatives noted; no lordship. |
| Pancha Mahapurusha, Gaja Kesari, Budha-Aditya, Chandra-Mangala | HIGH | Formation rules well-attested. |
| Dhana / Raja yoga variants | HIGH (principle) / MEDIUM (weighting) | Lord-linkage principle solid; strength is chart-specific. |
| Neecha Bhanga & Vipreet Raja yoga | HIGH (rules) / MEDIUM (outcome) | Recognised cancellation/reversal sets; strength varies. |
| Kemadruma & cancellations | HIGH (principle) / MEDIUM (scope) | Planet-set & cancellation list vary by author; err to cancellation. |
| Jaimini chara karakas (AK/AmK/DK) | HIGH (method) / MEDIUM (scheme) | 7- vs 8-karaka choice noted. |
| Interpretive/effect wording | Editorial paraphrase | Non-fatalistic, display-safe summaries grounded in the above. |

**Overarching disclaimer for display:** This reading is for educational and cultural
guidance. Vedic astrology describes tendencies and timing, not fixed outcomes; results
depend on effort and free will. It is not a substitute for professional medical, legal,
or financial advice.
