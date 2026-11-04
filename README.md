# 감정의 궤적 (EMOTION TRACE)

나의 감정이 모여, 나만의 궤도가 되다. 일기를 쓰면 AI가 7가지 감정의 비율을 읽고, 하루하루가 별과 행성이 되는 웹 서비스.

- 감정 모델: KLUE-RoBERTa를 KOTE 데이터(평가자 5명의 투표 비율)로 학습 → https://huggingface.co/dmsdltmd/night-sky-emotion
- 감정 7종: 기쁨, 설렘, 평온, 지침, 슬픔, 불안, 분노

## 화면
| 화면 | 하는 일 |
|---|---|
| 홈 (오늘의 별) | 오늘의 문장, 감정 비율 도넛, 10초 감정 기록·AI 일기 저장, 최근 7일의 감정, 기록 탐색 |
| 감정 달력 (프론트엔드 추가) | 날짜별 감정 색상·기록 확인, 해당 날짜의 일기 수정 화면으로 이동 |
| 별자리 갤러리 (프론트엔드 추가) | 월간 별자리 작품 감상·PNG 저장, 실제 DB에 저장하지 않는 미리보기 |
| 감정 태양계 (원본 유지) | 태양 = 그 달의 나, 행성 = 감정 7개 (자주 느낀 감정일수록 안쪽 궤도, 비율이 클수록 큰 행성) |
| 감정 유니버스 (원본 유지) | 감정이 비슷한 날은 가까이 (PCA 2D/3D), 유사한 감정의 날 목록, 별지도 체험 미리보기 |
| 나의 감정 리포트 (원래 '우주의 기록') | 월간 리포트: 감정 분포, 감정 변화 추이, 감정 조합, 크게 변화한 날, 최근 일기, 전체 기록 검색 |
| 감정 타임캡슐 (원본 유지) | 7·14·30일 전의 기록이 편지로 도착, 지금의 내가 답장, 그때와 지금의 감정 비교 |

홈에서는 일기 대신 **10초 기록**(감정 1~2개 + 세기 + 한 줄)도 할 수 있고, 연속 기록 일수가 표시돼요.

## 파일
| 파일 | 역할 |
|---|---|
| `app.py` | 7개 화면을 연결하는 Streamlit 앱 진입점과 기존 기능 |
| `emotion_calendar.py` | 감정 달력 (프론트엔드 추가) |
| `emotion_gallery.py` | 별자리 갤러리 (프론트엔드 추가) |
| `emotion_home.py`, `emotion_guides.py` | 홈 탐색과 도움말 UI |
| `model.py` | Hugging Face에서 모델 불러오기, 감정 예측 |
| `db.py` | Supabase에 일기 저장/불러오기 (키가 없으면 체험 모드) |
| `analysis.py` | 별 위치(PCA), 비슷한 날(코사인 유사도), 전환점(JSD), 월간 비교 |
| `sky.py` + `templates/sky.html` | 밤하늘 그림 (HTML/JS) |
| `supabase_schema.sql` | Supabase 표 만드는 SQL |

## 내 컴퓨터에서 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```
`.streamlit/secrets.toml`이 없으면 체험 모드로 실행돼요 (기록이 브라우저 창에만 잠깐 저장).

## 배포 (GitHub + Streamlit Cloud)
1. Supabase: 새 프로젝트 → SQL Editor에 `supabase_schema.sql` 붙여넣고 Run → Project Settings > API에서 URL과 anon key 복사
2. GitHub: 이 폴더를 저장소로 올리기 (`secrets.toml`은 올리지 않기, `.gitignore`에 들어 있음)
3. share.streamlit.io → Create app → 저장소 / 브랜치 `main` / 파일 `app.py` 선택
4. Advanced settings → Secrets 칸에 아래 붙여넣기 → Deploy
   ```toml
   SUPABASE_URL = "https://xxxx.supabase.co"
   SUPABASE_KEY = "eyJ..."
   ```
5. 이후 GitHub에 올리면 웹이 자동으로 업데이트돼요.

## 참고
- 감정 결과는 글에서 보이는 감정의 비율이에요. 심리 상태를 진단하지 않아요.
- 시연용 설정이라 Supabase 키를 아는 사람은 누구나 읽고 쓸 수 있어요.
