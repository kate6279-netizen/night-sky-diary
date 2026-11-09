"""감정의 궤적 — 홈·타임캡슐 UI 스타일. 저장 및 AI 기능은 변경하지 않습니다."""
import streamlit as st

HOME_STYLE = """<style>
.st-key-et_explore [data-testid="stVerticalBlockBorderWrapper"]{background:linear-gradient(150deg,rgba(30,37,75,.87),rgba(12,19,43,.97))!important;border:1px solid rgba(171,171,244,.18)!important;border-radius:19px!important;box-shadow:0 14px 35px rgba(3,5,23,.16),inset 0 1px 0 rgba(255,255,255,.05)!important}
.st-key-et_explore [data-testid="stPageLink"] a{background:rgba(129,122,232,.10)!important}
.st-key-et_explore [data-testid="stPageLink"] a:hover{background:rgba(140,129,239,.22)!important}
.quick-result{box-shadow:0 20px 42px rgba(5,8,31,.20),inset 0 1px 0 rgba(255,255,255,.07)!important}
.arrive{border-radius:14px}
</style>"""

CAPSULE_STYLE = """<style>
.kpi{position:relative;overflow:hidden;padding:20px 20px 18px!important;background:linear-gradient(140deg,rgba(35,40,88,.93),rgba(12,18,44,.96))!important;border:1px solid rgba(181,170,255,.21)!important;border-radius:18px!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 15px 34px rgba(4,5,25,.13)}
.kpi::before{content:"";position:absolute;top:0;left:0;width:64%;height:1px;background:linear-gradient(90deg,var(--c,#b8a7ff),transparent);opacity:.64}
.kpi b{font-size:28px!important;letter-spacing:-.04em}
.kpi span{display:block;margin-top:5px;line-height:1.6;color:#bec5e5!important}
.letter{overflow:hidden;padding:32px 30px 27px!important;border-radius:20px!important;border:1px solid rgba(203,182,255,.34)!important;background:radial-gradient(circle at 100% 0%,rgba(176,137,239,.15),transparent 45%),linear-gradient(155deg,#282342 0%,#1b1e3e 50%,#121c38 100%)!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.085),0 20px 40px rgba(4,5,23,.20)}
.letter::before{left:0!important;right:0!important;height:3px!important;background:linear-gradient(90deg,transparent,var(--c,#c6adff),#d9c7ff,transparent)!important}
.letter::after{content:"✉";position:absolute;right:23px;top:19px;color:rgba(225,211,255,.26);font-size:29px}
.letter .from{color:#e1c4ff!important;font-weight:700!important;letter-spacing:.07em!important}
.letter .when{margin-top:7px!important;color:#b5c1e2!important}
.letter .body{font-family:"Nanum Myeongjo","Malgun Gothic",serif!important;color:#f8f3ff!important;font-size:17px!important;line-height:2.05!important;padding:22px 0 18px;border-top:1px solid rgba(190,180,245,.15);border-bottom:1px solid rgba(190,180,245,.15)}
.letter .mix{height:6px!important;margin-top:21px!important;max-width:none!important;border-radius:15px;overflow:hidden}
.letter .tags{margin-top:9px;color:#c8c7e5!important}
.then-now{padding:15px 8px 12px;border-radius:16px;background:radial-gradient(circle at 40% 30%,rgba(145,116,230,.15),transparent 65%),rgba(15,19,41,.35)}
.then-now .orb{width:54px!important;height:54px!important;box-shadow:0 0 0 5px color-mix(in srgb,var(--c) 11%,transparent),0 0 23px color-mix(in srgb,var(--c) 55%,transparent)!important}
.then-now .arrow{color:#c3b4fa!important;font-size:23px!important}
.sim{font-size:12px!important;line-height:1.8}
.stTabs [data-baseweb="tab-list"]{gap:9px!important}
.stTabs button[data-baseweb="tab"]{border-radius:12px 12px 0 0!important;color:#babde3!important;padding:10px 20px!important;font-weight:700!important}
.stTabs button[data-baseweb="tab"][aria-selected="true"]{color:#fff!important;background:rgba(135,117,226,.16)!important}
.thread{gap:12px;padding:22px 0!important}
.bubble{border-radius:16px!important;line-height:1.85!important;padding:16px 19px!important;box-shadow:0 12px 26px rgba(5,6,29,.12)}
.bubble.past{background:linear-gradient(140deg,rgba(71,72,122,.26),rgba(27,33,67,.6))!important}
.bubble.now{background:linear-gradient(135deg,rgba(126,100,223,.32),rgba(170,123,207,.17))!important}
@media(max-width:680px){.letter{padding:22px 18px!important}.bubble{max-width:90%;font-size:12px}.kpi{padding:15px 12px!important}.kpi b{font-size:21px!important}}
</style>"""

def render_home_theme() -> None:
    st.markdown(HOME_STYLE, unsafe_allow_html=True)

def render_capsule_theme() -> None:
    st.markdown(CAPSULE_STYLE, unsafe_allow_html=True)
