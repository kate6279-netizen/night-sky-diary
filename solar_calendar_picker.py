"""감정 태양계 오른쪽 위 달력 팝업.

브라우저에서 DateInput 동적 파일을 불러오는 오류를 피하려고 Streamlit 버튼으로
달력을 구성합니다. 이 파일은 기존 DB·AI 모델을 읽기만 하고 수정하지 않습니다.
"""
from __future__ import annotations

import calendar
import datetime as dt
import html

import streamlit as st

import analysis

EMOTION_COLORS = (
    "#ffcf4a", "#ff8fb1", "#6fd3a8", "#9aa6b8",
    "#5b84f0", "#b08cf0", "#f0645a",
)
WEEKDAYS = ("월", "화", "수", "목", "금", "토", "일")


def shift_month(ym: str, offset: int) -> str:
    """YYYY-MM을 월 단위로 이동합니다. 12월/1월 경계도 처리합니다."""
    year, month = map(int, ym.split("-"))
    total = year * 12 + month - 1 + offset
    if total < 12:
        raise ValueError("1년 이전 달은 선택할 수 없어요.")
    new_year, zero_month = divmod(total, 12)
    return f"{new_year:04d}-{zero_month + 1:02d}"


def _month_entries(ym: str, entries: list[dict]) -> dict[str, dict]:
    return {
        str(entry["date"]): entry
        for entry in entries
        if str(entry.get("date", "")).startswith(ym + "-")
    }


def _emotion(entry: dict) -> tuple[str, str]:
    idx = int(analysis.effective(entry).argmax())
    return analysis.EMO[idx], EMOTION_COLORS[idx]


def _calendar_css(ym: str, by_date: dict[str, dict], selected: str, today: dt.date) -> str:
    """이 달에 기록이 있는 날짜만 감정별 색으로 표시합니다."""
    css = [
        "<style>",
        # 넓은 그리드를 팝업 안에 표시하되 모바일 뷰포트를 벗어나지 않게 합니다.
        'div[data-testid="stPopoverBody"]:has([class*="st-key-solar_picker_root"])'
        '{width:min(440px,calc(100vw - 24px))!important;max-width:calc(100vw - 24px)!important;}',
        '[class*="st-key-solar_picker_root"] [data-testid="stHorizontalBlock"]:has([class*="st-key-solar_cal_day_"])'
        '{flex-wrap:nowrap!important;gap:4px!important;}',
        '[class*="st-key-solar_picker_root"] [data-testid="stHorizontalBlock"]:has([class*="st-key-solar_cal_day_"]) [data-testid="stColumn"]'
        '{min-width:0!important;width:0!important;flex:1 1 0!important;}',
        '[class*="st-key-solar_cal_day_"] button'
        '{width:100%!important;min-height:39px!important;min-width:0!important;'
        'padding:4px 0!important;border-radius:10px!important;'
        'font-size:12px!important;font-weight:650!important;'
        'background:#171c38!important;color:#e8eaff!important;'
        'border:1px solid rgba(155,159,224,.22)!important;}',
        '[class*="st-key-solar_cal_day_"] button:hover:not(:disabled)'
        '{filter:brightness(1.22)!important;transform:translateY(-1px)!important;}',
        '[class*="st-key-solar_cal_day_"] button:disabled'
        '{opacity:.35!important;}',
        '.solar-picker-weekdays{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));'
        'gap:4px;text-align:center;margin:7px 0 9px;font-size:11px;'
        'font-weight:700;color:#bfc2e9;}',
        '.solar-picker-legend{display:flex;flex-wrap:wrap;gap:7px 13px;'
        'color:#cdd2f2;font-size:11px;margin:12px 0 3px;}',
        '.solar-picker-legend i{display:inline-block;width:8px;height:8px;'
        'margin-right:4px;border-radius:50%;background:var(--emo);box-shadow:0 0 7px var(--emo);}',
    ]
    for date, entry in by_date.items():
        _, color = _emotion(entry)
        class_name = f"st-key-solar_cal_day_{date.replace('-', '')}"
        border = color if date == selected else color + "90"
        css.append(
            f"div.{class_name} button{{background:linear-gradient(145deg,{color}45,#171c38)!important;"
            f"border:1px solid {border}!important;color:#fff!important;}}"
        )
    if selected.startswith(ym + "-"):
        css.append(
            f"div.st-key-solar_cal_day_{selected.replace('-', '')} button"
            "{outline:2px solid #e4d7ff!important;outline-offset:-3px!important;}"
        )
    if today.strftime("%Y-%m") == ym:
        css.append(
            f"div.st-key-solar_cal_day_{today.strftime('%Y%m%d')} button"
            "{box-shadow:0 0 0 1px #ffcf6a!important;}"
        )
    css.append("</style>")
    return "".join(css)


def render_solar_calendar(ym: str, entries: list[dict], on_date_open=None) -> None:
    """기존 감정 태양계의 상단 📅 팝업 안에 호출합니다."""
    today = dt.date.today()
    current_month = today.strftime("%Y-%m")
    year, month = map(int, ym.split("-"))
    by_date = _month_entries(ym, entries)
    selected = str(st.session_state.get("solar_selected_date", ""))
    if not selected.startswith(ym + "-"):
        selected = ""

    with st.container(key="solar_picker_root"):
        st.markdown(_calendar_css(ym, by_date, selected, today), unsafe_allow_html=True)
        prev_month = shift_month(ym, -1)
        next_month = shift_month(ym, 1)
        before, heading, after = st.columns([1, 4, 1], gap="small", vertical_alignment="center")
        if before.button("‹", key=f"solar_cal_prev_{ym}", help="이전 달", use_container_width=True):
            st.session_state["ym"] = prev_month
            st.session_state.pop("solar_selected_date", None)
            st.rerun()
        heading.markdown(
            f'<div style="text-align:center;font-size:15px;font-weight:700;color:#f2edff">'
            f'{year}년 {month}월</div>', unsafe_allow_html=True
        )
        if after.button("›", key=f"solar_cal_next_{ym}",
                        disabled=next_month > current_month, help="다음 달",
                        use_container_width=True):
            st.session_state["ym"] = next_month
            st.session_state.pop("solar_selected_date", None)
            st.rerun()

        st.markdown(
            '<div class="solar-picker-weekdays">'
            + "".join(f"<span>{day}</span>" for day in WEEKDAYS)
            + "</div>", unsafe_allow_html=True,
        )
        for week in calendar.monthcalendar(year, month):
            columns = st.columns(7, gap="small")
            for weekday, day in enumerate(week):
                with columns[weekday]:
                    if not day:
                        st.markdown('<div style="min-height:39px"></div>', unsafe_allow_html=True)
                        continue
                    date_key = f"{ym}-{day:02d}"
                    entry = by_date.get(date_key)
                    mood = _emotion(entry)[0] if entry is not None else "기록 없음"
                    label = f"{day} ✦" if entry is not None else str(day)
                    with st.container(key=f"solar_cal_day_{date_key.replace('-', '')}"):
                        if st.button(
                            label, key=f"solar_pick_{date_key.replace('-', '')}",
                            help=f"{month}월 {day}일 · {mood}",
                            disabled=dt.date(year, month, day) > today,
                            use_container_width=True,
                        ):
                            st.session_state["solar_selected_date"] = date_key
                            st.rerun()

        legend = "".join(
            f'<span><i style="--emo:{color}"></i>{html.escape(emotion)}</span>'
            for emotion, color in zip(analysis.EMO, EMOTION_COLORS)
        )
        st.markdown(f'<div class="solar-picker-legend">{legend}</div>',
                    unsafe_allow_html=True)
        if not selected:
            st.caption("✦ 날짜를 눌러 그날의 기록을 확인하세요. 색깔이 있는 날에는 기록이 있어요.")
            return

        st.divider()
        selected_date = dt.date.fromisoformat(selected)
        entry = by_date.get(selected)
        st.markdown(f"**✦ {selected_date.month}월 {selected_date.day}일의 기록**")
        if entry is None:
            st.caption("이 날짜에는 아직 저장한 감정 기록이 없어요.")
        else:
            mood, color = _emotion(entry)
            st.markdown(
                f'<span style="color:{color};font-weight:700">● {html.escape(mood)}</span>'
                f' <span style="font-size:12px;color:#aeb5d8">· '
                f'{"10초 기록" if entry.get("kind") == "quick" else "감정 일기"}</span>',
                unsafe_allow_html=True,
            )
            st.caption(str(entry.get("text") or "기록된 메모가 없어요.")[:220])

        if on_date_open is not None and st.button(
            "✎ 이 날짜 기록 보기·수정" if entry else "＋ 이 날짜에 기록하기",
            key=f"solar_cal_open_{selected.replace('-', '')}",
            use_container_width=True,
        ):
            on_date_open(selected_date)
