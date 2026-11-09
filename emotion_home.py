"""홈 화면의 간결한 기능 탐색 카드.

이번 화면에서는 중복 통계, 미완성 포춘쿠키/메시지, 배지 UI를 표시하지 않습니다.
"""
import html
import streamlit as st


_HOME_CSS = '''<style>
.et-nav-head{margin:20px 0 13px}
.et-nav-head b{display:block;font-size:16px;font-weight:800;color:#f3f0ff}
.et-nav-head p{color:#9ba8d1;font-size:12px;margin:5px 0 0}
.et-nav-desc{color:#adb7da;font-size:12px;line-height:1.75;min-height:41px;margin:4px 0 10px}
.st-key-et_explore [data-testid="stVerticalBlockBorderWrapper"]{background:linear-gradient(145deg,rgba(29,37,75,.84),rgba(11,17,37,.94));border:1px solid rgba(163,178,255,.18)!important;border-radius:17px!important;box-shadow:0 10px 30px rgba(3,8,28,.15),inset 0 1px 0 rgba(255,255,255,.05)!important}
.st-key-et_explore [data-testid="stPageLink"] a{background:rgba(125,112,238,.12);border-radius:10px;padding:9px 10px!important;border:1px solid rgba(173,158,255,.24);min-height:42px}
.st-key-et_explore [data-testid="stPageLink"] a:hover{background:rgba(139,123,255,.22)}
</style>'''


def render_home_extras(entries, today, top_emotion, streak_days, PAGES):
    """합의된 핵심 화면(태양계·유니버스·리포트)으로 안내합니다."""
    st.markdown(_HOME_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="et-nav-head"><b>✦ 기록 돌아보기</b>'
        '<p>쌓여가는 기록을 다른 방식으로 바라보세요.</p></div>',
        unsafe_allow_html=True,
    )
    choices = (
        ('solar', '감정 태양계', '한 달의 감정을 행성으로 보기'),
        ('universe', '감정 유니버스', '감정의 연결과 시간의 흐름'),
        ('archive', '나의 감정 리포트', '월간 감정 변화 보기'),
    )
    with st.container(key='et_explore'):
        # 아래 가로 열은 이 컨테이너 안에 있어야 스타일이 적용됩니다.
        cols = st.columns(3, gap='small')
        for col, (page_key, label, description) in zip(cols, choices):
            with col:
                with st.container(border=True):
                    st.markdown(
                        '<div class="et-nav-desc">' + html.escape(description) + '</div>',
                        unsafe_allow_html=True,
                    )
                    st.page_link(PAGES[page_key], label=label)
