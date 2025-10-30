# 파일명: safetrip_app_v7_full.py
import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(
    page_title="SafeTrip: 여행 안전 보고서 (V7)", 
    page_icon="✈️", 
    layout="wide"
)

st.title("✈️ SafeTrip: 여행 안전 보고서 및 점검 (V7)")
st.markdown("여행할 **국가**와 **도시**를 선택하고 **'안전 보고서 검색'** 버튼을 눌러 맞춤형 정보를 확인하세요.")
st.markdown("---")

# --- 1. V6 전체 데이터 + 지도/좌표 ---
safety_data = {
    "한국": {"도시": ["서울","부산","제주","인천","대구","대전","광주","울산"],
             "위험 정보": ["치안: 대체로 안전","교통: 출퇴근 시간 혼잡"],
             "대처 요령": ["대중교통 이용 권장"],
             "현지 연락처": {"긴급 전화":"112/119"},
             "추천": {"명소":["경복궁","남산타워"], "맛집":["광장시장","명동교자"], "핫플":["홍대","성수동"]},
             "지도":"images/한국.png",
             "좌표":{"서울":(300,200),"부산":(400,350),"제주":(200,500),"인천":(250,180),"대구":(320,300),"대전":(280,270),"광주":(260,350),"울산":(420,330)}
            },
    "일본": {"도시": ["도쿄","오사카","후쿠오카","삿포로","나고야","교토","요코하마"],
             "위험 정보": ["자연재해: 지진 가능성","치안: 유흥가 호객행위 주의"],
             "대처 요령": ["지진 발생 시 'DROP, COVER, HOLD ON' 기억"],
             "현지 연락처": {"긴급 전화":"110/119"},
             "추천": {"명소":["후지산","도쿄타워"], "맛집":["라멘골목","오코노미야키"], "핫플":["시부야","신주쿠"]},
             "지도":"images/일본.png",
             "좌표":{"도쿄":(250,180),"오사카":(180,300),"후쿠오카":(100,350),"삿포로":(200,80),"나고야":(200,250),"교토":(190,280),"요코하마":(260,190)}
            },
    "태국": {"도시":["방콕","치앙마이","푸켓","파타야","끄라비","코사무이"],
             "위험 정보":["치안: 관광지 소매치기 주의","교통: 툭툭 이용 시 가격 흥정 필수"],
             "대처 요령":["정부 공인된 택시 앱 사용"],
             "현지 연락처":{"긴급 전화":"191/1669"},
             "추천":{"명소":["왓 아룬","왕궁"],"맛집":["카오산 로드 노점","팟타이"],"핫플":["루프탑 바","클럽"]},
             "지도":"images/태국.png",
             "좌표":{"방콕":(250,300),"치앙마이":(200,100),"푸켓":(180,400),"파타야":(260,320),"끄라비":(170,420),"코사무이":(220,410)}
            },
    "미국": {"도시":["뉴욕","LA","샌프란시스코","시카고","마이애미","라스베이거스","하와이"],
             "위험 정보":["치안: 도심 일부 지역 범죄율 높음","법규: 총기 사고 주의"],
             "대처 요령":["야간에는 인적 드문 곳 피하기"],
             "현지 연락처":{"긴급 전화":"911"},
             "추천":{"명소":["자유의 여신상","그랜드 캐니언"],"맛집":["인앤아웃버거"],"핫플":["타임스퀘어"]},
             "지도":"images/미국.png",
             "좌표":{"뉴욕":(350,200),"LA":(50,300),"샌프란시스코":(70,150),"시카고":(300,180),"마이애미":(380,350),"라스베이거스":(100,250),"하와이":(20,400)}
            },
    "프랑스": {"도시":["파리","니스","마르세유","리옹"],
               "위험 정보":["치안: 관광지 소매치기 성행","시위: 노동조합 및 정치적 시위 빈번"],
               "대처 요령":["시위 구역 회피"],
               "현지 연락처":{"긴급 전화":"17/15"},
               "추천":{"명소":["에펠탑","루브르"],"맛집":["크루아상","마카롱"],"핫플":["마레 지구"]},
               "지도":"images/프랑스.png",
               "좌표":{"파리":(250,200),"니스":(400,350),"마르세유":(380,400),"리옹":(300,300)}
              },
    # 나머지 V6 국가/도시 데이터도 같은 방식으로 추가...
}

check_list = [
    "여권/비자 유효 기간 확인",
    "여행자 보험 가입 완료",
    "현지 긴급 연락처 저장",
    "신용카드 분실 신고처 메모",
    "여행지 날씨 및 복장 확인",
    "상비약 준비"
]

# --- 2. 세션 상태 초기화 ---
if "selected_country" not in st.session_state: st.session_state.selected_country = "한국"
if "selected_city" not in st.session_state: st.session_state.selected_city = "서울"
if "checklist_status" not in st.session_state: st.session_state.checklist_status = {item: False for item in check_list}
if "report_searched" not in st.session_state: st.session_state.report_searched = False
if "balloons_shown" not in st.session_state: st.session_state.balloons_shown = False

# --- 3. 사용자 입력 UI ---
col_country, col_city = st.columns(2)

with col_country:
    country_list = list(safety_data.keys())
    country_selected = st.selectbox("① 여행할 국가 선택 🌍", country_list,
                                    index=country_list.index(st.session_state.selected_country))
    if country_selected != st.session_state.selected_country:
        st.session_state.selected_country = country_selected
        st.session_state.selected_city = safety_data[country_selected]["도시"][0]
        st.session_state.report_searched = False
        st.session_state.balloons_shown = False

with col_city:
    city_list = safety_data[st.session_state.selected_country]["도시"]
    city_selected = st.selectbox("② 여행할 도시 선택 🏙️", city_list,
                                 index=city_list.index(st.session_state.selected_city))
    if city_selected != st.session_state.selected_city:
        st.session_state.selected_city = city_selected
        st.session_state.report_searched = False
        st.session_state.balloons_shown = False

col_btn1, _ = st.columns([2,3])
with col_btn1:
    if st.button("안전 보고서 검색", type="primary"):
        st.session_state.report_searched = True
        st.rerun()

st.markdown("---")

# --- 4. 안전 보고서 섹션 ---
if st.session_state.report_searched:
    country = st.session_state.selected_country
    city = st.session_state.selected_city
    info = safety_data[country]
    
    st.header(f"🔍 {city}, {country} 안전 보고서")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚠️ 위험 정보","✅ 대처 요령","📞 현지 연락처","📝 여행 전 점검","✨ 추천 명소/핫플"])
    
    with tab1:
        st.subheader("⚠️ 주요 안전 위험 및 유의 사항")
        for r in info["위험 정보"]:
            st.warning(r)
    with tab2:
        st.subheader("✅ 위험 상황별 행동 요령")
        for t in info["대처 요령"]:
            st.success(t)
    with tab3:
        st.subheader("📞 현지 비상 연락망")
        st.text(f"🚨 긴급 전화: {info['현지 연락처']['긴급 전화']}")
    with tab4:
        st.subheader("📝 여행 전 점검")
        new_status = {}
        for item in check_list:
            checked = st.checkbox(item, value=st.session_state.checklist_status[item], key=f"{item}_{country}")
            new_status[item] = checked
        st.session_state.checklist_status = new_status
        
        if all(new_status.values()) and not st.session_state.balloons_shown:
            st.balloons()
            st.session_state.balloons_shown = True
        
        if st.button("체크리스트 초기화"):
            st.session_state.checklist_status = {item: False for item in check_list}
            st.rerun()
    
    with tab5:
        st.subheader(f"✨ {city} 추천 명소, 맛집, 핫플")
        st.markdown("• " + "\n• ".join(info["추천"]["명소"]))
        st.markdown("• " + "\n• ".join(info["추천"]["맛집"]))
        st.markdown("• " + "\n• ".join(info["추천"]["핫플"]))

    # --- 지도 이미지 + 선택 도시 마크 ---
    st.subheader(f"🌐 {country} 지도")
    map_img = Image.open(info["지도"])
    draw = ImageDraw.Draw(map_img)
    if city in info["좌표"]:
        x, y = info["좌표"][city]
        draw.ellipse((x-5, y-5, x+5, y+5), fill="red")
    st.image(map_img, use_column_width=True)

st.markdown("---")
st.markdown("© 2025 SafeTrip Assistant")
