import streamlit as st
import datetime
import numpy as np
import pandas as pd

# 1. 페이지 설정 (라이트/다크 모두 어울리는 아이콘으로 변경)
st.set_page_config(page_title="SYSO AI Alignment", page_icon="🧬", layout="wide")

# 2. 커스텀 CSS (핵심: 어떤 테마에서도 가독성이 좋은 반투명 스타일)
st.markdown("""
    <style>
    /* 메트릭 카드: 배경에 투명도를 주어 시스템 테마 배경색이 비치도록 설정 */
    div[data-testid="stMetric"] {
        background-color: rgba(124, 77, 255, 0.08); 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid rgba(124, 77, 255, 0.2);
        border-left: 5px solid #7c4dff;
    }
    /* 텍스트 가독성 보정 */
    .stMarkdown h4 {
        color: #7c4dff;
        font-weight: 600;
    }
    /* 하단 가이드 박스 스타일링 */
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 섹션
st.title("🧬 지원님 맞춤형 수면 솔루션")
st.markdown("#### *SYSO Algorithm based Data-Driven Circadian Alignment & Morning Forecast*")
st.divider()

# 4. 입력 섹션: 사이드바 (원본 로직 유지)
with st.sidebar:
    st.header("⌚ 실시간 데이터 분석")
    st.info("갤럭시/애플워치 생체 지표 연동 중...")
    
    # 데이터 입력 슬라이더
    temp_trend = st.slider("야간 손목 온도 추이 (CBT 변곡점 예측)", -1.0, 1.0, 0.2)
    sleep_efficiency = st.slider("최근 7일 수면 효율 (%)", 50, 100, 88)
    hrv_today = st.number_input("오늘 아침 HRV (심박 변이도)", value=52)
    
    st.divider()
    st.subheader("📋 주관적 컨디션")
    subjective_fatigue = st.select_slider("기상 직후 잔여 졸음 정도", 
                                          options=["매우 개운", "개운", "보통", "약간 졸림", "매우 졸림"], 
                                          value="보통")

# 5. 메인 분석 엔진 (원본 PK & 서카디안 로직 유지)
base_time = datetime.datetime.combine(datetime.date.today(), datetime.time(22, 0))
offset_map = {"매우 개운": -30, "개운": -15, "보통": 0, "약간 졸림": 30, "매우 졸림": 60}
logic_offset = offset_map[subjective_fatigue]

# 온도 기반 DLMO 예측 보정
temp_correction = -20 if temp_trend > 0.4 else 10 

# 최종 Sync Time 도출
sync_time_start = base_time + datetime.timedelta(minutes=logic_offset + temp_correction)
sync_time_end = sync_time_start + datetime.timedelta(minutes=30)

# 6. 결과 레이아웃 (3단 구성)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎯 섭취 골든 타임")
    st.metric(label="Intake Time (섭취 가이드)", 
              value=f"{sync_time_start.strftime('%H:%M')} ~ {sync_time_end.strftime('%H:%M')}")
    st.caption("상쾌한 아침을 위한 최적 섭취 가이드")

with col2:
    # 서카디안 정렬 지수 계산
    alignment_score = int(sleep_efficiency * 0.7 + (1 - abs(temp_trend)) * 30)
    st.subheader("📊 나의 생체 시계 점수")
    st.metric(label="Circadian Alignment Index", value=f"{alignment_score} / 100")
    st.progress(alignment_score / 100)

with col3:
    # 굿모닝 리커버리 예측
    recovery_forecast = int((hrv_today / 80 * 50) + (sleep_efficiency / 100 * 50))
    st.subheader("☀️ 오늘 아침 나의 컨디션")
    st.metric(label="Morning Condition Score", value=f"{recovery_forecast} 점")
    st.caption("오늘 예상 컨디션 지수")

st.divider()

# 7. 기술적 시각화: 1구획 모델 시뮬레이션
st.subheader("📈 나의 수면 리듬을 읽는 시간")
t = np.linspace(0, 12, 100)
cp = 5 * (np.exp(-0.3 * t) - np.exp(-1.5 * t)) 

chart_data = pd.DataFrame({
    'Time (hours)': t,
    'Plant-based Melatonin Conc.': cp,
    'Therapeutic Window': [0.8] * len(t)
})

# 스트림릿 기본 차트는 테마를 자동으로 따라갑니다.
st.line_chart(chart_data.set_index('Time (hours)'))

# 분석 가이드 메시지
st.info(f"💡 **AI 가이드:** 현재 데이터 분석 결과, 지원님의 생체 시계는 실제 수면보다 {abs(logic_offset)}분 가량 편차가 있습니다. 오늘 밤 정해진 **'Sync Time'**에 루틴을 수행하여 리듬을 보정하는 것을 추천합니다.")

# 8. 하단 사이드바 (기술 정보)
st.sidebar.markdown("""
---
**Technical Edge:**
- PK-based Intake Window
- DLMO Prediction via CBT
- Morning Condition Score
""")
