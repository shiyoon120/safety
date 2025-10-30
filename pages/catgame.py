import streamlit as st
import random
import time

st.set_page_config(page_title="🔥 소방대 출동! 🔥", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #ff6666;
    color: white;
}
.big-button {
    font-size:24px;
    height:60px;
    width:100px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔥 소방대 출동! 🔥")

# --------------------------
# 상태 초기화
# --------------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 1
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'fires' not in st.session_state:
    st.session_state.fires = []
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'time_left' not in st.session_state:
    st.session_state.time_left = 30

# --------------------------
# 게임 시작/재시작
# --------------------------
def start_game():
    st.session_state.stage = 1
    st.session_state.score = 0
    st.session_state.game_active = True
    init_stage(st.session_state.stage)

def init_stage(stage):
    fire_count = stage + 2  # 단계마다 불 개수 증가
    st.session_state.fires = ['🔥' for _ in range(fire_count)]
    st.session_state.time_left = max(10, 30 - stage*3)

def end_game(reason="끝!"):
    st.session_state.game_active = False
    st.success(f"💥 게임 종료! 이유: {reason} 💥 최종 점수: {st.session_state.score}")

# --------------------------
# 게임 진행
# --------------------------
if not st.session_state.game_active:
    if st.button("게임 시작"):
        start_game()
else:
    st.write(f"단계: {st.session_state.stage} | 점수: {st.session_state.score} | 남은 시간: {st.session_state.time_left}s")

    # 화면을 5칸 열로 나누어 불, 소화기, 엘리베이터 배치
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(st.session_state.fires):
            if col.button(st.session_state.fires[i], key=f"fire{i}"):
                st.session_state.fires.pop(i)
                st.session_state.score += 1
                st.experimental_rerun()
        elif i == len(st.session_state.fires):
            if col.button("🧯", key="extinguisher"):
                # 주변 불 2개 제거
                for _ in range(min(2, len(st.session_state.fires))):
                    st.session_state.fires.pop(0)
                st.session_state.score += 2
                st.experimental_rerun()
        else:
            if col.button("🛗", key="elevator"):
                end_game(reason="엘리베이터 눌렀어요!")

    # 시간 감소
    st.session_state.time_left -= 1
    time.sleep(1)
    if st.session_state.time_left <= 0:
        end_game(reason="시간 초과!")

    # 다음 단계 체크
    if len(st.session_state.fires) == 0:
        st.success("🎉 단계 클리어! 다음 단계로 이동합니다!")
        st.session_state.stage += 1
        init_stage(st.session_state.stage)

    if st.button("다시하기"):
        start_game()
