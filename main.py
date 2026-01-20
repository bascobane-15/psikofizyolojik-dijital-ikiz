import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kutup Dijital İkiz v2", layout="wide")

# --- SADECE SOL YAZILARI KOYU YAPAN CSS ---
st.markdown("""
    <style>
    /* Ana Arka Plan Degradesi */
    .stApp { background: linear-gradient(to bottom, #0a192f, #112240); color: white; }
    
    /* SOL PANEL (SIDEBAR) ÖZEL AYARLARI */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6 !important; /* Sol tarafı hafif gri/açık yapıyoruz ki siyah yazı görünsün */
    }

    /* SOLDAKİ TÜM YAZILARI ZORLA SİYAH YAPAR */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #000000 !important; /* SİYAH YAZI */
        font-weight: 700 !important; /* KALIN YAZI */
    }

    /* Sağ taraftaki metrik kutuları ve ana başlıklar beyaz kalsın */
    div[data-testid="metric-container"] {
        background-color: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        padding: 15px;
        border-radius: 12px;
    }
    
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. SOL PANEL (MENÜ VE GİRDİLER)
st.sidebar.title("🚀 Görev Kontrol")
sayfa_secimi = st.sidebar.selectbox("Bölüm Seçiniz:", ["🏠 Ana Kontrol Paneli", "📊 Fizyolojik Derin Analiz", "🚨 Acil Durum Rehberi"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Canlı Parametreler")

# Parametrelerin (Aynen Korundu)
izolasyon = st.sidebar.slider("İzolasyon Süresi (Gün)", 0, 120, 60)

gorev_yogunlugu = st.sidebar.select_slider(
    "Görev Yoğunluğu",
    options=["Düşük", "Orta", "Yüksek"],
    value="Orta"
)

sosyal_etkilesim = st.sidebar.select_slider(
    "Sosyal Etkileşim",
    options=["Çok Sınırlı", "Sınırlı", "Günlük"],
    value="Sınırlı"
)

isik_maruziyeti = st.sidebar.select_slider(
    "Işık Maruziyeti / Risk Seviyesi",
    options=["Düşük", "Orta", "Yüksek", "Çok Yüksek"],
    value="Orta"
)

uyku = st.sidebar.slider("Uyku Süresi (Saat)", 4.0, 9.0, 7.0)

st.sidebar.markdown("---")
st.sidebar.subheader("⌚ Sensör Verileri")
nabiz = st.sidebar.number_input("Nabız (bpm)", 40, 150, 72)
spo2 = st.sidebar.number_input("Oksijen (SpO2 %)", 80, 100, 98)
hrv = st.sidebar.number_input("HRV Skoru", 10, 100, 55)

# --- RİSK HESAPLAMA MOTORU (Aynen Korundu) ---
def akademik_risk_hesapla():
    p_skor = 0
    if izolasyon > 90: p_skor += 35
    elif izolasyon >= 30: p_skor += 20
    if gorev_yogunlugu == "Yüksek": p_skor += 25
    if sosyal_etkilesim == "Çok Sınırlı": p_skor += 25
    isik_risk_map = {"Düşük": 25, "Orta": 35, "Yüksek": 55, "Çok Yüksek": 65}
    isik_riski = isik_risk_map[isik_maruziyeti]
    f_skor = 0
    if uyku < 6: f_skor += 30
    if spo2 < 94: f_skor += 30
    if hrv < 45: f_skor += 20
    toplam_risk = (p_skor + f_skor + isik_riski) / 3
    return min(100, int(toplam_risk)), p_skor, f_skor

risk_skoru, p_indeks, f_indeks = akademik_risk_hesapla()

# ==========================================
# SAYFA İÇERİKLERİ
# ==========================================
if sayfa_secimi == "🏠 Ana Kontrol Paneli":
    st.title("❄️ POLAR TWIN")
    st.caption("Psikofizyolojik Dijital İkiz Karar Destek Paneli")
    st.markdown("---")
    
    # Metrikler (Sağ Taraf - Beyaz Yazı)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Psikolojik Yük", f"%{p_indeks}")
    with c2: st.metric("Fizyolojik Yük", f"%{f_indeks}")
    with c3: st.metric("Oksijen Durumu", f"%{spo2}")
    with c4: 
        durum = "KRİTİK" if risk_skoru > 60 else ("RİSKLİ" if risk_skoru > 40 else "STABİL")
        st.metric("Bütünleşik Risk", f"%{risk_skoru}", delta=durum, delta_color="inverse")

    st.markdown("---")
    
    col_graph, col_info = st.columns([2, 1])
    with col_graph:
        st.subheader("📊 Görev Süreci Risk Projeksiyonu")
        gunler = [30, 60, 90, 120]
        riskler = [25, 35, 55, 65] 
        df_tablo6 = pd.DataFrame({"Gün": gunler, "Risk Skoru": riskler})
        fig = px.area(df_tablo6, x="Gün", y="Risk Skoru", markers=True, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_info:
        st.subheader("📋 Durum Özeti")
        st.info("Takım: POLAR TWIN")
        if risk_skoru > 50:
            st.error("Müdahale Gerekli")
        else:
            st.success("Sistem Stabil")

elif sayfa_secimi == "📊 Fizyolojik Derin Analiz":
    st.title("📊 Detaylı Analiz")
    st.write("Bu bölümdeki veriler sensörlerinizle senkronize çalışmaktadır.")

else:
    st.title("🚨 Acil Durum Rehberi")
    st.write("Tablo 6 ve Tablo 1 uyarınca belirlenen müdahale adımları...")
