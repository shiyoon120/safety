# 파일명: safetrip_app_v3.py
import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="SafeTrip: 여행 안전 보고서 (V3)", 
    page_icon="✈️", 
    layout="wide"
)
st.title("✈️ SafeTrip: 여행 안전 보고서 및 점검")
st.markdown("여행할 **도시**를 입력하거나 목록에서 **국가**를 선택하여 맞춤형 안전 정보를 확인하세요.")
st.markdown("---")

# --- 1. 샘플 데이터 확장 (지원 국가 대폭 추가 및 구조화) ---
# 데이터는 '국가' 키로 저장되며, 도시 검색 시 해당 국가의 데이터를 보여줍니다.
safety_data = {
    # 아시아/오세아니아 (총 10개국)
    "한국": {"도시": ["서울", "부산", "제주"], "위험 정보": ["치안: 대체로 안전", "교통: 출퇴근 시간 혼잡"], "대처 요령": ["대중교통 이용 권장"], "현지 연락처": {"긴급 전화": "112 (경찰), 119 (구급/소방)"}},
    "일본": {"도시": ["도쿄", "오사카", "후쿠오카"], "위험 정보": ["자연재해: 지진 가능성", "치안: 유흥가 호객행위 주의"], "대처 요령": ["지진 발생 시 'DROP, COVER, HOLD ON' 기억"], "현지 연락처": {"긴급 전화": "110 (경찰), 119 (구급/소방)"}},
    "태국": {"도시": ["방콕", "치앙마이", "푸켓"], "위험 정보": ["치안: 관광지 소매치기 주의", "교통: 툭툭 이용 시 가격 흥정 필수"], "대처 요령": ["정부 공인된 택시 앱 사용"], "현지 연락처": {"긴급 전화": "191 (경찰), 1669 (앰뷸런스)"}},
    "베트남": {"도시": ["하노이", "호찌민", "다낭"], "위험 정보": ["교통: 오토바이 교통량 매우 많음", "치안: 핸드폰 날치기 주의"], "대처 요령": ["길거리 걸을 때 소지품 보호 철저"], "현지 연락처": {"긴급 전화": "113 (경찰), 115 (앰뷸런스)"}},
    "캄보디아": {"도시": ["프놈펜", "시엠립"], "위험 정보": ["치안: 절도 발생 증가", "질병: 뎅기열 모기 주의"], "대처 요령": ["야간 외출 시 택시 이용"], "현지 연락처": {"긴급 전화": "117 (경찰), 119 (앰뷸런스)"}},
    "필리핀": {"도시": ["마닐라", "세부"], "위험 정보": ["치안: 테러 위험 지역 존재", "자연재해: 태풍/지진/화산 활동 주의"], "대처 요령": ["외교부 여행경보 확인 필수"], "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)"}},
    "인도네시아": {"도시": ["자카르타", "발리"], "위험 정보": ["자연재해: 화산 활동 및 쓰나미 가능성", "교통: 무면허 운전 위험"], "대처 요령": ["현지 택시 대신 검증된 교통수단 이용"], "현지 연락처": {"긴급 전화": "110 (경찰), 118 (앰뷸런스)"}},
    "호주": {"도시": ["시드니", "멜버른"], "위험 정보": ["자연재해: 산불 및 폭우", "환경: 독성 생물 주의"], "대처 요령": ["여행 시 야생동물과의 접촉 자제"], "현지 연락처": {"긴급 전화": "000 (경찰/구급/소방)"}},
    "인도": {"도시": ["뉴델리", "뭄바이"], "위험 정보": ["치안: 여성 여행객 특별 주의", "위생: 수질 및 음식 위생 주의"], "대처 요령": ["여성 전용 칸이나 숙소 이용 고려"], "현지 연락처": {"긴급 전화": "100 (경찰), 102 (앰뷸런스)"}},
    "중국": {"도시": ["베이징", "상하이"], "위험 정보": ["법규: 인터넷 검열 및 데이터 통제", "교통: 차량 통행량 많음"], "대처 요령": ["VPN 등 통신 환경 사전 준비"], "현지 연락처": {"긴급 전화": "110 (경찰), 120 (앰뷸런스)"}},

    # 미주 (총 4개국)
    "미국": {"도시": ["뉴욕", "LA", "샌프란시스코"], "위험 정보": ["치안: 도심 일부 지역 범죄율 높음", "법규: 총기 사고 주의"], "대처 요령": ["야간에는 인적이 드문 곳 피하기"], "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)"}},
    "캐나다": {"도시": ["토론토", "밴쿠버"], "위험 정보": ["자연재해: 겨울철 폭설 및 한파", "환경: 야생동물과의 조우 주의"], "대처 요령": ["기온 변화에 맞는 의류 준비"], "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)"}},
    "멕시코": {"도시": ["멕시코시티", "칸쿤"], "위험 정보": ["치안: 조직 범죄 관련 위험 지역 존재", "교통: 교통 경찰 사칭 사기 주의"], "대처 요령": ["관광객 밀집 지역에 머물기"], "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)"}},
    "브라질": {"도시": ["리우데자네이루", "상파울루"], "위험 정보": ["치안: 강도 및 소매치기 위험 매우 높음", "질병: 지카 바이러스, 황열병 주의"], "대처 요령": ["고가품 착용 최소화"], "현지 연락처": {"긴급 전화": "190 (경찰), 192 (앰뷸런스)"}},

    # 유럽 (총 7개국)
    "영국": {"도시": ["런던", "에든버러"], "위험 정보": ["테러: 테러 경계 수준 상시 확인", "교통: 좌측통행 주의"], "대처 요령": ["좌측통행 습관화"], "현지 연락처": {"긴급 전화": "999 또는 112 (경찰/구급/소방)"}},
    "프랑스": {"도시": ["파리", "니스"], "위험 정보": ["치안: 관광지 소매치기 성행", "시위: 노동조합 및 정치적 시위 빈번"], "대처 요령": ["시위 구역 회피"], "현지 연락처": {"긴급 전화": "17 (경찰), 15 (앰뷸런스)"}},
    "이탈리아": {"도시": ["로마", "밀라노"], "위험 정보": ["치안: 집시 및 다중시설 소매치기 주의", "환경: 관광지 주변 사기꾼 주의"], "대처 요령": ["가방은 몸 앞으로 메기"], "현지 연락처": {"긴급 전화": "112 (경찰/구급/소방)"}},
    "독일": {"도시": ["베를린", "뮌헨"], "위험 정보": ["치안: 대체로 안전하나, 기차역 주변 주의", "교통: 무임승차 단속 엄격"], "대처 요령": ["기차표는 반드시 유효성 확인"], "현지 연락처": {"긴급 전화": "110 (경찰), 112 (구급/소방)"}},
    "스페인": {"도시": ["바르셀로나", "마드리드"], "위험 정보": ["치안: 다발성 소매치기", "법규: 거리에서 흡연 규제 엄격"], "대처 요령": ["지정된 흡연 구역 이용"], "현지 연락처": {"긴급 전화": "112 (경찰/구급/소방)"}},
    "러시아": {"도시": ["모스크바", "상트페테르부르크"], "위험 정보": ["법규: 현지 법규 및 정부 정책 변화에 유의", "환경: 겨울철 혹한"], "대처 요령": ["외교부 지침 상시 확인"], "현지 연락처": {"긴급 전화": "102 (경찰), 103 (앰뷸런스)"}},
    "튀르키예": {"도시": ["이스탄불", "앙카라"], "위험 정보": ["치안: 국경 인접 지역 여행 경보 확인", "자연재해: 지진 가능성"], "대처 요령": ["여행 전 지진 대피 훈련 숙지"], "현지 연락처": {"긴급 전화": "112 (경찰/구급/소방)"}},
}

# 도시 이름을 검색했을 때 해당 도시가 속한 국가를 찾아주는 매핑 테이블 생성
city_to_country = {}
for country, info in safety_data.items():
    for city in info["도시"]:
        city_to_country[city.lower()] = country

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
    st.session_state.selected_country = "한국" 
if "search_initiated" not in st.session_state:
    st.session_state.search_initiated = False
if "checklist_status" not in st.session_state:
    st.session_state.checklist_status = {item: False for item in check_list}

# --- 3. 사용자 입력 섹션 (도시 입력으로 변경) ---

col_select, col_input = st.columns(2)

# Selectbox 입력 (국가 선택)
with col_select:
    selected_from_list = st.selectbox(
        "① 국가 목록에서 선택 🌍", 
        list(safety_data.keys()), 
        index=list(safety_data.keys()).index(st.session_state.selected_country),
        key="country_select"
    )

# Text_input 입력 (도시 이름 입력)
with col_input:
    # 사용자 정의 입력 기능을 도시 검색에 맞게 수정
    city_input = st.text_input(
        "② 여행할 도시 이름 입력 (예: 파리, 뉴욕)", 
        placeholder="도시 이름 입력 후 검색 버튼 클릭",
        key="city_input"
    )

# 검색할 최종 국가 결정 로직
final_country = selected_from_list # 기본값은 selectbox에서 선택된 국가
search_term_used = selected_from_list # 검색에 사용된 최종 용어 (국가명 또는 도시명)

if city_input:
    # 도시 입력이 있을 경우, 소문자로 변환하여 매핑 테이블에서 국가를 찾음
    country_from_city = city_to_country.get(city_input.lower())
    if country_from_city:
        final_country = country_from_city
        search_term_used = city_input
    else:
        # 도시를 찾지 못했으나, selectbox 값을 기본으로 유지
        pass 
        
# --- 버튼 섹션 ---
col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1])

with col_btn1:
    if st.button("안전 보고서 검색", type="primary", use_container_width=True):
        st.session_state.selected_country = final_country
        st.session_state.search_initiated = True
        st.session_state.search_term_used = search_term_used # 검색 용어 저장
        st.experimental_rerun()

with col_btn2:
    if st.button("초기화", use_container_width=True):
        st.session_state.selected_country = "한국"
        st.session_state.search_initiated = False
        st.session_state.checklist_status = {item: False for item in check_list}
        st.experimental_rerun()

with col_btn3:
    # 지도 기능은 구현이 어려우므로 시각적인 도움을 주는 영역으로 대체 (구현 예정 문구 유지)
    if st.button("지도에서 선택 (구현 예정)", disabled=True, use_container_width=True):
         st.info("지도 선택 기능은 현재 개발 중입니다. 목록이나 입력창을 이용해 주세요.")


st.markdown("---")

# --- 4. 안전 보고서 섹션 (Tabs로 전문화) ---

if not st.session_state.search_initiated:
    st.info("위에 여행할 국가를 선택하거나 **도시를 입력**한 후 '안전 보고서 검색' 버튼을 눌러주세요.")
else:
    # 최종 선택된 국가의 정보
    country_info = safety_data.get(st.session_state.selected_country)
    
    # 검색된 국가가 데이터에 없는 경우의 대체 정보
    if not country_info:
        st.error(f"❌ **{st.session_state.selected_country}**에 대한 상세 정보가 없습니다. 목록에서 선택하거나 다른 도시를 검색해 주세요.")
        # 정보가 없을 때 표시할 기본값 설정
        country_info = {"위험 정보": ["상세 정보 없음. 일반 안전 수칙 준수."], 
                        "대처 요령": ["일반 안전 수칙 확인."], 
                        "현지 연락처": {"긴급 전화": "현지 긴급 연락처 검색 필요", "대사관": "현지 대사관 연락처 검색 필요"}}

    st.header(f"🔍 **{st.session_state.selected_country}** 안전 보고서")
    
    # 탭 구성 (전문성 강화)
    tab1, tab2, tab3, tab4 = st.tabs(["⚠️ 위험 정보", "✅ 대처 요령", "📞 현지 연락처", "📝 여행 전 점검"])

    with tab1:
        st.subheader("⚠️ 주요 안전 위험 및 유의 사항")
        for risk in country_info["위험 정보"]:
            st.warning(f"**{risk}**")
        st.markdown("---")
        st.info("💡 여행지별 특화된 위험 요소를 사전에 인지하는 것이 중요합니다. 특히 도시별로 치안 수준이 다를 수 있습니다.")

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
        * **🇰🇷 주 현지 대한민국 대사관/영사관:** 해당 지역 대사관/영사관을 검색하여 메모해 주세요.
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
