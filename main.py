# safetrip_app.py
import streamlit as st
import random

st.set_page_config(page_title="SafeTrip: 여행 전 안전 점검 도우미", layout="centered")
st.title("🌍 SafeTrip: 여행 전 안전 점검 도우미")

# --- 샘플 데이터 ---
places = {
    "캄보디아": ["최근 범죄 발생 증가", "치안 불안정", "야간 외출 주의"],
    "일본": ["지진 가능성", "일부 지역 방사능 모니터링 필요"],
    "태국": ["소매치기·사기 주의", "야간 유흥가 주의"],
    "미국": ["도심 지역 일부 범죄 주의", "총기 사고 주의"],
    "한국": ["대체로 안전, 기상·교통 유의"]
}

safety_tips = [
    "여권 사본을 따로 보관하세요.",
    "공항에서 낯선 사람의 짐을 들어주지 마세요.",
    "현지 비상연락망(대사관/영사관)을 메모하세요.",
    "숙소 주변의 CCTV 및 대피로를 확인하세요."
]

# --- 세션 상태 초기화 (페이지가 새로고침 되어도 정보 유지) ---
if "show_info" not in st.session_state:
    st.session_state.show_info = False

# 사용자 입력 UI (원래 화면 그대로)
country = st.selectbox("여행할 나라를 선택하세요 ✈️", list(places.keys()))
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("안전 정보 확인하기"):
        # 버튼을 누르면 정보 표시 상태로 전환
        st.session_state.show_info = True

with col2:
    if st.button("초기화"):
        st.session_state.show_info = False

st.markdown("---")

# --- 안전 정보 표시 영역 ---
if st.session_state.show_info:
    st.subheader(f"🗺️ {country} 여행 안전 정보")
    for risk in places.get(country, ["해당 국가의 정보가 없습니다. 일반 안전 수칙을 확인하세요."]):
        st.warning(risk)

    st.subheader("📋 여행 전 기본 안전 수칙")
    for tip in random.sample(safety_tips, 2):
        st.info(tip)

    st.markdown("---")

    # --- 여기서 스위치(체크박스)로 대처법 토글 ---
    # 체크박스는 Streamlit에서 토글(스위치처럼) 동작하며 상태가 유지됩니다.
    show_emergency = st.checkbox("🚨 위험 상황 대처법 보기", value=False, key=f"emergency_{country}")

    if show_emergency:
        st.markdown("### 🚨 위험 상황 대처법")
        st.markdown(
            """
            **1) 소매치기 / 강도**
            - 즉시 안전한 곳으로 이동하고, 숙소 프런트나 현지 경찰에 신고하세요.
            - 여권 분실 시 한국 대사관/영사관에 연락하세요.

            **2) 자연재해 (지진, 태풍 등)**
            - 실내: 탁자 밑으로 들어가 머리를 보호하세요.
            - 실외: 전봇대·간판 등 위험물에서 멀리 떨어지세요.

            **3) 테러 / 폭동**
            - 인파를 피해 안전한 건물 안으로 대피하세요.
            - 대사관/언론/공식 채널 공지를 확인하고 지시에 따르세요.

            **4) 응급 연락처**
            - 한국인 여행객 긴급 연락: 해당 지역 한국대사관/영사관
            - 출국 전 대사관 전화번호는 메모해 두세요.
            """
        )

    # (선택) 추가 안내: "더 자세한 도움 보기" 같은 링크나 버튼을 여기에 추가할 수 있음.
else:
    st.info("위 '안전 정보 확인하기' 버튼을 눌러 선택한 국가의 안전 정보를 확인하세요.")
