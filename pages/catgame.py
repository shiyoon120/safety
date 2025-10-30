import streamlit as st
import random
import time

st.set_page_config(page_title="🔥 소방대 출동! 🔥", layout="wide")

# --------------------------
# 스타일링: 배경 빨강, 버튼 글씨 흰색
# --------------------------
st.markdown("""
<style>
.stApp {
    background-color: #ff6666;
    color: white;
}
.button-red {
    background-color: #cc0000;
    color: white;
    border: 2px solid white;
    font-size: 24px;
    padding: 10px;
    border-radius: 10px;
}
.button-red:hover {
    background-color: #ff3333;
}
</style>
""", unsafe_allow_html=True)

st.title("🔥 소방대 출동! 🔥")

# --------------------------
# 게임 설명
# --------------------------
st.markdown("""
**게임 방법:**  
1. 🔥 불 버튼 클릭 → 불 꺼짐, 점수 +1  
2. 🧯 소화기 클릭 → 주변 불 2개 꺼짐, 점수 +2  
3. 🛗 엘리베이터 클릭 → 게임 즉시 종료  
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
    if st.button("게임 시작", key="start"):
        start_game()
else:
    st.write(f"단계: {st.session_state.stage} | 점수: {st.session_state.score} | 남은 시간: {st.session_state.time_left}s")

    # 버튼 배치
    cols = st.columns(5)
    button_keys = []

    # 불 버튼
    for i in range(len(st.session_state.fires)):
        button_keys.append(f"fire_{i}")
        if cols[i].button(st.session_state.fires[i], key=button_keys[i]):
            # 클릭 시 안전하게 제거
            st.session_state.fires[i] = None
            st.session_state.score += 1
            st.experimental_rerun()

    # 소화기 버튼
    if len(cols) > len(st.session_state.fires):
        idx = len(st.session_state.fires)
        if cols[idx].button("🧯 소화기", key="extinguisher"):
            # 주변 불 2개 제거
            removed = 0
            for j in range(len(st.session_state.fires)):
                if st.session_state.fires[j] is not None and removed < 2:
                    st.session_state.fires[j] = None
                    removed += 1
            st.session_state.score += removed * 1
            st.experimental_rerun()

    # 엘리베이터 버튼
    if len(cols) > len(st.session_state.fires)+1:
        idx = len(st.session_state.fires)+1
        if cols[idx].button("🛗 엘리베이터", key="elevator"):
            end_game(reason="엘리베이터 눌렀어요!")

    # 시간 감소
    st.session_state.time_left -= 1
    time.sleep(1)
    if st.session_state.time_left <= 0:
        end_game(reason="시간 초과!")

    # 다음 단계 체크
    if all(f is None for f in st.session_state.fires):
        st.success("🎉 단계 클리어! 다음 단계로 이동합니다!")
        st.session_state.stage += 1
        init_stage(st.session_state.stage)

    # 다시하기 버튼
    if st.button("다시하기", key="restart"):
        start_game()
