"""감정의 궤적 (EMOTION TRACE) - Streamlit 메인

실행: streamlit run app.py
화면: 홈(오늘의 별) / 감정 태양계 / 감정 유니버스 / 우주의 기록(월간 리포트)
"""
import calendar
import datetime as dt
import html

import streamlit as st
import streamlit.components.v1 as components

import analysis as A
import db
import quotes
import sky
from emotion_calendar import page_calendar
from emotion_gallery import page_gallery, sample_entries as demo_universe_entries
from emotion_home import render_home_extras
from emotion_guides import render_home_side, render_explainer
from model import EMO, predict
from samples import SAMPLES

st.set_page_config(page_title="감정의 궤적", page_icon="✦", layout="wide")
COL = dict(zip(EMO, sky.COLORS))
WEEK = "월화수목금토일"

# 주의: 아래 스타일 안에는 빈 줄을 넣지 마세요. 빈 줄이 있으면 화면에 코드가 글자로 보여요.
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@300;400;500;700&family=Nanum+Myeongjo:wght@700;800&display=swap" rel="stylesheet">
<style>
:root { --night:#070a1d; --card:rgba(16,20,46,.82); --line:rgba(140,150,255,.15); --line-hi:rgba(165,155,255,.42); --ink:#eef0ff; --sub:#a3a8cf; --faint:#6b7099; --violet:#8b7bff; --gold:#ffcf6a; }
html, body, .stApp, .stMarkdown, button, input, textarea, [data-testid="stSidebar"] { font-family:"Gothic A1","Apple SD Gothic Neo","Malgun Gothic",sans-serif !important; }
.stApp { background: radial-gradient(1100px 520px at 75% -12%, #18205a 0%, transparent 60%), radial-gradient(900px 480px at 5% 108%, #170f44 0%, transparent 60%), var(--night); }
header[data-testid="stHeader"] { background: transparent; pointer-events:none; }
header[data-testid="stHeader"] button, header[data-testid="stHeader"] a { pointer-events:auto; }
[data-testid="stToolbarActions"], [data-testid="stMainMenu"], [data-testid="stStatusWidget"] { display:none !important; }
[data-testid="stSidebarCollapseButton"], [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] { display:flex !important; visibility:visible !important; opacity:1 !important; pointer-events:auto !important; z-index:1000; }
[data-testid="stSidebarCollapseButton"] button, [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] button { color:#cfd2ff !important; background:rgba(139,123,255,.14) !important; border:1px solid var(--line-hi) !important; border-radius:10px !important; }
[data-testid="stAppDeployButton"], footer, #MainMenu { display:none !important; }
.block-container { max-width: 1380px; padding-top: 1.3rem; padding-bottom: 3rem; }
/* ----- 사이드바 ----- */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0b0e2a 0%, #070919 100%); border-right: 1px solid var(--line); }
[data-testid="stSidebar"][aria-expanded="true"] { min-width: 250px !important; max-width: 260px !important; }
.brand { display:flex; gap:12px; align-items:center; padding:2px 2px 22px; }
.brand svg { width:34px; height:34px; flex:none; }
.brand b { display:block; font-size:18px; font-weight:700; color:#ecebff; }
.brand span { font-size:9.5px; color:var(--faint); letter-spacing:.26em; }
[class*="st-key-nav_"] a { border-radius:10px !important; padding:10px 14px !important; margin:1px 0; border:1px solid transparent; }
[class*="st-key-nav_"] a:hover { background: rgba(139,123,255,.08) !important; }
[class*="st-key-nav_"] a p { font-size:14px !important; color:#d9dbf2 !important; }
[class*="st-key-nav_"] a span[data-testid="stIconMaterial"] { font-size:20px !important; color:#b9b0ff !important; margin-right:8px; }
.side-gap { height: 34vh; }
.st-key-side_bottom .stButton > button, .st-key-side_bottom [data-testid="stPopover"] button { border:0 !important; background:transparent !important; justify-content:flex-start; padding:.45rem .9rem; color:#c3c7e6; font-weight:400; }
.st-key-side_bottom .stButton > button:hover, .st-key-side_bottom [data-testid="stPopover"] button:hover { background: rgba(255,255,255,.04) !important; }
/* ----- 페이지 머리 ----- */
.head h1 { font-size:26px !important; font-weight:700 !important; margin:0 !important; padding:0 !important; color:#f2f0ff; display:flex; align-items:baseline; gap:12px; }
.head h1 small { margin-left:12px; font-size:14px; font-weight:400; color:var(--sub); }
.head p { margin:6px 0 0; font-size:13px; color:var(--sub); line-height:1.6; }
.user-chip { display:flex; align-items:center; justify-content:flex-end; gap:9px; font-size:13px; color:#d6d9f2; }
.user-chip i { width:30px; height:30px; border-radius:50%; display:grid; place-items:center; font-style:normal; background:linear-gradient(135deg,#8b7bff,#5b84f0); color:#fff; font-size:12px; font-weight:700; }
.st-key-mnav [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; gap:.5rem; align-items:center; }
.st-key-mnav [data-testid="stColumn"] { min-width:0 !important; }
.st-key-mpill { border:1px solid var(--line); border-radius:10px; background:var(--card); padding:0 4px; }
.st-key-mpill [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; gap:0; align-items:center; }
.st-key-mpill button, .st-key-mpill button:disabled, .st-key-mpill button:hover { height:36px; border:0 !important; background:transparent !important; box-shadow:none !important; padding:0; font-size:16px; color:#c9cdf0; }
.st-key-mpill button:disabled { color:#3d4270 !important; }
.st-key-mpill [data-testid="stMarkdownContainer"], .st-key-mpill .stMarkdown { margin:0 !important; }
.st-key-all_rec, .st-key-all_rec [data-testid="stButton"], .st-key-all_rec button { width:100% !important; }
.month-pill { display:flex; align-items:center; justify-content:center; height:36px; font-size:13px; font-weight:500; font-variant-numeric:tabular-nums; white-space:nowrap; }
.month-pill span { color:var(--faint); margin-left:8px; font-size:11px; }
.st-key-calpick [data-testid="stPopover"] button { height:38px; border-radius:10px; background:var(--card); border:1px solid var(--line); padding:0 6px; width:100%; }
.cal { display:grid; place-items:center; height:38px; border:1px solid var(--line); border-radius:10px; background:var(--card); font-size:15px; }
.st-key-more [data-testid="stPopover"] button { border:0 !important; background:transparent !important; color:var(--sub); width:auto; padding:.3rem .6rem; }
.st-key-save .stButton > button { width:auto; padding:.4rem 1.6rem; float:right; }
.trail { position:relative; display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); text-align:center; padding-top:2px; }
.trail::before { content:""; position:absolute; left:7%; right:7%; top:15px; height:1px; background:linear-gradient(90deg, transparent, rgba(165,155,255,.35), transparent); }
.trail div { position:relative; display:grid; justify-items:center; gap:5px; font-size:11px; color:var(--sub); font-variant-numeric:tabular-nums; }
.trail i { width:22px; height:22px; border-radius:50%; background:radial-gradient(circle at 34% 30%, #ffffff 0%, var(--c) 32%, var(--c2) 78%, #0a0c24 100%); box-shadow:0 0 14px var(--c); }
.trail i.off { background:#0b0e26; box-shadow:none; border:1px dashed rgba(165,155,255,.3); }
.trail b { font-weight:500; color:var(--c); font-size:11.5px; margin-top:-2px; }
/* ----- 입력칸, 버튼, 카드 ----- */
.stTextArea textarea { background:rgba(8,10,28,.55) !important; border:1px solid var(--line) !important; border-radius:12px !important; font-size:14.5px !important; line-height:1.75 !important; color:var(--ink) !important; }
.stTextArea textarea:focus { border-color:var(--violet) !important; box-shadow:0 0 0 1px var(--violet) !important; }
.stDateInput input, .stTextInput input, [data-baseweb="select"] > div { background:rgba(8,10,28,.55) !important; border-radius:10px !important; }
.stButton > button, [data-testid="stPopover"] button { border-radius:999px; padding:.45rem 1.1rem; font-weight:500; border:1px solid var(--line-hi); background:transparent; width:100%; }
.stButton > button[kind="primary"], .stFormSubmitButton > button { background:linear-gradient(135deg,#ff9fc6,#6f5ef0) !important; color:#fff !important; border:0 !important; font-weight:700; box-shadow:0 6px 22px rgba(120,100,255,.26); border-radius:999px; width:100%; }
.stButton > button[kind="primary"]:hover { filter:brightness(1.08); color:#fff; }
[data-testid="stVerticalBlockBorderWrapper"] { background:var(--card); border:1px solid var(--line) !important; border-radius:16px; }
.ctitle { font-size:14px; font-weight:700; color:#eceaff; margin:0 0 10px; }
.note { color:var(--sub); font-size:12.5px; }
/* 최근 7일 */
.week { display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); gap:6px; text-align:center; }
.week div { display:grid; justify-items:center; gap:6px; font-size:11.5px; color:var(--sub); font-variant-numeric:tabular-nums; }
.week i { width:26px; height:26px; border-radius:50%; background:radial-gradient(circle at 34% 30%, #ffffff 0%, var(--c) 32%, var(--c2) 78%, #0a0c24 100%); box-shadow:0 0 14px var(--c); }
.week i.off { background:rgba(255,255,255,.05); box-shadow:none; border:1px dashed rgba(165,155,255,.25); }
.week b { font-weight:500; color:var(--c); font-size:12px; }
/* 로그인 */
.st-key-login_box label { width:100%; justify-content:center; } .st-key-login_box label p { text-align:center; width:100%; font-size:14px !important; color:var(--sub) !important; }
.st-key-login_box input { text-align:center; font-size:15px !important; }
.st-key-login_box [data-testid="stElementContainer"]:has([data-testid="stFormSubmitButton"]), .st-key-login_box [data-testid="stFormSubmitButton"], .st-key-login_box [data-testid="stFormSubmitButton"] > div, .st-key-login_box [data-testid="stFormSubmitButton"] button { width:100% !important; }
.welcome [data-testid="stHeaderActionElements"] { display:none !important; } .st-key-login_box .note { font-size:12.5px !important; }
.welcome { text-align:center; padding:26px 10px 8px; }
.welcome svg { width:54px; height:54px; }
.welcome h2 { font-size:28px !important; margin:10px 0 4px !important; }
.welcome p { color:var(--sub); font-size:13.5px; margin:0 0 6px; }
/* 기록 보관함 */
.streak { float:right; font-size:12px; font-weight:500; color:var(--gold); }
.streak.off { color:var(--faint); }
.st-key-mode [data-testid="stButtonGroup"] { justify-content:flex-end; }
/* 감정 선택 버튼 기본 디자인 */
/* EMOTION_CARDS_V1: 감정 카드 버튼 디자인 */
.st-key-quick [data-testid="stButtonGroup"] button:nth-of-type(1) { --star:#FFCF4A; --symbol:"☀"; }
.st-key-quick [data-testid="stButtonGroup"] button:nth-of-type(2) { --star:#FF8FB1; --symbol:"✧"; }
.st-key-quick [data-testid="stButtonGroup"] button:nth-of-type(3) { --star:#6FD3A8; --symbol:"✳"; }
.st-key-quick [data-testid="stButtonGroup"] button:nth-of-type(4) { --star:#9AA6B8; --symbol:"☾"; }
.st-key-quick [data-testid="stButtonGroup"] button:nth-of-type(5) { --star:#5B84F0; --symbol:"✦"; }
.st-key-quick [data-testid="stButtonGroup"] button:nth-of-type(6) { --star:#B08CF0; --symbol:"✷"; }
.st-key-quick [data-testid="stButtonGroup"] button:nth-of-type(7) { --star:#F0645A; --symbol:"✹"; }
.st-key-quick [data-testid="stButtonGroup"] button { --star:#B08CF0; --symbol:"✦"; box-sizing:border-box !important; display:inline-flex !important; flex-direction:column !important; align-items:center !important; justify-content:center !important; flex:1 1 72px !important; min-width:65px !important; max-width:125px !important; min-height:86px !important; height:86px !important; gap:5px !important; padding:8px 6px !important; border-radius:16px !important; border:1px solid rgba(164,170,220,.22) !important; background:linear-gradient(155deg,#20294c,#10162d) !important; color:#e9eaff !important; font-weight:600 !important; font-size:13px !important; line-height:1.25 !important; box-shadow:inset 0 1px 0 rgba(255,255,255,.04) !important; transition:transform .18s ease,filter .18s ease,box-shadow .18s ease,border-color .18s ease !important; }
.st-key-quick [data-testid="stButtonGroup"] button::before { content:var(--symbol); display:block; flex:none; color:var(--star); font-size:26px; line-height:1; font-weight:400; text-shadow:0 0 12px color-mix(in srgb,var(--star) 55%,transparent); }
.st-key-quick [data-testid="stButtonGroup"] button:hover:not(:disabled) { transform:translateY(-3px) !important; border-color:var(--star) !important; filter:brightness(1.12) !important; box-shadow:0 6px 18px rgba(8,8,29,.45) !important; }
.st-key-quick [data-testid="stButtonGroup"] button:is([data-selected],[kind="pillsActive"]) { color:#FFFFFF !important; background:linear-gradient(155deg,color-mix(in srgb,var(--star) 33%,#111832),#11182f) !important; border-color:var(--star) !important; box-shadow:0 0 0 1px color-mix(in srgb,var(--star) 38%,transparent),0 7px 20px color-mix(in srgb,var(--star) 22%,transparent) !important; transform:translateY(-2px) !important; }
.st-key-quick [data-testid="stButtonGroup"] button:is([data-selected],[kind="pillsActive"])::before { animation:emotion-card-twinkle 2s ease-in-out infinite; }
.st-key-quick [data-testid="stButtonGroup"] button:focus-visible { outline:2px solid var(--star) !important; outline-offset:3px !important; }
@keyframes emotion-card-twinkle { 0%,100% { transform:scale(1); opacity:1; } 50% { transform:scale(1.15); opacity:.75; } }
@media (max-width:600px) { .st-key-quick [data-testid="stButtonGroup"] button { flex:1 1 72px !important; min-width:65px !important; min-height:78px !important; height:78px !important; } }
@media (prefers-reduced-motion:reduce) { .st-key-quick [data-testid="stButtonGroup"] button,.st-key-quick [data-testid="stButtonGroup"] button::before { animation:none !important; transition:none !important; } }
/* 타임캡슐 디자인 - 기존 CSS */
.arrive {
    display:flex;
    align-items:center;
    gap:14px;
    padding:4px 2px;
}
.arrive .env {
    width:40px;
    height:40px;
    border-radius:12px;
    display:grid;
    place-items:center;
    flex:none;
    font-size:20px;
    background:radial-gradient(circle at 30% 30%, rgba(255,207,106,.35), rgba(255,207,106,.05));
    border:1px solid rgba(255,207,106,.4);
}
.arrive b { display:block; font-size:14.5px; color:#fff3d6; }
.arrive span { font-size:12.5px; color:var(--sub); }
.kpi { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:14px 16px; }
.kpi b { display:block; font-size:24px; font-weight:700; color:var(--c,#eef0ff); font-variant-numeric:tabular-nums; }
.kpi span { font-size:12px; color:var(--sub); }
.letter { position:relative; border-radius:16px; padding:22px 24px 20px; background:linear-gradient(180deg, rgba(255,240,210,.06), rgba(255,240,210,.02)), rgba(14,16,40,.9); border:1px solid rgba(255,207,106,.28); }
.letter::before { content:""; position:absolute; left:24px; right:24px; top:0; height:2px; background:linear-gradient(90deg, transparent, var(--c), transparent); }
.letter .from { font-size:12px; letter-spacing:.14em; color:var(--gold); }
.letter .when { font-size:13px; color:var(--sub); margin:4px 0 14px; }
.letter .body { font-family:"Nanum Myeongjo",serif; font-size:17px; line-height:1.9; color:#f4f1ff; white-space:pre-wrap; }
.letter .mix { display:flex; gap:2px; height:5px; margin:18px 0 6px; max-width:320px; }
.letter .mix i { display:block; border-radius:3px; }
.letter .tags { font-size:12px; color:var(--sub); }
.then-now { display:grid; grid-template-columns:1fr auto 1fr; gap:12px; align-items:center; text-align:center; }
.then-now .orb { width:42px; height:42px; border-radius:50%; margin:0 auto 6px; background:radial-gradient(circle at 34% 30%, #fff 0%, var(--c) 34%, var(--c2) 80%, #0a0c24 100%); box-shadow:0 0 16px var(--c); }
.then-now b { display:block; font-size:14px; color:var(--c); }
.then-now small { font-size:11.5px; color:var(--faint); }
.then-now .arrow { color:var(--faint); font-size:18px; }
.sim { text-align:center; font-size:13px; color:#d6d9f2; margin-top:12px; }
.thread { display:grid; gap:10px; padding:16px 0; border-top:1px solid var(--line); }
.bubble { max-width:78%; padding:12px 16px; border-radius:14px; font-size:13.5px; line-height:1.75; }
.bubble small { display:block; font-size:11px; color:var(--faint); margin-bottom:4px; }
.bubble.past { background:rgba(255,255,255,.04); border:1px solid var(--line); justify-self:start; border-top-left-radius:4px; }
.bubble.now { background:linear-gradient(135deg, rgba(139,123,255,.28), rgba(111,94,240,.18)); border:1px solid rgba(165,155,255,.4); justify-self:end; border-top-right-radius:4px; }
.rec2 { display:grid; grid-template-columns:62px minmax(0,1fr); gap:10px; padding:7px 0; font-size:12.5px; border-bottom:1px solid rgba(140,150,255,.08); }
.rec2 b { font-weight:500; white-space:nowrap; font-variant-numeric:tabular-nums; }
.rec2 span { color:#cfd2ec; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.arc { display:grid; grid-template-columns:96px minmax(0,1fr); gap:16px; padding:14px 4px; border-top:1px solid var(--line); }
.arc .d b { display:block; font-size:15px; font-variant-numeric:tabular-nums; }
.arc .d small { color:var(--faint); font-size:11.5px; }
.arc .pill { display:inline-block; font-size:11.5px; padding:2px 9px; border-radius:99px; margin-right:6px; }
.arc .mix { display:flex; gap:2px; height:5px; margin:8px 0; max-width:260px; }
.arc .mix i { display:block; border-radius:3px; }
.arc p { margin:0; font-size:13.5px; line-height:1.7; color:#d6d9f0; }
/* EMOTION_INTENSITY_V1: 별빛 감정 세기 */
.st-key-quick [data-testid="stSlider"] { position:relative; margin-top:8px !important; margin-bottom:8px !important; padding:17px 17px 24px !important; border-radius:18px !important; border:1px solid rgba(175,155,255,.32) !important; background:linear-gradient(135deg,rgba(40,44,90,.72),rgba(15,19,45,.92)) !important; box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 10px 26px rgba(5,7,28,.16) !important; }
.st-key-quick [data-testid="stSlider"]::after { content:"✦ 나의 별빛이 얼마나 강하게 빛나고 있나요?"; display:block; padding-top:9px; color:#b9b2e9; font-size:11px; line-height:1.6; letter-spacing:.01em; pointer-events:none; }
.st-key-quick [data-testid="stSlider"] label { color:#f0eaff !important; font-weight:700 !important; }
.st-key-quick [data-testid="stSlider"] [role="slider"] { background:radial-gradient(circle at 30% 25%,#ffffff 0%,#f2d6ff 32%,#a68bff 72%,#7669e8 100%) !important; border:2px solid #f6e7ff !important; box-shadow:0 0 0 4px rgba(180,145,255,.19),0 0 17px rgba(176,143,255,.8) !important; }
.st-key-quick [data-testid="stSlider"] [role="slider"]:hover { box-shadow:0 0 0 6px rgba(180,145,255,.24),0 0 25px rgba(192,157,255,.9) !important; }
.st-key-quick [data-testid="stSliderThumbValue"] { color:#f5d6ff !important; font-weight:700 !important; text-shadow:0 0 9px rgba(175,128,255,.3); }
.st-key-quick [data-testid="stSliderTickBar"] { opacity:1 !important; color:#aeb6d9 !important; font-size:12px !important; }
@media (prefers-reduced-motion:reduce) { .st-key-quick [data-testid="stSlider"] [role="slider"] { transition:none !important; } }
/* EMOTION_MEMO_V1: 마음 메모 입력창 */
.st-key-quick [data-testid="stTextInput"] { margin-top:7px !important; }
.st-key-quick [data-testid="stTextInput"] label { font-weight:700 !important; color:#f0eaff !important; }
.st-key-quick [data-testid="stTextInput"] [data-baseweb="input"] { background:linear-gradient(125deg,rgba(35,40,82,.85),rgba(15,19,44,.96)) !important; border:1px solid rgba(171,154,255,.43) !important; border-radius:14px !important; box-shadow:inset 0 1px 0 rgba(255,255,255,.07),0 5px 18px rgba(5,7,28,.15) !important; transition:border-color .2s ease,box-shadow .2s ease !important; overflow:hidden !important; }
.st-key-quick [data-testid="stTextInput"] [data-baseweb="input"]:focus-within { border-color:#d4b4ff !important; box-shadow:0 0 0 3px rgba(171,136,255,.19),0 0 18px rgba(157,125,255,.16) !important; }
.st-key-quick [data-testid="stTextInput"] input { min-height:47px !important; background:transparent !important; color:#f0ecff !important; font-size:14px !important; padding:0 16px !important; }
.st-key-quick [data-testid="stTextInput"] input::placeholder { color:#9ca5c7 !important; opacity:1 !important; }
@media (prefers-reduced-motion:reduce) { .st-key-quick [data-testid="stTextInput"] [data-baseweb="input"] { transition:none !important; } }
/* EMOTION_SAVE_BUTTON_V1: 오늘의 별 만들기 버튼 */
.st-key-q_save .stButton > button[kind="primary"],.st-key-q_save button[kind="primary"] { width:100% !important; min-height:56px !important; border-radius:16px !important; display:flex !important; align-items:center !important; justify-content:center !important; background:linear-gradient(112deg,#6456CF 0%,#8772E9 52%,#D38BC1 100%) !important; color:#FFFFFF !important; border:1px solid rgba(230,213,255,.62) !important; box-shadow:0 8px 23px rgba(111,83,222,.29),inset 0 1px 0 rgba(255,255,255,.22) !important; font-size:15px !important; font-weight:700 !important; letter-spacing:.01em !important; text-shadow:0 1px 4px rgba(45,36,96,.34) !important; transition:filter .18s ease,transform .18s ease,box-shadow .18s ease !important; }
.st-key-q_save .stButton > button[kind="primary"]:hover,.st-key-q_save button[kind="primary"]:hover { filter:brightness(1.11) !important; transform:translateY(-2px) !important; box-shadow:0 11px 28px rgba(133,107,243,.42),0 0 18px rgba(180,150,255,.2) !important; }
.st-key-q_save .stButton > button[kind="primary"]:active,.st-key-q_save button[kind="primary"]:active { transform:translateY(0) !important; filter:brightness(.98) !important; }
.st-key-q_save .stButton > button[kind="primary"]:focus-visible,.st-key-q_save button[kind="primary"]:focus-visible { outline:2px solid #F2D5FF !important; outline-offset:3px !important; }
@media (prefers-reduced-motion:reduce) { .st-key-q_save .stButton > button[kind="primary"],.st-key-q_save button[kind="primary"] { transition:none !important; } }
/* EMOTION_RESULT_CARD_V1: 저장한 감정 별 카드 */
.st-key-quick .quick-result { --star:#ffcf4a; --star2:#b08cf0; position:relative; isolation:isolate; overflow:hidden; padding:22px 14px 20px; margin:12px 0 4px; border:1px solid rgba(190,174,255,.38); border-radius:19px; background:radial-gradient(circle at 50% 15%,color-mix(in srgb,var(--star) 16%,transparent),transparent 58%),linear-gradient(165deg,#20264b,#10162e); text-align:center; box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 12px 26px rgba(5,6,24,.24); }
.st-key-quick .quick-result-kicker { color:#cfbefd; font-size:10px; letter-spacing:.16em; font-weight:700; }
.st-key-quick .quick-result-star { position:relative; display:grid; place-items:center; width:90px; height:90px; margin:14px auto 12px; border-radius:50%; background:radial-gradient(circle at 31% 27%,#fff 0%,color-mix(in srgb,var(--star) 55%,white) 13%,var(--star) 48%,color-mix(in srgb,var(--star2) 56%,#13152e) 88%); box-shadow:0 0 0 9px color-mix(in srgb,var(--star) 8%,transparent),0 0 29px color-mix(in srgb,var(--star) 36%,transparent); }
.st-key-quick .quick-result-star::after { content:"✦"; position:absolute; font-size:17px; color:#fff3cb; top:-16px; right:-14px; text-shadow:0 0 12px #fff4b5; animation:quick-result-spark 2.4s ease-in-out infinite; }
.st-key-quick .quick-result-title { font-size:17px; font-weight:800; color:#fff8e6; line-height:1.6; }
.st-key-quick .quick-result-copy { font-size:12px; color:#c5ccec; line-height:1.75; margin-top:6px; }
.st-key-quick .quick-result-tags { display:flex; justify-content:center; flex-wrap:wrap; gap:6px; margin:12px 0 0; }
.st-key-quick .quick-result-tag { display:inline-flex; align-items:center; border-radius:999px; padding:5px 10px; border:1px solid color-mix(in srgb,var(--tag) 55%,transparent); background:color-mix(in srgb,var(--tag) 12%,transparent); color:#f1efff; font-size:11px; font-weight:600; }
.st-key-quick .quick-result-footer { margin-top:12px; color:#adb8dc; font-size:11px; }
@keyframes quick-result-spark { 0%,100% { transform:scale(.8); opacity:.65; } 50% { transform:scale(1.22); opacity:1; } }
@media (prefers-reduced-motion:reduce) { .st-key-quick .quick-result-star::after { animation:none !important; } }
/* EMOTION_INTENSITY_CHOICE_V2: 3단계 별빛 카드 */
.st-key-intensity_choice { border:1px solid rgba(174,158,255,.35) !important; border-radius:18px !important; padding:17px !important; margin:12px 0 !important; background:linear-gradient(145deg,rgba(39,43,87,.75),rgba(13,17,42,.93)) !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] { width:100% !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] > div:last-child { display:grid !important; grid-template-columns:repeat(3,minmax(0,1fr)) !important; gap:9px !important; width:100% !important; max-width:none !important; overflow:visible !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button:nth-of-type(1) { --energy:#AABADB; --energy-symbol:"✧"; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button:nth-of-type(2) { --energy:#C5A6FF; --energy-symbol:"✦"; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button:nth-of-type(3) { --energy:#FFCF6A; --energy-symbol:"✺"; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button { box-sizing:border-box !important; flex:1 1 0 !important; min-width:0 !important; max-width:none !important; width:100% !important; height:85px !important; min-height:85px !important; margin:0 !important; padding:10px 5px !important; border:1px solid #464F77 !important; border-radius:14px !important; background:linear-gradient(150deg,#202A4A,#101831) !important; color:#E8EAFF !important; box-shadow:none !important; transform:none !important; display:flex !important; flex-direction:column !important; align-items:center !important; justify-content:center !important; gap:6px !important; font-size:14px !important; text-align:center !important; font-weight:700 !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button::before { content:var(--energy-symbol) !important; display:block !important; color:var(--energy) !important; text-shadow:0 0 12px color-mix(in srgb,var(--energy) 50%,transparent) !important; font-size:27px !important; line-height:1 !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button:is([data-selected],[kind="segmented_controlActive"]) { background:linear-gradient(160deg,color-mix(in srgb,var(--energy) 23%,#161D3D),#171B39) !important; border:1px solid var(--energy) !important; color:#FFFFFF !important; box-shadow:0 0 0 1px color-mix(in srgb,var(--energy) 35%,transparent),0 6px 18px color-mix(in srgb,var(--energy) 20%,transparent) !important; transform:translateY(-1px) !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button:is([data-selected],[kind="segmented_controlActive"])::before { animation:emotion-energy-glow 2.1s ease-in-out infinite !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button:hover:not(:disabled) { filter:brightness(1.1) !important; border-color:var(--energy) !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button:focus-visible { outline:2px solid var(--energy) !important; outline-offset:3px !important; }
.st-key-intensity_choice::after { content:"✦ 나의 별빛이 얼마나 강하게 빛나고 있나요?"; display:block; padding-top:9px; color:#B5B5E5; font-size:11px; }
@keyframes emotion-energy-glow { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:.75; transform:scale(1.18); } }
@media (prefers-reduced-motion:reduce) { .st-key-intensity_choice [data-testid="stButtonGroup"] button,.st-key-intensity_choice [data-testid="stButtonGroup"] button::before { animation:none !important; transition:none !important; } }
/* EMOTION_INTENSITY_EQUAL_WIDTH_V1 */
.st-key-intensity_choice [data-testid="stButtonGroup"] { display:block !important; width:100% !important; max-width:100% !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] div:has(> button[data-variant="segmented_control"]) { display:grid !important; grid-template-columns:repeat(3,minmax(0,1fr)) !important; column-gap:10px !important; row-gap:10px !important; align-items:stretch !important; width:100% !important; min-width:0 !important; max-width:100% !important; overflow:visible !important; }
.st-key-intensity_choice [data-testid="stButtonGroup"] button[data-variant="segmented_control"] { box-sizing:border-box !important; display:flex !important; width:100% !important; min-width:0 !important; max-width:none !important; flex:none !important; margin:0 !important; }
</style>""", unsafe_allow_html=True)

LOGO = ('<svg viewBox="0 0 40 40" fill="none"><path d="M20 3l2.6 13.4L36 20l-13.4 2.6L20 37l-2.6-14.4L4 20l13.4-3.6z" fill="url(#lg)" opacity=".95"/>'
        '<path d="M20 9l1.3 9.7L31 20l-9.7 1.3L20 31l-1.3-9.7L9 20l9.7-1.3z" fill="#fff" opacity=".55"/>'
        '<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfc6ff"/><stop offset="1" stop-color="#7f8cff"/></linearGradient></defs></svg>')


# ---------- 공통 도우미 ----------
def top_emotion(e: dict) -> str:
    return e["corrected"] if e.get("corrected") in EMO else EMO[max(range(len(EMO)), key=lambda i: e["probs"][i])]


QUICK_WEIGHT = {"조금": 0.55, "보통": 0.7, "많이": 0.85}


def quick_probs(picked: list[str], level: str) -> list[float]:
    """10초 기록: 고른 감정(1~2개)과 세기로 7감정 비율 만들기
    예) 불안 '많이' → 불안 85%, 나머지 6감정이 15%를 나눠 가짐
        설렘+불안 '보통' → 설렘 42%, 불안 28%, 나머지가 30%를 나눠 가짐"""
    w = QUICK_WEIGHT[level]
    main = {picked[0]: w} if len(picked) == 1 else {picked[0]: w * .6, picked[1]: w * .4}
    rest = (1 - w) / (len(EMO) - len(main))
    return [main.get(e, rest) for e in EMO]



def limit_quick_selection():
    """Keep the last valid selection when a third emotion is clicked."""
    current = list(st.session_state.get("q_pick") or [])
    if len(current) > 2:
        st.session_state["q_pick"] = list(st.session_state.get("_q_pick_last_valid", current[:2]))
    else:
        st.session_state["_q_pick_last_valid"] = current


def streak_days(dates: set[str], today: dt.date) -> int:
    """오늘(오늘 기록이 없으면 어제)부터 거꾸로 며칠 연속 기록했는지"""
    d = today if today.isoformat() in dates else today - dt.timedelta(days=1)
    n = 0
    while d.isoformat() in dates:
        n += 1
        d -= dt.timedelta(days=1)
    return n


MILESTONES = (7, 14, 30)


def capsule_letters(entries: list[dict], today: dt.date, everything: bool = False):
    """타임캡슐 편지함
    - 기본: 7·14·30일째 되는 날 도착해서, 도착한 지 일주일이 안 된 편지 (아직 답장 안 한 것)
    - everything=True: 7일이 지난 모든 기록 (지난 편지 모두 보기)
    '오늘 도착'한 편지가 맨 앞"""
    out = []
    for e in entries:
        age = (today - dt.date.fromisoformat(e["date"])).days
        if e.get("reply") or age < MILESTONES[0]:
            continue
        fresh = any(0 <= age - m < 7 for m in MILESTONES)
        if fresh or everything:
            out.append({**e, "age": age, "today": age in MILESTONES})
    return sorted(out, key=lambda x: (not x["today"], -dt.date.fromisoformat(x["date"]).toordinal()))


def next_arrival(entries: list[dict], today: dt.date) -> int | None:
    """다음 편지가 며칠 뒤에 도착하는지"""
    waits = []
    for e in entries:
        age = (today - dt.date.fromisoformat(e["date"])).days
        waits += [m - age for m in MILESTONES if m > age]
    return min(waits) if waits else None


def month_options(entries):
    cur = dt.date.today().strftime("%Y-%m")
    return sorted({e["date"][:7] for e in entries} | {cur}, reverse=True)


def header(title: str, desc: str, months=None, pill=None, small: str = ""):
    """왼쪽: 제목 + 설명 / 오른쪽: 달 이동(‹ 2026년 10월 ›) 또는 사용자 이름"""
    left, right = st.columns([2.4, 1.15], vertical_alignment="center")
    left.markdown(f'<div class="head"><h1>{title}{f"<small>{small}</small>" if small else ""}</h1><p>{desc}</p></div>', unsafe_allow_html=True)
    nick = st.session_state.get("nickname", "")
    ym = None
    if months:
        ym = st.session_state.get("ym")
        # 달력에서 기록이 없는 달을 골랐어도 (오늘 이전이면) 그 달로 이동해요
        if ym and ym not in months and ym <= dt.date.today().strftime("%Y-%m"):
            months = sorted(set(months) | {ym}, reverse=True)
        if ym not in months:
            ym = months[0]
        i = months.index(ym)
        with right.container(key="mnav"):
            box, cal = st.columns([5, 1], gap="small", vertical_alignment="center")
            with box.container(key="mpill"):
                a, b, c = st.columns([1, 5, 1], gap="small", vertical_alignment="center")
                if a.button("‹", key="m_prev", disabled=i == len(months) - 1, help="이전 달"):
                    st.session_state["ym"] = months[i + 1]; st.rerun()
                b.markdown(f'<div class="month-pill">{(pill or (lambda s: f"{s[:4]}년 {int(s[5:])}월"))(ym)}<span>▾</span></div>', unsafe_allow_html=True)
                if c.button("›", key="m_next", disabled=i == 0, help="다음 달"):
                    st.session_state["ym"] = months[i - 1]; st.rerun()
            with cal.container(key="calpick"):
                with st.popover("📅", help="달력에서 날짜를 골라 그 달로 이동"):
                    picked = st.date_input("이동할 날짜", value=dt.date(int(ym[:4]), int(ym[5:]), 1),
                                           max_value=dt.date.today(), key=f"cal_{ym}")
                    if picked.strftime("%Y-%m") != ym:
                        st.session_state["ym"] = picked.strftime("%Y-%m"); st.rerun()
        st.session_state["ym"] = ym
    elif nick:
        right.markdown(f'<div class="user-chip">{html.escape(nick)}님 <i>{html.escape(nick[:1])}</i></div>', unsafe_allow_html=True)
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    return ym


def login_card():
    """닉네임이 없으면 시작 화면"""
    st.markdown('<div style="height:9vh"></div>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        with st.container(border=True, key="login_box"):
            st.markdown(f'<div class="welcome">{LOGO}<h2>감정의 궤적</h2><p>나의 감정이 모여, 나만의 궤도가 되다.</p></div>', unsafe_allow_html=True)
            with st.form("login", border=False):
                name = st.text_input("내 우주 이름", max_chars=20, placeholder="닉네임을 적어 주세요")
                if st.form_submit_button("시작하기") and name.strip():
                    st.session_state["nickname"] = name.strip()
                    st.rerun()
            st.markdown('<p class="note" style="text-align:center">이름으로 내 기록을 구분해요.<br>다음에도 같은 이름으로 들어오면 돼요.</p>', unsafe_allow_html=True)
    st.stop()


def nick_or_login() -> str:
    nick = st.session_state.get("nickname", "")
    if not nick:
        login_card()
    return nick


# ---------- 화면 1: 홈 (오늘의 별) ----------
# EMOTION_RESULT_CARD_V1
def show_quick_result_card(result):
    """저장 후 한 번 표시할 카드. 저장·선택 로직은 수정하지 않습니다."""
    if not result:
        return
    emotions = [e for e in result.get("emotions", []) if e in COL]
    if not emotions:
        return
    main_color = COL[emotions[0]]
    second_color = COL[emotions[1]] if len(emotions) > 1 else COL[emotions[0]]
    tags = "".join(
        f'<span class="quick-result-tag" style="--tag:{COL[e]}">✦ {html.escape(e)}</span>'
        for e in emotions
    )
    intensity = html.escape(str(result.get("intensity", "보통")))
    st.markdown(
        f'<div class="quick-result" style="--star:{main_color};--star2:{second_color}">'
        '<div class="quick-result-kicker">✦ YOUR EMOTION STAR ✦</div>'
        '<div class="quick-result-star"></div>'
        '<div class="quick-result-title">오늘의 별이 탄생했어요!</div>'
        '<div class="quick-result-copy">오늘의 감정이 나만의 우주에 기록되었어요.</div>'
        f'<div class="quick-result-tags">{tags}</div>'
        f'<div class="quick-result-footer">감정의 세기 · {intensity}　|　아래 오늘의 감정 기록에서 다시 만나요</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def page_home():
    nick = nick_or_login()
    entries = {e["date"]: e for e in db.load_entries(nick)}
    today = dt.date.today()

    # 어느 날의 일기인지 (기본: 오늘, '⋯'에서 다른 날로 바꿀 수 있어요)
    day = st.session_state.get("day", today)
    key = day.isoformat()
    old = entries.get(key)
    if st.session_state.get("draft_date") != key:
        st.session_state["draft_date"] = key
        st.session_state["draft_text"] = old["text"] if old else ""
        st.session_state["draft_fix"] = old.get("corrected") if old else None
    probs = old["probs"] if old else None

    q, by = quotes.pick(EMO, probs, day)
    sub = "당신의 감정이 모여 오늘도 특별한 궤적을 만들었어요." if old else "오늘의 감정을 기록하고, 나만의 궤도를 이어가 보세요."
    components.html(sky.hero_html(f"{day.year}년 {day.month}월 {day.day}일 {WEEK[day.weekday()]}요일", q, by, sub, probs, user=nick), height=320)
    if day != today:
        st.caption(f"✎ {day.year}년 {day.month}월 {day.day}일의 기록을 편집 중이에요.")
        if st.button("오늘 기록으로 돌아가기", key="return_to_today"):
            st.session_state.pop("day", None)
            st.session_state["draft_date"] = None
            st.session_state["rec_mode"] = "10초 기록"
            st.rerun()

    # 타임캡슐: 지난 나의 편지가 도착했으면 알려 주기
    letters = capsule_letters(list(entries.values()), today)
    if letters:
        fresh = [x for x in letters if x["today"]]
        lead = fresh[0] if fresh else letters[0]
        with st.container(border=True):
            l, r = st.columns([3, 1], vertical_alignment="center")
            title = f"{lead['age']}일 전의 내가 보낸 편지가 도착했어요" if fresh else f"아직 읽지 않은 편지가 {len(letters)}통 있어요"
            l.markdown(f'<div class="arrive"><div class="env">✉</div><div><b>{title}</b>'
                       f'<span>{int(lead["date"][5:7])}월 {int(lead["date"][8:])}일의 나에게 지금의 마음으로 답장해 보세요.</span></div></div>', unsafe_allow_html=True)
            r.page_link(PAGES["capsule"], label="편지 열어 보기 →")

    c1, c2 = st.columns([1, 1.25], gap="medium")
    with c1:
        with st.container(border=True):
            st.markdown('<div class="ctitle">오늘의 감정 비율</div>', unsafe_allow_html=True)
            if probs:
                components.html(sky.donut_html(probs), height=220)
            render_home_side(probs, EMO, COL, PAGES)
    with c2:
        with st.container(border=True):
            t, m = st.columns([1, 1.3], vertical_alignment="center")
            t.markdown('<div class="ctitle" style="margin:0">오늘의 기록</div>', unsafe_allow_html=True)
            with m.container(key="mode"):
                mode = st.segmented_control("기록 방식", ["일기 쓰기", "10초 기록"], default="10초 기록",
                                            key="rec_mode", label_visibility="collapsed")
            if mode == "10초 기록":
                with st.container(key="quick"):                    
                    picked = st.pills("지금 마음에 가장 가까운 감정 (최대 2개)", EMO, selection_mode="multi", key="q_pick", on_change=limit_quick_selection)
                    with st.container(key="intensity_choice"):
                        level = st.segmented_control("감정의 세기", ["조금", "보통", "많이"], default="보통", selection_mode="single", key="q_level", width="stretch") or "보통"
                    line = st.text_input("오늘 마음 한 줄 메모 (선택)", max_chars=60, key="q_line", placeholder="지금 마음을 짧게 남겨보세요 ✨ (선택)")
                    if st.button("오늘의 별 만들기 ✨", type="primary", key="q_save", use_container_width=True):
                        if not picked:
                            st.warning("감정을 하나 이상 골라 주세요.")
                        elif len(picked) > 2:
                            st.warning("감정은 2개까지 고를 수 있어요.")
                        else:
                            p = quick_probs(picked, level)
                            text = line.strip() or f"10초 기록 · {' + '.join(picked)} ({level})"
                            # 직접 고른 감정이라 '내가 고친 감정'으로도 남겨 둬요 (모델 재학습 데이터)
                            db.save_entry(nick, key, text, p, picked[0], kind="quick")
                            st.session_state["quick_saved_result"] = {"emotions": list(picked), "intensity": level}
                            st.toast(f"{day.month}월 {day.day}일, {' + '.join(picked)}의 별이 떴어요", icon="✨")
                            st.rerun()
                    show_quick_result_card(st.session_state.pop("quick_saved_result", None))
            else:
                text = st.text_area("일기", key="draft_text", height=190, max_chars=500, label_visibility="collapsed",
                                    placeholder="오늘 있었던 일과 그때의 마음을 편하게 적어 보세요.")
                l, r = st.columns([1, 1], vertical_alignment="center")
                with l.container(key="more"):
                    with st.popover("기록 관리 ⋯", help="날짜 변경, 감정 수정, 기록 삭제"):
                        new_day = st.date_input("날짜", value=day, max_value=today)
                        if new_day != day:
                            st.session_state["day"] = new_day; st.rerun()
                        fix = st.session_state.get("draft_fix")
                        pick = st.radio("내 느낌과 가장 가까운 감정", ["AI 결과 그대로"] + EMO, index=(EMO.index(fix) + 1) if fix in EMO else 0)
                        new_fix = None if pick == "AI 결과 그대로" else pick
                        if new_fix != fix:
                            st.session_state["draft_fix"] = new_fix
                            if old:
                                db.save_entry(nick, key, old["text"], old["probs"], new_fix, kind=old.get("kind", "diary"))
                            st.rerun()
                        if old:
                            st.divider()
                            st.caption("기록 삭제는 되돌릴 수 없어요.")
                            with st.form(key=f"delete_form_{key}", clear_on_submit=True):
                                confirm_delete = st.checkbox("이 날짜의 기록을 삭제하겠습니다")
                                if st.form_submit_button("기록 삭제"):
                                    if confirm_delete:
                                        db.delete_entry(nick, key)
                                        st.session_state["draft_date"] = None
                                        st.toast("선택한 날짜의 기록이 삭제됐어요.", icon="🗑️")
                                        st.rerun()
                                    else:
                                        st.warning("삭제 확인란을 선택해 주세요.")
                with r.container(key="save"):
                    if st.button("저장하기", type="primary"):
                        if not text.strip():
                            st.warning("일기를 먼저 적어 주세요.")
                        else:
                            with st.spinner("AI가 감정을 읽는 중..."):
                                p = old["probs"] if old and old["text"] == text.strip() else predict(text.strip())
                            db.save_entry(nick, key, text.strip(), p, st.session_state.get("draft_fix"))
                            st.toast(f"{day.month}월 {day.day}일의 행성이 생겼어요", icon="✨")
                            st.rerun()

    # 최근 감정 기록 (최근 7일)
    cells = []
    for i in range(6, -1, -1):
        d = today - dt.timedelta(days=i)
        e = entries.get(d.isoformat())
        if e:
            t = top_emotion(e)
            order = sorted(range(len(EMO)), key=lambda k: -e["probs"][k])
            c2_ = COL[EMO[order[1]]] if EMO[order[0]] == t else COL[EMO[order[0]]]
            cells.append(f'<div style="--c:{COL[t]};--c2:{c2_}"><i></i>{d.month}.{d.day:02d}<b>{t}</b></div>')
        else:
            cells.append(f'<div style="--c:#6b7099"><i class="off"></i>{d.month}.{d.day:02d}<b>-</b></div>')
    with st.container(border=True):
        n = streak_days(set(entries), today)
        badge = (f'<span class="streak">🔥 {n}일 연속 기록 중</span>' if n >= 2 else
                 '<span class="streak off">오늘 기록하면 연속 기록이 시작돼요</span>' if today.isoformat() not in entries else
                 '<span class="streak">✦ 오늘의 별이 떴어요</span>')
        st.markdown(f'<div class="ctitle">오늘의 감정 기록{badge}</div><div class="trail">' + "".join(cells) + "</div>", unsafe_allow_html=True)
        st.page_link(PAGES["calendar"], label="한 달의 감정 달력 보기 →")

    render_home_extras(entries, today, top_emotion, streak_days, PAGES)


# ---------- 화면 2: 감정 태양계 ----------
def page_solar():
    nick = nick_or_login()
    entries = db.load_entries(nick)
    ym = header("감정 태양계", "일곱 개의 감정 행성이 만들어 가는 나만의 우주를 탐험해 보세요", month_options(entries))
    render_explainer("solar")
    cur = [e for e in entries if e["date"].startswith(ym)]
    components.html(sky.solar_html(cur, f"{ym[:4]}년 {int(ym[5:])}월", height=600), height=610)


# ---------- 화면 3: 감정 유니버스 ----------
def range_label(ym: str) -> str:
    y, m = int(ym[:4]), int(ym[5:])
    return f"{y}년 {m}월 1일 - {m}월 {calendar.monthrange(y, m)[1]}일"


def page_universe():
    nick = nick_or_login()
    entries = db.load_entries(nick)
    ym = header("감정 유니버스", "당신의 감정이 만들어 낸 데이터의 별들을 탐험해 보세요. 비슷한 감정을 가진 날들이 서로 연결되어 있어요.",
                month_options(entries), pill=range_label)
    render_explainer("universe")
    cur = [e for e in entries if e["date"].startswith(ym)]
    if len(cur) < 2:
        st.info("감정이 비슷했던 날을 비교하려면 서로 다른 날짜의 기록이 2일 이상 필요해요.")
        if st.toggle("✦ 예시 감정 별지도로 사용법 체험하기", key="universe_demo"):
            y, m = map(int, ym.split("-"))
            cur = demo_universe_entries(y, m)
            st.caption("현재는 체험용 가상 기록을 보여드리고 있어요. 실제 기록이나 데이터베이스에는 저장되지 않아요.")
    components.html(sky.universe_html(cur, height=640), height=650)


# ---------- 화면 4: 우주의 기록 (월간 리포트) ----------
def page_archive():
    nick = nick_or_login()
    entries = db.load_entries(nick)
    ym = st.session_state.get("ym") or dt.date.today().strftime("%Y-%m")
    ym = header("나의 감정 리포트", "기록된 감정의 비율과 변화를 살펴보세요", month_options(entries),
                small=f"{ym[:4]}년 {int(ym[5:])}월")
    render_explainer("archive")
    y, m = int(ym[:4]), int(ym[5:])
    cur = [e for e in entries if e["date"].startswith(ym)]
    if not cur:
        st.info("이 달에는 아직 감정 기록이 없어요. 홈에서 첫 기록을 남기면 여기서 감정 변화를 살펴볼 수 있어요.")
        st.page_link(PAGES["home"], label="✦ 오늘의 감정 기록하러 가기")
        return
    if len(cur) < 3:
        st.caption(f"이 달의 기록은 {len(cur)}일이에요. 지금은 기록된 감정을 확인하고, 기록이 쌓이면 변화를 비교해 보세요.")
    components.html(sky.report_html(cur, y, m, part="top"), height=290)
    l, r = st.columns([2, 1], gap="medium")
    with l:
        components.html(sky.report_html(cur, y, m, part="bottom"), height=315)
    with r:
        with st.container(border=True, height=313):
            st.markdown('<div class="ctitle">최근 일기</div>' + "".join(
                f'<div class="rec2"><b>{int(e["date"][5:7])}월 {int(e["date"][8:])}일</b><span>{html.escape(e["text"])}</span></div>'
                for e in sorted(cur, key=lambda e: e["date"], reverse=True)[:5]), unsafe_allow_html=True)
            if st.button("전체 기록 보기", key="all_rec"):
                st.session_state["show_all"] = not st.session_state.get("show_all", False)
    if not st.session_state.get("show_all"):
        return
    with st.container(border=True):
        st.markdown('<div class="ctitle">전체 기록</div>', unsafe_allow_html=True)
        a, b = st.columns([2, 1])
        q = a.text_input("검색", placeholder="일기 내용으로 찾기 (예: 발표)", label_visibility="collapsed")
        f = b.selectbox("감정", ["모든 감정"] + EMO, label_visibility="collapsed")
        rows = sorted(entries, key=lambda e: e["date"], reverse=True)
        if q.strip():
            rows = [e for e in rows if q.strip() in e["text"]]
        if f != "모든 감정":
            rows = [e for e in rows if top_emotion(e) == f]
        st.markdown(f'<p class="note">{len(rows)}개의 기록</p>', unsafe_allow_html=True)
        out = []
        for e in rows[:60]:
            d = dt.date.fromisoformat(e["date"])
            t = top_emotion(e)
            order = sorted(range(len(EMO)), key=lambda i: -e["probs"][i])
            mix = "".join(f'<i style="flex:{e["probs"][i]:.3f};background:{COL[EMO[i]]}"></i>' for i in order if e["probs"][i] >= .01)
            out.append(f'<div class="arc"><div class="d"><b>{d.month}월 {d.day}일</b><small>{d.year} · {WEEK[d.weekday()]}요일</small></div>'
                       f'<div><span class="pill" style="background:{COL[t]}26;color:{COL[t]}">{t}</span>'
                       f'<span class="note">{" · ".join(f"{EMO[i]} {round(e["probs"][i]*100)}%" for i in order[:3])}</span>'
                       f'<div class="mix">{mix}</div><p>{html.escape(e["text"])}</p></div></div>')
        st.markdown("".join(out) or '<p class="note">찾는 기록이 없어요.</p>', unsafe_allow_html=True)


# ---------- 화면 5: 감정 타임캡슐 ----------
def page_capsule():
    nick = nick_or_login()
    entries = db.load_entries(nick)
    today = dt.date.today()
    header("감정 타임캡슐", "7일, 14일, 30일 전의 내가 보낸 편지가 도착해요. 지금의 마음으로 그때의 나에게 답장해 보세요.")
    render_explainer("capsule")
    allmode = st.session_state.get("cap_all", False)
    letters = capsule_letters(entries, today, everything=allmode)
    fresh_n = len(capsule_letters(entries, today))
    replied = sorted([e for e in entries if e.get("reply")], key=lambda e: e.get("reply_at") or "", reverse=True)
    wait = next_arrival(entries, today)
    nxt = (today + dt.timedelta(days=wait)) if wait else None
    k1, k2, k3 = st.columns(3)
    k1.markdown(f'<div class="kpi" style="--c:#ffcf6a"><b>{fresh_n}통</b><span>이번 주 도착한 편지</span></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi" style="--c:#b3a6ff"><b>{len(replied)}통</b><span>주고받은 편지</span></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi"><b>{f"{nxt.month}월 {nxt.day}일" if nxt else "-"}</b><span>{"다음 편지 도착" + (f" (D-{wait})" if wait else "") if nxt else "기록을 남기면 7일 뒤 편지가 도착해요"}</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)

    t1, t2 = st.tabs([f"도착한 편지 {fresh_n}", f"주고받은 편지 {len(replied)}"])
    with t1:
        st.toggle("지난 기록 모두 보기 (7일이 지난 모든 기록에 답장할 수 있어요)", key="cap_all")
        if not letters:
            first = f"{nxt.month}월 {nxt.day}일" if nxt else "7일 뒤"
            st.markdown(f'<div class="empty" style="min-height:280px"><div><b>✉</b>아직 도착한 편지가 없어요.<br>'
                        f'오늘 남긴 기록은 7일, 14일, 30일 뒤에 편지가 되어 돌아와요.<br>다음 편지는 <u>{first}</u>에 도착해요.</div></div>',
                        unsafe_allow_html=True)
        else:
            def label(x):
                d = dt.date.fromisoformat(x["date"])
                return f"{'✦ 오늘 도착 · ' if x['today'] else ''}{d.month}월 {d.day}일 · {x['age']}일 전 · {top_emotion(x)}"
            pick = st.selectbox("열어 볼 편지", range(len(letters)), format_func=lambda i: label(letters[i]), label_visibility="collapsed")
            x = letters[pick]
            d = dt.date.fromisoformat(x["date"])
            t = top_emotion(x)
            order = sorted(range(len(EMO)), key=lambda i: -x["probs"][i])
            mix = "".join(f'<i style="flex:{x["probs"][i]:.3f};background:{COL[EMO[i]]}"></i>' for i in order if x["probs"][i] >= .01)
            left, right = st.columns([1.5, 1], gap="large")
            with left:
                st.markdown(f'<div class="letter" style="--c:{COL[t]}"><div class="from">{x["age"]}일 전의 내가 보낸 편지</div>'
                            f'<div class="when">{d.year}년 {d.month}월 {d.day}일 {WEEK[d.weekday()]}요일</div>'
                            f'<div class="body">{html.escape(x["text"])}</div><div class="mix">{mix}</div>'
                            f'<div class="tags">{" · ".join(f"{EMO[i]} {round(x["probs"][i]*100)}%" for i in order[:3])}</div></div>',
                            unsafe_allow_html=True)
                st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
                reply = st.text_area("지금의 내가 그때의 나에게", key=f"reply_{x['date']}", height=130, max_chars=500,
                                     placeholder="그때의 나에게 하고 싶은 말을 적어 보세요.")
                st.caption("이렇게 시작해도 좋아요 · “그때 걱정했던 일은…” · “지금의 나는…” · “그때의 나에게 고마운 건…”")
                if st.button("답장 보내기 ✉", type="primary", key=f"send_{x['date']}"):
                    if not reply.strip():
                        st.warning("답장을 먼저 적어 주세요.")
                    else:
                        db.save_reply(nick, x["date"], reply.strip(), today.isoformat())
                        st.toast("답장이 그때의 나에게 닿았어요", icon="💌")
                        st.rerun()
            with right:
                with st.container(border=True):
                    st.markdown('<div class="ctitle">그때와 지금</div>', unsafe_allow_html=True)
                    now = next((e for e in entries if e["date"] == today.isoformat()), None)
                    then_c2 = COL[EMO[order[1]]]
                    if now:
                        nt = top_emotion(now)
                        no = sorted(range(len(EMO)), key=lambda i: -now["probs"][i])
                        sim = float(A.cosine_matrix(A.matrix([x, now]))[0, 1])
                        st.markdown(f'<div class="then-now"><div style="--c:{COL[t]};--c2:{then_c2}"><div class="orb"></div><b>{t}</b><small>{d.month}월 {d.day}일</small></div>'
                                    f'<div class="arrow">→</div>'
                                    f'<div style="--c:{COL[nt]};--c2:{COL[EMO[no[1]]]}"><div class="orb"></div><b>{nt}</b><small>오늘</small></div></div>'
                                    f'<div class="sim">그때와 지금의 감정은 <b>{round(sim*100)}%</b> 닮았어요.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="then-now"><div style="--c:{COL[t]};--c2:{then_c2}"><div class="orb"></div><b>{t}</b><small>{d.month}월 {d.day}일</small></div>'
                                    f'<div class="arrow">→</div><div style="--c:#6b7099;--c2:#2a2f55"><div class="orb" style="box-shadow:none;opacity:.5"></div><b>?</b><small>오늘</small></div></div>'
                                    '<div class="sim">오늘의 감정을 기록하면 그때와 얼마나 달라졌는지 보여 줄게요.</div>', unsafe_allow_html=True)
                        st.page_link(PAGES["home"], label="오늘 기록하러 가기 →")
                    same = [e for e in entries if top_emotion(e) == t and e["date"] > x["date"]]
                    st.markdown(f'<div class="note" style="margin:14px 0 6px;padding-top:12px;border-top:1px solid var(--line)">'
                                f'{"그 뒤로 " + t + "이(가) 가장 컸던 날이 " + str(len(same)) + "번 더 있었어요." if same else "그 뒤로는 " + t + "이(가) 가장 큰 날이 없었어요."}</div>',
                                unsafe_allow_html=True)
    with t2:
        if not replied:
            st.markdown('<div class="empty" style="min-height:220px"><div><b>💌</b>아직 주고받은 편지가 없어요.<br>도착한 편지에 답장하면 여기에 쌓여요.</div></div>',
                        unsafe_allow_html=True)
        for e in replied:
            d = dt.date.fromisoformat(e["date"])
            r = dt.date.fromisoformat(e["reply_at"]) if e.get("reply_at") else None
            t = top_emotion(e)
            st.markdown(f'<div class="thread"><div class="bubble past"><small>{d.month}월 {d.day}일의 나 · <span style="color:{COL[t]}">{t}</span></small>{html.escape(e["text"])}</div>'
                        f'<div class="bubble now"><small>{f"{r.month}월 {r.day}일의 나" if r else "지금의 나"}</small>{html.escape(e["reply"])}</div></div>',
                        unsafe_allow_html=True)


# ---------- 화면 목록 (기본 메뉴는 숨기고 사이드바에 직접 그려요) ----------
def page_calendar_route():
    """선택한 날짜의 일기로 이동합니다. 저장된 데이터를 직접 바꾸지는 않아요."""
    def open_for_editing(chosen_date):
        st.session_state["day"] = chosen_date
        st.session_state["draft_date"] = None
        st.session_state["rec_mode"] = "일기 쓰기"
        st.switch_page(PAGES["home"])
    page_calendar(on_edit=open_for_editing)


PAGES = {
    "home": st.Page(page_home, title="홈", icon=":material/home:", url_path="home", default=True),
    "calendar": st.Page(page_calendar_route, title="감정 달력", icon=":material/calendar_month:", url_path="calendar"),
    "gallery": st.Page(page_gallery, title="별자리 갤러리", icon=":material/auto_awesome:", url_path="gallery"),
    "solar": st.Page(page_solar, title="감정 태양계", icon=":material/trip_origin:", url_path="solar"),
    "universe": st.Page(page_universe, title="감정 유니버스", icon=":material/hub:", url_path="universe"),
    "archive": st.Page(page_archive, title="나의 감정 리포트", icon=":material/insights:", url_path="archive"),
    "capsule": st.Page(page_capsule, title="감정 타임캡슐", icon=":material/mail:", url_path="capsule"),
}
nav = st.navigation(list(PAGES.values()), position="hidden")
current = next(k for k, p in PAGES.items() if p.title == nav.title)

with st.sidebar:
    st.markdown(f'<div class="brand">{LOGO}<div><b>감정의 궤적</b><span>EMOTION TRACE</span></div></div>', unsafe_allow_html=True)
    st.markdown(f'<style>.st-key-nav_{current} a {{ background:linear-gradient(135deg,rgba(139,123,255,.3),rgba(90,80,210,.14)) !important;'
                f' border-color:rgba(165,155,255,.4) !important; }} .st-key-nav_{current} a p {{ color:#fff !important; font-weight:700; }}</style>',
                unsafe_allow_html=True)
    # 태양계·유니버스는 기존 링크와 코드를 유지하되 기본 메뉴에서는 숨깁니다.
    for k in ("home", "calendar", "archive", "gallery", "capsule"):
        with st.container(key=f"nav_{k}"):
            st.page_link(PAGES[k])
    st.markdown('<div class="side-gap"></div>', unsafe_allow_html=True)
    nick = st.session_state.get("nickname", "")
    with st.container(key="side_bottom"):
        with st.popover("⚙  설정", width="stretch"):
            if nick:
                st.markdown(f"**{html.escape(nick)}**님의 하늘")
                mine = db.load_entries(nick)
                st.caption(f"지금까지 {len(mine)}개의 기록")
            if db.is_demo():
                st.caption("체험 모드예요. 기록은 이 창에만 잠깐 저장돼요.")
                if nick and st.button("예시 기록 채우기", help="두 달 치 예시 일기 31개를 실제 모델로 분석해서 채워요"):
                    bar = st.progress(0.0, text="예시 일기를 분석하는 중...")
                    today = dt.date.today()
                    for i, (ago, text) in enumerate(SAMPLES):
                        db.save_entry(nick, (today - dt.timedelta(days=ago)).isoformat(), text, predict(text), None)
                        bar.progress((i + 1) / len(SAMPLES), text=f"예시 일기를 분석하는 중... {i+1}/{len(SAMPLES)}")
                    st.session_state["draft_date"] = None
                    st.rerun()
        if nick and st.button("⏻  로그아웃"):
            for k in ("nickname", "draft_date", "draft_text", "draft_fix", "day", "ym"):
                st.session_state.pop(k, None)
            st.rerun()

nav.run()