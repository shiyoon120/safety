import streamlit as st

st.set_page_config(page_title="여행 안전 프로그램", page_icon="✈️", layout="centered")

# -------------------------------
# 페이지 상태 저장 (이게 핵심!)
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

# 페이지 이동 함수
def change_page(page_name):
    st.session_state.page = page_name

# -------------------------------
# 메인 화면
# -------------------------------
if st.session_state.page == "main":
    st.title("✈️ 여행 안전 프로그램")
    st.write("안전한 여행을 위한 정보를 제공합니다. 아래 항목을 선택하세요!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌍 위험 지역 안내"):
            change_page("risk")
    with col2:
        if st.button("🚨 위험 상황 대처법"):
            change_page("emergency")

    st.markdown("---")
    if st.button("🧳 여행 전 안전 점검표 보기"):
        change_page("checklist")

# -------------------------------
# 위험 지역 안내
# -------------------------------
elif st.session_state.page == "risk":
    st.header("⚠️ 최근 여행 자제 지역")
    st.write("""
    - 이스라엘, 가자지구 : 무력 충돌 위험
    - 미얀마, 수단 : 내전으로 인한 안전 우려
    - 캄보디아 일부 지역 : 보이스피싱 및 인신매매 조직 주의
    - 멕시코 일부 지역 : 마약 관련 범죄 다발
    """)
    st.markdown("---")
    if st.button("🏠 메인으로 돌아가기"):
        change_page("main")

# -------------------------------
# 위험 상황 대처법 (수정된 부분!!)
# -------------------------------
elif st.session_state.page == "emergency":
    st.header("🚨 위험 상황 대처법")
    st.write("""
    여행 중 예상치 못한 사고가 발생했을 때는 다음을 기억하세요.

    **1️⃣ 소매치기 / 강도**
    - 즉시 안전한 곳으로 이동하고, 호텔 프런트나 현지 경찰에 신고하세요.
    - 여권 분실 시 한국 대사관 또는 영사관에 연락하세요.

    **2️⃣ 자연재해 (지진, 태풍 등)**
    - 건물 안에 있을 경우 탁자 아래로 들어가 머리를 보호하세요.
    - 외부에 있을 경우 전봇대나 간판에서 멀리 떨어지세요.

    **3️⃣ 테러 / 폭동**
    - 인파를 피하고 안전한 건물 안으로 대피하세요.
    - 현지 뉴스나 대사관 안내를 반드시 확인하세요.
    """)
    st.markdown("---")
    if st.button("🏠 메인으로 돌아가기"):
        change_page("main")

# -------------------------------
# 여행 전 안전 점검표
# -------------------------------
elif st.session_state.page == "checklist":
    st.header("🧳 여행 전 안전 점검표")
    st.write("""
    - ✅ 여권 및 비자 확인
    - ✅ 여행자 보험 가입
    - ✅ 응급약품 챙기기
    - ✅ 현지 응급 연락처 메모하기
    - ✅ 귀중품 분산 보관하기
    """)
    st.markdown("---")
    if st.button("🏠 메인으로 돌아가기"):
        change_page("main")
