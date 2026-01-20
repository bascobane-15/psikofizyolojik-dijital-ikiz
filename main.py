import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA AYARLARI (En üstte kalmalı)
st.set_page_config(page_title="Kutup Dijital İkiz", layout="wide")

# --- GELİŞMİŞ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #0a192f, #112240); color: white; }
    [data-testid="stSidebar"] { background-color: #020c1b !important; }
    div[data-testid="metric-container"] {
        background-color: rgba(0, 212, 255, 0.05);
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
izolasyon = st.sidebar.slider("İzolasyon (Gün)", 0, 180, 60)
uyku = st.sidebar.slider("Uyku (Saat)", 4.0, 10.0, 7.5)
nabiz = st.sidebar.number_input("Nabız (bpm)", 40, 150, 72)
spo2 = st.sidebar.number_input("Oksijen (SpO2 %)", 80, 100, 98)
hrv = st.sidebar.number_input("HRV Skoru", 10, 100, 55)

# --- RİSK HESAPLAMA MOTORU (Her sayfada kullanılabilir) ---
risk_skoru = min(100, int((100 - spo2) * 3 + (90 - hrv) * 0.5 + (izolasyon / 5)))

# ==========================================
# SAYFA 1: ANA KONTROL PANELİ (SENİN EKRANIN)
# ==========================================
if sayfa_secimi == "🏠 Ana Kontrol Paneli":
    st.title("❄️ Kutup Görevi: Psikofizyolojik Dijital İkiz")
    st.markdown("---")
    
    # Metrikler
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Kalp Hızı", f"{nabiz} bpm")
    with c2: st.metric("Oksijen", f"%{spo2}")
    with c3: st.metric("HRV Durumu", hrv)
    with c4: 
        durum = "KRİTİK" if risk_skoru > 60 else "STABİL"
        st.metric("Genel Risk", f"%{risk_skoru}", delta=durum, delta_color="inverse")

    st.markdown("---")
    
    # Grafik ve Notlar
    col_sol, col_sag = st.columns([2, 1])
    with col_sol:
        st.subheader("📈 Risk Projeksiyonu")
        df_risk = pd.DataFrame({"Zaman": np.arange(10), "Risk": np.random.normal(risk_skoru, 2, 10)})
        fig = px.area(df_risk, x="Zaman", y="Risk", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col_sag:
        st.subheader("📝 Görev Notları")
        st.info(f"Gün {izolasyon}: Personel adaptasyonu devam ediyor.")
        if risk_skoru > 50:
            st.warning("Dikkat: Yüksek izolasyon yükü tespit edildi.")
        else:
            st.success("Sistem nominal seviyede.")

# ==========================================
# SAYFA 2: DERİN ANALİZ
# ==========================================
elif sayfa_secimi == "📊 Fizyolojik Derin Analiz":
    st.title("📊 Detaylı Sağlık Analizi")
    st.write("Sensör verilerinin detaylı korelasyon grafikleri.")
    
    # Örnek bir dağılım grafiği
    df_ana = pd.DataFrame({
        'Zaman': range(24),
        'Nabız': np.random.normal(nabiz, 5, 24),
        'Stres': np.random.uniform(20, 80, 24)
    })
    fig_corr = px.scatter(df_ana, x="Nabız", y="Stres", size="Stres", color="Stres", template="plotly_dark")
    st.plotly_chart(fig_corr, use_container_width=True)

# ==========================================
# SAYFA 3: ACİL DURUM REHBERİ
# ==========================================
else:
    st.title("🚨 Acil Durum Protokolleri")
    st.error("Kritik eşik aşıldığında uygulanacak adımlar:")
    st.markdown("""
    1. **Oksijen %90 altı:** Derhal istasyon içi destek ünitesine bağlanın.
    2. **Nabız 120+ (Dinlenme):** Medikal sorumluya haber verin.
    3. **Psikolojik Kırılma:** 'Dark Sky' protokolünü başlatın ve dış dünya ile görüntülü temas kurun.
    """)
    st.image("https://images.unsplash.com/photo-1517030330234-94c4fa948ebc?auto=format&fit=crop&q=80&w=1000", caption="Antarktika İstasyon Güvenliği")
