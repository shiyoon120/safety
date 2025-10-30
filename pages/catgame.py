# 파일명: fire_cat_game_v4.py
import streamlit as st
import random
from time import sleep 

# --- 1. 기본 설정 및 상태 관리 ---

st.set_page_config(
    page_title="냥이의 안전한 집 탈출!",
    page_icon="😼",
    layout="wide" 
)

# 게임 상태 초기화
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 0  # 0: 시작, 1: 압력, 2: 진압, 3: 대피, 99: 실패, 100: 성공
    st.session_state.fire_loc = random.randint(1, 3) 
    st.session_state.is_pressure_ok = False # 압력 확인 성공 여부
    st.session_state.hits = 0 # 화재 진압 횟수 (미니 게임용)
    st.session_state.fail_reason = ""
    st.session_state.game_started = False 

# --- 2. 유틸리티 함수 ---

def go_to_stage(stage):
    """게임 단계를 변경하고 페이지를 새로고침(rerun)합니다."""
    st.session_state.game_stage = stage
    st.rerun()

def reset_game():
    """게임을 초기 상태로 되돌립니다."""
    st.toast("게임을 다시 시작합니다! 😼", icon="🔄")
    sleep(1) 
    st.session_state.game_stage = 0
    st.session_state.fire_loc = random.randint(1, 3)
    st.session_state.is_pressure_ok = False
    st.session_state.hits = 0
    st.session_state.fail_reason = ""
    st.session_state.game_started = False
    st.rerun()

def show_fail_reason(reason):
    """실패 화면과 이유를 보여줍니다."""
    st.session_state.fail_reason = reason
    go_to_stage(99)

# --- 3. 게임 화면 렌더링 함수 ---

# A. 시작 화면 (Stage 0)
def render_stage_0():
    if not st.session_state.game_started:
        st.title("🔥 냥이의 안전한 집 탈출! 🚨")
        st.markdown("## 😺 **귀여운 냥이 '안전이'와 함께 화재 안전 훈련을 시작할까요?** 🐾")
        st.markdown("---")
        
        st.write("### 🏠 🛋️ 🧸 🐈 🚪")
        st.write("### 🚨 **3단계 미션을 성공하고 안전이를 구해주세요!** 🚨")
        
        st.markdown("---")
        
        col_start, col_dummy = st.columns([1, 2])
        with col_start:
            if st.button("▶️ 훈련 시작! (1단계로 이동)", type="primary", use_container_width=True):
                st.session_state.game_started = True
                go_to_stage(1)


# B. 1단계: 소화기 압력 확인 (준비 단계)
def render_stage_1():
    st.header("1단계: 소화기 압력 확인 (준비) 🔋")
    st.markdown("### **소화기를 사용하기 전에 압력 게이지를 확인해야 해요!**")
    st.markdown("---")

    st.subheader("소화기 압력 게이지 확인:")
    st.markdown("**소화기 압력 슬라이더를 움직여 초록색 안전 구간(50~70)에 정확히 맞추세요!**")
    
    # 초기값 0으로 설정
    pressure = st.slider("소화기 압력 게이지 조정", 0, 100, 0, key="pressure_slider")
    
    is_pressure_ok = (50 <= pressure <= 70)
    st.session_state.is_pressure_ok = is_pressure_ok
    
    col_p1, col_p2 = st.columns([1, 4])
    with col_p1:
        if is_pressure_ok:
            st.success("👍 합격!")
        else:
            st.error("⚠️ 확인!")
    with col_p2:
        if is_pressure_ok:
            st.info("🔥 압력 확인 완료! 이제 불을 끄러 갈까요?")
            if st.button("다음 단계 (2단계)로 이동", type="secondary"):
                go_to_stage(2)
        else:
            st.warning("압력이 올바르지 않으면 소화기가 작동하지 않을 수 있어요!")
            st.info("압력을 먼저 맞춰주세요.")


# C. 2단계: 화재 진압 미니 게임 (액션 단계)
def render_stage_2():
    st.header("🔥 2단계: 불꽃 진압 미니 게임! 💨")
    st.markdown("### **불이 다시 커지고 있어요! 소화 버튼을 **10번** 빠르게 눌러 불을 완전히 꺼야 합니다!**")
    st.markdown("---")

    if not st.session_state.is_pressure_ok:
        st.warning("🚨 1단계에서 소화기 압력을 먼저 맞춰야 2단계로 진행할 수 있습니다!")
        if st.button("1단계로 돌아가기"):
            go_to_stage(1)
        return # 1단계 미완료 시 여기서 렌더링 종료

    # 게임 목표 설정
    TARGET_HITS = 10
    
    st.markdown(f"## 🔥 **진압 횟수: {st.session_state.hits} / {TARGET_HITS}** 💧")
    
    progress_percent = st.session_state.hits / TARGET_HITS if TARGET_HITS > 0 else 0
    st.progress(progress_percent, text=f"불이 꺼지는 중... ({int(progress_percent * 100)}%)")

    # 불 이모지와 소화 버튼 (빠르게 클릭 유도)
    st.markdown("### 🗑️ 🔥 🔥 🔥 🔥 🛋️")

    # 버튼을 누르면 횟수 증가
    if st.button("💧 소화 버튼 빨리 누르기!", key="fire_game_button", type="primary"):
        st.session_state.hits += 1
        st.rerun() 

    if st.session_state.hits >= TARGET_HITS:
        st.success("✅ **대성공!** 불을 완전히 진압했어요! 소화기 사용법을 완벽히 익혔군요!")
        st.balloons()
        if st.button("다음 단계 (3단계)로 이동 - 대피 경로 선택", type="secondary"):
            go_to_stage(3)
    
    elif st.session_state.hits > 0 and st.session_state.hits < TARGET_HITS:
        # 난이도 조절을 위해 일정 시간이 지나면 (예: 10초) 실패 처리 가능
        st.info("🔥 서둘러야 해요! 불이 다시 커질 수 있어요!")
        
    # **실패 조건 예시 (시간 제한이 없어 일단 성공만 구현)**
    # 만약 시간 제한 기능을 추가하고 싶다면, 시작 시간을 session_state에 저장하고, 현재 시간과 비교하여 실패 처리해야 합니다.

# D. 3단계: 안전한 대피 경로 선택 (판단 단계)
def render_stage_3():
    st.header("🏃‍♀️ 3단계: 안전한 대피 경로 선택! 🚨")
    st.markdown("### **불은 껐지만 연기가 자욱해요. 안전이와 함께 올바른 대피 경로를 선택해야 합니다!**")
    st.markdown("---")
    
    st.subheader("안전한 대피 경로 선택:")
    
    evac_choice = st.radio(
        "건물 밖으로 나가기 위해 가장 안전한 선택은 무엇일까요? 🤔",
        ["A. 계단 비상구를 찾아 낮은 자세로 신속하게 이동한다.", "B. 엘리베이터가 보이니까 버튼을 눌러 빠르게 내려간다."],
        index=None,
        key="evac_radio"
    )

    if st.button("탈출 선택 완료", type="primary"):
        if "A. 계단 비상구를 찾아" in evac_choice:
            st.toast("잠시만 기다려주세요...", icon="⏳")
            sleep(1)
            go_to_stage(100)
        elif "B. 엘리베이터가 보이니까" in evac_choice:
            show_fail_reason("🚨 엘리베이터는 화재 시 정전되거나 고장으로 갇힐 위험이 있어 **절대** 이용하면 안 됩니다! 🙅‍♀️ 계단 비상구를 이용해야 합니다.")
        else:
            st.warning("경로 A 또는 B를 선택해 주세요.")

# E. 실패/성공 화면
def render_stage_99():
    st.error("🛑 게임 실패! 😭")
    st.markdown("---")
    st.markdown(f"## **🚨 안전이 탈출 실패!**")
    st.markdown(f"### **실패한 이유: {st.session_state.fail_reason}**")
    st.markdown("---")
    st.markdown("### **다음에 꼭 기억해서 안전이를 지켜주세요!** 😿")
    if st.button("다시 도전하기", type="primary"):
        reset_game()

def render_stage_100():
    st.balloons()
    st.success("🎉 최종 성공! 💯")
    st.markdown("---")
    st.markdown("## **'안전이'와 함께 무사히 대피했습니다! 정말 잘했어요!** 😻")
    st.markdown("---")
    st.markdown("### **✨ 배운 점:** 소화기 준비-진압-대피 3단계를 완벽하게 수행했습니다!")
    if st.button("처음으로 돌아가기", type="primary"):
        reset_game()

# --- 4. 메인 게임 루프 ---

def main():
    if st.session_state.game_stage == 0:
        render_stage_0()
    elif st.session_state.game_stage == 1:
        render_stage_1()
    elif st.session_state.game_stage == 2:
        render_stage_2()
    elif st.session_state.game_stage == 3:
        render_stage_3()
    elif st.session_state.game_stage == 99:
        render_stage_99()
    elif st.session_state.game_stage == 100:
        render_stage_100()

if __name__ == "__main__":
    main()
