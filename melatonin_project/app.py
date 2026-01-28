import streamlit as st
import datetime
import numpy as np
import pandas as pd

# 1. 페이지 설정 (아이콘 수정: 밤/낮 모두 어울리는 기어로 변경)
st.set_page_config(page_title="SYSO AI Alignment", page_icon="🧬", layout="wide")

# 2. 커스텀 CSS (라이트/다크 모드 범용 스타일)
st.markdown("""
    <style>
    /* 메트릭 카드: 배경색에 투명도를 주어 테마에 적응하도록 설정 */
    div[data-testid="stMetric"] {
        background-color: rgba(124, 77, 255, 0.05); 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid rgba(124, 77, 255, 0.3);
        border-left: 5px solid #7c4dff;
    }
    /* 폰트 스타일 미세 조정 */
    .stMarkdown h4 {
        color: #7c4dff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 섹션 (아이콘을 낮/밤 중립적인 것으로 변경)
st.title("🧬 지원님 맞춤형 수면 솔루션")
st.markdown("#### *SYSO Algorithm based Data-Driven Circadian Alignment & Morning Forecast*")
st.divider()

# 4. 입력 섹션 (사이드바)
with st.sidebar:
    st.header("⌚ Real-time Sync")
    st.info("갤럭시/애플워치 생체 지표 연동 중...")
    
    temp_trend = st.slider("야간 손목 온도 추이 (CBT 변곡점 예측)", -1.0, 1.0, 0.2)
    sleep_efficiency = st.slider("최근 7일 수면 효율 (%)", 50, 100, 88)
    hrv_today = st.number_input("오늘 아침 HRV (심박 변이도)", value=52)
    
    st.divider()
    st.subheader("📋 주관적 컨디션")
    subjective_fatigue = st.select_slider("기상 직후 잔여 졸음 정도", 
                                          options=["매우 개운", "개운", "보통", "약간 졸림", "매우 졸림"], 
                                          value="보통")

# 5. 메인 분석 엔진 (로직 동일)
base_time = datetime.datetime.combine(datetime.date.today(), datetime.time(22, 0))
offset_map = {"매우 개운": -30, "개운": -15, "보통": 0, "약간 졸림": 30, "매우 졸림": 60}
logic_offset = offset_map[subjective_fatigue]
temp_correction = -20 if temp_trend > 0.4 else 10 

sync_time_start = base_time + datetime.timedelta(minutes=logic_offset + temp_correction)
sync_time_end = sync_time_start + datetime.timedelta(minutes=30)

# 6. 결과 레이아웃
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎯 섭취 골든 타임")
    st.metric(label="Intake Time (섭취 가이드)", 
              value=f"{sync_time_start
