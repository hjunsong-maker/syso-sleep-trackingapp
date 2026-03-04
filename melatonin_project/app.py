import streamlit as st
import datetime
import numpy as np
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="SYSO AI Alignment", page_icon="🌙", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #7c4dff; }
    </style>
    """, unsafe_allow_html=True)

# 2. 헤더 및 사이드바
st.title("🌙 SYSO: 생체 리듬 동기화 알고리즘")
st.markdown("#### *Data-Driven Circadian Alignment & Morning Forecast*")
st.divider()

with st.sidebar:
    st.header("⌚ Real-time Sync")
    temp_trend = st.slider("야간 손목 온도 추이 (CBT 예측)", -1.0, 1.0, 0.2)
    sleep_efficiency = st.slider("최근 7일 수면 효율 (%)", 50, 100, 88)
    hrv_today = st.number_input("오늘 아침 HRV", value=52)
    st.divider()
    subjective_fatigue = st.select_slider("기상 직후 컨디션", options=["매우 개운", "개운", "보통", "약간 졸림", "매우 졸림"], value="보통")

# 3. 탭 구성
tab1, tab2 = st.tabs(["👤 실시간 개인 대시보드", "📊 임상 시험 결과 요약 (N=30)"])

with tab1:
    st.subheader("개인 시뮬레이션 화면입니다. (발표용은 옆의 탭을 눌러주세요)")
    st.info("좌측 슬라이더를 움직여 실시간 동기화를 테스트해보세요.")

with tab2:
    st.markdown("### Clinical Trial Results Summary (N=30)")
    c1, c2, c3 = st.columns(3)
    with c1: st.info("🎯 **평균 섭취 타임**\n### 22:15 ± 10m")
    with c2: st.success("📊 **생체 시계 점수**\n### 68.2 → 88.5 (+30%)")
    with c3: st.warning("☀️ **아침 컨디션**\n### 55.1 → 82.4 (+50%)")
        
    st.divider()
    col_chart, col_table = st.columns([1.2, 1])
    
    with col_chart:
        st.markdown("**Mean Sleep Rhythm & Melatonin Profiles**")
        # Plotly 대신 Streamlit 기본 차트 사용
        x_time = np.linspace(0, 24, 100)
        baseline = 2.0 * np.exp(-0.5 * (x_time - 10)**2) + 0.8
        post = 2.8 * np.exp(-0.8 * (x_time - 7)**2) + 0.6
        
        chart_data = pd.DataFrame({
            'Time': x_time,
            'Baseline (Pre)': baseline,
            'Post-intervention': post
        }).set_index('Time')
        
        st.line_chart(chart_data) # 기본 차트로 출력
        
    with col_table:
        st.markdown("**Detailed Comparison**")
        df_clinical = pd.DataFrame({
            "Metric": ["Alignment Score", "Morning Condition", "Sleep Efficiency", "HRV (SDNN)"],
            "Pre": ["68.2", "55.1", "72.1%", "45ms"],
            "Post": ["88.5", "82.4", "89.6%", "68ms"],
            "P-value": ["p<0.001", "p<0.001", "p<0.001", "p=0.002"]
        })
        st.dataframe(df_clinical, hide_index=True, use_container_width=True)
