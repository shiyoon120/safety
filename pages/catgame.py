# 파일명: firemeow_app.py
import streamlit as st
import random

st.title("🐾 불이야냥! (Fire Meow!) 🧯")

fires = ["주방", "전기 콘센트", "쓰레기통", "촛불", "캠핑장"]
tips = {
    "주방": "요리할 때 자리를 비우면 안돼냥!",
    "전기 콘센트": "코드 여러 개 꽂으면 위험하다냥!",
    "쓰레기통": "유리병이 햇빛에 반사되면 불날 수 있다냥!",
    "촛불": "촛불은 꺼지지 않으면 위험하다냥!",
    "캠핑장": "모닥불은 꼭 꺼지고 확인하라냥!"
}

fire = random.choice(fires)
st.subheader(f"🔥 {fire}에서 불이 났다냥!! 어서 불을 꺼보자냥!")

if "success" not in st.session_state:
    st.session_state.success = 0
    st.session_state.round = 1

if st.button("💧 물풍선 던지기!"):
    st.session_state.success += 1
    st.success("불이 조금 약해졌다냥!")
    st.session_state.round += 1

if st.button("🔥 그냥 보기"):
    st.warning("불이 점점 커지고 있다냥!")
    st.session_state.round += 1

if st.session_state.round > 3:
    if st.session_state.success >= 2:
        st.balloons()
        st.success("🎉 불이 완전히 꺼졌다냥!")
    else:
        st.error("😭 아깝다냥! 불이 완전히 꺼지진 않았지만, 다음엔 더 잘할거다냥!")
    st.info(f"🐾 원인은 **{fire}** 때문이래냥!\n📘 예방법: {tips[fire]}")
    if st.button("다시 하기 🔁"):
        st.session_state.success = 0
        st.session_state.round = 1
        st.experimental_rerun()
