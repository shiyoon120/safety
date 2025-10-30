# 파일명: fire_cat_game.py
import streamlit as st
import random
from time import sleep # 재시작 시 딜레이를 위해 사용

# --- 1. 기본 설정 및 상태 관리 ---

st.set_page_config(
    page_title="냥이의 안전한 집 탈출!",
    page_icon="🐱",
    layout="wide" # 넓은 화면 레이아웃 사용
)

# 게임 상태 초기화
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 0  # 0: 시작, 1: 1단계, 2: 2단계, 99: 실패, 100: 성공
    st.session_state.fire_loc = random.randint(1, 3) # 불이 난 위치 (1, 2, 3 중 하나)
    st.session_state.is_fire_out = False # 불을 껐는지 여부
    st.session_state.fail_reason = "" # 실패 이유 저장

# --- 2. 유틸리티 함수 ---

def go_to_stage(stage):
    """게임 단계를 변경하고 페이지를 새로고침(rerun)합니다."""
    st.session_state.game_stage = stage
    st.rerun()

def reset_game():
    """게임을 초기 상태로 되돌립니다."""
    st.toast("게임을 다시 시작합니다! 😼", icon="🔄")
    sleep(1) # 잠시 딜레이
    st.session_state.game_stage = 0
    st.session_state.fire_loc = random.randint(1, 3)
    st.session_state.is_fire_out = False
    st.session_state.fail_reason = ""
    st.rerun()

def show_fail_reason(reason):
    """실패 화면과 이유를 보여줍니다."""
    st.session_state.fail_reason = reason
    go_to_stage(99)

# --- 3. 게임 화면 렌더링 함수 ---

# A. 시작 화면 (Stage 0)
def render_stage_0():
    st.title("🔥 냥이의 안전한 집 탈출! 🚨")
    st.markdown("## **귀여운 냥이 '안전이'와 함께 화재 안전 훈련을 해보세요!** 🐱")
    st.markdown("---")
    
    # 귀여운 픽셀 느낌 연출
    st.markdown("### 🏠 🏠 🏠 🏠 🏠 🏠 🏠 🏠 🏠")
    st.markdown("### 😺 (안전이) 🐾")
    st.markdown("### 규칙: **초기 진압**과 **안전한 대피**가 핵심이에요!")
    st.markdown("---")

    if st.button("게임 시작! (1단계로 이동)", type="primary"):
        go_to_stage(1)

# B. 1단계: 초기 화재 진압 (클릭으로 불 끄기)
def render_stage_1():
    st.header("1단계: 초기 화재 진압! 🔥")
    st.markdown("### **집 안에서 작은 불꽃을 발견했어요! 고양이 털에 옮겨붙기 전에 빨리 꺼야 해요!**")
    st.markdown("---")
    
    # 3개의 공간(컬럼)에 불 이모지 배치
    col1, col2, col3 = st.columns(3)
    fire_pos_list = [col1, col2, col3]
    
    # 불이 난 위치에만 버튼/물 이모지 표시
    with fire_pos_list[st.session_state.fire_loc - 1]:
        if not st.session_state.is_fire_out:
            # 불이 안 꺼졌을 때: 불 버튼 표시
            if st.button("🔥 (클릭해서 물 뿌리기!)", key="fire_button"):
                st.session_state.is_fire_out = True
                st.toast("💧 성공! 물을 뿌려 불을 껐어요!", icon="💧")
                st.snow() # 불을 껐다는 효과 연출
                st.rerun() 
        else:
            # 불이 꺼졌을 때: 물 이모지 표시
            st.markdown("## 💧") 
            st.markdown("### **초기 진압 완료!**")
    
    # 나머지 두 곳은 빈 공간으로 표시
    for i, col in enumerate(fire_pos_list):
        if i != st.session_state.fire_loc - 1:
            with col:
                st.markdown("### 🪑") # 가구 이모지

    st.markdown("---")

    if st.session_state.is_fire_out:
        st.success("✅ 초기 진압 성공! 이제 연기가 자욱하니 안전하게 대피 경로를 찾아야 해요. 🚨")
        if st.button("다음 단계로 이동 (2단계)", type="primary"):
            go_to_stage(2)
    else:
        st.info("🚨 불이 난 곳을 찾아서 이모지 버튼을 **한 번만** 클릭하세요!")

# C. 2단계: 안전한 대피 경로 선택
def render_stage_2():
    st.header("2단계: 안전하게 대피하기! 🏃‍♀️")
    st.markdown("### **불은 껐지만 연기가 나고 있어요. 소화기 상태를 확인하고 올바른 대피 경로를 선택하세요!**")
    st.markdown("---")

    # 1. 소화기 사용 훈련 (막대바/슬라이더)
    st.subheader("1. 소화기 압력 확인 훈련:")
    st.markdown("**소화기 사용 전, 압력 게이지가 초록색 구간(50~70)에 있는지 확인하세요!**")
    
    pressure = st.slider("소화기 압력 게이지 조정", 0, 100, 50, key="pressure_slider")
    
    is_pressure_ok = (50 <= pressure <= 70)
    
    col_p1, col_p2 = st.columns([1, 4])
    with col_p1:
        if is_pressure_ok:
            st.success("👍 합격!")
        else:
            st.error("⚠️ 불합격!")
    with col_p2:
        if is_pressure_ok:
            st.info("🔥 소화기 사용 준비 완료! 다음 단계로 가세요.")
        else:
            st.warning("압력이 적정하지 않다면 소화기 역할을 제대로 못 해요! 압력을 다시 맞추세요.")
            
    st.markdown("---")

    # 2. 대피 경로 선택
    st.subheader("2. 안전한 대피 경로 선택:")
    
    if is_pressure_ok:
        evac_choice = st.radio(
            "건물 밖으로 나가기 위해 어떤 경로를 선택해야 할까요? 😱",
            ["1. ✅ 계단을 이용해 낮은 자세로 대피한다.", "2. ❌ 엘리베이터 버튼을 누르고 빠르게 내려간다."],
            index=None,
            key="evac_radio"
        )

        if st.button("대피 경로 선택 완료", type="primary"):
            if "계단을 이용해" in evac_choice:
                st.toast("똑똑해요! 계단이 정답이에요!", icon="✨")
                go_to_stage(100) # 최종 성공
            elif "엘리베이터 버튼을 누르고" in evac_choice:
                # 요청하신 '엘베를 누르면 게임 종료' 조건
                show_fail_reason("화재 시 **엘리베이터**는 정전되거나 멈춰서 갇힐 수 있어요. **절대** 이용하면 안 됩니다! 🙅‍♀️")
            else:
                st.warning("경로를 선택해 주세요.")
    else:
        st.info("먼저 소화기 압력 훈련을 완료해야 경로를 선택할 수 있어요.")

# D. 실패/성공 화면
def render_stage_99():
    st.error("🛑 게임 실패! 😭")
    st.markdown(f"## **실패한 이유**")
    st.markdown(f"### **{st.session_state.fail_reason}**")
    st.markdown("---")
    st.markdown("### **이유를 꼭 기억해서 다음에는 안전이를 지켜주세요!** 😿")
    if st.button("다시 도전하기", type="primary"):
        reset_game()

def render_stage_100():
    st.balloons()
    st.success("🎉 최종 성공! 💯")
    st.markdown("## **축하합니다! 안전하게 대피했습니다! '안전이'가 고마워해요!** 😻")
    st.markdown("---")
    st.markdown("### **배운 점:** 초기 진압과 계단을 이용한 안전한 대피가 생명을 구합니다!")
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
    elif st.session_state.game_stage == 99:
        render_stage_99()
    elif st.session_state.game_stage == 100:
        render_stage_100()

if __name__ == "__main__":
    main()
