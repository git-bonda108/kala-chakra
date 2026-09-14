"""Kala Chakra — Streamlit Vedic Horoscope Studio.

Anyone enters name, DOB, TOB and place (or uploads an existing horoscope). The
deterministic engine computes rashi / nakshatra / lagna / dasha and detects
classical yogas; the specialist narrator reads each life dimension — personality,
career, finance, education, romance, health — plus the dasha timeline. Output is
rich, cross-checks any uploaded document, and exports to a PDF in en / hi / te.
"""

from __future__ import annotations

import calendar
import os
from datetime import date, datetime, time

import streamlit as st

from kala.analysis import planet_strength
from kala.chart import Native, chart_dasha_at, compute_chart, format_dms
from kala.config import get_settings
from kala.constants import (
    SOUTH_INDIAN_CELLS,
    graha_name,
    nakshatra_name,
    rashi_name,
)
from kala.geo import CITY_NAMES, resolve_city, tz_offset_for
from kala.i18n import LANGS, t
from kala.feedback import record_feedback, summary as feedback_summary
from kala.orchestration import run_orchestration
from kala.parsing import parse_upload, source_from_chart
from kala.pdf_report import build_pdf
from kala.validators import cross_validate
from kala.vimsottari import antardasha_ladder


def load_eval_report():
    import json
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval", "report.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return None
    return None


st.set_page_config(page_title="Kala Chakra", page_icon="🕉️", layout="wide")

SETTINGS = get_settings()
# Secrets come from the environment ONLY — never from the UI.
api_key = SETTINGS.openai_api_key or None

# ---- Sidebar: language + engine status ------------------------------------
with st.sidebar:
    st.markdown("### 🕉️ Kala Chakra")
    lang = st.selectbox(
        "Language / भाषा / భాష",
        options=list(LANGS.keys()),
        format_func=lambda k: LANGS[k],
        index=0,
    )
    st.divider()
    if SETTINGS.live_agents:
        st.success(f"{t('engine_mode', lang)}: {t('openai_live', lang)}")
        st.caption(f"model: {SETTINGS.agents_model}")
    else:
        st.info(f"{t('engine_mode', lang)}: {t('local_engine', lang)}")
        st.caption(t("key_hint", lang))
    st.divider()
    st.caption(t("footer_rule", lang))

st.title(t("title", lang))
st.write(t("tagline", lang))

# ---- Input form ------------------------------------------------------------
with st.form("birth"):
    st.subheader(t("birth_details", lang))
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input(t("name", lang), value="")
        st.markdown(f"**{t('dob', lang)}**")
        _years = list(range(date.today().year, 1899, -1))  # today … 1900, no cap
        dcol_y, dcol_m, dcol_d = st.columns(3)
        with dcol_y:
            byear = st.selectbox(t("year", lang), _years, index=_years.index(1990))
        with dcol_m:
            bmonth = st.selectbox(t("month", lang), list(range(1, 13)), index=0)
        with dcol_d:
            _max_day = calendar.monthrange(int(byear), int(bmonth))[1]
            bday = st.selectbox(t("day", lang), list(range(1, _max_day + 1)), index=0)
        dob = date(int(byear), int(bmonth), int(bday))
        unknown_time = st.checkbox(t("unknown_time", lang), value=False)
        tob = st.time_input(t("tob", lang), value=time(6, 0), disabled=unknown_time)
    with c2:
        place_mode = st.radio(
            t("place", lang),
            [t("city", lang), t("manual_coords", lang)],
            horizontal=True,
        )
        if place_mode == t("city", lang):
            city = st.selectbox(t("city", lang), CITY_NAMES, index=CITY_NAMES.index("Hyderabad, India"))
            lat = lon = tz = None
            place_label = city
        else:
            city = None
            lat = st.number_input(t("lat", lang), value=17.3850, format="%.4f")
            lon = st.number_input(t("lon", lang), value=78.4867, format="%.4f")
            tz = st.number_input(t("tz", lang), value=5.5, step=0.5, format="%.2f")
            place_label = f"{lat:.3f}, {lon:.3f}"

    st.subheader(t("uploads", lang))
    st.caption(t("uploads_help", lang))
    uploads = st.file_uploader(
        t("uploads", lang),
        type=["pdf", "png", "jpg", "jpeg", "webp", "txt", "md", "csv"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button(t("generate", lang), type="primary", use_container_width=True)

# ---- Compute ---------------------------------------------------------------
if submitted:
    if not name.strip():
        name = "—"
    birth_time = time(6, 0) if unknown_time else tob
    birth_dt = datetime(dob.year, dob.month, dob.day, birth_time.hour, birth_time.minute)

    if place_mode == t("city", lang):
        loc = resolve_city(city, birth_dt)
        lat, lon, tz = loc.lat, loc.lon, loc.tz_offset_hours
        place_label = f"{city} ({loc.tz_name})"
    else:
        _, tzname = tz_offset_for(lat, lon, birth_dt)

    native = Native(
        name=name.strip(),
        date=dob.isoformat(),
        time=birth_time.strftime("%H:%M:%S"),
        tz_offset_hours=float(tz),
        lat=float(lat),
        lon=float(lon),
        place=place_label,
    )

    with st.spinner(t("computing", lang)):
        chart = compute_chart(native)
        epoch_iso = date.today().isoformat()

        validation = None
        parsed_labels = []
        if uploads:
            computed_src = source_from_chart(chart)
            for up in uploads:
                src = parse_upload(up.name, up.getvalue(), api_key or None)
                parsed_labels.append((src.label, src))
            doc_src = next((s for _, s in parsed_labels if s.periods), None)
            if doc_src is not None:
                validation = cross_validate(computed_src, doc_src)

        result = run_orchestration(chart, epoch_iso, lang, validation, api_key or None)

    st.session_state["chart"] = chart
    st.session_state["epoch"] = epoch_iso
    st.session_state["validation"] = validation
    st.session_state["parsed"] = parsed_labels
    st.session_state["results_by_lang"] = {lang: result}


# ---- Render helpers --------------------------------------------------------
def _south_indian_chart(chart, rlang: str) -> str:
    by_rashi = {}
    for p in chart.placements:
        by_rashi.setdefault(p.rashi, []).append(graha_name(p.graha, rlang))
    grid = "<table style='border-collapse:collapse;width:380px;font-size:13px'>"
    for row in SOUTH_INDIAN_CELLS:
        grid += "<tr>"
        for cell in row:
            if cell is None:
                grid += "<td style='border:1px solid #b45; height:74px; background:#faf3e0'></td>"
            else:
                marks = "<br>".join(by_rashi.get(cell, []))
                lag = " ⬅" if cell == chart.lagna_rashi else ""
                grid += (
                    "<td style='border:1px solid #b45; height:74px; width:92px; vertical-align:top; "
                    "padding:3px; background:#fffdf6'>"
                    f"<div style='font-size:10px;color:#b45'>{rashi_name(cell, rlang)}{lag}</div>"
                    f"<div style='color:#1d3a73'>{marks}</div></td>"
                )
        grid += "</tr>"
    return grid + "</table>"


# ---- Render ----------------------------------------------------------------
chart = st.session_state.get("chart")

if not chart:
    st.info(t("no_result", lang))
else:
    rlang = lang
    epoch_iso = st.session_state["epoch"]
    results_by_lang = st.session_state.setdefault("results_by_lang", {})
    if rlang not in results_by_lang:
        with st.spinner(t("computing", rlang)):
            results_by_lang[rlang] = run_orchestration(
                chart, epoch_iso, rlang, st.session_state.get("validation"), api_key or None
            )
    result = results_by_lang[rlang]
    hit = chart_dasha_at(chart, epoch_iso)

    # ---- Header metrics ----
    st.header(t("summary", rlang))
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t("moon", rlang), rashi_name(chart.rashi, rlang), format_dms(chart.moon_sidereal))
    m2.metric(t("nakshatra", rlang), nakshatra_name(chart.nakshatra, rlang), f"pada {chart.pada}")
    m3.metric(t("lagna", rlang), rashi_name(chart.lagna_rashi, rlang))
    if hit and hit["mahadasha"]:
        md = hit["mahadasha"]
        sub = graha_name(hit["antardasha"].lord, rlang) if hit["antardasha"] else ""
        m4.metric(t("current_period", rlang), f"{graha_name(md.lord, rlang)} / {sub}", f"{md.start} → {md.end}")

    tab_read, tab_chart = st.tabs([f"📜 {t('reading_tab', rlang)}", f"🗺️ {t('chart_tab', rlang)}"])

    # ---------------- Life Reading tab ----------------
    with tab_read:
        st.subheader(t("predictions", rlang))
        for sec in result.sections:
            with st.container(border=True):
                st.markdown(f"**{sec.title}**")
                st.write(sec.body)

        st.subheader(f"✨ {t('yogas', rlang)}")
        if result.yogas:
            for yname, yeff in result.yogas:
                with st.container(border=True):
                    st.markdown(f"**{yname}**")
                    st.write(yeff)
        else:
            st.caption(t("no_yogas", rlang))

        if result.remedies:
            st.subheader(t("remedies", rlang))
            for r in result.remedies:
                st.markdown(f"- {r}")

        st.caption(f"{t('engine_mode', rlang)}: {result.mode}")

        if result.validation:
            st.subheader(t("validation", rlang))
            v = result.validation
            if v.status == "CONSISTENT":
                st.success(f"{t('consistent', rlang)} — {v.message}")
            elif v.status == "CONFLICT":
                st.warning(f"{t('conflict', rlang)} — {v.message}")
                if v.candidates:
                    st.write("Candidates: " + " · ".join(v.candidates))
            else:
                st.info(v.message)
            with st.expander("Details"):
                for d in v.details:
                    st.write("—", d)
        parsed = st.session_state.get("parsed") or []
        if parsed:
            with st.expander(f"Parsed documents ({len(parsed)})"):
                for label, src in parsed:
                    st.markdown(f"**{label}** — confidence {src.confidence}")
                    if src.periods:
                        st.write({"periods": [f"{p.level}:{p.lord} {p.start}–{p.end}" for p in src.periods]})
                    if src.illegible:
                        st.caption("Not read (not guessed): " + "; ".join(src.illegible))

    # ---------------- Chart & Tables tab ----------------
    with tab_chart:
        left, right = st.columns([1, 1])
        with left:
            st.subheader(t("grahas", rlang))
            st.dataframe(
                {
                    t("graha", rlang): [graha_name(p.graha, rlang) + (" (R)" if p.retrograde else "") for p in chart.placements],
                    t("degree", rlang): [format_dms(p.sidereal) for p in chart.placements],
                    t("house", rlang): [p.house for p in chart.placements],
                    "Rashi": [rashi_name(p.rashi, rlang) for p in chart.placements],
                    t("nakshatra", rlang): [f"{nakshatra_name(p.nakshatra, rlang)} {p.pada}" for p in chart.placements],
                    t("d9", rlang): [rashi_name(p.navamsa, rlang) for p in chart.placements],
                },
                hide_index=True,
                use_container_width=True,
            )
            st.subheader(t("planet_report", rlang))
            strengths = [planet_strength(chart, p.graha) for p in chart.placements]
            st.dataframe(
                {
                    t("graha", rlang): [graha_name(s.graha, rlang) for s in strengths],
                    t("strength", rlang): [f"{s.score}/10" for s in strengths],
                    "": [{"strong": "🟢", "moderate": "🟡", "weak": "🔴"}[s.label] for s in strengths],
                    "Dignity": [s.dignity for s in strengths],
                },
                hide_index=True,
                use_container_width=True,
            )
        with right:
            st.subheader(t("mahadasha", rlang))
            st.dataframe(
                {
                    t("graha", rlang): [graha_name(s.lord, rlang) for s in chart.ladder],
                    "Start": [s.start for s in chart.ladder],
                    "End": [s.end for s in chart.ladder],
                    "Y-M-D": [s.duration.as_str() for s in chart.ladder],
                },
                hide_index=True,
                use_container_width=True,
            )
            if hit and hit["mahadasha"]:
                st.subheader(f"{t('antardasha', rlang)} · {graha_name(hit['mahadasha'].lord, rlang)}")
                ad_ladder = antardasha_ladder(hit["mahadasha"])
                cur_ad = hit["antardasha"].lord if hit["antardasha"] else None
                st.dataframe(
                    {
                        t("graha", rlang): [("▶ " if s.lord == cur_ad else "") + graha_name(s.lord, rlang) for s in ad_ladder],
                        "Start": [s.start for s in ad_ladder],
                        "End": [s.end for s in ad_ladder],
                    },
                    hide_index=True,
                    use_container_width=True,
                )

        st.subheader("Rasi Chakra (D1)")
        st.markdown(_south_indian_chart(chart, rlang), unsafe_allow_html=True)

    # ---- PDF export ----
    st.divider()
    st.header(t("download_pdf", rlang))
    pdf_lang = st.selectbox(
        t("pdf_lang", rlang),
        options=list(LANGS.keys()),
        format_func=lambda k: LANGS[k],
        index=list(LANGS.keys()).index(rlang),
    )
    if st.button(t("download_pdf", rlang) + " →"):
        pdf_result = result
        if pdf_lang != rlang:
            pdf_result = run_orchestration(chart, epoch_iso, pdf_lang, result.validation, api_key or None)
        pdf_bytes = build_pdf(chart, pdf_result, epoch_iso, pdf_lang)
        st.download_button(
            label=f"⬇ {chart.native.name or 'horoscope'}.pdf",
            data=pdf_bytes,
            file_name=f"kala_chakra_{(chart.native.name or 'horoscope').replace(' ', '_')}_{pdf_lang}.pdf",
            mime="application/pdf",
        )

    # ---- Feedback (learning loop) ----
    st.divider()
    st.subheader(t("feedback", rlang))
    fb1, fb2, _ = st.columns([1, 1, 6])
    if fb1.button("👍", key="fb_up"):
        record_feedback({"rating": "up", "name": chart.native.name, "lang": rlang, "mode": result.mode})
        st.success(t("feedback_thanks", rlang))
    if fb2.button("👎", key="fb_down"):
        record_feedback({"rating": "down", "name": chart.native.name, "lang": rlang, "mode": result.mode})
        st.success(t("feedback_thanks", rlang))

# ---- Accuracy & evaluation (always available) ------------------------------
with st.expander(f"🎯 {t('accuracy', lang)}"):
    report = load_eval_report()
    if report:
        st.metric("Golden accuracy", f"{report['accuracy'] * 100:.1f}%",
                  f"{report['passed']}/{report['total_checks']} checks")
        for case in report["cases"]:
            icon = "✅" if case["pass"] else "❌"
            st.markdown(f"{icon} **{case['id']}** ({case['kind']})")
            fails = [c for c in case["checks"] if not c["pass"]]
            for c in fails:
                st.caption(f"✗ {c['check']}: got {c['got']} want {c['want']}")
        st.caption("Run `python3 -m eval.harness` to refresh. External case GR-001 is verified against the handover; others are regression snapshots.")
    else:
        st.caption("No eval report yet. Run `python3 -m eval.harness`.")
    fb = feedback_summary()
    if fb["total"]:
        st.caption(f"User feedback: {fb['up']}👍 / {fb['down']}👎"
                   + (f" · satisfaction {fb['satisfaction'] * 100:.0f}%" if fb["satisfaction"] is not None else ""))

st.divider()
st.caption(t("footer_rule", lang))
