# 파일명: safetrip_app_v2.py
import streamlit as st
import random
import pandas as pd
from io import StringIO

st.set_page_config(
    page_title="SafeTrip: 여행 안전 보고서 (V2)", 
    page_icon="✈️", 
    layout="wide" # 넓은 레이아웃 사용
)
st.title("✈️ SafeTrip: 여행 안전 보고서 및 점검")
st.markdown("여행지를 입력하거나 목록에서 선택하여 맞춤형 안전 정보를 확인하세요.")
st.markdown("---")

# --- 1. 샘플 데이터 확장 및 구조화 ---
# 치안, 자연재해, 질병/위생 등 위험 요소를 세분화
safety_data = {
    "캄보디아": {
        "위험 정보": ["**치안**: 소매치기 및 절도 발생 증가.", "**질병**: 뎅기열, 말라리아 모기 주의.", "**교통**: 오토바이 사고 위험 높음."],
        "대처 요령": ["야간 외출 시 택시 이용.", "장기 노출 옷 및 모기 기피제 사용.", "여권은 안전금고에 보관."],
        "현지 연락처": {"긴급 전화": "117 (경찰), 119 (앰뷸런스)", "대사관": "+855-23-211-937 (프놈펜)"}
    },
    "일본": {
        "위험 정보": ["**자연재해**: 지진 및 쓰나미 가능성.", "**치안**: 대체로 안전하나, 유흥가 호객행위 주의.", "**환경**: 일부 지역 방사능 모니터링 필요."],
        "대처 요령": ["지진 발생 시 'DROP, COVER, HOLD ON' 기억.", "숙소의 대피 경로 및 대피 장소 확인.", "비상 식량/물 준비."],
        "현지 연락처": {"긴급 전화": "110 (경찰), 119 (구급/소방)", "대사관": "+81-3-3452-7611 (도쿄)"}
    },
    "태국": {
        "위험 정보": ["**치안**: 관광지 소매치기, 바가지 요금 사기 주의.", "**교통**: 택시 및 툭툭 이용 시 가격 흥정 필수.", "**질병**: 식중독 및 수인성 질병 주의."],
        "대처 요령": ["여행자 보험 가입 필수.", "음식은 익혀 먹고, 포장된 물만 마시기.", "정부 공인된 택시 앱 사용."],
        "현지 연락처": {"긴급 전화": "191 (경찰), 1669 (앰뷸런스)", "대사관": "+66-2-247-7537~39 (방콕)"}
    },
    "미국": {
        "위험 정보": ["**치안**: 도심 일부 지역 범죄율 높음.", "**법규**: 주(State)별 총기 소지법 및 마약 관련 법규 상이.", "**자연재해**: 허리케인, 토네이도 등 기상 이변 가능성."],
        "대처 요령": ["야간에는 인적이 드문 곳 피하기.", "현지 문화 및 법규 사전 숙지.", "비상 상황 시 즉시 911 신고."],
        "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)", "총영사관": "+1-213-385-9300 (LA)"}
    },
    "한국": {
        "위험 정보": ["**치안**: 대체로 안전.", "**교통**: 출퇴근 시간 교통 체증 유의.", "**기상**: 여름철 장마/태풍, 겨울철 폭설 대비."],
        "대처 요령": ["대중교통 이용 권장.", "날씨 정보 상시 확인."],
        "현지 연락처": {"긴급 전화": "112 (경찰), 119 (구급/소방)", "여행자 안내": "1330"}
    }
}

# 여행 전 필수 점검 리스트
check_list = [
    "여권/비자 유효 기간 확인",
    "여행자 보험 가입 완료",
    "현지 긴급 연락처 저장",
    "신용카드 분실 신고처 메모",
    "여행지 날씨 및 복장 확인",
    "상비약(해열제, 소화제 등) 준비"
]

# --- 2. 세션 상태 초기화 및 관리 ---

if "selected_country" not in st.session_state:
    st.session_state.selected_country = "한국" # 초기값 설정
if "search_initiated" not in st.session_state:
    st.session_state.search_initiated = False
if "checklist_status" not in st.session_state:
    # 체크리스트 상태 초기화
    st.session_state.checklist_status = {item: False for item in check_list}

# --- 3. 사용자 입력 섹션 (입력 방식 다양화) ---

col_select, col_input = st.columns(2)

# Selectbox 입력
with col_select:
    selected_from_list = st.selectbox(
        "① 목록에서 선택 ✈️", 
        list(safety_data.keys()), 
        index=list(safety_data.keys()).index(st.session_state.selected_country),
        key="country_select"
    )

# Text_input 입력
with col_input:
    # 사용자 정의 입력 기능 추가
    country_input = st.text_input(
        "② 직접 국가 이름 입력 (예: 프랑스, 이탈리아)", 
        placeholder="국가명 입력 후 검색 버튼 클릭",
        key="country_input"
    )

# 검색할 최종 국가 결정
final_country = selected_from_list
if country_input and country_input in safety_data:
    final_country = country_input

# --- 버튼 섹션 ---
col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1])

with col_btn1:
    if st.button("안전 보고서 검색", type="primary", use_container_width=True):
        st.session_state.selected_country = final_country
        st.session_state.search_initiated = True
        st.experimental_rerun()

with col_btn2:
    if st.button("초기화", use_container_width=True):
        st.session_state.selected_country = "한국"
        st.session_state.search_initiated = False
        st.session_state.checklist_status = {item: False for item in check_list}
        st.experimental_rerun()

with col_btn3:
    # 지도 기능은 Streamlit 자체에서 구현이 복잡하므로, 지도 시뮬레이션을 위한 더미 버튼 제공
    if st.button("지도에서 선택 (구현 예정)", disabled=True, use_container_width=True):
         st.info("지도 선택 기능은 현재 개발 중입니다. 목록이나 입력창을 이용해 주세요.")


st.markdown("---")

# --- 4. 안전 보고서 섹션 (Tabs로 전문화) ---

if not st.session_state.search_initiated:
    st.info("위에 여행할 국가를 선택하거나 입력한 후 '안전 보고서 검색' 버튼을 눌러주세요.")
else:
    country_info = safety_data.get(st.session_state.selected_country)
    
    if not country_info:
        st.error(f"❌ **{st.session_state.selected_country}**에 대한 상세 정보가 없습니다. 일반 안전 수칙을 확인하세요.")
        country_info = {"위험 정보": ["상세 정보 없음. 일반 안전 수칙 준수."], "대처 요령": ["일반 안전 수칙 확인."], "현지 연락처": {"긴급 전화": "현지 긴급 연락처 검색 필요", "대사관": "현지 대사관 연락처 검색 필요"}}

    st.header(f"🔍 **{st.session_state.selected_country}** 안전 보고서")
    
    # 탭 구성 (전문성 강화)
    tab1, tab2, tab3, tab4 = st.tabs(["⚠️ 위험 정보", "✅ 대처 요령", "📞 현지 연락처", "📝 여행 전 점검"])

    with tab1:
        st.subheader("⚠️ 주요 안전 위험 및 유의 사항")
        for risk in country_info["위험 정보"]:
            st.warning(f"**{risk}**")
        st.markdown("---")
        st.info("💡 여행지별 특화된 위험 요소를 사전에 인지하는 것이 중요합니다.")

    with tab2:
        st.subheader("✅ 위험 상황별 행동 요령")
        for tip in country_info["대처 요령"]:
            st.success(f"**{tip}**")
        
        st.markdown("---")
        # 일반적인 긴급 상황 대처법
        st.markdown("#### 🚨 일반 긴급 상황 대처법")
        st.markdown("""
        * **도난/분실:** 즉시 경찰 신고 및 영사관에 연락. 신용카드 정지.
        * **자연재해:** 현지 재난 방송 청취, 대피소로 이동. 절대 당황하지 않기.
        * **긴급 의료:** 앰뷸런스 호출 후, 보험사에 연락하여 병원 정보 확인.
        """)
        
    with tab3:
        st.subheader("📞 현지 필수 비상 연락망")
        contact = country_info["현지 연락처"]
        
        st.markdown(f"""
        * **🚨 현지 긴급 전화 (경찰/소방/앰뷸런스):** **{contact.get("긴급 전화", "정보 없음")}**
        * **🇰🇷 주 현지 대한민국 대사관/영사관:** **{contact.get("대사관", "정보 없음")}**
        """)
        st.markdown("---")
        st.info("☎️ 현지 긴급 전화와 대사관 번호를 출국 전 **반드시 메모**해 두세요.")

    with tab4:
        st.subheader("📝 여행 전 필수 점검 목록")
        st.markdown("아래 항목을 모두 완료하여 안전한 여행을 준비하세요.")
        
        # 체크리스트 항목 렌더링 및 상태 업데이트
        new_checklist_status = {}
        for item in check_list:
            # key를 사용하여 상태가 유지되도록 함
            is_checked = st.checkbox(item, value=st.session_state.checklist_status[item], key=f"check_{item}")
            new_checklist_status[item] = is_checked

        st.session_state.checklist_status = new_checklist_status
        
        # 완료 상태 피드백
        completed_count = sum(st.session_state.checklist_status.values())
        total_count = len(check_list)
        
        st.markdown(f"---")
        if completed_count == total_count:
            st.balloons()
            st.success("🎉 **모든 점검 완료! 안전한 여행이 될 거예요!**")
        else:
            st.warning(f"⚠️ **{total_count}개 중 {completed_count}개 완료.** 남은 항목을 마저 점검하세요!")

# --- 5. 마무리 ---
st.sidebar.markdown("## 📚 안전 여행 가이드")
st.sidebar.info("여행 안전은 준비에서 시작됩니다. 이 가이드가 당신의 여행을 더 안전하게 지켜줄 거예요.")

st.markdown("---")
st.markdown("© 2025 SafeTrip Assistant")
