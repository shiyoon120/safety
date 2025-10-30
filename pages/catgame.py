import streamlit as st
import random
import time

st.set_page_config(page_title="🔥 화재 예방 게임 🔥", page_icon="🔥", layout="wide")

# --------------------------
# 스타일링: 배경 빨간색, 텍스트 흰색
# --------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #ffcccc;
        color: white;
    }
    .fire {
        font-size: 30px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔥 귀여운 화재예방 게임 🔥")

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
# 게임 시작/종료 함수
# --------------------------
def start_game():
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.game_active = True

def end_game():
    st.session_state.game_active = False
    st.success(f"🔥 게임 종료! 최종 점수: {st.session_state.score} 🔥")

# --------------------------
# 게임 시작 버튼
# --------------------------
if not st.session_state.game_active:
    if st.button("게임 시작"):
        start_game()
else:
    # --------------------------
    # 막대바 슬라이더
    # --------------------------
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
            display += f"<div class='fire'>{'&nbsp;'*fire_pos}🔥</div>"
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
        st.success(f"🔥 {score_increment}개의 불을 막았어요! 레벨: {st.session_state.level}")
    else:
        end_game()

    # 점수와 레벨 표시
    st.write(f"현재 점수: {st.session_state.score}")
    st.write(f"현재 레벨: {st.session_state.level}")

    # 다시하기 버튼
    if st.button("다시하기"):
        start_game()
