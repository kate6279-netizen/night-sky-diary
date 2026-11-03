"""감정의 궤적 — 한 달의 기록을 작품으로 만드는 별자리 갤러리."""
from __future__ import annotations

import datetime as dt
import html
from collections import Counter

import streamlit as st
import streamlit.components.v1 as components

import analysis
import db
import sky
from emotion_calendar import preview_entries


def page_gallery() -> None:
    st.markdown('<div class="head"><h1>나의 별자리 갤러리 <small>MONTHLY CONSTELLATION</small></h1><p>하루의 마음이 하나의 별이 되고, 기록이 모여 나만의 한 달을 그려요.</p></div>', unsafe_allow_html=True)
    nick = st.session_state.get("nickname", "")
    if not nick:
        st.info("먼저 홈 화면에서 내 우주 이름을 입력해 주세요.")
        return

    entries = db.load_entries(nick)
    today = dt.date.today()
    months = set()
    for offset in range(12):
        number = today.year * 12 + today.month - 1 - offset
        y, m0 = divmod(number, 12)
        months.add(f"{y:04d}-{m0 + 1:02d}")
    for e in entries:
        try:
            months.add(dt.date.fromisoformat(str(e["date"])).strftime("%Y-%m"))
        except (TypeError, ValueError, KeyError):
            continue

    ym = st.selectbox("감상할 달", sorted(months, reverse=True),
                      format_func=lambda m: f"{m[:4]}년 {int(m[5:])}월",
                      key="gallery_month")
    year, month = (int(x) for x in ym.split("-"))
    preview = st.toggle("✨ 별자리 작품 미리보기", key="gallery_preview",
                        help="기록이 없어도 화면을 체험할 수 있어요. 샘플은 저장되지 않습니다.")
    month_entries = [e for e in entries if str(e.get("date", "")).startswith(ym)]
    if preview:
        real_dates = {str(e["date"]) for e in month_entries}
        month_entries.extend(e for e in preview_entries(year, month) if e["date"] not in real_dates)
        st.caption("✦ 미리보기 모드 · 샘플 별은 저장되지 않는 가상 기록입니다.")
    month_entries.sort(key=lambda e: e["date"])

    names = [analysis.EMO[int(analysis.effective(e).argmax())] for e in month_entries]
    most = Counter(names).most_common(1)[0][0] if names else "아직 없어요"
    st.markdown(
        '<div style="display:flex;gap:12px;flex-wrap:wrap;margin:14px 0 18px">'
        f'<div style="flex:1;min-width:160px;border:1px solid rgba(160,157,255,.2);border-radius:15px;background:#151a35;padding:16px 18px"><span style="color:#aeb4df;font-size:12px">이달의 별</span><div style="color:#fff;font-size:24px;font-weight:800">{len(month_entries)}개</div></div>'
        f'<div style="flex:1;min-width:160px;border:1px solid rgba(160,157,255,.2);border-radius:15px;background:#151a35;padding:16px 18px"><span style="color:#aeb4df;font-size:12px">가장 자주 빛난 감정</span><div style="color:#fff;font-size:24px;font-weight:800">{html.escape(most)}</div></div>'
        f'<div style="flex:1;min-width:160px;border:1px solid rgba(160,157,255,.2);border-radius:15px;background:#151a35;padding:16px 18px"><span style="color:#aeb4df;font-size:12px">이달의 이야기</span><div style="color:#fff;font-size:24px;font-weight:800">{month}월의 하늘</div></div>'
        '</div>', unsafe_allow_html=True
    )

    components.html(sky.poster_html(month_entries, year, month, height=545), height=558, scrolling=False)
    if not month_entries:
        st.info("아직 이 달의 별이 없어요. 홈에서 감정을 기록하거나 위의 미리보기를 켜보세요.")
    else:
        st.caption("✦ 별을 클릭하면 그날의 감정과 기록을 볼 수 있어요. 포스터 오른쪽 위에서 PNG 이미지로 저장할 수도 있습니다.")
    st.markdown('<div style="padding:17px 20px;margin-top:10px;border:1px solid rgba(160,157,255,.2);border-radius:16px;background:linear-gradient(120deg,rgba(139,123,255,.16),rgba(91,132,240,.06));color:#cbd2f5;line-height:1.8;font-size:13px"><b style="color:#fff">나만의 우주는 매일 자라요.</b><p style="margin:5px 0 0">날마다 감정을 기록하면 새로운 별이 생기고, 한 달의 궤적이 하나의 그림으로 완성됩니다. 색은 그날의 대표 감정을 나타내요.</p></div>', unsafe_allow_html=True)
