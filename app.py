import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="전치제 금손 3종 랭킹", page_icon="👑", layout="centered")

# --- CSS 스타일링 ---
st.markdown("""
    <style>
    /* 전체 배경을 강제로 다크 모드로 고정 */
    .stApp { background-color: #0e1117 !important; }
    
    /* 메인 타이틀 */
    .title-glow { text-align: center !important; color: #ffffff !important; text-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b, 0 0 30px #ff4b4b !important; font-family: 'Arial Black', sans-serif !important; font-size: 38px !important; margin-bottom: 10px !important; line-height: 1.2 !important; }
    .subtitle-glow { text-align: center !important; color: #00ffcc !important; text-shadow: 0 0 8px #00ffcc !important; font-weight: bold !important; font-size: 18px !important; margin-bottom: 40px !important; }
    
    /* 🚨 종목별 제목 강제 스타일링 (스트림릿 간섭 차단용) */
    .game-title-water { color: #00d2ff !important; text-align: center !important; text-shadow: 0 0 10px #00d2ff !important; font-size: 28px !important; font-weight: 900 !important; margin-bottom: 10px !important; }
    .game-title-dart { color: #ff3366 !important; text-align: center !important; text-shadow: 0 0 10px #ff3366 !important; font-size: 28px !important; font-weight: 900 !important; margin-bottom: 10px !important; }
    .game-title-click { color: #ffd32a !important; text-align: center !important; text-shadow: 0 0 10px #ffd32a !important; font-size: 28px !important; font-weight: 900 !important; margin-bottom: 10px !important; }

    /* HTML 표(Table) 스타일링 */
    table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 10px; }
    th { background-color: #262730 !important; color: #ffffff !important; font-size: 20px !important; padding: 15px !important; text-align: center !important; border-bottom: 2px solid #ffffff !important; }
    td { background-color: #1e1e1e !important; color: #ffffff !important; font-weight: bold !important; padding: 18px !important; text-align: center !important; border-bottom: 1px solid #333333 !important; }
    
    /* 1,2,3위 글자 크기와 색상 강조 */
    tbody tr:nth-child(1) td { color: #ffd700 !important; font-size: 30px !important; text-shadow: 0 0 10px #ffd70055 !important; }
    tbody tr:nth-child(2) td { color: #c0c0c0 !important; font-size: 24px !important; }
    tbody tr:nth-child(3) td { color: #cd7f32 !important; font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# 2. 메인 타이틀 (h1 태그 대신 div 태그를 사용하여 간섭 차단)
st.markdown("<div class='title-glow'>👑 금손 3종 경기 실시간 랭킹 👑</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-glow'>컵과 다트로 증명하는 우리 학교 신의 손끝!</div>", unsafe_allow_html=True)

# ==========================================
# 🚨 구글 시트 CSV 링크 (단 1개)
URL_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQV-2yxMLZLhS3qZEFNVGO4UsOS0vIl0SbDOQJ9smkAt5TEfY5h-3h4puEl5ROBotqOqxuv2-NX6mxd/pub?output=csv"
# ==========================================

# 3. 구글 시트 데이터 불러오기 함수 (5초마다 새로고침)
@st.cache_data(ttl=5)
def load_data(url):
    try:
        df = pd.read_csv(url).fillna("")
        return df
    except:
        return None

df_total = load_data(URL_SHEET)

# 4. 세로로 나란히 렌더링
if df_total is not None and len(df_total.columns) >= 9:
    
    # 데이터 분리
    data_water = df_total.iloc[:, 0:3].copy()
    data_dart  = df_total.iloc[:, 3:6].copy()
    data_click = df_total.iloc[:, 6:9].copy()

    # 열(Column) 이름 강제 고정 ('.1', '.2' 제거)
    data_water.columns = ["순위", "이름(소속)", "오차(g)"]
    data_dart.columns  = ["순위", "이름(소속)", "합산점수"]
    data_click.columns = ["순위", "이름(소속)", "클릭수"]

    # --- 1번 종목 (네온 블루) ---
    st.divider()
    st.markdown("<div class='game-title-water'>💧 양치컵 절대 감각</div>", unsafe_allow_html=True)
    st.markdown(data_water.to_html(index=False, escape=False), unsafe_allow_html=True)
    st.write("")

    # --- 2번 종목 (네온 핑크) ---
    st.divider()
    st.markdown("<div class='game-title-dart'>🎯 덴탈 스나이퍼</div>", unsafe_allow_html=True)
    st.markdown(data_dart.to_html(index=False, escape=False), unsafe_allow_html=True)
    st.write("")

    # --- 3번 종목 (네온 옐로우) ---
    st.divider()
    st.markdown("<div class='game-title-click'>🖱️ 15초 광클</div>", unsafe_allow_html=True)
    st.markdown(data_click.to_html(index=False, escape=False), unsafe_allow_html=True)
    st.divider()

else:
    st.error("구글 시트 링크를 잘못 입력했거나, 시트의 열(Column) 개수가 9개가 아닙니다. 확인해주세요!")
