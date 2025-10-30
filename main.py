import streamlit as st

st.set_page_config(page_title="여행 안전 프로그램", page_icon="✈️")

# --- 세션 상태 초기화 ---
if "page" not in st.session_state:
    st.session_state.page = "main"

# --- 페이지 전환 함수 ---
def go_to(page_name):
    st.session_state.page = page_name

# --- 메인 화면 ---
if st.session_state.page == "main":
    st.title("✈️ 여행 안전 프로그램")
    st.write("여행 중 안전을 지키기 위한 정보를 알아보세요!")

    if st.button("위험 지역 안내"):
        go_to("risk_area")
    if st.button("위험 상황 대처법"):
        go_to("emergency")
    if st.button("여행 전 안전 점검"):
        go_to("checklist")

# --- 위험 지역 안내 ---
elif st.session_state.page == "risk_area":
    st.header("⚠️ 위험 지역 안내")
    st.write("최근 위험 국가나 여행 자제 지역 정보를 제공합니다.")
    if st.button("🏠 메인으로 돌아가기"):
        go_to("main")

# --- 위험 상황 대처법 ---
elif st.session_state.page == "emergency":
    st.header("🚨 위험 상황 대처법")
    st.write("""
    - 소매치기를 당했다면 즉시 현지 경찰에 신고하세요.
    - 여권 분실 시 대사관 또는 영사관에 방문하세요.
    - 테러나 폭동 발생 시 인파를 피해 안전한 건물 안으로 대피하세요.
    """)
    if st.button("🏠 메인으로 돌아가기"):
        go_to("main")

# --- 여행 전 안전 점검 ---
elif st.session_state.page == "checklist":
    st.header("🧳 여행 전 안전 점검")
    st.write("""
    - 여권 및 비자 확인
    - 여행자 보험 가입
    - 응급약품 챙기기
    - 현지 응급 연락처 메모하기
    """)
    if st.button("🏠 메인으로 돌아가기"):
        go_to("main")
