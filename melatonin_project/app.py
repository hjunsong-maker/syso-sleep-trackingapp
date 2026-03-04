import streamlit as st
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="SYSO AI Alignment", page_icon="🌙", layout="wide")

# 2. 커스텀 CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #7c4dff; }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 섹션
st.title("🌙 SYSO: 생체 리듬 동기화 알고리즘")
st.markdown("#### *Data-Driven Circadian Alignment & Morning Forecast*")
st.divider()

# 4. 사이드바 설정
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
    st.markdown("""
---
**Technical Edge:**
- PK-based Intake Window
- DLMO Prediction via CBT
- Morning Recovery Forecasting
""")

# 5. 탭 구성
tab1, tab2 = st.tabs(["👤 실시간 개인 대시보드", "📊 임상 시험 결과 요약 (N=30)"])

# --- Tab 1: 개인 대시보드 ---
with tab1:
    base_time = datetime.datetime.combine(datetime.date.today(), datetime.time(22, 0))
    offset_map = {"매우 개운": -30, "개운": -15, "보통": 0, "약간 졸림": 30, "매우 졸림": 60}
    logic_offset = offset_map[subjective_fatigue]
    temp_correction = -20 if temp_trend > 0.4 else 10 

    sync_time_start = base_time + datetime.timedelta(minutes=logic_offset + temp_correction)
    sync_time_end = sync_time_start + datetime.timedelta(minutes=30)
