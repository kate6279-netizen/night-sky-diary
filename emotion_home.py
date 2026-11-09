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
.st-key-et_explore [data-testid="stVerticalBlockBorderWrapper"]{background:linear-gradient(130deg,rgba(32,36,80,.68),rgba(11,15,35,.88));border:1px solid rgba(163,155,255,.23)!important;border-radius:15px!important}
.st-key-et_explore [data-testid="stPageLink"] a{background:rgba(125,112,238,.12);border-radius:10px;padding:9px 10px!important;border:1px solid rgba(173,158,255,.24);min-height:42px}
.st-key-et_explore [data-testid="stPageLink"] a:hover{background:rgba(139,123,255,.22)}
</style>'''


def render_home_extras(entries, today, top_emotion, streak_days, PAGES):
    """합의된 핵심 화면(태양계·유니버스·리포트)으로 안내합니다."""
    st.markdown(_HOME_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="et-nav-head"><b>✦ 기록 돌아보기</b>'
        '<p>감정 행성에서 날짜를 찾고, 별자리에서 마음의 연결을 발견해 보세요.</p></div>',
        unsafe_allow_html=True,
    )
    choices = (
        ('solar', '감정 태양계', '감정 행성을 살펴보고 📅 버튼에서 날짜별 기록 확인'),
        ('universe', '감정 유니버스', '닮은 감정의 별을 연결하며 나만의 우주 탐험'),
        ('archive', '나의 감정 리포트', '최근 감정의 변화와 월간 기록을 살펴보기'),
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
