# 파일명: fire_cat_game_final_v11.py
import streamlit as st
import random
from time import sleep 

# --- 1. 기본 설정 및 상태 관리 ---

st.set_page_config(
    page_title="냥이의 안전한 집 탈출! - 최종 훈련",
    page_icon="😼",
    layout="wide" 
)

# P.A.S.S. 순서 정의
PASS_STEPS_EASY = ["P: 핀 뽑기", "A: 노즐 조준", "S1: 손잡이 누르기", "S2: 빗자루 쓸듯 분사"]
PASS_STEPS_HARD = ["핀 뽑기", "노즐 조준", "손잡이 누르기", "쓸어 분사"] # 버튼에 표시될 텍스트

# 게임 상태 초기화
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 0  # 0: 시작, 1: 압력, 2: 화재 종류, 3: PASS, 4: 대피, 99: 실패, 100: 성공
    st.session_state.is_pressure_ok = False
    st.session_state.fire_type = random.choice(["주방(유류)", "전기"])
    st.session_state.pass_status = {step: False for step in PASS_STEPS_HARD}
    st.session_state.current_pass_index = 0
    st.session_state.step_2_success = False 
    st.session_state.fail_reason = ""
    st.session_state.game_started = False
    st.session_state.show_balloons = False # 풍선 제어 플래그
    # 3단계 난이도 상향을 위한 무작위 순서
    st.session_state.pass_random_order = PASS_STEPS_HARD[:] 
    random.shuffle(st.session_state.pass_random_order) # 초기 순서 무작위화

# --- 2. 유틸리티 함수 ---

def go_to_stage(stage):
    """게임 단계를 변경하고 페이지를 새로고침(rerun)합니다."""
    # 성공 단계로 진입할 때만 풍선 플래그를 True로 설정
    if stage == 100:
        st.session_state.show_balloons = True
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
    st.session_state.pass_status = {step: False for step in PASS_STEPS_HARD}
    st.session_state.current_pass_index = 0
    st.session_state.step_2_success = False
    st.session_state.fail_reason = ""
    st.session_state.game_started = False
    st.session_state.show_balloons = False # 풍선 플래그 초기화
    # 새로운 무작위 순서 생성
    st.session_state.pass_random_order = PASS_STEPS_HARD[:]
    random.shuffle(st.session_state.pass_random_order)
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

# B. 1단계: 소화기 압력 확인
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
            st.markdown(" ")
        elif pressure != 0:
            if pressure < 50:
                st.error("앗! 너무 낮아요! 📉")
            else: 
                st.error("앗! 너무 높아요! 📈")
        else:
            st.markdown(" ")
    
    with col_p2:
        if is_pressure_ok:
            st.info("✅ 압력 확인 완료! 소화기를 사용할 수 있어요.")
            if st.button("다음 단계 (2단계)로 이동", type="secondary"):
                go_to_stage(2)
        else:
            st.warning("압력이 올바르지 않으면 소화기가 작동하지 않을 수 있어요!")
            st.info("압력을 먼저 맞춰주세요.")

# C. 2단계: 화재 종류별 진압 선택
def render_stage_2():
    st.header("🔥 2단계: 화재 종류별 진압 방법 선택!")
    st.markdown(f"### **현재 화재는 **{st.session_state.fire_type}** 화재예요! 올바른 진압 방법을 고르세요.**")
    st.markdown("---")
    
    if "주방" in st.session_state.fire_type:
        st.markdown("## 🍳 🔥 (기름이 타는 냄새!)")
        correct_choice = "C. 젖은 담요를 덮어 산소를 차단한다."
        correct_advice = "**올바른 방법:** 유류 화재는 물을 쓰면 안 되고, 산소를 차단하는 **담요**를 써야 안전해요."
    else: # 전기 화재
        st.markdown("## 🔌 💻 🔥 (전기 장치에서 불꽃이!)")
        correct_choice = "B. 소화기를 사용하거나 전원을 차단한다."
        correct_advice = "**올바른 방법:** 전기 화재는 감전 위험이 없도록 **소화기**나 **전원 차단**이 필수예요."

    st.markdown("---")
    
    # 이미 정답을 맞췄으면 바로 피드백 표시
    if st.session_state.step_2_success:
        st.success("✨ 정답! 올바른 진압 방법을 선택했어요.")
        if st.button("다음 단계 (3단계)로 이동", type="secondary"):
            go_to_stage(3)
        return

    # 정답을 맞추지 않았을 경우에만 라디오 버튼과 확인 버튼 표시
    evac_choice = st.radio(
        "이 화재에 가장 적합한 초기 진압 방법은 무엇일까요? 🤔",
        ["A. 물을 뿌려서 온도를 낮춘다.", "B. 소화기를 사용하거나 전원을 차단한다.", "C. 젖은 담요를 덮어 산소를 차단한다."],
        index=None,
        key="fire_type_radio"
    )

    if st.button("진압 방법 선택 완료", type="primary"):
        if evac_choice == correct_choice:
            st.session_state.step_2_success = True
            st.rerun() # 성공 상태를 반영하기 위해 리런 (정답 피드백 표시)
        else:
            fail_reason = ""
            if "A. 물을 뿌려서" in evac_choice and "주방" in st.session_state.fire_type:
                fail_reason = f"🚨 기름(유류) 화재에 물을 뿌리면 폭발적으로 번져요! **물은 절대 안 됩니다.**\n\n{correct_advice}"
            elif "C. 젖은 담요를 덮어" in evac_choice and "전기" in st.session_state.fire_type:
                 fail_reason = f"🚨 전기 화재에 젖은 담요를 사용하면 감전의 위험이 있어요! **소화기** 사용이 안전합니다.\n\n{correct_advice}"
            else:
                fail_reason = f"🚨 잘못된 진압 방법으로 화재가 커졌어요! 화재 종류에 따라 진압 방법이 달라요.\n\n{correct_advice}"
            
            show_fail_reason(fail_reason)

# D. 3단계: P.A.S.S. 순서 맞추기
def render_stage_3():
    st.header("💧 3단계: 소화기 P.A.S.S. 순서 훈련!")
    st.markdown("### **소화기 사용의 4단계 순서(P.A.S.S.)를 기억하며 올바른 동작을 순서대로 눌러 불을 완전히 꺼주세요!**")
    st.markdown("---")

    # 현재 진행 상황 표시 (남은 단계 수만 표시)
    remaining_steps = 4 - st.session_state.current_pass_index
    st.subheader(f"✅ 남은 단계 수: **{remaining_steps}**")
    
    col_pass = st.columns(4)
    
    correct_step_hard_text = PASS_STEPS_HARD[st.session_state.current_pass_index] if st.session_state.current_pass_index < 4 else None

    # 무작위 순서로 섞인 버튼 배치
    for i, step_hard_text in enumerate(st.session_state.pass_random_order):
        with col_pass[i]:
            if st.session_state.pass_status[step_hard_text]:
                # 이미 완료된 단계 (초록색)
                st.success(f"✅ {step_hard_text}")
            elif step_hard_text == correct_step_hard_text:
                # 현재 정답 버튼 (일반색)
                if st.button(f"⚫ {step_hard_text}", key=f"pass_btn_{i}"):
                    st.session_state.current_pass_index += 1
                    st.session_state.pass_status[step_hard_text] = True
                    st.toast(f"'{step_hard_text}' 완료!", icon="👍")
                    st.rerun() 
            else:
                # 오답 버튼 (일반색)
                if st.button(f"⚫ {step_hard_text}", key=f"pass_btn_{i}"):
                    # 순서를 틀렸을 때 즉시 실패
                    correct_step_name = PASS_STEPS_EASY[st.session_state.current_pass_index]
                    show_fail_reason(f"🚨 P.A.S.S. 순서가 틀렸어요! 올바른 순서는 **{correct_step_name}** 입니다. (당신은 '{step_hard_text}'을 먼저 눌렀어요.)")

    st.markdown("---")
    
    # 4단계 모두 완료 시 (교육적인 설명 추가)
    if st.session_state.current_pass_index == 4:
        st.success("🎉 P.A.S.S. 순서 완벽! 불이 완전히 진압되었어요!")
        st.markdown("### **⭐ 잠깐! P.A.S.S. 란 무엇일까요?**")
        st.markdown("""
        P.A.S.S.는 소화기를 올바르게 사용하는 4단계 행동 요령입니다. 당신은 이 순서를 성공적으로 해냈어요!
        * **P (Pull):** 안전핀을 **뽑고**
        * **A (Aim):** 노즐을 불이 난 곳으로 **조준하고**
        * **S (Squeeze):** 손잡이를 **누르고**
        * **S (Sweep):** 불이 난 곳을 **쓸어 끄듯이** 분사합니다.
        """)
        if st.button("다음 단계 (4단계)로 이동 - 최종 대피", type="secondary"):
            go_to_stage(4)
            
# E. 4단계: 안전한 대피 경로 선택 (아이콘/화살표 통일)
def render_stage_4():
    st.header("🏃‍♀️ 4단계: 안전한 대피 경로 선택! 🚨")
    st.markdown("### **모든 진압이 끝났지만, 건물 밖으로 나가기 위해 마지막으로 안전한 경로를 선택해야 합니다!**")
    st.markdown("---")
    
    st.subheader("최종 대피 경로 선택:")
    
    col_stair, col_elev = st.columns(2)

    # 1. 계단 버튼 (정답) - 화살표 통일 (⬇️)
    with col_stair:
        if st.button("⬇️ 계단 이용", key="stair_button", use_container_width=True):
            st.toast("똑똑해요! 계단이 안전합니다.", icon="✨")
            sleep(1)
            go_to_stage(100)
        st.markdown("### 🏃‍♀️ **A. 계단 비상구를 찾아 낮은 자세로 신속하게 이동한다.**")
        
    # 2. 엘리베이터 버튼 (오답) - 아이콘 (🛗) 및 화살표 통일 (⬇️)
    with col_elev:
        if st.button("⬇️ 🛗 엘리베이터 이용", key="elev_button", use_container_width=True):
            show_fail_reason("🚨 엘리베이터는 화재 시 정전되거나 고장으로 갇힐 위험이 있어 **절대** 이용하면 안 됩니다! 🙅‍♀️ 계단 비상구를 이용해야 합니다.")
        st.markdown("### **B. 엘리베이터가 보이니까 버튼을 눌러 빠르게 내려간다.**") 
    
    st.markdown("---")


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
    # --- 풍선 효과 제어 ---
    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False # 풍선 플래그 즉시 끄기

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
