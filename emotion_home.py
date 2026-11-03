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
    """네 가지 탐색 경로만 표시해 사용자 선택을 돕습니다."""
    st.markdown(_HOME_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="et-nav-head"><b>✦ 나의 우주 둘러보기</b>'
        '<p>오늘의 기록을 네 가지 방법으로 다시 만날 수 있어요.</p></div>',
        unsafe_allow_html=True,
    )
    choices = (
        ('calendar', '감정 달력', '어느 날 어떤 감정을 느꼈는지 날짜별로 확인'),
        ('solar', '감정 태양계', '이번 달 가장 많았던 감정을 행성으로 비교'),
        ('universe', '감정 유니버스', '마음이 비슷했던 날짜와 기록을 찾아보기'),
        ('gallery', '별자리 갤러리', '한 달의 별을 하나의 작품으로 감상'),
    )
    with st.container(key='et_explore'):
        # 아래 가로 열은 이 컨테이너 안에 있어야 스타일이 적용됩니다.
        cols = st.columns(4, gap='small')
        for col, (page_key, label, description) in zip(cols, choices):
            with col:
                with st.container(border=True):
                    st.markdown(
                        '<div class="et-nav-desc">' + html.escape(description) + '</div>',
                        unsafe_allow_html=True,
                    )
                    st.page_link(PAGES[page_key], label=label)
