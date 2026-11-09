"""감정의 궤적: 간결한 홈 감정 요약과 페이지별 사용 안내.

화면 출력 전용. 저장/모델 호출을 수행하지 않습니다.
"""
import html
import streamlit as st


_CSS = '''<style>
.et-mini-empty{text-align:center;padding:25px 12px 22px;line-height:1.85;color:#aeb7df}
.et-mini-orb{width:58px;height:58px;margin:0 auto 13px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#fff8e8 0%,#b6a9ff 16%,#7158d7 42%,#26204e 78%);box-shadow:0 0 30px rgba(154,127,255,.25),0 0 0 9px rgba(154,127,255,.05)}
.et-mini-empty strong{display:block;color:#f1edff;font-size:15px;font-weight:800}
.et-mini-empty p{font-size:12.5px;line-height:1.8;margin:7px 0 0}
.et-mini-dots{display:flex;gap:9px;justify-content:center;margin:17px 0 0}
.et-mini-dots i{display:block;width:8px;height:8px;border-radius:50%;background:var(--dot);box-shadow:0 0 8px var(--dot)}
.et-mini-wrap{padding:4px 2px 3px;border-top:1px solid rgba(161,153,255,.17);margin-top:3px}
.et-mini-label{font-size:11px;color:#b5b4e8;font-weight:800;letter-spacing:.04em;margin:10px 0}
.et-mini-mood{display:flex;align-items:center;gap:12px;padding:10px 4px}
.et-mini-mood .et-mood-orb{width:21px;height:21px;border-radius:50%;background:radial-gradient(circle at 32% 25%,#fff 0%,var(--c) 43%,#11172e 100%);box-shadow:0 0 13px var(--c);flex:none}
.et-mini-mood .et-mood-text{flex:1;min-width:0}
.et-mini-mood b{display:block;font-size:13px;color:#f2efff}
.et-mini-mood span{display:block;font-size:11.5px;color:#9da8d2;margin-top:2px}
.et-mini-mood .et-mood-value{font-size:17px;font-weight:800;color:#eeeaff}
.et-mini-footer{color:#8996bf;font-size:11px;line-height:1.65;margin:8px 0 0}
.et-usage{margin:8px 0 15px;padding:15px 17px;border:1px solid rgba(165,154,255,.24);border-radius:14px;background:linear-gradient(105deg,rgba(80,69,153,.21),rgba(19,26,56,.72));display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.et-usage-copy{flex:1;min-width:240px}
.et-usage-copy strong{display:block;font-size:13px;color:#efeaff;margin-bottom:5px}
.et-usage-copy span{font-size:12px;color:#abb5dd;line-height:1.7}
.et-usage-steps{display:flex;flex-wrap:wrap;gap:6px}
.et-usage-steps i{font-style:normal;border:1px solid rgba(167,154,255,.26);border-radius:100px;padding:6px 9px;background:rgba(13,18,44,.65);color:#d2ccf8;font-size:11.5px}
@media(max-width:680px){.et-usage{padding:12px 13px;gap:10px}.et-usage-copy{min-width:0;flex-basis:100%}.et-mini-empty{padding:19px 9px 16px}}
</style>'''


def _style():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_home_side(probs, emotions, colors, pages):
    """감정 그래프 아래에 있는 요약. 기능 설명이나 중복 링크는 만들지 않습니다."""
    _style()
    if not probs:
        colors_html = ''.join(f'<i style="--dot:{html.escape(str(colors[emo]), quote=True)}"></i>' for emo in emotions)
        st.markdown(
            '<div class="et-mini-empty"><div class="et-mini-orb"></div>'
            '<strong>오늘의 감정 별이 기다리고 있어요</strong>'
            '<p>오른쪽에서 감정을 고르고 저장해 보세요.<br>7가지 감정의 색이 이곳에 채워져요.</p>'
            '<div class="et-mini-dots">' + colors_html + '</div></div>',
            unsafe_allow_html=True,
        )
        return
    order = sorted(range(len(probs)), key=lambda idx: -float(probs[idx]))[:2]
    parts = ['<div class="et-mini-wrap"><div class="et-mini-label">✦ 오늘의 주요 감정</div>']
    for pos, idx in enumerate(order):
        emotion = html.escape(str(emotions[idx]))
        c = html.escape(str(colors[emotions[idx]]), quote=True)
        percentage = round(float(probs[idx]) * 100)
        role = '대표 감정' if pos == 0 else '함께 나타난 감정'
        parts.append(
            f'<div class="et-mini-mood"><i class="et-mood-orb" style="--c:{c}"></i>'
            f'<div class="et-mood-text"><b>{emotion}</b><span>{role}</span></div>'
            f'<div class="et-mood-value">{percentage}%</div></div>'
        )
    parts.append('<p class="et-mini-footer">비율은 기록에서 계산한 값이며 심리 진단이나 AI 신뢰도가 아니에요.</p></div>')
    st.markdown(''.join(parts), unsafe_allow_html=True)


_GUIDES = {
    'solar': (
        '한 달의 감정 비중을 행성으로 비교해요.',
        '큰 행성은 비중이 높은 감정이에요. 행성을 누르면 해당 감정의 정보를 볼 수 있고, 오른쪽 위 📅 버튼에서는 날짜별 기록을 확인할 수 있어요.',
        ('감정 행성', '행성 클릭', '📅 날짜 확인'),
    ),
    'universe': (
        '같은 감정 기록을 평면(2D) 또는 입체(3D)로 살펴보는 지도예요.',
        '2D는 위에서 보는 지도, 3D는 드래그해 돌려보는 지도예요. 별 하나가 하루의 기록이고, 가까운 별은 감정이 비슷한 편이에요.',
        ('2D: 평면 보기', '3D: 마우스로 회전', '별 클릭: 닮은 날'),
    ),
    'archive': (
        '기록을 그래프와 통계로 돌아보는 곳이에요.',
        '이 화면에서는 월간 감정 변화와 지난 일기를 그래프로 보고 검색할 수 있어요.',
        ('월간 통계', '감정 변화', '지난 일기 검색'),
    ),
    'capsule': (
        '과거의 나에게 답장을 남기는 공간이에요.',
        '7·14·30일 전의 기록을 다시 읽고 오늘의 마음과 비교하거나 답장을 쓸 수 있어요.',
        ('지난 편지', '그때와 지금', '답장 쓰기'),
    ),
}


def render_explainer(kind):
    """기능별 짧은 한 줄 설명. 길고 반복되는 3개 설명 카드는 사용하지 않습니다."""
    if kind not in _GUIDES:
        return
    _style()
    title, desc, steps = _GUIDES[kind]
    pills = ''.join(f'<i>{html.escape(step)}</i>' for step in steps)
    st.markdown(
        '<div class="et-usage"><div class="et-usage-copy"><strong>' + html.escape(title)
        + '</strong><span>' + html.escape(desc) + '</span></div>'
        + '<div class="et-usage-steps">' + pills + '</div></div>',
        unsafe_allow_html=True,
    )
