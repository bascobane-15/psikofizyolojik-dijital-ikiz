import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA AYARLARI (En başta olmalı)
st.set_page_config(page_title="POLAR TWIN | Dijital İkiz", layout="wide")

# --- GELİŞMİŞ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #0a192f, #112240); color: #FFFFFF !important; }
    p, span, label, .stMarkdown, [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 600; }
    [data-testid="stSidebar"] { background-color: #020c1b !important; border-right: 2px solid #00d4ff; }
    h1, h2, h3 { color: #00d4ff !important; text-shadow: 2px 2px 4px #000000; }
    div[data-testid="metric-container"] {
        background-color: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        padding: 15px;
        border-radius: 15px;
    }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. LOGOLAR VE BAŞLIK
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_l:
    st.image("https://upload.wikimedia.org/wikipedia/tr/b/b3/Teknofest_logo.png", width=130)
with col_m:
    st.markdown("<h1 style='text-align: center;'>🚀 POLAR TWIN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Teknofest & TÜBİTAK Proje Paneli</p>", unsafe_allow_html=True)
with col_r:
    st.image("https://upload.wikimedia.org/wikipedia/tr/0/07/T%C3%9CB%C4%B0TAK_logo.png", width=110)

st.markdown("---")

# 3. YAN PANEL (PARAMETRELER)
st.sidebar.title("📑 Menü")
sayfa = st.sidebar.selectbox("Bölüm Seçiniz:", ["🏠 Ana Kontrol Paneli", "📊 Fizyolojik Derin Analiz", "🚨 Acil Durum Rehberi"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Görev Değişkenleri")
izolasyon = st.sidebar.slider("İzolasyon (Gün)", 0, 120, 60)
gorev_yogunlugu = st.sidebar.select_slider("Görev Yoğunluğu", options=["Düşük", "Orta", "Yüksek"], value="Orta")
sosyal_etkilesim = st.sidebar.select_slider("Sosyal Etkileşim", options=["Düşük", "Orta", "Yüksek"], value="Orta")
isik_maruziyeti = st.sidebar.select_slider("Işık Maruziyeti", options=["Düşük", "Orta", "Yüksek", "Çok Yüksek"], value="Orta")

st.sidebar.subheader("⌚ Sensör Verileri")
nabiz = st.sidebar.number_input("Nabız (bpm)", 40, 150, 72)
spo2 = st.sidebar.number_input("Oksijen (SpO2 %)", 80, 100, 98)
hrv = st.sidebar.number_input("HRV Skoru", 10, 100, 55)

# --- RİSK HESAPLAMA (TABLO 1 VE 6 TEMELLİ) ---
def hesapla():
    # Psikolojik Risk (İzolasyon ve Sosyal Etkileşim)
    p_risk = (izolasyon / 120 * 40) + (30 if sosyal_etkilesim == "Düşük" else 10)
    # Fizyolojik Risk (Oksijen ve Nabız)
    f_risk = (100 - spo2) * 5 + (abs(nabiz - 72) * 0.5)
    # Işık Riski (Tablo 6)
    i_map = {"Düşük": 25, "Orta": 35, "Yüksek": 55, "Çok Yüksek": 65}
    i_risk = i_map[isik_maruziyeti]
    
    total = min(100, int((p_risk + f_risk + i_risk) / 3))
    return total, int(p_risk), int(f_risk)

risk_skoru, p_indeks, f_indeks = hesapla()

# --- SAYFA İÇERİKLERİ ---
if sayfa == "🏠 Ana Kontrol Paneli":
    # Metrikler
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Psikolojik Yük", f"%{p_indeks}")
    with c2: st.metric("Fizyolojik Yük", f"%{f_indeks}")
    with c3: st.metric("Oksijen Durumu", f"%{spo2}")
    with c4: st.metric("Genel Risk", f"%{risk_skoru}", delta="KRİTİK" if risk_skoru > 60 else "STABİL", delta_color="inverse")

    st.markdown("---")
    
    # Grafikler
    col_g, col_s = st.columns([2, 1])
    with col_g:
        st.subheader("📈 Görev Süreci Risk Projeksiyonu")
        # Gerçekçi veri eğrisi oluşturma
        gunler = np.arange(0,
