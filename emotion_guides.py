"""Emotion Trace: UI explanations and compact home insights.

Display-only helpers. No AI calls and no database writes.
"""
import html

import streamlit as st


_GUIDE_STYLES = """<style>
.et-insight-head{display:flex;gap:10px;align-items:center;margin-bottom:12px;color:#f2efff;font-weight:800;font-size:15px}
.et-insight-head .et-spark{display:grid;place-items:center;width:32px;height:32px;border-radius:10px;background:rgba(160,143,255,.15);color:#cfb7ff;font-size:20px}
.et-insight-tip{padding:12px 14px;border:1px solid rgba(159,151,255,.27);border-radius:12px;background:linear-gradient(130deg,rgba(143,118,255,.13),rgba(91,132,240,.06));color:#d0d5f2;font-size:12.5px;line-height:1.85;margin-bottom:12px}
.et-insight-row{display:flex;gap:10px;align-items:center;padding:11px 2px;border-bottom:1px solid rgba(160,165,230,.13)}
.et-insight-row:last-of-type{border-bottom:0}
.et-insight-star{display:block;width:15px;height:15px;flex:none;border-radius:50%;background:radial-gradient(circle at 32% 28%,#fff 0%,var(--mood) 43%,#141b3b 100%);box-shadow:0 0 13px var(--mood)}
.et-insight-data{flex:1;min-width:0}
.et-insight-data b{display:block;color:#f6f4ff;font-size:13px}
.et-insight-data small{display:block;color:#aab3d7;font-size:12px;margin-top:3px}
.et-insight-value{font-size:18px;color:#fff;font-weight:800;font-variant-numeric:tabular-nums}
.et-insight-label{font-size:12px;font-weight:800;color:#c7beff;margin:16px 0 10px}
.et-insight-pair{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0 12px}
.et-insight-pair>div{padding:12px;border-radius:12px;background:rgba(26,32,65,.75);border:1px solid rgba(165,155,255,.2)}
.et-insight-pair b{display:block;font-size:12.5px;color:#e8e8ff;margin-bottom:4px}
.et-insight-pair span{display:block;font-size:11.5px;color:#b4bddf;line-height:1.6}
.et-explain{margin:6px 0 17px;padding:17px 18px;border:1px solid rgba(159,148,255,.28);border-radius:16px;background:linear-gradient(118deg,rgba(64,56,131,.25),rgba(13,18,43,.85))}
.et-explain-kicker{font-size:10px;color:#baaaff;font-weight:800;letter-spacing:.15em}
.et-explain-title{margin:6px 0 14px;color:#f1efff;font-size:15px;font-weight:800;line-height:1.6}
.et-explain-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.et-explain-cell{background:rgba(15,20,48,.7);border:1px solid rgba(155,150,232,.18);border-radius:12px;padding:12px 13px}
.et-explain-cell b{display:block;color:#f1eaff;font-size:12.5px;margin-bottom:5px}
.et-explain-cell span{display:block;font-size:11.7px;color:#aeb6d7;line-height:1.75}
@media(max-width:800px){.et-explain-grid{grid-template-columns:1fr;}.et-explain-cell{padding:10px 13px}}
@media(max-width:480px){.et-insight-pair{grid-template-columns:1fr}}
</style>"""


def _style():
    st.markdown(_GUIDE_STYLES, unsafe_allow_html=True)


def render_home_side(probs, emotions, colors, pages):
    """Show a useful card below the home donut without changing data."""
    _style()
    with st.container(border=True):
        st.markdown('<div class="et-insight-head"><span class="et-spark">✦</span>오늘의 감정 한눈에 보기</div>', unsafe_allow_html=True)
        if probs and len(probs) == len(emotions):
            order = sorted(range(len(probs)), key=lambda idx: -float(probs[idx]))[:2]
            rows = []
            for n, idx in enumerate(order):
                label = "가장 큰 감정" if n == 0 else "함께 나타난 감정"
                color = html.escape(str(colors[emotions[idx]]), quote=True)
                mood = html.escape(str(emotions[idx]))
                percent = round(float(probs[idx]) * 100)
                rows.append(
                    f'<div class="et-insight-row"><i class="et-insight-star" style="--mood:{color}"></i>'
                    f'<div class="et-insight-data"><b>{mood}</b><small>{label}</small></div>'
                    f'<span class="et-insight-value">{percent}%</span></div>'
                )
            st.markdown(''.join(rows), unsafe_allow_html=True)
            st.caption("기록된 감정 비중을 보기 쉽게 정리한 값이에요. AI 분석 신뢰도를 의미하지 않아요.")
        else:
            st.markdown('<div class="et-insight-tip">아직 오늘의 별이 없어요.<br>오른쪽에서 감정을 선택하고 저장하면 대표 감정과 비율이 여기에 표시돼요.</div>', unsafe_allow_html=True)

        st.markdown('<div class="et-insight-label">✧ 다음엔 어디로 가볼까요?</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="et-insight-pair">'
            '<div><b>☀ 감정 태양계</b><span>한 달에 어떤 감정을 많이 느꼈는지 확인</span></div>'
            '<div><b>✦ 감정 유니버스</b><span>감정이 비슷했던 날짜끼리 찾아보기</span></div>'
            '</div>', unsafe_allow_html=True,
        )
        a, b = st.columns(2, gap="small")
        with a:
            st.page_link(pages["solar"], label="태양계 보기")
        with b:
            st.page_link(pages["universe"], label="유니버스 보기")


_EXPLAINERS = {
    "solar": (
        "☀ 감정 태양계는 '한 달의 감정 구성'을 보는 곳이에요.",
        (
            ("① 행성 = 감정 하나", "기쁨·설렘·평온·지침·슬픔·불안·분노, 총 7개 감정을 행성으로 표현해요."),
            ("② 크기와 궤도 읽기", "비율이 높은 감정은 더 크게, 자주 나타난 감정은 중심에 가까운 궤도로 표시돼요."),
            ("③ 이렇게 사용해요", "행성을 눌러 해당 감정의 비중을 살펴보세요. 이번 달 마음의 전체 분위기를 파악할 수 있어요."),
        ),
    ),
    "universe": (
        "✦ 감정 유니버스는 '감정이 비슷한 날'을 찾는 지도예요.",
        (
            ("① 별 하나 = 기록한 하루", "일기를 남긴 날짜마다 별이 생겨요. 여러 날의 감정이 모여 지도가 만들어져요."),
            ("② 가까운 별은 무슨 뜻?", "두 날짜의 감정 비율이 비슷하면 별들이 가까이 표시되는 경향이 있어요."),
            ("③ 이렇게 사용해요", "별을 클릭해 날짜와 기록을 보고, 감정별 필터나 2D·3D 화면으로 비교해 보세요."),
        ),
    ),
    "archive": (
        "▤ 우주의 기록은 '감정 통계와 지난 일기'를 돌아보는 곳이에요.",
        (
            ("① 이달의 기록 통계", "한 달간 기록한 감정 비율과 변화 추이를 숫자와 그래프로 확인해요."),
            ("② 지난 기록 찾기", "최근 일기와 전체 기록에서 날짜·내용·감정별 기록을 찾아볼 수 있어요."),
            ("③ 다른 화면과 차이", "달력은 날짜별 색을, 갤러리는 별자리 작품을, 이 화면은 기록의 변화와 데이터를 보여줘요."),
        ),
    ),
    "capsule": (
        "✉ 감정 타임캡슐은 '과거의 나에게 답장하는 공간'이에요.",
        (
            ("① 편지가 도착해요", "기록을 남긴 지 7·14·30일이 지나면 지난 기록을 편지로 볼 수 있어요."),
            ("② 그때와 지금 비교", "과거에 느낀 감정과 오늘 느낀 감정을 나란히 살펴봐요."),
            ("③ 답장을 남겨보세요", "과거의 나에게 지금 하고 싶은 말을 쓰고 주고받은 편지에서 다시 읽을 수 있어요."),
        ),
    ),
}


def render_explainer(kind):
    """Compact usage guide for pages with similar cosmic names."""
    if kind not in _EXPLAINERS:
        return
    _style()
    title, items = _EXPLAINERS[kind]
    cells = ''.join(
        '<div class="et-explain-cell"><b>'
        + html.escape(heading) + '</b><span>' + html.escape(description) + '</span></div>'
        for heading, description in items
    )
    st.markdown(
        '<div class="et-explain"><div class="et-explain-kicker">HOW TO EXPLORE</div>'
        '<div class="et-explain-title">' + html.escape(title) + '</div>'
        '<div class="et-explain-grid">' + cells + '</div></div>',
        unsafe_allow_html=True,
    )
