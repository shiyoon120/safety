import streamlit as st
import random
import time
from PIL import Image
import requests
from io import BytesIO

# --------------------------
# 고양이 이미지
# --------------------------
cat_url = "https://cataas.com/cat"
response = requests.get(cat_url)
img = Image.open(BytesIO(response.content))

st.title("🔥 귀여운 고양이 화재예방 게임 🔥")
st.image(img, caption="우리 고양이와 함께 불을 막아요!", use_column_width=True)

# --------------------------
# 게임 상태 초기화
# --------------------------
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'game_active' not in st.session_state:
    st.session_state.game_active = False

# --------------------------
# 게임 시작 / 종료
# --------------------------
def start_game():
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.game_active = True

def end_game():
    st.session_state.game_active = False
    st.success(f"게임 종료! 최종 점수: {st.session_state.score}")

# --------------------------
# 게임 시작 버튼
# --------------------------
if not st.session_state.game_active:
    if st.button("게임 시작"):
        start_game()
else:
    barrier = st.slider("막대바 위치 조절", min_value=0, max_value=100, value=50)
    placeholder = st.empty()

    # 레벨에 따라 불 개수와 속도 조정
    fire_count = min(5, st.session_state.level + 2)
    speed = max(0.05, 0.3 - st.session_state.level * 0.02)

    fires = [random.randint(0, 100) for _ in range(fire_count)]
    score_increment = 0

    # --------------------------
    # 애니메이션 반복
    # --------------------------
    for step in range(100, -1, -5):
        display = ""
        for fire_pos in fires:
            display += f"<div style='font-size:30px; text-align:center;'>{'&nbsp;'*fire_pos}🔥</div>"
        placeholder.markdown(display, unsafe_allow_html=True)
        time.sleep(speed)

    # --------------------------
    # 충돌 체크
    # --------------------------
    for fire_pos in fires:
        if abs(barrier - fire_pos) < 10:
            score_increment += 1

    if score_increment > 0:
        st.session_state.score += score_increment
        st.session_state.level = 1 + st.session_state.score // 5
        st.success(f"성공! {score_increment}개의 불을 막았어요! 레벨: {st.session_state.level}")
    else:
        end_game()

    st.write(f"현재 점수: {st.session_state.score}")
    st.write(f"현재 레벨: {st.session_state.level}")

    if st.button("다시하기"):
        start_game()
