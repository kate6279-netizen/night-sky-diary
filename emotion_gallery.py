"""월간 별자리 갤러리. 저장 기능이나 AI 모델은 수정하지 않습니다."""
import calendar
import datetime as dt
import html
from collections import Counter

import streamlit as st
import streamlit.components.v1 as components

import analysis
import db
import sky


def sample_entries(year, month):
    """저장하지 않는 미리보기 기록."""
    samples = ((1, 0), (3, 4), (5, 2), (7, 1), (9, 3), (12, 5),
               (15, 2), (17, 0), (20, 6), (22, 4), (25, 1), (28, 2))
    out = []
    last_day = calendar.monthrange(year, month)[1]
    for day, index in samples:
        if day > last_day:
            continue
        probabilities = [0.03] * 7
        probabilities[index] = 0.82
        out.append({"date": f"{year:04d}-{month:02d}-{day:02d}",
                    "text": f"디자인 미리보기 · {analysis.EMO[index]}의 별",
                    "probs": probabilities, "corrected": None, "kind": "quick"})
    return out


def page_gallery():
    st.markdown('<div class="head"><h1>별자리 갤러리 <small>MY CONSTELLATION</small></h1><p>하루의 마음이 별 하나가 되어 한 달의 그림을 만들어요.</p></div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:12px 16px;border:1px solid rgba(165,154,255,.24);border-radius:13px;background:linear-gradient(110deg,rgba(125,112,235,.16),rgba(20,26,56,.65));margin:12px 0 18px;color:#d0d5fa;font-size:12.5px;line-height:1.8"><strong style="color:#f5f2ff">작품을 감상하는 방법</strong> · 별 하나는 하루의 감정이고, 별을 이은 선은 기록한 날짜의 흐름이에요. 별을 클릭해 그날의 일기를 보고, 작품 오른쪽 위에서 PNG 이미지로 저장할 수 있어요.</div>', unsafe_allow_html=True)
    nickname = st.session_state.get("nickname", "")
    if not nickname:
        st.info("홈에서 내 우주 이름을 먼저 입력해 주세요.")
        return

    entries = db.load_entries(nickname)
    today = dt.date.today()
    months = set()
    for offset in range(12):
        number = today.year * 12 + today.month - 1 - offset
        year, month_zero = divmod(number, 12)
        months.add(f"{year:04d}-{month_zero + 1:02d}")
    for entry in entries:
        try:
            months.add(dt.date.fromisoformat(str(entry["date"])).strftime("%Y-%m"))
        except (ValueError, KeyError, TypeError):
            pass

    chosen = st.selectbox("감상할 달", sorted(months, reverse=True),
                          format_func=lambda value: f"{value[:4]}년 {int(value[5:])}월",
                          key="star_gallery_month")
    year, month = map(int, chosen.split("-"))
    preview = st.toggle("✨ 별자리 미리보기", key="star_gallery_preview",
                        help="예시 기록은 실제로 저장되지 않습니다.")
    current = [entry for entry in entries if str(entry.get("date", "")).startswith(chosen)]
    if preview:
        existing = {entry["date"] for entry in current}
        current.extend(entry for entry in sample_entries(year, month) if entry["date"] not in existing)
        st.caption("미리보기 모드 · 예시 별은 실제 저장된 기록이 아니에요.")
    current.sort(key=lambda entry: entry["date"])
    emotions = [analysis.EMO[int(analysis.effective(entry).argmax())] for entry in current]
    dominant = Counter(emotions).most_common(1)[0][0] if emotions else "기록 없음"
    st.markdown(
        '<div style="display:flex;flex-wrap:wrap;gap:12px;margin:12px 0 18px">'
        f'<div style="flex:1;min-width:140px;padding:16px;border-radius:14px;background:#171d3c;border:1px solid #33385f"><small>이달의 별</small><div style="font-size:24px;font-weight:800;color:#fff">{len(current)}개</div></div>'
        f'<div style="flex:1;min-width:140px;padding:16px;border-radius:14px;background:#171d3c;border:1px solid #33385f"><small>대표 감정</small><div style="font-size:24px;font-weight:800;color:#fff">{html.escape(dominant)}</div></div>'
        '</div>', unsafe_allow_html=True)
    components.html(sky.poster_html(current, year, month, height=540, preview=preview), height=552, scrolling=False)
    if not current:
        st.info("아직 이번 달 별이 없어요. 감정을 기록하거나 위의 미리보기를 켜보세요.")
    elif preview:
        st.caption("미리보기 작품에는 가상 날짜가 포함되어 있고, 저장한 PNG에도 미리보기 표시가 남아요.")
    else:
        st.caption("별을 눌러 날짜별 감정을 확인하고, 오른쪽 위 'PNG 저장' 버튼으로 작품을 저장해 보세요.")
