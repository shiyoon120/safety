# 파일명: fire_cat_game_final_v6.py
import streamlit as st
import random
from time import sleep 

# --- 1. 기본 설정 및 상태 관리 ---

st.set_page_config(
    page_title="냥이의 안전한 집 탈출! - 4단계 훈련",
    page_icon="😼",
    layout="wide" 
)

# P.A.S.S. 순서 정의
PASS_STEPS = ["P: 핀 뽑기", "A: 노즐 조준", "S: 손잡이 누르기", "S: 빗자루 쓸듯 분사"]

# 게임 상태 초기화
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 0  # 0: 시작, 1: 압력, 2: 화재 종류, 3: PASS, 4: 대피, 99: 실패, 100: 성공
    st.session_state.is_pressure_ok = False # 1단계 성공 여부
    st.session_state.fire_type = random.choice(["주방(유류)", "전기"]) # 2단계 화재 종류
    st.session_state.pass_status = {step: False for step in PASS_STEPS} # 3단계 진행 상황
    st.session_state.current_pass_index = 0 # 현재 진행해야 할 PASS 순서 인덱스 (0, 1, 2, 3)
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
    # 모든 상태를 초기화
    st.session_state.game_stage = 0
    st.session_state.is_pressure_ok = False
    st.session_state.fire_type = random.choice(["주방(유류)", "전기"])
    st.session_state.pass_status = {step: False for step in PASS_STEPS}
    st.session_state.current_pass_index = 0
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
        st.markdown("## 😺 **4단계 화재 안전 훈련을 시작해서 안전이를 구해주세요!** 🐾")
        st.markdown("---")
        
        st.write("### 🏠 🛋️ 🧸 🐈 🚪")
        st.write("### **훈련 단계:** 1.압력확인 -> 2.진압선택 -> 3.PASS순서 -> 4.대피로선택")
        
        st.markdown("---")
        
        col_start, col_dummy = st.columns([1, 2])
        with col_start:
            if st.button("▶️ 훈련 시작! (1단계로 이동)", type="primary", use_container_width=True):
                st.session_state.game_started = True
                go_to_stage(1)

# B. 1단계: 소화기 압력 확인 (경고문 추가)
def render_stage_1():
    st.header("1단계: 소화기 압력 확인 (준비) 🔋")
    st.markdown("### **소화기를 사용하기 전에 압력 게이지를 확인해야 해요!**")
    st.markdown("---")

    st.subheader("소화기 압력 게이지 확인:")
    st.markdown("**슬라이더를 움직여 초록색 안전 구간(50~70)에 정확히 맞추세요!**")
    
    pressure = st.slider("소화기 압력 게이지 조정", 0, 100, 0, key="pressure_slider")
    
    is_pressure_ok = (50 <= pressure <= 70)
    st.session_state.is_pressure_ok = is_pressure_ok
    
    col_p1, col_p2 = st.columns([1, 4])
    with col_p1:
        if is_pressure_ok:
            st.success("👍 합격!")
        else:
            # --- 잘못된 압력 선택 시 빨간 경고문 ---
            st.error("⚠️ 잘못된 압력!")
    
    with col_p2:
        if is_pressure_ok:
            st.info("✅ 압력 확인 완료! 소화기를 사용할 수 있어요.")
            if st.button("다음 단계 (2단계)로 이동", type="secondary"):
                go_to_stage(2)
        else:
            st.warning("압력이 올바르지 않으면 소화기가 작동하지 않을 수 있어요!")
            st.info("압력을 먼저 맞춰주세요.")

# C. 2단계: 화재 종류별 진압 선택 (이동 오류 수정)
def render_stage_2():
    st.header("🔥 2단계: 화재 종류별 진압 방법 선택!")
    st.markdown(f"### **현재 화재는 **{st.session_state.fire_type}** 화재예요! 올바른 진압 방법을 고르세요.**")
    st.markdown("---")
    
    # 화재 시각화 및 정답 설정
    if "주방" in st.session_state.fire_type:
        st.markdown("## 🍳 🔥 (기름이 타는 냄새!)")
        correct_choice = "C. 젖은 담요를 덮어 산소를 차단한다."
    else: # 전기 화재
        st.markdown("## 🔌 💻 🔥 (전기 장치에서 불꽃이!)")
        correct_choice = "B. 소화기를 사용하거나 전원을 차단한다."

    st.markdown("---")
    
    evac_choice = st.radio(
        "이 화재에 가장 적합한 초기 진압 방법은 무엇일까요? 🤔",
        ["A. 물을 뿌려서 온도를 낮춘다.", "B. 소화기를 사용하거나 전원을 차단한다.", "C. 젖은 담요를 덮어 산소를 차단한다."],
        index=None,
        key="fire_type_radio"
    )

    # 이 버튼을 누르지 않으면 아래 로직이 실행되지 않도록 분리
    if st.button("진압 방법 선택 완료", type="primary"):
        if evac_choice == correct_choice:
            st.session_state.step_2_success = True
            st.success("✨ 정답! 올바른 진압 방법을 선택했어요.")
            
        else:
            if "A. 물을 뿌려서" in evac_choice and "주방" in st.session_state.fire_type:
                show_fail_reason("🚨 기름(유류) 화재에 물을 뿌리면 폭발적으로 번져요! **물은 절대 안 됩니다.**")
            elif "C. 젖은 담요를 덮어" in evac_choice and "전기" in st.session_state.fire_type:
                 show_fail_reason("🚨 전기 화재에 젖은 담요를 사용하면 감전의 위험이 있어요! **전기 화재는 소화기나 전원 차단이 우선입니다.**")
            else:
                show_fail_reason("🚨 잘못된 진압 방법으로 화재가 커졌어요! 화재 종류에 따라 진압 방법이 달라요.")

    # 정답을 맞췄을 때만 다음 단계 버튼 표시 (별도의 if문으로 분리)
    if 'step_2_success' in st.session_state and st.session_state.step_2_success:
        if st.button("다음 단계 (3단계)로 이동", type="secondary"):
            del st.session_state.step_2_success # 상태 초기화
            go_to_stage(3)


# D. 3단계: P.A.S.S. 순서 맞추기
def render_stage_3():
    st.header("💧 3단계: 소화기 P.A.S.S. 순서 훈련!")
    st.markdown("### **이제 소화기를 잡았어요. 올바른 순서로 사용해야 불이 완전히 꺼져요!**")
    st.markdown("---")

    # 현재 진행 상황 표시
    st.subheader(f"✅ 다음 순서: **{PASS_STEPS[st.session_state.current_pass_index]}**")
    
    col_pass = st.columns(4)
    
    is_success = True
    
    for i, step in enumerate(PASS_STEPS):
        with col_pass[i]:
            if st.session_state.current_pass_index == i:
                # 현재 눌러야 할 버튼
                if st.button(f"🔴 {step}", key=f"pass_btn_{i}", type="primary", use_container_width=True):
                    st.session_state.current_pass_index += 1
                    st.session_state.pass_status[step] = True
                    st.toast(f"{step} 완료!", icon="👍")
                    st.rerun()
            elif st.session_state.pass_status[step]:
                # 이미 완료된 단계
                st.success(f"✅ {step}")
            else:
                # 순서를 틀렸을 때 누른 버튼
                if st.button(f"⚫ {step}", key=f"pass_btn_{i}", use_container_width=True):
                    show_fail_reason(f"🚨 P.A.S.S. 순서가 틀렸어요! **{PASS_STEPS[st.session_state.current_pass_index]}** 단계를 먼저 수행해야 합니다. (당신은 {step}을 먼저 눌렀어요.)")
                    is_success = False

    st.markdown("---")
    
    # 4단계 모두 완료 시 (인덱스가 4가 되면 성공)
    if st.session_state.current_pass_index == 4:
        st.success("🎉 P.A.S.S. 순서 완벽! 불이 완전히 진압되었어요!")
        if st.button("다음 단계 (4단계)로 이동 - 최종 대피", type="secondary"):
            go_to_stage(4)
            

# E. 4단계: 안전한 대피 경로 선택
def render_stage_4():
    st.header("🏃‍♀️ 4단계: 안전한 대피 경로 선택! 🚨")
    st.markdown("### **모든 진압이 끝났지만, 건물 밖으로 나가기 위해 마지막으로 안전한 경로를 선택해야 합니다!**")
    st.markdown("---")
    
    st.subheader("최종 대피 경로 선택:")
    
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
            go_to_stage(100) # 최종 성공
        elif "B. 엘리베이터가 보이니까" in evac_choice:
            show_fail_reason("🚨 엘리베이터는 화재 시 정전되거나 고장으로 갇힐 위험이 있어 **절대** 이용하면 안 됩니다! 🙅‍♀️ 계단 비상구를 이용해야 합니다.")
        else:
            st.warning("경로 A 또는 B를 선택해 주세요.")

# F. 실패/성공 화면
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
    st.markdown("### **✨ 배운 점:** 소화기 준비, 화재 판단, 소화기 사용, 대피까지! 4단계를 모두 완벽하게 수행했습니다.")
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
    elif st.session_state.game_stage == 4:
        render_stage_4()
    elif st.session_state.game_stage == 99:
        render_stage_99()
    elif st.session_state.game_stage == 100:
        render_stage_100()

if __name__ == "__main__":
    main()
