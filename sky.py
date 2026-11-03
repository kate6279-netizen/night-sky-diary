"""별자리 화면(HTML/JS) 만들기

Python에서 계산한 별 위치·일기 내용을 JSON으로 묶어서 templates/sky.html 안에 넣어요.
별을 누르면 일기가 뜨는 건 전부 JS 안에서 처리돼서 Python과 주고받을 필요가 없어요.
"""
import json
import calendar
from pathlib import Path

import numpy as np
import analysis as A

COLORS = ["#ffcf4a", "#ff8fb1", "#6fd3a8", "#9aa6b8", "#5b84f0", "#b08cf0", "#f0645a"]  # EMO 순서
TEMPLATE = (Path(__file__).parent / "templates" / "sky.html").read_text(encoding="utf-8")
MAP_TEMPLATE = (Path(__file__).parent / "templates" / "sky_map.html").read_text(encoding="utf-8")


PLANET_JS = (Path(__file__).parent / "templates" / "planet.js").read_text(encoding="utf-8")


def _render(data: dict, height: int, template: str = TEMPLATE) -> str:
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")  # 일기에 </script>가 있어도 안전하게
    # __PLANET_JS__ 자리에는 공통 행성 그리기 코드를 넣어요
    return template.replace("__PLANET_JS__", PLANET_JS).replace("__DATA__", js).replace("__HEIGHT__", str(height))


def _stars(entries, X, xy=None, sims=None):
    out = []
    for i, e in enumerate(entries):
        s = {"date": e["date"], "day": int(e["date"][8:10]), "text": e["text"],
             "p": [round(float(v), 4) for v in X[i]], "corrected": e.get("corrected")}
        if xy is not None:
            s["x"], s["y"] = float(xy[i, 0]), float(xy[i, 1])
        if sims is not None:
            s["similar"] = sims[i]
        out.append(s)
    return out


def map_html(entries: list[dict], height: int = 880, extra: dict | None = None) -> str:
    """탐험 화면: 감정이 비슷한 날은 가까이, 비슷한 날끼리 선으로 연결
    extra: 화면 위 숫자 카드에 쓸 값 (예: {"pos_delta": 12.0} = 긍정 감정이 지난달보다 12%p 늘었음)"""
    X = A.matrix(entries)
    dates = [e["date"] for e in entries]
    data = {"mode": "map", "emo": A.EMO, "colors": COLORS, "seed": 7,
            "stars": _stars(entries, X, A.layout(X), A.similar_days(X, dates)),
            # 지도에서는 별마다 가장 비슷한 날 2개까지 이어요 (유사도 0.6 이상)
            "links": A.links(X, threshold=0.6, k=2), "extra": extra or {}}
    return _render(data, height, MAP_TEMPLATE)


def poster_html(entries: list[dict], year: int, month: int, height: int = 640, preview: bool = False) -> str:
    """월간 포스터: 한 달의 별을 날짜 순서로 잇기"""
    X = A.matrix(entries)
    dates = [e["date"] for e in entries]
    mean = A.month_mean(entries)
    top = int(mean.argmax()) if len(entries) else -1
    sub = f"{len(entries)}일의 별 · 가장 많이 빛난 감정 {A.EMO[top]}" if top >= 0 else "아직 별이 없어요"
    data = {"mode": "poster", "emo": A.EMO, "colors": COLORS, "seed": year * 13 + month,
            "year": year, "month": month, "preview": bool(preview),
            "days": calendar.monthrange(year, month)[1], "top": top,
            "title": f"{month}월의 하늘", "subtitle": sub,
            "stars": _stars(entries, X, sims=A.similar_days(X, dates)), "links": []}
    return _render(data, height)


STAR_TEMPLATE = (Path(__file__).parent / "templates" / "star.html").read_text(encoding="utf-8")


def star_html(probs: list[float], label: str = "", height: int = 300) -> str:
    """오늘의 별 미리보기: 감정 비율로 별 하나 그리기"""
    data = {"p": [round(float(v), 4) for v in probs], "colors": COLORS, "label": label}
    return _render(data, height, STAR_TEMPLATE)


# ---------- 감정의 궤적 화면들 ----------
def _tpl(name):
    return (Path(__file__).parent / "templates" / name).read_text(encoding="utf-8")


SOLAR_TEMPLATE, UNIVERSE_TEMPLATE, REPORT_TEMPLATE = _tpl("solar.html"), _tpl("universe.html"), _tpl("report.html")
HERO_TEMPLATE, DONUT_TEMPLATE = _tpl("hero.html"), _tpl("donut.html")

DESC = {
    "기쁨": "밝고 따뜻한 에너지가 가득했던 날들이에요.",
    "설렘": "무언가를 기다리며 두근거렸던 날들이에요.",
    "평온": "고요하고 안정적인 에너지가 흐르던 날들이에요.",
    "지침": "많이 애쓰느라 몸과 마음이 무거웠던 날들이에요.",
    "슬픔": "마음이 조금 가라앉아 있던 날들이에요.",
    "불안": "걱정이 마음을 오래 붙잡고 있던 날들이에요.",
    "분노": "마음이 뜨겁게 끓어올랐던 날들이에요.",
}
MESSAGE = {
    "기쁨": "오늘은 긍정적인 에너지가 가득한 하루였어요.",
    "설렘": "무언가를 기다리는 두근거림이 느껴지는 하루였어요.",
    "평온": "고요하고 안정적인 에너지가 흐르는 하루였어요.",
    "지침": "많이 애쓴 하루였어요. 오늘은 조금 쉬어 가도 괜찮아요.",
    "슬픔": "마음이 조금 가라앉은 하루였어요. 그런 날도 있어요.",
    "불안": "걱정이 마음을 오래 붙잡은 하루였어요.",
    "분노": "마음이 뜨겁게 끓어오른 하루였어요.",
}


def hero_html(date_label: str, quote: str, author: str, sub: str, probs: list[float] | None, user: str = "", height: int = 320) -> str:
    """홈 맨 위: 날짜 + 오늘의 문장 / 오늘의 행성 / 오늘의 감정 카드"""
    top = second = -1
    conf = 0.0
    msg = ""
    if probs:
        order = sorted(range(len(probs)), key=lambda i: -probs[i])
        top, second, conf = order[0], order[1], float(probs[order[0]])
        msg = MESSAGE[A.EMO[top]]
    data = {"emo": A.EMO, "colors": COLORS, "date": date_label, "quote": quote, "author": author, "sub": sub,
            "top": top, "second": second, "conf": round(conf, 4), "msg": msg, "user": user}
    return _render(data, height, HERO_TEMPLATE)


def donut_html(probs: list[float] | None, height: int = 170) -> str:
    """오늘의 감정 비율 도넛"""
    return _render({"emo": A.EMO, "colors": COLORS, "p": [round(float(v), 4) for v in probs] if probs else None},
                   height, DONUT_TEMPLATE)


def solar_html(entries: list[dict], label: str, height: int = 600) -> str:
    """감정 태양계: 태양 = 그 달의 나, 행성 = 감정 7개 (자주 느낀 감정일수록 안쪽 궤도), 행성 크기 = 평균 비율"""
    X = A.matrix(entries)
    mean = A.month_mean(entries)
    tops = [int(x.argmax()) for x in X]
    planets = []
    for k in range(len(A.EMO)):
        days = [{"date": e["date"], "text": e["text"], "v": round(float(X[i][k]), 4)}
                for i, e in enumerate(entries) if tops[i] == k]
        planets.append({"k": k, "share": round(float(mean[k]), 4), "count": len(days), "days": days})
    data = {"emo": A.EMO, "colors": COLORS, "desc": DESC, "label": label, "total": len(entries),
            "sun": int(mean.argmax()) if len(entries) else -1, "planets": planets}
    return _render(data, height, SOLAR_TEMPLATE)


def universe_html(entries: list[dict], height: int = 640) -> str:
    """감정 유니버스: 감정이 비슷한 날은 가까이(PCA 2D/3D) + 비슷한 날 연결 + 유사한 감정의 날 목록"""
    X = A.matrix(entries)
    dates = [e["date"] for e in entries]
    stars = _stars(entries, X, A.layout(X), A.similar_days(X, dates, top=5))
    for s, p in zip(stars, A.layout3(X)):
        s["x3"], s["y3"], s["z3"] = (round(float(v), 4) for v in p)
    data = {"emo": A.EMO, "colors": COLORS, "stars": stars, "links": A.links(X, threshold=0.6, k=2)}
    return _render(data, height, UNIVERSE_TEMPLATE)


def report_html(cur: list[dict], year: int, month: int, part: str = "top", height: int = 330) -> str:
    """우주의 기록 - 월간 리포트: 감정 분포, 감정 변화 추이, 감정 조합, 크게 변화한 날, 최근 일기"""
    X = A.matrix(cur)
    # part="top": 감정 분포 + 감정 변화 추이 / part="bottom": 감정 조합 + 크게 변화한 날
    data = {"emo": A.EMO, "colors": COLORS, "days": len(cur), "year": year, "month": month, "part": part,
            "mean": [round(float(v), 4) for v in A.month_mean(cur)],
            "series": [{"date": e["date"], "p": [round(float(v), 4) for v in X[i]]} for i, e in enumerate(cur)],
            "pairs": [list(p) for p in A.co_occurring(cur)], "turns": A.turning_points(cur, top=4),
            "recent": [{"date": e["date"], "text": e["text"]} for e in sorted(cur, key=lambda e: e["date"], reverse=True)[:5]]}
    return _render(data, height, REPORT_TEMPLATE)
