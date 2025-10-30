import streamlit as st
import random
import time

st.set_page_config(page_title="🔥 소방대 출동! 🔥", layout="wide")

# --------------------------
# 스타일링
# --------------------------
st.markdown("""
<style>
.stApp {
    background-color: #ffb366;  /* 주황 배경으로 게임 느낌 */
    color: white;
}
.game-button {
    background-color: orange;
    color: white;
    font-size: 24px;
    padding: 15px 25px;
    border-radius: 12px;
    border: 2px solid white;
    margin: 5px;
    cursor: pointer;
}
.game-button:hover {
    background-color: #ff8000;
}
.button-container {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔥 소방대 출동! 🔥")

# --------------------------
# 게임 설명
# --------------------------
st.markdown("""
**게임 방법:**  
1. 🔥 불 클릭 → 불 꺼짐, 점수 +1  
2. 🧯 소화기 클릭 → 주변 불 2개 꺼짐, 점수 +2  
3. 🛗 엘리베이터 클릭 → 즉시 게임 종료  
4. 제한 시간 안에 모든 불을 끄세요!  
5. 단계별 난이도 증가 (불 개수 ↑, 시간 ↓)
""")

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
    fire_count = stage + 2
    st.session_state.fires = ['🔥' for _ in range(fire_count)]
    st.session_state.time_left = max(10, 30 - stage*3)

def end_game(reason="끝!"):
    st.session_state.game_active = False
    st.success(f"💥 게임 종료! 이유: {reason} 💥 최종 점수: {st.session_state.score}")

# --------------------------
# 게임 진행
# --------------------------
if not st.session_state.game_active:
    if st.button("게임 시작", key="start"):
        start_game()
else:
    st.write(f"단계: {st.session_state.stage} | 점수: {st.session_state.score} | 남은 시간: {st.session_state.time_left}s")

    # 버튼 표시 영역
    cols = st.columns(5)

    # 불 버튼
    for i in range(len(st.session_state.fires)):
        if st.session_state.fires[i] is not None:
            fire_html = f"""<div class="button-container">
                <button class="game-button" onclick="window.location.reload();">{st.session_state.fires[i]}</button>
            </div>"""
            cols[i].markdown(fire_html, unsafe_allow_html=True)

    # 소화기 버튼
    if len(cols) > len(st.session_state.fires):
        idx = len(st.session_state.fires)
        extinguisher_html = """<div class="button-container">
            <button class="game-button" onclick="window.location.reload();">🧯 소화기</button>
        </div>"""
        cols[idx].markdown(extinguisher_html, unsafe_allow_html=True)

    # 엘리베이터 버튼
    if len(cols) > len(st.session_state.fires)+1:
        idx = len(st.session_state.fires)+1
        elevator_html = """<div class="button-container">
            <button class="game-button" onclick="window.location.reload();">🛗 엘리베이터</button>
        </div>"""
        cols[idx].markdown(elevator_html, unsafe_allow_html=True)

    # 제한 시간 감소
    st.session_state.time_left -= 1
    time.sleep(1)
    if st.session_state.time_left <= 0:
        end_game(reason="시간 초과!")

    # 단계 클리어 체크
    if all(f is None for f in st.session_state.fires):
        st.success("🎉 단계 클리어! 다음 단계로 이동합니다!")
        st.session_state.stage += 1
        init_stage(st.session_state.stage)

    # 다시하기 버튼
    if st.button("다시하기", key="restart"):
        start_game()
