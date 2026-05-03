import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정 (가로로 넓게)
st.set_page_config(page_title="전치제 금손 3종 랭킹", page_icon="👑", layout="wide")

# --- CSS 스타일링 ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-glow { text-align: center; color: #fff; text-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b; font-family: 'Arial Black', sans-serif; font-size: 45px !important; margin-bottom: 5px; }
    .subtitle-glow { text-align: center; color: #00ffcc; text-shadow: 0 0 8px #00ffcc; font-weight: bold; font-size: 22px !important; margin-bottom: 30px; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 30px; }
    th { background-color: #262730; color: #ffffff; font-size: 20px !important; padding: 12px; text-align: center !important; border-bottom: 2px solid #ffffff; }
    td { background-color: #1e1e1e; color: #ffffff; font-weight: bold; padding: 15px; text-align: center !important; border-bottom: 1px solid #333333; }
    /* 1,2,3위 글자 크기와 색상 강조 */
    tbody tr:nth-child(1) td { color: #ffd700 !important; font-size: 30px !important; text-shadow: 0 0 10px #ffd70055; }
    tbody tr:nth-child(2) td { color: #c0c0c0 !important; font-size: 24px !important; }
    tbody tr:nth-child(3) td { color: #cd7f32 !important; font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-glow'>👑 금손 3종 경기 실시간 랭킹 👑</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='subtitle-glow'>컵과 다트로 증명하는 우리 학교 신의 손끝!</h4>", unsafe_allow_html=True)
st.divider()

# ==========================================
# 🚨 여기에 방금 복사한 구글 시트 CSV 링크 '단 1개'만 넣으세요!
URL_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQV-2yxMLZLhS3qZEFNVGO4UsOS0vIl0SbDOQJ9smkAt5TEfY5h-3h4puEl5ROBotqOqxuv2-NX6mxd/pub?output=csv"
# ==========================================

# 구글 시트 데이터를 불러오는 함수 (5초마다 새로고침)
@st.cache_data(ttl=5)
def load_data(url):
    try:
        # 빈칸(NaN)이 있으면 에러가 나지 않도록 빈 문자열("")로 채웁니다.
        df = pd.read_csv(url).fillna("")
        return df
    except:
        return None

# 전체 데이터 한 번에 불러오기
df_total = load_data(URL_SHEET)

if df_total is not None and len(df_total.columns) >= 9:
    # 위치를 기준으로 데이터를 3개씩 자릅니다 (0~2열, 3~5열, 6~8열)
    data_water = df_total.iloc[:, 0:3]
    data_dart  = df_total.iloc[:, 3:6]
    data_click = df_total.iloc[:, 6:9]

    # 가로로 3등분하여 배치
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<h2 style='color: #3498db; text-align: center; text-shadow: 2px 2px 4px #000;'>💧 양치컵 절대 감각</h2>", unsafe_allow_html=True)
        st.markdown(data_water.to_html(index=False, escape=False), unsafe_allow_html=True)

    with col2:
        st.markdown("<h2 style='color: #e74c3c; text-align: center; text-shadow: 2px 2px 4px #000;'>🎯 덴탈 스나이퍼</h2>", unsafe_allow_html=True)
        st.markdown(data_dart.to_html(index=False, escape=False), unsafe_allow_html=True)

    with col3:
        st.markdown("<h2 style='color: #f1c40f; text-align: center; text-shadow: 2px 2px 4px #000;'>🖱️ 15초 광클</h2>", unsafe_allow_html=True)
        st.markdown(data_click.to_html(index=False, escape=False), unsafe_allow_html=True)

else:
    st.error("구글 시트 링크를 잘못 입력했거나, 시트의 열(Column) 개수가 9개가 아닙니다. 확인해주세요!")