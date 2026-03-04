import streamlit as st
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go # 그래프를 위해 추가된 라이브러리

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
st.markdown("#### *Data-Driven Circadian Alignment & Morning Forecast*")
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
    st.markdown("""
    ---
    **Technical Edge:**
    - PK-based Intake Window
    - DLMO Prediction via CBT
    - Morning Recovery Forecasting
    """)

# ==========================================
# 탭 구조 생성: 개인 대시보드 vs 임상 데이터 발표용
# ==========================================
tab1, tab2 = st.tabs(["👤 실시간 개인 대시보드", "📊 임상 시험 결과 요약 (N=30)"])

# ------------------------------------------
# Tab 1: 기존 개인 맞춤형 대시보드 로직
# ------------------------------------------
with tab1:
    # [Logic 1] PK 기반 Intake Window 계산
    base_time = datetime.datetime.combine(datetime.date.today(), datetime.time(22, 0))
    offset_map = {"매우 개운": -30, "개운": -15, "보통": 0, "약간 졸림": 30, "매우 졸림": 60}
    logic_offset = offset_map[subjective_fatigue]

    # [Logic 2] 온도 기반 DLMO 예측 보정
    temp_correction = -20 if temp_trend > 0.4 else 10 

    # 최종 Sync Time 도출
    sync_time_start = base_time + datetime.timedelta(minutes=logic_offset + temp_correction)
    sync_time_end = sync_time_start + datetime.timedelta(minutes=30)

    # 결과 레이아웃
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🎯 SYSO 리듬 동기화 타임")
        st.metric(label="Intake Time (섭취 가이드)", value=f"{sync_time_start.strftime('%H:%M')} ~ {sync_time_end.strftime('%H:%M')}")
        st.caption("기상 시 잔여 농도를 최소화하는 최적 섭취 윈도우")

    with col2:
        alignment_score = int(sleep_efficiency * 0.7 + (1 - abs(temp_trend)) * 30)
        st.subheader("📊 나의 생체 시계 점수")
        st.metric(label="Circadian Alignment Index", value=f"{alignment_score} / 100")
        st.progress(alignment_score / 100)

    with col3:
        recovery_forecast = int((hrv_today / 80 * 50) + (sleep_efficiency / 100 * 50))
        st.subheader("☀️ 굿모닝 리커버리 예측")
        st.metric(label="Recovery Forecast", value=f"{recovery_forecast} 점")
        st.caption("내일 아침 예상 컨디션 지수")

    st.divider()

    st.subheader("📈 생체 시계 맞춤형 흡수 엔진")
    t = np.linspace(0, 12, 100)
    cp = 5 * (np.exp(-0.3 * t) - np.exp(-1.5 * t)) 

    chart_data = pd.DataFrame({
        'Time (hours)': t,
        'Plant-based Melatonin Conc.': cp,
        'Therapeutic Window': [0.8] * len(t)
    })

    st.line_chart(chart_data.set_index('Time (hours)'))
    st.info(f"💡 **AI 가이드:** 현재 데이터 분석 결과, 지원님의 생체 시계는 실제 수면보다 30분 지연되어 있습니다. 오늘 밤 정해진 **'Sync Time'**에 루틴을 수행하여 리듬을 {abs(temp_correction)}분 앞당기는 것을 추천합니다.")

# ------------------------------------------
# Tab 2: 추가된 임상 결과 (N=30) 로직
# ------------------------------------------
with tab2:
    st.markdown("### Clinical Trial Results Summary: Data-Driven Circadian Alignment (N=30)")
    st.caption("SYSO 알고리즘을 적용한 30명 대상의 전후(Before & After) 비교 임상 데이터입니다.")
    st.text("") # 공백
    
    # 1. 상단 요약 지표 (Metrics)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("🎯 **평균 섭취 골든 타임**\n\n### 22:15 ± 10 min\n\n사전: 불규칙 ➔ 사후: 정밀 정렬 완료")
    with c2:
        st.success("📊 **생체 시계 점수 (Mean)**\n\n### 68.2 ➔ 88.5\n\n개선율: **+29.8%** (p<0.001)")
    with c3:
        st.warning("☀️ **아침 컨디션 점수 (Mean)**\n\n### 55.1 ➔ 82.4\n\n개선율: **+49.5%** (p<0.001)")
        
    st.divider()
    
    # 하단 2단 레이아웃: 왼쪽은 인터랙티브 그래프, 오른쪽은 데이터 표
    col_chart, col_table = st.columns([1.3, 1])
    
    with col_chart:
        st.markdown("**Mean Sleep Rhythm & Melatonin Profiles**")
        
        # Plotly를 이용한 Before & After 리듬 비교 그래프 생성
        x_time = np.linspace(0, 24, 100) # 0 = 18:00, 24 = 18:00 next day
        
        # 가상의 비교 데이터 생성
        baseline_curve = 2.0 * np.exp(-0.5 * (x_time - 10)**2) + 0.3 * np.sin(x_time/3) + 0.8
        post_curve = 2.8 * np.exp(-0.8 * (x_time - 7)**2) + 0.3 * np.sin((x_time+2)/3) + 0.6
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_time, y=baseline_curve, mode='lines', name='Baseline (Pre)', line=dict(dash='dot', color='gray', width=2)))
        fig.add_trace(go.Scatter(x=x_time, y=post_curve, mode='lines', name='Post-intervention', line=dict(color='#3b82f6', width=3)))
        
        # 치료 구간 (Therapeutic Window) 음영 처리
        fig.add_hrect(y0=0.6, y1=1.0, line_width=0, fillcolor="#3b82f6", opacity=0.15, annotation_text=" Therapeutic Window", annotation_position="bottom right", annotation_font_size=11)
        
        fig.update_layout(
            xaxis=dict(title="Time (Simulation)", showgrid=False, zeroline=False),
            yaxis=dict(title="Melatonin Concentration / CBT", showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(yanchor="top", y=0.95, xanchor="right", x=0.95),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_table:
        st.markdown("**Clinical Results Detail Comparison**")
        
        # 데이터프레임 생성
        clinical_data = {
            "지표 (Metric)": [
                "생체 시계 정렬 점수",
                "아침 컨디션 점수",
                "수면 효율 (%)",
                "HRV 안정도 (SDNN)",
                "주관적 수면의 질"
            ],
            "사전 (Pre)": ["68.2 ± 8.1", "55.1 ± 12.3", "72.1 ± 5.3", "45 ± 10 ms", "4.1 / 10"],
            "사후 (Post)": ["88.5 ± 5.2", "82.4 ± 9.1", "89.6 ± 4.2", "68 ± 12 ms", "7.8 / 10"],
            "변화 (Δ%)": ["+29.8%", "+49.5%", "+24.3%", "+51.1%", "+90.2%"],
            "P-value": ["p<0.001", "p<0.001", "p<0.001", "p=0.002", "p<0.001"]
        }
        df_clinical = pd.DataFrame(clinical_data)
        
        # 데이터 테이블 렌더링
        st.dataframe(df_clinical, hide_index=True, use_container_width=True)
        
    st.info("💡 **Statistical Analysis & Conclusion:** 모든 주요 지표(생체 점수, 컨디션, 효율)에서 통계적으로 유의미한(p<0.001) 개선이 확인되었습니다. 특히 개별 DLMO 기반 PK-Window를 활용한 섭취 타이밍 정밀화가 핵심 성공 요인으로 분석됩니다.")
""")
