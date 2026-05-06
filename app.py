import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="전치제 금손 3종 랭킹", page_icon="👑", layout="centered")

# 🚨 확대/축소 허용 스크립트
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
    /* 🚨 제목 위 여백(padding-top)을 4rem으로 늘려 충분한 공간 확보 */
    .block-container {
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
        padding-top: 4rem !important; 
        padding-bottom: 2rem !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    .stApp { background-color: #0e1117 !important; }
    
    /* 메인 타이틀 및 서브타이틀 (1줄 고정) */
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
    
    /* 새로고침 안내 문구 */
    .refresh-notice {
        text-align: center !important;
        color: #ffeb3b !important;
        font-size: 13px !important;
        font-weight: bold !important;
        margin-bottom: 25px !important;
        background-color: rgba(255, 235, 59, 0.1);
        padding: 10px;
        border-radius: 8px;
        border: 1px dashed #ffeb3b;
        line-height: 1.5;
    }

    /* 탭 메뉴 스타일 */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 14px !important;
        font-weight: bold !important;
    }
    
    /* 종목별 제목 (1줄 고정) */
    .game-title-water { color: #00d2ff !important; text-align: center !important; text-shadow: 0 0 10px #00d2ff !important; font-size: 34px !important; font-weight: 900 !important; margin-bottom: 10px !important; white-space: nowrap !important; }
    .game-title-dart { color: #ff3366 !important; text-align: center !important; text-shadow: 0 0 10px #ff3366 !important; font-size: 34px !important; font-weight: 900 !important; margin-bottom: 10px !important; white-space: nowrap !important; }
    .game-title-click { color: #ffd32a !important; text-align: center !important; text-shadow: 0 0 10px #ffd32a !important; font-size: 34px !important; font-weight: 900 !important; margin-bottom: 10px !important; white-space: nowrap !important; }

    /* 표 스타일 (가로폭 유연) */
    table { 
        width: 100% !important; 
        table-layout: auto !important; 
        border-collapse: collapse; 
        margin-top: 5px; 
        margin-bottom: 20px; 
    }
    
    th { background-color: #262730 !important; color: #ffffff !important; font-size: 16px !important; padding: 10px 5px !important; text-align: center !important; border-bottom: 2px solid #ffffff !important; white-space: nowrap !important; }
    td { background-color: #1e1e1e !important; color: #ffffff !important; font-weight: bold !important; padding: 12px 5px !important; text-align: center !important; border-bottom: 1px solid #333333 !important; white-space: nowrap !important; }
    
    /* 순위 강조 */
    tbody tr:nth-child(1) td { color: #ffd700 !important; font-size: 24px !important; text-shadow: 0 0 10px #ffd70055 !important; }
    tbody tr:nth-child(2) td { color: #c0c0c0 !important; font-size: 20px !important; }
    tbody tr:nth-child(3) td { color: #cd7f32 !important; font-size: 17px !important; }
    </style>
""", unsafe_allow_html=True)

# 2. 상단 제목 및 안내
st.markdown("<div class='title-glow'>👑 실시간 랭킹 👑</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-glow'>컵과 다트로 증명하는 우리 학교 신의 손끝!</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='refresh-notice'>
        🔄 최신 랭킹을 보려면 페이지를 새로고침 해주세요!<br>
        <span style='font-size: 11px; font-weight: normal; color: #dddddd;'>서버 환경에 따라 1~2분 정도 반영이 늦을 수 있습니다.</span>
    </div>
""", unsafe_allow_html=True)

# 🚨 구글 시트 CSV 링크
URL_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQV-2yxMLZLhS3qZEFNVGO4UsOS0vIl0SbDOQJ9smkAt5TEfY5h-3h4puEl5ROBotqOqxuv2-NX6mxd/pub?output=csv"

@st.cache_data(ttl=5)
def get_data_from_gsheets(url):
    try:
        df = pd.read_csv(url).fillna("")
        return df
    except:
        return None

df_total = get_data_from_gsheets(URL_SHEET)

# 3. 탭 구성
tabs = st.tabs(["전체 종목", "양치컵 333g", "다트 양궁", "15초 광클"])

if df_total is not None and len(df_total.columns) >= 9:
    # 데이터 분리
    data_water = df_total.iloc[:, 0:3].copy()
    data_dart  = df_total.iloc[:, 3:6].copy()
    data_click = df_total.iloc[:, 6:9].copy()

    # 열 이름 설정
    data_water.columns = ["순위", "이름(소속)", "무게(g)"]
    data_dart.columns  = ["순위", "이름(소속)", "합산점수"]
    data_click.columns = ["순위", "이름(소속)", "클릭수"]

    # --- 탭 1: 전체 종목 (TOP 3만) ---
    with tabs[0]:
        st.markdown("<div class='game-title-water'>💧 양치컵 333g</div>", unsafe_allow_html=True)
        st.markdown(data_water.head(3).to_html(index=False, escape=False), unsafe_allow_html=True)
        
        st.divider()
        st.markdown("<div class='game-title-dart'>🎯 다트 양궁</div>", unsafe_allow_html=True)
        st.markdown(data_dart.head(3).to_html(index=False, escape=False), unsafe_allow_html=True)
        
        st.divider()
        st.markdown("<div class='game-title-click'>🖱️ 15초 광클</div>", unsafe_allow_html=True)
        st.markdown(data_click.head(3).to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- 탭 2: 양치컵 (전체) ---
    with tabs[1]:
        st.markdown("<div class='game-title-water'>💧 양치컵 333g 전체 순위</div>", unsafe_allow_html=True)
        st.markdown(data_water.to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- 탭 3: 다트 양궁 (전체) ---
    with tabs[2]:
        st.markdown("<div class='game-title-dart'>🎯 다트 양궁 전체 순위</div>", unsafe_allow_html=True)
        st.markdown(data_dart.to_html(index=False, escape=False), unsafe_allow_html=True)

    # --- 탭 4: 15초 광클 (전체) ---
    with tabs[3]:
        st.markdown("<div class='game-title-click'>🖱️ 15초 광클 전체 순위</div>", unsafe_allow_html=True)
        st.markdown(data_click.to_html(index=False, escape=False), unsafe_allow_html=True)

else:
    st.error("데이터를 불러올 수 없습니다. 구글 시트 링크나 형식을 확인해 주세요!")
