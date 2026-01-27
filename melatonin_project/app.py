import streamlit as st
import datetime
import numpy as np
import pandas as pd

# 1. 페이지 설정 (비즈니스 대시보드 스타일)
st.set_page_config(page_title="SYSO AI Alignment", page_icon="🌙", layout="wide")

# 2. 커스텀 CSS (심미적 완성도)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #7c4dff; }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 섹션
st.title("🌙 SYSO: 생체 리듬 동기화 알고리즘")
st.markdown("#### *SYSO Algorithm based Data-Driven Circadian Alignment & Morning Forecast*")
st.divider()

# 4. 입력 섹션: 웨어러블 데이터 연동 시뮬레이션
with st.sidebar:
    st.header("⌚ Real-time Sync")
    st.info("갤럭시/애플워치 생체 지표 연동 중...")
    
    # DLMO 예측을 위한 손목 온도 변수
    temp_trend = st.slider("야간 손목 온도 추이 (CBT 변곡점 예측)", -1.0, 1.0, 0.2)
    # 수면 구조 분석 (REM/Deep)
    sleep_efficiency = st.slider("최근 7일 수면 효율 (%)", 50, 100, 88)
    # 기상 시 HRV
    hrv_today = st.number_input("오늘 아침 HRV (심박 변이도)", value=52)
    
    st.divider()
    st.subheader("📋 주관적 컨디션")
    subjective_fatigue = st.select_slider("기상 직후 잔여 졸음 정도", 
                                          options=["매우 개운", "개운", "보통", "약간 졸림", "매우 졸림"], 
                                          value="보통")

# 5. 메인 분석 엔진 (PK & 서카디안 로직)
# [Logic 1] PK 기반 Intake Window 계산
# 식물성 멜라토닌 Tmax(최고 농도 도달 시간)를 1시간으로 가정
base_time = datetime.datetime.combine(datetime.date.today(), datetime.time(22, 0))
# 기상 졸음(잔여농도)에 따른 지연값 계산
offset_map = {"매우 개운": -30, "개운": -15, "보통": 0, "약간 졸림": 30, "매우 졸림": 60}
logic_offset = offset_map[subjective_fatigue]

# [Logic 2] 온도 기반 DLMO 예측 보정
temp_correction = -20 if temp_trend > 0.4 else 10 # 온도가 높으면 리듬 지연 -> 전진 섭취 유도

# 최종 Sync Time 도출
sync_time_start = base_time + datetime.timedelta(minutes=logic_offset + temp_correction)
sync_time_end = sync_time_start + datetime.timedelta(minutes=30)

# 6. 결과 레이아웃
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎯 섭취 골든 타임")
    st.metric(label="Intake Time (섭취 가이드)", value=f"{sync_time_start.strftime('%H:%M')} ~ {sync_time_end.strftime('%H:%M')}")
    st.caption("상쾌한 아침을 위한 최적 섭취 가이드")

with col2:
    # 서카디안 정렬 지수 (Circadian Alignment Index) 계산
    # 수면 효율과 체온 안정도를 점수화
    alignment_score = int(sleep_efficiency * 0.7 + (1 - abs(temp_trend)) * 30)
    st.subheader("📊 나의 생체 시계 점수")
    st.metric(label="Circadian Alignment Index (서카디안 정렬 지수)", value=f"{alignment_score} / 100")
    st.progress(alignment_score / 100)

with col3:
    # 굿모닝 리커버리 예측 (Morning Forecast)
    # HRV와 수면 효율을 결합하여 다음 날 컨디션 예측
    recovery_forecast = int((hrv_today / 80 * 50) + (sleep_efficiency / 100 * 50))
    st.subheader("☀️ 오늘 아침 나의 컨디션")
    st.metric(label="morning condition score (모닝 컨디션 점수)", value=f"{recovery_forecast} 점")
    st.caption("오늘 예상 컨디션 지수")

st.divider()

# 7. 기술적 시각화: 1구획 모델(One-Compartment Model) 시뮬레이션
st.subheader("📈 나의 수면 리듬을 읽는 시간")
t = np.linspace(0, 12, 100)
# 식물성 원료의 흡수/소실 곡선 시뮬레이션
cp = 5 * (np.exp(-0.3 * t) - np.exp(-1.5 * t)) # 가상의 1구획 흡수 모델

chart_data = pd.DataFrame({
    'Time (hours)': t,
    'Plant-based Melatonin Conc.': cp,
    'Therapeutic Window': [0.8] * len(t)
})

st.line_chart(chart_data.set_index('Time (hours)'))
st.info(f"💡 **AI 가이드:** 현재 데이터 분석 결과, 지원님의 생체 시계는 실제 수면보다 30분 지연되어 있습니다. 오늘 밤 정해진 **'Sync Time'**에 루틴을 수행하여 리듬을 {abs(temp_correction)}분 앞당기는 것을 추천합니다.")

# 8. 하단 법적/기술적 가이드 (발표 참고용)
st.sidebar.markdown("""
---
**Technical Edge:**
- PK-based Intake Window
- DLMO Prediction via CBT
- morning condition score
""")
