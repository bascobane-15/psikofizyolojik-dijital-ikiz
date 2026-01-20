import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- ARKA PLAN VE TEMA AYARI ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364); /* Derin kutup mavisi */
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #101820;
    }
    /* Metrik kutularını daha belirgin yapalım */
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
    }
    h1, h2, h3, p {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Sayfa Ayarları
st.set_page_config(page_title="Dijital İkiz Karar Destek Paneli", layout="wide")

st.title("❄️ Kutup Görevi: Psikofizyolojik Dijital İkiz")
st.markdown("---")

# 2. SOL PANEL
st.sidebar.header("📥 Görev Değişkenleri")

izolasyon = st.sidebar.slider("İzolasyon Süresi (Gün)", 0, 180, 120)
uyku = st.sidebar.slider("Günlük Uyku Süresi (Saat)", 4.0, 9.0, 5.5)
gorev_yogunlugu = st.sidebar.selectbox("Görev Yoğunluğu", ["Düşük", "Orta", "Yüksek"], index=2)
sosyal_etkilesim = st.sidebar.selectbox("Sosyal Etkileşim", ["Günlük", "Sınırlı", "Çok Sınırlı"], index=2)
isik_duzeyi = st.sidebar.selectbox("Işık Maruziyeti", ["Normal", "Düşük/Düzensiz"], index=1)

# 3. FİZYOLOJİK KATMAN (Artık Hepsi Göstergeli)
st.sidebar.subheader("⌚ Sensör Verileri")
hrv = st.sidebar.number_input("Kalp Hızı Değişkenliği (HRV)", 20, 100, 45)
nabiz = st.sidebar.number_input("Nabız (bpm)", 50, 120, 85)
# Oksijen saturasyonu artık + ve - ile kontrol ediliyor
spo2 = st.sidebar.number_input("Oksijen Saturasyonu (SpO2 %)", 80, 100, 98)

# 4. RİSK HESAPLAMA MOTORU
def risk_hesapla():
    p_stres = 0
    if izolasyon > 90: p_stres += 40
    elif izolasyon > 30: p_stres += 20
    if gorev_yogunlugu == "Yüksek": p_stres += 30
    if sosyal_etkilesim == "Çok Sınırlı": p_stres += 30
    
    f
