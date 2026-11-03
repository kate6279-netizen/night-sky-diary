import datetime as dt
from collections import Counter
import html
import streamlit as st

def render_home_extras(entries, today, top_emotion, streak_days, PAGES):
    st.markdown('<style>.weekly-pulse{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}.weekly-pulse span{flex:1;min-width:160px;border:1px solid rgba(155,146,252,.32);padding:14px 17px;border-radius:14px;background:rgba(31,36,78,.64);color:#abb8dd;font-size:12px}.weekly-pulse b{display:block;color:#fff;font-size:19px;margin-top:6px}.journey-title{font-size:16px;font-weight:800;color:#eeeaff;margin:19px 0 10px}.streak-badges{display:flex;gap:10px;flex-wrap:wrap;margin:15px 0 12px}.streak-badges span{border:1px solid #394269;border-radius:99px;padding:8px 12px;color:#a5afce;font-size:12px}.streak-badges span.earned{border-color:#ffcf6a;color:#ffcf6a;background:rgba(255,207,106,.1)}</style>', unsafe_allow_html=True)
    last_7_days = [entries.get((today - dt.timedelta(days=i)).isoformat()) for i in range(7)]
    last_7_days = [entry for entry in last_7_days if entry]
    top_week = Counter(top_emotion(entry) for entry in last_7_days).most_common(1)
    top_week = top_week[0][0] if top_week else '아직 없어요'
    st.markdown(f'<div class="weekly-pulse"><span>최근 7일 기록 <b>{len(last_7_days)} / 7일</b></span><span>이번 주 대표 감정 <b>{html.escape(top_week)}</b></span><span>연속 기록 <b>{streak_days(set(entries), today)}일</b></span></div>', unsafe_allow_html=True)
    st.markdown('<div class="journey-title">✦ 감정이 쌓여 나의 우주가 돼요</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.page_link(PAGES['calendar'], label='🗓 감정 달력 보러 가기')
    with b:
        st.page_link(PAGES['gallery'], label='✦ 한 달의 별자리 갤러리')
    st.markdown('<div class="journey-title">✧ 오늘의 작은 메시지</div>', unsafe_allow_html=True)
    messages = ('오늘의 작은 기록이 내일의 별이 돼요.', '마음의 색은 매일 달라도 괜찮아요.', '오늘도 나의 우주에 새로운 빛이 생겨요.', '별 하나의 시작은 짧은 기록이에요.', '오늘의 기분이 무엇이든 소중한 나의 일부예요.', '한 번의 기록이 내 마음을 이해하는 단서가 돼요.', '나만의 속도로 기록을 쌓아가도 좋아요.')
    if st.button('오늘의 별 메시지 열기 ✨', key='home_daily_message'):
        st.session_state['home_message_open'] = today.isoformat()
    if st.session_state.get('home_message_open') == today.isoformat():
        st.info(messages[today.toordinal() % len(messages)])
    streak = streak_days(set(entries), today)
    st.markdown('<div class="streak-badges">' + ''.join(f'<span class="{\"earned\" if streak >= goal else \"\"}">✦ {goal}일 {\"달성\" if streak >= goal else \"도전\"}</span>' for goal in (3, 7, 30)) + '</div>', unsafe_allow_html=True)
