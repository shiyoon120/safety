# 파일명: fire_cat_game_v2.py
import streamlit as st
import random
from time import sleep 

# --- 0. 설정: 귀여운 배경 음악 (HTML을 이용해 삽입) ---
# 주의: 일부 브라우저는 자동 재생을 막을 수 있습니다.
BGM_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" # 저작권 없는 예시 MP3 링크 사용

BGM_HTML = f"""
<audio controls autoplay loop style="display:none">
  <source src="{BGM_URL}" type="audio/mp3">
</audio>
"""
st.markdown(BGM_HTML, unsafe_allow_html=True)


# --- 1. 기본 설정 및 상태 관리 ---
st.set_page_config(
    page_title="냥이의 안전한 집 탈출! V2",
    page_icon="😼",
    layout="wide"
)

# 게임 상태 초기화
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 0  # 0: 시작, 1: 1단계, 2: 2단계, 99: 실패, 100: 성공
    st.session_state.fire_loc = random.randint(1, 3) 
    st.session_state.is_fire_out = False 
    st.session_state.fail_reason = "" 
    st.session_state.game_started = False # 시작 버튼 눌림 여부

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
    st.session_state.is_fire_out = False
    st.session_state.fail_reason = ""
    st.session_state.game_started = False
    st.rerun()

def show_fail_reason(reason):
    """실패 화면과 이유를 보여줍니다."""
    st.session_state.fail_reason = reason
    go_to_stage(99)

# --- 3. 게임 화면 렌더링 함수 ---

# A. 시작 화면 (Stage 0) - 귀엽고 단순하게
def render_stage_0():
    if not st.session_state.game_started:
        st.markdown("<h1 style='text-align: center; color: #ff6347;'>🔥 냥이의 안전한 집 탈출! 🚨</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px;'>😺 **귀여운 냥이 '안전이'와 함께 안전 훈련을 시작할까요?** 🐾</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # 픽셀 아트/게임 분위기 연출
        col_c, col_c2 = st.columns([1, 1])
        with col_c:
            st.markdown("### ", unsafe_allow_html=True) # 공백
        with col_c2:
            st.image("https://i.ibb.co/6P0S00q/cat-pixel-art.png", width=250) # 예시 픽셀 고양이 이미지 (대체 필요)
        
        st.markdown("---")
        
        c1, c2, c3 = st.columns(3)
        with c2:
            if st.button("▶️ 훈련 시작! (1단계로 이동)", type="primary", use_container_width=True):
                st.session_state.game_started = True
                go_to_stage(1)

# B. 1단계: 초기 화재 진압 - 불난 느낌 연출 추가
def render_stage_1():
    st.markdown("<h2 style='color: #ff6347;'>🔥 1단계: 작은 불꽃 진압! 💨</h2>", unsafe_allow_html=True)
    st.markdown("### **집 안에 **작은 불**이 났어요! 연기(💨)가 나기 시작했어요. 빠르게 진압해야 해요!**")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    fire_pos_list = [col1, col2, col3]
    
    # 불난 장소와 주변 연출
    for i, col in enumerate(fire_pos_list):
        with col:
            st.markdown("### " + ("💨" * (i * 2 + 1))) # 연기량 차등 적용

            if i + 1 == st.session_state.fire_loc:
                # 불이 난 위치
                if not st.session_state.is_fire_out:
                    # 불이 안 꺼졌을 때
                    st.markdown("## 🗑️ 🔥 (휴지통에서 불이! 빨리 소화해야 해!)")
                    if st.button("💧 소화 버튼 누르기", key="fire_button", type="primary"):
                        st.session_state.is_fire_out = True
                        st.toast("초기 진압 성공!", icon="💧")
                        st.snow() 
                        st.rerun() 
                else:
                    # 불이 꺼졌을 때
                    st.markdown("## 💧") 
                    st.markdown("### **진압 완료!**")
            else:
                # 불이 안 난 위치: 귀여운 고양이 물건 배치
                if i == 0:
                    st.markdown("## 🧶 (냥이 장난감)")
                elif i == 2:
                    st.markdown("## 🛋️ (푹신한 소파)")
    
    st.markdown("---")

    if st.session_state.is_fire_out:
        st.success("✅ 초기 진압 성공! 이제 대피 경로를 찾아 안전하게 밖으로 나가야 해요. 🚨")
        if st.button("다음 단계 (2단계)로 이동", type="secondary"):
            go_to_stage(2)
    else:
        st.info("🚨 불이 난 곳 아래의 **'소화 버튼'**을 누르세요!")

# C. 2단계: 안전한 대피 경로 선택 - 정답 노출 방지 및 압력 초기값 0
def render_stage_2():
    st.markdown("<h2 style='color: #ff6347;'>🏃‍♀️ 2단계: 소화기 확인 및 대피 경로 선택! 🚨</h2>", unsafe_allow_html=True)
    st.markdown("### **소화기 상태를 점검하고, 연기가 가득한 복도에서 가장 안전한 대피 경로를 선택해야 합니다!**")
    st.markdown("---")

    # 1. 소화기 사용 훈련 (압력 초기값 0)
    st.subheader("1. 소화기 압력 게이지 확인:")
    st.markdown("**소화기 압력 슬라이더를 움직여 초록색 안전 구간(50~70)에 정확히 맞추세요!**")
    
    # 초기값 0으로 설정
    pressure = st.slider("소화기 압력 게이지 조정", 0, 100, **0**, key="pressure_slider")
    
    is_pressure_ok = (50 <= pressure <= 70)
    
    col_p1, col_p2 = st.columns([1, 4])
    with col_p1:
        if is_pressure_ok:
            st.success("👍 합격!")
        else:
            st.error("⚠️ 확인!")
    with col_p2:
        if is_pressure_ok:
            st.info("🔥 압력 확인 완료! 이제 안전이와 함께 탈출 경로를 고민하세요.")
        else:
            st.warning("압력이 올바르지 않으면 소화기가 작동하지 않을 수 있어요!")
            
    st.markdown("---")

    # 2. 대피 경로 선택 - 답을 알려주지 않도록 질문 수정
    st.subheader("2. 안전한 대피 경로 선택:")
    
    if is_pressure_ok:
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
                # 요청하신 '엘베를 누르면 게임 종료' 조건
                show_fail_reason("🚨 엘리베이터는 화재 시 정전되거나 고장으로 갇힐 위험이 있어 **절대** 이용하면 안 됩니다! 🙅‍♀️ 계단 비상구를 이용해야 합니다.")
            else:
                st.warning("경로 A 또는 B를 선택해 주세요.")
    else:
        st.info("먼저 소화기 압력 훈련을 완료해야 대피 경로를 선택할 수 있어요.")

# D. 실패/성공 화면
def render_stage_99():
    st.markdown("<h1 style='color: red; text-align: center;'>🛑 게임 실패! 😭</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"## **🚨 안전이 탈출 실패!**")
    st.markdown(f"### **실패한 이유: {st.session_state.fail_reason}**")
    st.markdown("---")
    st.markdown("### **다음에는 꼭 기억해서 안전이를 지켜주세요!** 😿")
    if st.button("다시 도전하기", type="primary"):
        reset_game()

def render_stage_100():
    st.balloons()
    st.markdown("<h1 style='color: green; text-align: center;'>🎉 최종 성공! 💯</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## **'안전이'와 함께 무사히 대피했습니다! 정말 잘했어요!** 😻")
    st.markdown("---")
    st.markdown("### **✨ 배운 점:** 초기 진압에 성공했고, 안전한 계단 대피를 선택했습니다! 이 두 가지는 생명을 구하는 가장 중요한 행동입니다.")
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
