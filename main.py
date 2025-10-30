# 파일명: safetrip_app.py
import streamlit as st
import random

st.title("🌍 SafeTrip: 여행 전 안전 점검 도우미")

places = {
    "캄보디아": ["최근 범죄 발생 증가", "치안 불안정", "야간 외출 주의"],
    "일본": ["지진 가능성", "방사능 위험 지역 점검 필요"],
    "태국": ["소매치기 많음", "야간 유흥가 주의"],
    "미국": ["총기 사건 주의", "야간 도심 혼자 이동 금지"],
    "한국": ["안전함 👍", "기상 상황만 주의"]
}

safety_tips = [
    "여권 사본을 따로 보관하세요.",
    "공항에서 낯선 사람의 짐을 들어주지 마세요.",
    "현지 비상연락망을 메모해 두세요.",
    "숙소 주변 CCTV 및 대피로를 확인하세요."
]

country = st.selectbox("여행할 나라를 선택하세요 ✈️", list(places.keys()))

if st.button("안전 정보 확인하기"):
    st.subheader(f"🗺️ {country} 여행 안전 정보")
    for risk in places[country]:
        st.warning(risk)

    st.subheader("📋 여행 전 기본 안전 수칙")
    for tip in random.sample(safety_tips, 2):
        st.info(tip)

    if st.toggle("위험 상황 대처법 보기 🚨"):
        st.markdown("""
        **긴급 상황 시 행동 요령**
        1️⃣ 가까운 대사관 또는 영사관에 즉시 연락  
        2️⃣ 숙소 관리자나 현지 경찰에 신고  
        3️⃣ 신변이 위험하면 대중이 많은 장소로 이동
        """)

st.caption("ⓒ 2025 SafeTrip Project")
