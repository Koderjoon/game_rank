import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="전치제 금손 3종 랭킹", page_icon="👑", layout="centered")

# 🚨 스트림릿 확대/축소 방지 완벽 무력화 (minimum-scale=0.3 추가로 축소 허용!)
components.html(
    """
    <script>
    const viewport = window.parent.document.querySelector('meta[name=viewport]');
    if (viewport) {
        viewport.content = 'width=device-width, initial-scale=1.0, minimum-scale=0.3, maximum-scale=5.0, user-scalable=yes';
    }
    </script>
    """,
    height=0,
    width=0
)

# --- CSS 스타일링 ---
st.markdown("""
    <style>
    /* 전체 화면 가로 폭을 모바일에 꽉 차게 고정 (가운데 정렬) */
    .block-container {
        width: 100% !important;
        max-width: 450px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    /* 전체 배경 다크 모드 */
    .stApp { background-color: #0e1117 !important; }
    
    /* 메인 타이틀 및 서브타이틀 */
    .title-glow { 
        text-align: center !important; 
        color: #ffffff !important; 
        text-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b !important; 
        font-family: 'Arial Black', sans-serif !important; 
        font-size: 34px !important; 
        margin-bottom: 10px !important; 
        line-height: 1.2 !important;
        white-space: nowrap !important;
    }
    .subtitle-glow { 
        text-align: center !important; 
        color: #00ffcc !important; 
        text-shadow: 0 0 8px #00ffcc !important; 
        font-weight: bold !important; 
        font-size: 16px !important; 
        margin-bottom: 30px !important; 
        white-space: nowrap !important;
    }
    
    /* 종목별 제목 */
    .game-title-water { color: #00d2ff !important; text-align: center !important; text-shadow: 0 0 10px #00d2ff !important; font-size: 38px !important; font-weight: 900 !important; margin-bottom: 15px !important; white-space: nowrap !important; }
    .game-title-dart { color: #ff3366 !important; text-align: center !important; text-shadow: 0 0 10px #ff3366 !important; font-size: 38px !important; font-weight: 900 !important; margin-bottom: 15px !important; white-space: nowrap !important; }
    .game-title-click { color: #ffd32a !important; text-align: center !important; text-shadow: 0 0 10px #ffd32a !important; font-size: 38px !important; font-weight: 900 !important; margin-bottom: 15px !important; white-space: nowrap !important; }

    /* 🚨 HTML 표(Table) 강제 고정 스타일링 (데이터 길이에 따라 안 변함!) */
    table { 
        width: 100% !important; 
        table-layout: fixed !important; /* 표 너비 요동침 방지 */
        border-collapse: collapse; 
        margin-top: 5px; 
        margin-bottom: 20px; 
    }
    
    /* 각 열의 가로 비율을 고정 (순위 25%, 이름 45%, 기록 30%) */
    th:nth-child(1), td:nth-child(1) { width: 25% !important; }
    th:nth-child(2), td:nth-child(2) { width: 45% !important; overflow: hidden; text-overflow: ellipsis; }
    th:nth-child(3), td:nth-child(3) { width: 30% !important; }

    th { background-color: #262730 !important; color: #ffffff !important; font-size: 17px !important; padding: 12px 5px !important; text-align: center !important; border-bottom: 2px solid #ffffff !important; white-space: nowrap !important; }
    td { background-color: #1e1e1e !important; color: #ffffff !important; font-weight: bold !important; padding: 15px 5px !important; text-align: center !important; border-bottom: 1px solid #333333 !important; white-space: nowrap !important; }
    
    /* 1,2,3위 글씨 크기 조정 (모바일에 딱 맞게 최적화) */
    tbody tr:nth-child(1) td { color: #ffd700 !important; font-size: 26px !important; text-shadow: 0 0 10px #ffd70055 !important; }
    tbody tr:nth-child(2) td { color: #c0c0c0 !important; font-size: 22px !important; }
    tbody tr:nth-child(3) td { color: #cd7f32 !important; font-size: 18px !important; }
    
    /* 새로고침 버튼 디자인 */
    div.stButton > button:first-child {
        background-color: #262730 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
        border-radius: 10px !important;
        border: 1px solid #444444 !important;
        margin-bottom: 20px !important;
    }
    div.stButton > button:hover {
        background-color: #ff4b4b !important;
        border-color: #ff4b4b !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 메인 제목 영역
st.markdown("<div class='title-glow'>👑 금손 3종 경기 실시간 랭킹 👑</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-glow'>컵과 다트로 증명하는 우리 학교 신의 손끝!</div>", unsafe_allow_html=True)

# 3. 새로고침 버튼 (상단)
if st.button("새로고침"):
    st.cache_data.clear()
    st.rerun()

# ==========================================
# 🚨 실제 구글 시트 CSV 링크
URL_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQV-2yxMLZLhS3qZEFNVGO4UsOS0vIl0SbDOQJ9smkAt5TEfY5h-3h4puEl5ROBotqOqxuv2-NX6mxd/pub?output=csv"
# ==========================================

# 4. 데이터 불러오기 함수
@st.cache_data(ttl=5)
def get_data_from_gsheets(url):
    try:
        df = pd.read_csv(url).fillna("")
        return df
    except:
        return None

df_total = get_data_from_gsheets(URL_SHEET)

# 5. 데이터 렌더링
if df_total is not None and len(df_total.columns) >= 9:
    # 데이터 분리 및 복사
    data_water = df_total.iloc[:, 0:3].copy()
    data_dart  = df_total.iloc[:, 3:6].copy()
    data_click = df_total.iloc[:, 6:9].copy()

    # 열 이름 강제 설정
    data_water.columns = ["순위", "이름(소속)", "무게(g)"]
    data_dart.columns  = ["순위", "이름(소속)", "합산점수"]
    data_click.columns = ["순위", "이름(소속)", "클릭수"]

    # --- 1번 종목 ---
    st.divider()
    st.markdown("<div class='game-title-water'>💧 양치컵 절대 감각</div>", unsafe_allow_html=True)
    st.markdown(data_water.to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- 2번 종목 ---
    st.divider()
    st.markdown("<div class='game-title-dart'>🎯 다트 양궁</div>", unsafe_allow_html=True)
    st.markdown(data_dart.to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- 3번 종목 ---
    st.divider()
    st.markdown("<div class='game-title-click'>🖱️ 15초 광클</div>", unsafe_allow_html=True)
    st.markdown(data_click.to_html(index=False, escape=False), unsafe_allow_html=True)
    st.divider()

else:
    st.error("데이터를 불러올 수 없습니다. 구글 시트 링크나 열 개수를 확인해 주세요!")
