import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="전치제 금손 3종 랭킹", page_icon="👑", layout="centered")

# --- CSS 스타일링 ---
st.markdown("""
    <style>
    /* 전체 배경 다크 모드 */
    .stApp { background-color: #0e1117 !important; }
    
    /* 타이틀 및 서브타이틀 */
    .title-glow { text-align: center !important; color: #ffffff !important; text-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b, 0 0 30px #ff4b4b !important; font-family: 'Arial Black', sans-serif !important; font-size: 38px !important; margin-bottom: 10px !important; line-height: 1.2 !important; }
    .subtitle-glow { text-align: center !important; color: #00ffcc !important; text-shadow: 0 0 8px #00ffcc !important; font-weight: bold !important; font-size: 18px !important; margin-bottom: 20px !important; }
    
    /* 종목별 제목 (크기 확대 42px) */
    .game-title-water { color: #00d2ff !important; text-align: center !important; text-shadow: 0 0 10px #00d2ff !important; font-size: 42px !important; font-weight: 900 !important; margin-bottom: 15px !important; }
    .game-title-dart { color: #ff3366 !important; text-align: center !important; text-shadow: 0 0 10px #ff3366 !important; font-size: 42px !important; font-weight: 900 !important; margin-bottom: 15px !important; }
    .game-title-click { color: #ffd32a !important; text-align: center !important; text-shadow: 0 0 10px #ffd32a !important; font-size: 42px !important; font-weight: 900 !important; margin-bottom: 15px !important; }

    /* HTML 표(Table) 스타일링 (두 줄 방지) */
    table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 20px; }
    th { background-color: #262730 !important; color: #ffffff !important; font-size: 22px !important; padding: 15px !important; text-align: center !important; border-bottom: 2px solid #ffffff !important; white-space: nowrap !important; }
    td { background-color: #1e1e1e !important; color: #ffffff !important; font-weight: bold !important; padding: 18px !important; text-align: center !important; border-bottom: 1px solid #333333 !important; white-space: nowrap !important; }
    
    /* 1,2,3위 글자 강조 */
    tbody tr:nth-child(1) td { color: #ffd700 !important; font-size: 32px !important; text-shadow: 0 0 10px #ffd70055 !important; }
    tbody tr:nth-child(2) td { color: #c0c0c0 !important; font-size: 26px !important; }
    tbody tr:nth-child(3) td { color: #cd7f32 !important; font-size: 22px !important; }
    
    /* 상단 새로고침 버튼 디자인 */
    div.stButton > button:first-child {
        background-color: #262730 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        height: 55px !important;
        width: 100% !important;
        border-radius: 10px !important;
        border: 1px solid #444444 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 15px !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #ff4b4b !important;
        border-color: #ff4b4b !important;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 메인 타이틀
st.markdown("<div class='title-glow'>👑 금손 3종 경기 실시간 랭킹 👑</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-glow'>컵과 다트로 증명하는 우리 학교 신의 손끝!</div>", unsafe_allow_html=True)

# 3. 수동 새로고침 버튼을 상단에 배치
if st.button("새로고침"):
    st.cache_data.clear() # 캐시 강제 초기화
    st.rerun() # 새로고침

# ==========================================
# 🚨 유저의 실제 구글 시트 CSV 링크 적용 완료!
URL_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQV-2yxMLZLhS3qZEFNVGO4UsOS0vIl0SbDOQJ9smkAt5TEfY5h-3h4puEl5ROBotqOqxuv2-NX6mxd/pub?output=csv"
# ==========================================

# 4. 구글 시트 데이터 불러오기 함수
@st.cache_data(ttl=5)
def get_data_from_gsheets(url):
    try:
        return pd.read_csv(url).fillna("")
    except:
        return None

df_total = get_data_from_gsheets(URL_SHEET)

# 5. 세로로 렌더링
if df_total is not None and len(df_total.columns) >= 9:
    
    data_water = df_total.iloc[:, 0:3].copy()
    data_dart  = df_total.iloc[:, 3:6].copy()
    data_click = df_total.iloc[:, 6:9].copy()

    # 열 이름 통일 ('오차(g)' 대신 '무게(g)' 적용)
    data_water.columns = ["순위", "이름(소속)", "무게(g)"]
    data_dart.columns  = ["순위", "이름(소속)", "합산점수"]
    data_click.columns = ["순위", "이름(소속)", "클릭수"]

    # --- 1번 종목 ---
    st.divider()
    st.markdown("<div class='game-title-water'>💧 양치컵 절대 감각</div>", unsafe_allow_html=True)
    st.markdown(data_water.to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- 2번 종목 ---
    st.divider()
    st.markdown("<div class='game-title-dart'>🎯 덴탈 스나이퍼</div>", unsafe_allow_html=True)
    st.markdown(data_dart.to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- 3번 종목 ---
    st.divider()
    st.markdown("<div class='game-title-click'>🖱️ 15초 광클</div>", unsafe_allow_html=True)
    st.markdown(data_click.to_html(index=False, escape=False), unsafe_allow_html=True)
    st.divider()

else:
    st.error("구글 시트 데이터가 비어있거나, 열(Column) 개수가 9개 미만입니다. 구글 시트 형식을 다시 확인해주세요!")
