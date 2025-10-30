# 파일명: safetrip_app_v5.py
# 파일명: safetrip_app_v6.py
import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="SafeTrip: 여행 안전 보고서 (V5)", 
    page_title="SafeTrip: 여행 안전 보고서 (V6)", 
    page_icon="✈️", 
    layout="wide"
)
st.title("✈️ SafeTrip: 여행 안전 보고서 및 점검 (최종판)")
st.title("✈️ SafeTrip: 여행 안전 보고서 및 점검 (최종 안정화)")
st.markdown("여행할 **국가**와 **도시**를 선택하고 **'안전 보고서 검색'** 버튼을 눌러 맞춤형 정보를 확인하세요.")
st.markdown("---")

# --- 1. 샘플 데이터 확장 (도시 목록 대폭 추가) ---
# --- 1. 샘플 데이터 확장 (추천 명소/핫플 정보 추가) ---
safety_data = {
    # 아시아/오세아니아 (총 10개국)
    "한국": {"도시": ["서울", "부산", "제주", "인천", "대구", "대전", "광주", "울산"], "위험 정보": ["치안: 대체로 안전", "교통: 출퇴근 시간 혼잡"], "대처 요령": ["대중교통 이용 권장"], "현지 연락처": {"긴급 전화": "112 (경찰), 119 (구급/소방)"}},
    "일본": {"도시": ["도쿄", "오사카", "후쿠오카", "삿포로", "나고야", "교토", "요코하마"], "위험 정보": ["자연재해: 지진 가능성", "치안: 유흥가 호객행위 주의"], "대처 요령": ["지진 발생 시 'DROP, COVER, HOLD ON' 기억"], "현지 연락처": {"긴급 전화": "110 (경찰), 119 (구급/소방)"}},
    "태국": {"도시": ["방콕", "치앙마이", "푸켓", "파타야", "끄라비", "코사무이"], "위험 정보": ["치안: 관광지 소매치기 주의", "교통: 툭툭 이용 시 가격 흥정 필수"], "대처 요령": ["정부 공인된 택시 앱 사용"], "현지 연락처": {"긴급 전화": "191 (경찰), 1669 (앰뷸런스)"}},
    "베트남": {"도시": ["하노이", "호찌민", "다낭", "나트랑", "푸꾸옥", "호이안"], "위험 정보": ["교통: 오토바이 교통량 매우 많음", "치안: 핸드폰 날치기 주의"], "대처 요령": ["길거리 걸을 때 소지품 보호 철저"], "현지 연락처": {"긴급 전화": "113 (경찰), 115 (앰뷸런스)"}},
    "캄보디아": {"도시": ["프놈펜", "시엠립", "시아누크빌"], "위험 정보": ["치안: 절도 발생 증가", "질병: 뎅기열 모기 주의"], "대처 요령": ["야간 외출 시 택시 이용"], "현지 연락처": {"긴급 전화": "117 (경찰), 119 (앰뷸런스)"}},
    "필리핀": {"도시": ["마닐라", "세부", "보라카이", "팔라완"], "위험 정보": ["치안: 테러 위험 지역 존재", "자연재해: 태풍/지진/화산 활동 주의"], "대처 요령": ["외교부 여행경보 확인 필수"], "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)"}},
    "인도네시아": {"도시": ["자카르타", "발리", "롬복", "욕야카르타"], "위험 정보": ["자연재해: 화산 활동 및 쓰나미 가능성", "교통: 무면허 운전 위험"], "대처 요령": ["현지 택시 대신 검증된 교통수단 이용"], "현지 연락처": {"긴급 전화": "110 (경찰), 118 (앰뷸런스)"}},
    "호주": {"도시": ["시드니", "멜버른", "브리즈번", "퍼스", "애들레이드"], "위험 정보": ["자연재해: 산불 및 폭우", "환경: 독성 생물 주의"], "대처 요령": ["여행 시 야생동물과의 접촉 자제"], "현지 연락처": {"긴급 전화": "000 (경찰/구급/소방)"}},
    "미국": {"도시": ["뉴욕", "LA", "샌프란시스코", "시카고", "마이애미", "라스베이거스", "하와이"], "위험 정보": ["치안: 도심 일부 지역 범죄율 높음", "법규: 총기 사고 주의"], "대처 요령": ["야간에는 인적이 드문 곳 피하기"], "현지 연락처": {"긴급 전화": "911 (경찰/구급/소방)"}},
    "프랑스": {"도시": ["파리", "니스", "마르세유", "리옹"], "위험 정보": ["치안: 관광지 소매치기 성행", "시위: 노동조합 및 정치적 시위 빈번"], "대처 요령": ["시위 구역 회피"], "현지 연락처": {"긴급 전화": "17 (경찰), 15 (앰뷸런스)"}},
    "이탈리아": {"도시": ["로마", "밀라노", "피렌체", "베네치아", "나폴리"], "위험 정보": ["치안: 집시 및 다중시설 소매치기 주의", "환경: 관광지 주변 사기꾼 주의"], "대처 요령": ["가방은 몸 앞으로 메기"], "현지 연락처": {"긴급 전화": "112 (경찰/구급/소방)"}},
    "스페인": {"도시": ["바르셀로나", "마드리드", "세비야", "발렌시아"], "위험 정보": ["치안: 다발성 소매치기", "법규: 거리에서 흡연 규제 엄격"], "대처 요령": ["지정된 흡연 구역 이용"], "현지 연락처": {"긴급 전화": "112 (경찰/구급/소방)"}},
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
@@ -49,38 +49,17 @@
    st.session_state.checklist_status = {item: False for item in check_list}
if "report_searched" not in st.session_state:
    st.session_state.report_searched = False
if "balloons_shown" not in st.session_state: # 풍선 제어 플래그
    st.session_state.balloons_shown = False

# --- 3. 추천 여행지 섹션 (메인 화면) ---
st.subheader("🌟 추천 여행지 핫스팟")
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
        if st.button(f"'{city}' 정보 바로 보기", key=f"rec_btn_{i}", use_container_width=True):
            st.session_state.selected_country = country
            st.session_state.selected_city = city
            st.session_state.report_searched = True
            st.rerun()

st.markdown("---")

# --- 4. 사용자 입력 섹션 (선택 후 검색 방식) ---
# --- 3. 사용자 입력 섹션 (선택 후 검색 방식) ---

st.subheader("📝 안전 보고서 생성")

col_country, col_city = st.columns(2)

# 1. 국가 선택 (Change State on Select)
# 1. 국가 선택
with col_country:
    def update_city_on_country_change():
        # 국가가 변경될 때 도시 선택값을 리셋
@@ -89,9 +68,10 @@ def update_city_on_country_change():
        if current_cities:
            st.session_state.selected_city = current_cities[0]
        else:
            st.session_state.selected_city = ""
            st.session_state.selected_city = "정보 없음"
        st.session_state.selected_country = country_key
        st.session_state.report_searched = False # 검색 상태 해제
        st.session_state.balloons_shown = False # 풍선 상태 리셋

    st.selectbox(
        "① 여행할 국가 선택 🌍", 
@@ -101,11 +81,10 @@ def update_city_on_country_change():
        on_change=update_city_on_country_change 
    )

# 2. 도시 선택 (Depend on Country)
# 2. 도시 선택
with col_city:
    current_cities = safety_data.get(st.session_state.selected_country, {}).get("도시", [])

    # 현재 선택된 도시가 목록에 없거나 목록이 비어있을 경우 처리
    if st.session_state.selected_city not in current_cities and current_cities:
        st.session_state.selected_city = current_cities[0]
    elif not current_cities:
@@ -127,7 +106,7 @@ def update_city_on_country_change():

st.markdown("---")

# --- 5. 안전 보고서 섹션 (검색 버튼 클릭 후에만 나타남) ---
# --- 4. 안전 보고서 섹션 (검색 버튼 클릭 후에만 나타남) ---

selected_country = st.session_state.selected_country
selected_city = st.session_state.selected_city
@@ -139,18 +118,20 @@ def update_city_on_country_change():
        st.error(f"❌ **{selected_country}**에 대한 상세 정보가 없습니다. 목록에서 다른 국가를 선택해 주세요.")
        country_info = {"위험 정보": ["상세 정보 없음. 일반 안전 수칙 준수."], 
                        "대처 요령": ["일반 안전 수칙 확인."], 
                        "현지 연락처": {"긴급 전화": "현지 긴급 연락처 검색 필요"}}
                        "현지 연락처": {"긴급 전화": "현지 긴급 연락처 검색 필요"},
                        "추천": {"명소": ["정보 없음"], "맛집": ["정보 없음"], "핫플": ["정보 없음"]}}

    st.header(f"🔍 **{selected_city}, {selected_country}** 안전 보고서")

    tab1, tab2, tab3, tab4 = st.tabs(["⚠️ 위험 정보", "✅ 대처 요령", "📞 현지 연락처", "📝 여행 전 점검"])
    # 새로운 탭 추가: '추천 명소'
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚠️ 위험 정보", "✅ 대처 요령", "📞 현지 연락처", "📝 여행 전 점검", "✨ 추천 명소/핫플"])

    with tab1:
        st.subheader("⚠️ 주요 안전 위험 및 유의 사항")
        for risk in country_info["위험 정보"]:
            st.warning(f"**{risk}**")
        st.markdown("---")
        # 사고 사례 대신 안전하게 정보를 얻도록 유도
        
        st.markdown("#### 📰 **현지 안전 이슈 검색**")
        st.info("💡 최근 발생한 사고나 뉴스는 실시간으로 변동됩니다. 아래 버튼을 이용해 직접 확인해 보세요.")
        search_query = f"{selected_country} {selected_city} 최근 안전 사고"
@@ -182,7 +163,6 @@ def update_city_on_country_change():
        * **🇰🇷 주 {selected_country} 대한민국 대사관/영사관:** (외교부 사이트에서 직접 검색 후 메모하세요.)
        """)

        # 사용자가 직접 연락처를 메모할 수 있는 텍스트 영역 추가
        st.text_area(
            "대사관/영사관 연락처 메모",
            placeholder="예: +XX-XXX-XXXX (주XX 대사관)",
@@ -197,9 +177,9 @@ def update_city_on_country_change():
        # 체크리스트 항목 렌더링 및 상태 업데이트
        new_checklist_status = {}
        for item in check_list:
            # 체크박스 키에 국가를 포함하여 다른 국가를 검색해도 체크 상태가 유지되지 않도록 함 (다른 나라 체크리스트 분리)
            is_checked = st.checkbox(item, value=st.session_state.checklist_status[item], key=f"check_{item}_{selected_country}")
            new_checklist_status[item] = is_checked

        st.session_state.checklist_status = new_checklist_status

        # 완료 상태 피드백
@@ -208,26 +188,89 @@ def update_city_on_country_change():

        st.markdown(f"---")
        if completed_count == total_count:
            st.balloons()
            # 풍선 제어: 완료 상태이고 아직 풍선이 나오지 않았다면 실행
            if not st.session_state.balloons_shown:
                st.balloons()
                st.session_state.balloons_shown = True # 풍선이 나왔음을 표시
            st.success("🎉 **모든 점검 완료! 안전한 여행이 될 거예요!**")
        else:
            st.warning(f"⚠️ **{total_count}개 중 {completed_count}개 완료.** 남은 항목을 마저 점검하세요!")
        
        # --- 체크리스트 초기화 버튼 위치 수정 ---
        if st.button("체크리스트 초기화", key="reset_checklist_btn"):
            st.session_state.checklist_status = {item: False for item in check_list}
            st.toast("체크리스트가 초기화되었습니다.", icon="🔄")
            st.rerun() # 초기화 후 화면 갱신

# --- 6. 마무리 및 초기화 버튼 수정 ---
st.markdown("---")
col_reset, col_guide = st.columns([1, 4])

with col_reset:
    # --- 체크리스트 초기화 버튼 오류 수정 ---
    if st.button("체크리스트 초기화", type="secondary", use_container_width=True):
        st.session_state.checklist_status = {item: False for item in check_list}
        st.toast("체크리스트가 초기화되었습니다.", icon="🔄")
        st.rerun() # 초기화 후 화면 갱신

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


# --- 5. 마무리 및 추천 여행지 재배치 ---

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
            st.rerun()

st.markdown("---")

col_guide, col_map = st.columns(2)

with col_guide:
    st.markdown("### 🗺️ 지도 기능에 대하여")
    # 지도 시각화가 어렵다는 점을 다시 안내합니다.
    st.info("기술적인 제약으로 인해 실시간 지도는 구현이 어렵습니다. 대신, 여행지 **관련 안전 지침을 시각화한 이미지**를 원하시면 요청해 주세요! (예: )")
    st.info("요청하신 대로 **실시간 지도** 대신 **국가 이미지 지도**로 대체하였습니다. 여행지의 지리적 위치를 시각적으로 확인해 보세요!")
    
with col_map:
    st.subheader(f"🌐 {selected_country} 지도 이미지")
    # 지도 이미지 태그 추가 (사용자 요청 반영)
    st.markdown(f"")

st.markdown("---")
st.markdown("© 2025 SafeTrip Assistant")
