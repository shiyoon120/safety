# 파일명: safetrip_app_v7_no_reset.py
import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="SafeTrip: 여행 안전 보고서 (V7)", 
    page_icon="✈️", 
    layout="wide"
)
st.title("✈️ SafeTrip: 여행 안전 보고서 및 점검 (최종 안정화)")
st.markdown("여행할 **국가**와 **도시**를 선택하고 **'안전 보고서 검색'** 버튼을 눌러 맞춤형 정보를 확인하세요.")
st.markdown("---")

# --- 1. 샘플 데이터 확장 ---
safety_data = {
    "한국": {"도시": ["서울", "부산", "제주", "인천", "대구", "대전", "광주", "울산"], "위험 정보": ["치안: 대체로 안전", "교통: 출퇴근 시간 혼잡"], "대처 요령": ["대중교통 이용 권장"], "현지 연락처": {"긴급 전화": "112 (경찰), 119 (구급/소방)"}, "추천": {"명소": ["경복궁", "남산타워"], "맛집": ["광장시장", "명동교자"], "핫플": ["홍대", "성수동"]}},
    "일본": {"도시": ["도쿄", "오사카", "후쿠오카", "삿포로", "나고야", "교토", "요코하마"], "위험 정보": ["자연재해: 지진 가능성", "치안: 유흥가 호객행위 주의"], "대처 요령": ["지진 발생 시 'DROP, COVER, HOLD ON' 기억"], "현지 연락처": {"긴급 전화": "110 (경찰), 119 (구급/소방)"}, "추천": {"명소": ["후지산", "도쿄 타워"], "맛집": ["라멘 골목", "오코노미야키"], "핫플": ["시부야", "신주쿠"]}},
    "태국": {"도시": ["방콕", "치앙마이", "푸켓", "파타야", "끄라비", "코사무이"], "위험 정보": ["치안: 관광지 소매치기 주의", "교통: 툭툭 이용 시 가격 흥정 필수"], "대처 요령": ["정부 공인된 택시 앱 사용"], "현지 연락처": {"긴급 전화": "191 (경찰), 1669 (앰뷸런스)"}, "추천": {"명소": ["왓 아룬", "왕궁"], "맛집": ["카오산 로드 노점", "팟타이"], "핫플": ["루프탑 바", "클럽"]}},
    "베트남": {"도시": ["하노이", "호찌민", "다낭", "나트랑", "푸꾸옥", "호이안"], "위험 정보": ["교통: 오토바이 교통량 매우 많음", "치안: 핸드폰 날치기 주의"], "대처 요령": ["길거리 걸을 때 소지품 보호 철저"], "현지 연락처": {"긴급 전화": "113 (경찰), 115 (앰뷸런스)"}, "추천": {"명소": ["하롱베이", "호이안 구시가지"], "맛집": ["쌀국수", "반미"], "핫플": ["카페거리", "비어헐"]}},
    "캄보디아": {"도시": ["프놈펜", "시엠립", "시아누크빌"], "위험 정보": ["치안: 절도 발생 증가", "질병: 뎅기열 모기 주의"], "대처 요령": ["야간 외출 시 택시 이용"], "현지 연락처": {"긴급 전화": "117 (경찰), 119 (앰뷸런스)"}, "추천": {"명소": ["앙코르와트"], "맛집": ["아목", "록락"], "핫플": ["펍 스트리트"]}},
    "필리핀": {"도시": ["마닐라", "세부", "보라카이", "팔라완"], "위험 정보": ["치안: 테러 위험 지역 존재", "자연재해: 태풍/지진/화산 활동 주의"], "대처 요령": ["외교부 여행경보 확인 필수"], "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)"}, "추천": {"명소": ["초콜릿 힐"], "맛집": ["레촌", "할로할로"], "핫플": ["화이트 비치"]}},
    "인도네시아": {"도시": ["자카르타", "발리", "롬복", "욕야카르타"], "위험 정보": ["자연재해: 화산 활동 및 쓰나미 가능성", "교통: 무면허 운전 위험"], "대처 요령": ["현지 택시 대신 검증된 교통수단 이용"], "현지 연락처": {"긴급 전화": "110 (경찰), 118 (앰뷸런스)"}, "추천": {"명소": ["우붓 원숭이 숲", "보로부두르 사원"], "맛집": ["나시 고랭"], "핫플": ["스미냑"]}},
    "호주": {"도시": ["시드니", "멜버른", "브리즈번", "퍼스", "애들레이드"], "위험 정보": ["자연재해: 산불 및 폭우", "환경: 독성 생물 주의"], "대처 요령": ["여행 시 야생동물과의 접촉 자제"], "현지 연락처": {"긴급 전화": "000 (경찰/구급/소방)"}, "추천": {"명소": ["오페라 하우스", "그레이트 오션 로드"], "맛집": ["미트 파이"], "핫플": ["달링 하버"]}},
    "미국": {"도시": ["뉴욕", "LA", "샌프란시스코", "시카고", "마이애미", "라스베이거스", "하와이"], "위험 정보": ["치안: 도심 일부 지역 범죄율 높음", "법규: 총기 사고 주의"], "대처 요령": ["야간에는 인적이 드문 곳 피하기"], "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)"}, "추천": {"명소": ["자유의 여신상", "그랜드 캐니언"], "맛집": ["인앤아웃 버거"], "핫플": ["타임스퀘어"]}},
    "프랑스": {"도시": ["파리", "니스", "마르세유", "리옹"], "위험 정보": ["치안: 관광지 소매치기 성행", "시위: 노동조합 및 정치적 시위 빈번"], "대처 요령": ["시위 구역 회피"], "현지 연락처": {"긴급 전화": "17 (경찰), 15 (앰뷸런스)"}, "추천": {"명소": ["에펠탑", "루브르 박물관"], "맛집": ["크루아상", "마카롱"], "핫플": ["마레 지구"]}},
    "이탈리아": {"도시": ["로마", "밀라노", "피렌체", "베네치아", "나폴리"], "위험 정보": ["치안: 집시 및 다중시설 소매치기 주의", "환경: 관광지 주변 사기꾼 주의"], "대처 요령": ["가방은 몸 앞으로 메기"], "현지 연락처": {"긴급 전화": "112 (경찰/구급/소방)"}, "추천": {"명소": ["콜로세움", "두오모 성당"], "맛집": ["파스타", "젤라또"], "핫플": ["트레비 분수"]}},
    "스페인": {"도시": ["바르셀로나", "마드리드", "세비야", "발렌시아"], "위험 정보": ["치안: 다발성 소매치기", "법규: 거리에서 흡연 규제 엄격"], "대처 요령": ["지정된 흡연 구역 이용"], "현지 연락처": {"긴급 전화": "112 (경찰/구급/소방)"}, "추천": {"명소": ["사그라다 파밀리아", "알람브라"], "맛집": ["빠에야", "츄러스"], "핫플": ["람블라스 거리"]}},
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
    st.session_state.selected_country = "한국" 
if "selected_city" not in st.session_state:
    st.session_state.selected_city = "서울"
# 'checklist_status'를 국가별로 분리 저장하는 딕셔너리로 초기화
if "checklist_status" not in st.session_state:
    st.session_state.checklist_status = {} # { "국가명": { "항목": False, ... } }
if "report_searched" not in st.session_state:
    st.session_state.report_searched = False
if "balloons_shown" not in st.session_state: # 풍선 제어 플래그
    st.session_state.balloons_shown = False


# --- 3. 사용자 입력 섹션 (선택 후 검색 방식) ---

st.subheader("📝 안전 보고서 생성")

col_country, col_city = st.columns(2)

# 1. 국가 선택
with col_country:
    def update_city_on_country_change():
        # 국가가 변경될 때 도시 선택값을 리셋
        country_key = st.session_state.country_select
        current_cities = safety_data.get(country_key, {}).get("도시", [])
        if current_cities:
            st.session_state.selected_city = current_cities[0]
        else:
            st.session_state.selected_city = "정보 없음"
        st.session_state.selected_country = country_key
        st.session_state.report_searched = False # 검색 상태 해제
        st.session_state.balloons_shown = False # 풍선 상태 리셋

    st.selectbox(
        "① 여행할 국가 선택 🌍", 
        list(safety_data.keys()), 
        index=list(safety_data.keys()).index(st.session_state.selected_country),
        key="country_select",
        on_change=update_city_on_country_change 
    )

# 2. 도시 선택
with col_city:
    current_cities = safety_data.get(st.session_state.selected_country, {}).get("도시", [])
    
    if st.session_state.selected_city not in current_cities and current_cities:
        st.session_state.selected_city = current_cities[0]
    elif not current_cities:
        st.session_state.selected_city = "정보 없음"

    st.selectbox(
        "② 여행할 도시 선택 🏙️",
        current_cities,
        index=current_cities.index(st.session_state.selected_city) if st.session_state.selected_city in current_cities else 0,
        key="city_select",
        on_change=lambda: st.session_state.update(selected_city=st.session_state.city_select, report_searched=False, balloons_shown=False) # 선택 시 검색 상태 해제 및 풍선 리셋
    )

col_btn1, col_btn2 = st.columns([1.5, 3])
with col_btn1:
    if st.button("안전 보고서 검색", type="primary", use_container_width=True):
        st.session_state.report_searched = True
        # 검색 시 현재 국가의 체크리스트 상태가 없으면 초기화
        if st.session_state.selected_country not in st.session_state.checklist_status:
            st.session_state.checklist_status[st.session_state.selected_country] = {item: False for item in check_list}
        st.rerun()

st.markdown("---")

# --- 4. 안전 보고서 섹션 (검색 버튼 클릭 후에만 나타남) ---

selected_country = st.session_state.selected_country
selected_city = st.session_state.selected_city
country_info = safety_data.get(selected_country)

if st.session_state.report_searched:
    
    if not country_info:
        st.error(f"❌ **{selected_country}**에 대한 상세 정보가 없습니다. 목록에서 다른 국가를 선택해 주세요.")
        country_info = {"위험 정보": ["상세 정보 없음. 일반 안전 수칙 준수."], 
                        "대처 요령": ["일반 안전 수칙 확인."], 
                        "현지 연락처": {"긴급 전화": "현지 긴급 연락처 검색 필요"},
                        "추천": {"명소": ["정보 없음"], "맛집": ["정보 없음"], "핫플": ["정보 없음"]}}

    st.header(f"🔍 **{selected_city}, {selected_country}** 안전 보고서")
    
    # 현재 국가의 체크리스트 상태 가져오기 
    current_checklist_status = st.session_state.checklist_status.get(selected_country, {item: False for item in check_list})
    
    # 새로운 탭 추가
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚠️ 위험 정보", "✅ 대처 요령", "📞 현지 연락처", "📝 여행 전 점검", "✨ 추천 명소/핫플"])

    with tab1:
        st.subheader("⚠️ 주요 안전 위험 및 유의 사항")
        for risk in country_info["위험 정보"]:
            st.warning(f"**{risk}**")
        st.markdown("---")
        
        st.markdown("#### 📰 **현지 안전 이슈 검색**")
        st.info("💡 최근 발생한 사고나 뉴스는 실시간으로 변동됩니다. 아래 버튼을 이용해 직접 확인해 보세요.")
        search_query = f"{selected_country} {selected_city} 최근 안전 사고"
        st.link_button(
            f"구글에서 '{selected_city} 안전 사고' 검색하기", 
            f"https://www.google.com/search?q={search_query}",
            use_container_width=True
        )
        

    with tab2:
        st.subheader("✅ 위험 상황별 행동 요령")
        for tip in country_info["대처 요령"]:
            st.success(f"**{tip}**")
        
        st.markdown("---")
        st.markdown("#### 🚨 일반 긴급 상황 대처법")
        st.markdown("""
        * **도난/분실:** 즉시 경찰 신고 및 영사관에 연락. 신용카드 정지.
        * **자연재해:** 현지 재난 방송 청취, 대피소로 이동.
        """)
        
    with tab3:
        st.subheader("📞 현지 필수 비상 연락망 및 메모")
        contact = country_info["현지 연락처"]
        
        st.markdown(f"""
        * **🚨 현지 긴급 전화 (경찰/소방/앰뷸런스):** **{contact.get("긴급 전화", "정보 없음")}**
        * **🇰🇷 주 {selected_country} 대한민국 대사관/영사관:** (외교부 사이트에서 직접 검색 후 메모하세요.)
        """)
        
        # 텍스트 에어리어는 세션 상태를 사용하지 않고 바로 키로 관리
        st.text_area(
            "대사관/영사관 연락처 메모",
            placeholder="예: +XX-XXX-XXXX (주XX 대사관)",
            key=f"embassy_memo_{selected_country}" # 국가별로 메모 분리
        )
        st.info("☎️ 현지 대사관 연락처는 [외교부 해외안전여행](https://www.mofa.go.kr/www/index.do) 사이트에서 **직접 확인** 후 메모해 두는 것이 가장 정확합니다.")

    with tab4:
        st.subheader("📝 여행 전 필수 점검 목록")
        st.markdown("아래 항목을 모두 완료하여 안전한 여행을 준비하세요.")
        
        # 체크리스트 항목 렌더링 및 상태 업데이트
        new_checklist_status = {}
        for item in check_list:
            # 현재 국가의 상태를 사용하여 체크박스를 표시
            is_checked = st.checkbox(item, 
                                     value=current_checklist_status.get(item, False), 
                                     key=f"check_{item}_{selected_country}")
            new_checklist_status[item] = is_checked
        
        # 변경된 상태를 현재 국가의 세션 상태에 반영
        st.session_state.checklist_status[selected_country] = new_checklist_status
        current_checklist_status = new_checklist_status # 반영된 상태로 업데이트
        
        # 완료 상태 피드백
        completed_count = sum(current_checklist_status.values())
        total_count = len(check_list)
        
        st.markdown(f"---")
        if completed_count == total_count:
            # 풍선 제어: 완료 상태이고 아직 풍선이 나오지 않았다면 실행
            if not st.session_state.balloons_shown:
                st.balloons()
                st.session_state.balloons_shown = True # 풍선이 나왔음을 표시
            st.success("🎉 **모든 점검 완료! 안전한 여행이 될 거예요!**")
        else:
            # 완료되지 않았으면 풍선 상태 리셋 (다시 체크 풀었을 경우)
            st.session_state.balloons_shown = False
            st.warning(f"⚠️ **{total_count}개 중 {completed_count}개 완료.** 남은 항목을 마저 점검하세요!")
        
        # --- 체크리스트 초기화 버튼 제거됨 ---


    with tab5:
        st.subheader(f"✨ {selected_city} 추천 명소, 맛집, 핫플")
        
        rec_data = country_info["추천"]
        
        col_m, col_b, col_h = st.columns(3)
        
        with col_m:
            st.info("📌 **추천 명소**")
            for item in rec_data["명소"]:
                st.markdown(f"• {item}")
        
        with col_b:
            st.info("🍽️ **추천 맛집**")
            for item in rec_data["맛집"]:
                st.markdown(f"• {item}")
                
        with col_h:
            st.info("🔥 **추천 핫플레이스**")
            for item in rec_data["핫플"]:
                st.markdown(f"• {item}")
                
        st.markdown("---")
        st.info("💡 더 많은 정보를 원하시면 구글에서 검색해 보세요.")
        search_query_trip = f"{selected_country} {selected_city} 추천 여행지"
        st.link_button(
            f"구글에서 '{selected_city} 추천 명소' 검색하기", 
            f"https://www.google.com/search?q={search_query_trip}",
            use_container_width=True
        )
    
    # --- 5. 지도 섹션 (검색 후에만 표시) ---
    st.markdown("---")
    col_guide, col_map = st.columns(2)

    with col_guide:
        st.markdown("### 🗺️ 지도 기능에 대하여")
        st.info("요청하신 대로 **실시간 지도** 대신 **국가 이미지 지도**로 대체하였습니다. 여행지의 지리적 위치를 시각적으로 확인해 보세요!")
        
    with col_map:
        st.subheader(f"🌐 {selected_country} 지리적 정보")
        # 실제 이미지를 넣을 수 없으므로, 아이콘과 텍스트로 대체
        st.warning(f"**🚧 지리적 위치 확인:** 현재 선택하신 **{selected_country}**의 도시 **{selected_city}**는 지도상에 [📍] 위치에 해당합니다.", icon="🗺️")
        st.caption("_(Streamlit 앱에 실제 지도를 표시하려면 별도의 이미지 파일을 준비하거나, `st.map()` 함수를 사용해야 합니다.)_")


# --- 6. 추천 여행지 섹션 (검색 전, 메인 화면에만 표시) ---
if not st.session_state.report_searched:
    st.markdown("---")
    st.subheader("🌟 놓치지 마세요! 추천 여행지 핫스팟")
    col_rec1, col_rec2, col_rec3 = st.columns(3)

    # 추천 로직 (임의 지정)
    recommendations = [
        ("도쿄", "일본", "안전한 치안, 지진 대비 필수!"),
        ("파리", "프랑스", "소매치기 주의, 문화재 중심 관광"),
        ("발리", "인도네시아", "자연재해 및 교통 혼잡 주의"),
    ]

    for i, (city, country, desc) in enumerate(recommendations):
        col = [col_rec1, col_rec2, col_rec3][i]
        with col:
            st.info(f"**{city} ({country})**", icon="📌")
            st.caption(desc)
            if st.button(f"'{city}' 정보 바로 보기", key=f"rec_btn_final_{i}", use_container_width=True):
                st.session_state.selected_country = country
                st.session_state.selected_city = city
                st.session_state.report_searched = True
                # 추천 국가/도시 선택 시 체크리스트 상태 초기화/불러오기
                if country not in st.session_state.checklist_status:
                    st.session_state.checklist_status[country] = {item: False for item in check_list}
                st.rerun()

st.markdown("—")
st.markdown("© 2025 SafeTrip Assistant")
