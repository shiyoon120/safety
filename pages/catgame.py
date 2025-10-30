import streamlit as st
import random

st.set_page_config(page_title="🔥 소방대 출동! 🔥", layout="wide")

st.title("🔥 소방대 출동! 🔥")

# --------------------------
# 상태 초기화
# --------------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 1
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'message' not in st.session_state:
    st.session_state.message = "게임 시작 버튼을 눌러주세요!"
if 'fires' not in st.session_state:
    st.session_state.fires = []
if 'items' not in st.session_state:
    st.session_state.items = []

# --------------------------
# 단계 초기화
# --------------------------
def init_stage(stage):
    st.session_state.message = f"단계 {stage}! 🔥 불을 꺼주세요!"
    fire_count = stage + 1
    st.session_state.fires = ['🔥' for _ in range(fire_count)]
    # 아이템 배치: 소화기 하나, 엘리베이터 하나
    st.session_state.items = ['🧯', '🛗']
    random.shuffle(st.session_state.items)

# --------------------------
# 게임 시작
# --------------------------
def start_game():
    st.session_state.stage = 1
    st.session_state.game_active = True
    init_stage(st.session_state.stage)

def next_stage():
    st.session_state.stage += 1
    init_stage(st.session_state.stage)

def reset_game():
    st.session_state.stage = 1
    st.session_state.game_active = False
    st.session_state.message = "게임 시작 버튼을 눌러주세요!"
    st.session_state.fires = []
    st.session_state.items = []

# --------------------------
# 게임 시작 버튼
# --------------------------
if not st.session_state.game_active:
    if st.button("게임 시작"):
        start_game()

# --------------------------
# 게임 화면
# --------------------------
if st.session_state.game_active:
    st.subheader(st.session_state.message)

    # 버튼 화면 구성
    cols = st.columns(len(st.session_state.fires) + len(st.session_state.items))
    idx = 0

    # 불 버튼
    for i in range(len(st.session_state.fires)):
        if st.session_state.fires[i] is not None:
            if cols[idx].button(st.session_state.fires[i], key=f"fire_{i}"):
                st.session_state.fires[i] = None
                st.session_state.message = "불을 껐습니다! 계속하세요."
            idx += 1

    # 아이템 버튼
    for i, item in enumerate(st.session_state.items):
        if item == '🧯':
            if cols[idx].button(item, key=f"extinguisher_{i}"):
                # 소화기 클릭 시 불 2개 제거
                removed = 0
                for j in range(len(st.session_state.fires)):
                    if st.session_state.fires[j] is not None and removed < 2:
                        st.session_state.fires[j] = None
                        removed += 1
                st.session_state.message = "소화기를 사용했습니다!"
            idx += 1
        elif item == '🛗':
            if cols[idx].button(item, key=f"elevator_{i}"):
                st.session_state.message = "엘리베이터를 눌렀어요! 게임 실패!"
                st.button("다시하기", on_click=reset_game)
            idx += 1

    # 단계 완료 체크
    if all(f is None for f in st.session_state.fires):
        st.session_state.message = "모든 불을 끄셨습니다! 다음 단계로 이동합니다!"
        st.button("다음 단계", on_click=next_stage)

    # 다시하기 버튼
    st.button("게임 다시하기", on_click=reset_game)
