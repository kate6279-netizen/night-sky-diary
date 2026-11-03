"""감정의 궤적: 색으로 보는 월간 감정 달력.

프론트엔드 전용 페이지입니다. 기존 AI 모델과 DB 저장 구조는 바꾸지 않고
현재 닉네임의 저장된 기록을 읽어서 날짜별 감정을 표시합니다.
"""
from __future__ import annotations

import calendar
import datetime as dt
import html
from collections import Counter

import streamlit as st

import analysis
import db

_COLORS = ("#ffcf4a", "#ff8fb1", "#6fd3a8", "#9aa6b8", "#5b84f0", "#b08cf0", "#f0645a")
_WEEKDAYS = ("월", "화", "수", "목", "금", "토", "일")


def _month_options(today: dt.date, entries: list[dict]) -> list[str]:
    """최근 12개월 및 실제 데이터가 있는 월만 표시합니다."""
    months = set()
    for offset in range(12):
        total = today.year * 12 + today.month - 1 - offset
        y, m0 = divmod(total, 12)
        months.add(f"{y:04d}-{m0+1:02d}")
    for entry in entries:
        date = str(entry.get("date", ""))
        try:
            parsed = dt.date.fromisoformat(date)
        except ValueError:
            continue
        months.add(parsed.strftime("%Y-%m"))
    return sorted(months, reverse=True)


def _emotion_of(entry: dict) -> tuple[int, list[float]]:
    """기존 분석 함수로 사용자가 고친 감정도 반영합니다."""
    weights = [float(x) for x in analysis.effective(entry)]
    return max(range(len(weights)), key=weights.__getitem__), weights


def _color_styles(year: int, month: int, by_date: dict[str, dict], selected: str) -> str:
    """선택된 달의 버튼만 꾸밉니다."""
    css = [
        "<style>",
        ".emo-calendar-weekdays{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:6px;text-align:center;margin:5px 0 12px}.emo-calendar-weekdays span{font-size:12px;color:#b2b8df;font-weight:700}",
        "div[data-testid='stHorizontalBlock']:has([class*='st-key-emo_cal_']){flex-wrap:nowrap!important;gap:6px!important;align-items:stretch!important}",
        "div[data-testid='stHorizontalBlock']:has([class*='st-key-emo_cal_']) [data-testid='stColumn']{flex:1 1 0!important;width:0!important;min-width:0!important}",
        "[class*='st-key-emo_cal_'] button{min-height:67px!important;border-radius:13px!important;font-size:15px!important;font-weight:700!important;transition:transform .15s,border-color .15s!important;}",
        "[class*='st-key-emo_cal_'] button:enabled:hover{transform:translateY(-2px)!important;}",
        "[class*='st-key-emo_cal_'] button:disabled{opacity:1!important;background:#15192f!important;color:#9da7cd!important;border:1px solid rgba(145,155,225,.2)!important;}",
        "@media(max-width:680px){[class*='st-key-emo_cal_'] button{min-height:43px!important;padding:4px 1px!important;font-size:11px!important;border-radius:9px!important;}}",
    ]
    for date, entry in by_date.items():
        if not date.startswith(f"{year:04d}-{month:02d}-"):
            continue
        idx, _ = _emotion_of(entry)
        color = _COLORS[idx]
        key = f"st-key-emo_cal_{date.replace('-', '')}"
        border = "cc" if date == selected else "77"
        bg = f"linear-gradient(145deg,{color}43,{color}12 55%,#10152c)"
        glow = f"box-shadow:0 0 0 1px {color}88,0 0 18px {color}30!important;" if date == selected else ""
        css.append(f"div.{key} button{{background:{bg}!important;border:1px solid {color}{border}!important;color:#fff!important;{glow}}}")
    css.append("</style>")
    return "".join(css)


def page_calendar(on_edit=None) -> None:
    """메뉴에서 실행하는 새 달력 페이지."""
    nick = st.session_state.get("nickname", "")
    st.markdown('<div class="head"><h1>감정 달력 <small>EMOTION CALENDAR</small></h1><p>하루의 마음이 색으로 남아, 한 달의 별자리가 되어 가요.</p></div>', unsafe_allow_html=True)
    if not nick:
        st.info("먼저 왼쪽 메뉴의 '홈'에서 내 우주 이름을 입력해 주세요.")
        return

    entries = db.load_entries(nick)
    by_date = {str(e["date"]): e for e in entries}
    today = dt.date.today()
    options = _month_options(today, entries)
    ym = st.selectbox("확인할 달", options, index=0, key="emotion_calendar_ym",
                      format_func=lambda x: f"{x[:4]}년 {int(x[5:])}월")
    year, month = map(int, ym.split("-"))
    n_days = calendar.monthrange(year, month)[1]
    month_rows = [e for e in entries if str(e["date"]).startswith(ym)]
    emotions = [analysis.EMO[_emotion_of(e)[0]] for e in month_rows]
    top = Counter(emotions).most_common(1)[0][0] if emotions else None
    count_text = f"{len(month_rows)} / {n_days}일"
    top_text = top or "아직 없어요"
    progress = round(len(month_rows) / n_days * 100)
    st.markdown(
        '<div style="display:flex;flex-wrap:wrap;gap:12px;margin:10px 0 22px">'
        f'<div style="flex:1;min-width:150px;padding:15px 18px;border:1px solid #343658;border-radius:15px;background:#151a35"><span style="color:#aeb4df;font-size:12px">이번 달 기록</span><div style="font-size:24px;font-weight:800;color:#f5f1ff">{count_text}</div></div>'
        f'<div style="flex:1;min-width:150px;padding:15px 18px;border:1px solid #343658;border-radius:15px;background:#151a35"><span style="color:#aeb4df;font-size:12px">가장 많이 나온 감정</span><div style="font-size:24px;font-weight:800;color:#f5f1ff">{html.escape(top_text)}</div></div>'
        f'<div style="flex:1;min-width:150px;padding:15px 18px;border:1px solid #343658;border-radius:15px;background:#151a35"><span style="color:#aeb4df;font-size:12px">한 달의 기록률</span><div style="font-size:24px;font-weight:800;color:#f5f1ff">{progress}%</div></div>'
        '</div>', unsafe_allow_html=True)
    legend = "　".join(
        f'<span style="white-space:nowrap;color:{color}">✦ <span style="color:#cdd2f2">{html.escape(emo)}</span></span>'
        for emo, color in zip(analysis.EMO, _COLORS)
    )
    st.markdown(f'<div style="font-size:13px;line-height:2.4;margin-bottom:10px">{legend}</div>', unsafe_allow_html=True)

    selected = st.session_state.get("emotion_calendar_selected", "")
    if selected not in by_date or not selected.startswith(ym):
        selected = max((str(e["date"]) for e in month_rows), default="")
    st.markdown(_color_styles(year, month, by_date, selected), unsafe_allow_html=True)

    st.markdown('<div class="emo-calendar-weekdays">' + ''.join(f'<span>{day}</span>' for day in _WEEKDAYS) + '</div>', unsafe_allow_html=True)

    for week in calendar.monthcalendar(year, month):
        cols = st.columns(7, gap="small")
        for weekday, d in enumerate(week):
            if not d:
                cols[weekday].markdown('<div style="height:48px"></div>', unsafe_allow_html=True)
                continue
            date_key = f"{ym}-{d:02d}"
            entry = by_date.get(date_key)
            if entry:
                idx, _ = _emotion_of(entry)
                mood = analysis.EMO[idx]
                label = f"✦ {d}"
                tooltip = f"{d}일 · {mood} · 클릭해서 기록 보기"
            else:
                label = str(d)
                tooltip = f"{d}일 · 기록 없음"
            with cols[weekday]:
                if st.button(label, key=f"emo_cal_{date_key.replace('-', '')}",
                             use_container_width=True, disabled=not bool(entry), help=tooltip):
                    st.session_state["emotion_calendar_selected"] = date_key
                    st.rerun()
    selected = st.session_state.get("emotion_calendar_selected", selected)
    if selected not in by_date or not selected.startswith(ym):
        selected = max((str(e["date"]) for e in month_rows), default="")

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    if not selected:
        st.info("아직 이 달의 감정 기록이 없어요. 홈에서 10초 기록이나 일기를 남겨 보세요. 기록하면 이 달력에 별이 생겨요.")
        return

    entry = by_date[selected]
    idx, weights = _emotion_of(entry)
    mood, color = analysis.EMO[idx], _COLORS[idx]
    date_obj = dt.date.fromisoformat(selected)
    kind = "10초 기록" if entry.get("kind") == "quick" else "일기"
    with st.container(border=True):
        st.markdown(
            f'<div style="color:#b4bce4;font-size:13px">{date_obj.year}년 {date_obj.month}월 {date_obj.day}일 · {kind}</div>'
            f'<div style="font-size:24px;font-weight:800;color:{color};margin:5px 0 12px">✦ {mood}의 별</div>',
            unsafe_allow_html=True)
        st.write(entry.get("text") or "기록된 메모가 없어요.")
        with st.expander("그날의 감정 비율 살펴보기"):
            for i in sorted(range(len(weights)), key=lambda j: -weights[j]):
                st.progress(min(1., max(0., weights[i])), text=f"{analysis.EMO[i]} · {round(weights[i]*100)}%")
            if kind == "10초 기록":
                st.caption("직접 선택한 감정을 바탕으로 계산한 비율이에요. AI 분석 신뢰도가 아닙니다.")
            else:
                st.caption("글에서 추정한 감정의 비율로, 실제 심리 상태를 진단하는 수치는 아니에요.")
        if on_edit is not None and st.button("✎ 이 날짜 기록 수정하기", key="calendar_edit_selected"):
            on_edit(date_obj)
