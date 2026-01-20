import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="POLAR TWIN | Dijital İkiz", layout="wide")

# --- GELİŞMİŞ TASARIM VE KONTRAST AYARI (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Plan ve Yazı Kontrastı */
    .stApp { 
        background: linear-gradient(to bottom, #0a192f, #112240); 
        color: #FFFFFF !important; /* Tüm yazıları net beyaz yapar */
    }
    
    /* Silik gri yazıları engelleme */
    p, span, label, .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* Yan Panel Tasarımı */
    [data-testid="stSidebar"] { 
        background-color: #020c1b !important; 
        border-right: 2px solid #00d4ff;
    }

    /* Başlıklar */
    h1, h2, h3 {
        color: #00d4ff !important;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Metrik Kutuları */
    div[data-testid="metric-container"] {
        background-color: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,212,255,0.2);
    }
    
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGOLAR VE TAKIM İSMİ ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])

with col_logo1:
    # Teknofest Logosu
    st.image("https://upload.wikimedia.org/wikipedia/tr/b/b3/Teknofest_logo.png", width=150)

with col_logo2:
    st.markdown("<h1 style='text-align: center;'>🚀 POLAR TWIN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>Psikofizyolojik Dijital İkiz Karar Destek Paneli</p>", unsafe_allow_html=True)

with col_logo3:
    # Tübitak Logosu
    st.image("https://upload.wikimedia.org/wikipedia/tr/0/07/T%C3%9CB%C4%B0TAK_logo.png", width=120)

st.markdown("---")

# 2. SOL PANEL (MENÜ VE PARAMETRELER)
st.sidebar.title("🚀 Görev Kontrol")
sayfa_secimi = st.sidebar.selectbox("Bölüm Seçiniz:", ["🏠 Ana Kontrol Paneli", "📊 Fizyolojik Derin Analiz", "🚨 Acil Durum Rehberi"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Görev Değişkenleri")

izolasyon = st.sidebar.slider("İzolasyon Süresi (Gün)", 0, 120, 60)

# 1- Parametrelerin Eklenmesi (İstediğin gibi genişletildi)
gorev_yogunlugu = st.sidebar.select_slider(
    "Görev Yoğunluğu",
    options=["Düşük", "Orta", "Yüksek"],
    value="Orta"
)

sosyal_etkilesim = st.sidebar.select_slider(
    "Sosyal Etkileşim",
    options=["Düşük", "Orta", "Yüksek"],
    value="Orta"
)

isik_maruziyeti = st.sidebar.select_slider(
    "Işık Maruziyeti",
    options=["Düşük", "Orta", "Yüksek", "Çok Yüksek"],
    value="Orta"
)

uyku = st.sidebar.slider("Günlük Uyku Süresi (Saat)", 4.0, 10.0, 7.5)

st.sidebar.markdown("---")
st.sidebar.subheader("⌚ Sensör Verileri")
nabiz = st.sidebar.number_input("Nabız (bpm)", 40, 150, 72)
spo2 = st.sidebar.number_input("Oksijen (SpO2 %)", 80, 100, 98)
hrv = st.sidebar.number_input("HRV Skoru", 10, 100, 55)

# 3. AKADEMİK RİSK HESAPLAMA (Tablo 1 ve 6 Temelli)
def risk_hesapla():
    # Psikolojik Etki
    p_skor = 0
    if izolasyon > 90: p_skor += 35
    if gorev_yogunlugu == "Yüksek": p_skor += 30
    if sosyal_etkilesim == "Düşük": p_skor += 35
    
    # Fizyolojik Etki
    f_skor = 0
    if uyku < 6: f_skor += 40
    if spo2 < 94: f_skor += 30
    if hrv < 45: f_skor += 30
    
    # Işık Etkisi
    isik_map = {"Düşük": 10, "Orta": 35, "Yüksek": 55, "Çok Yüksek": 75}
    i_skor = isik_map[isik_maruziyeti]
    
    total = (p_skor + f_skor + i_skor) / 3
    return min(100, int(total)), p_skor, f_skor

risk_skoru, p_indeks, f_indeks = risk_hesapla()

# ==========================================
# SAYFA 1: ANA KONTROL PANELİ
# ==========================================
if sayfa_secimi == "🏠 Ana Kontrol Paneli":
    
    # Metrikler (Net beyaz yazılar için düzenlendi)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Psikolojik Yük", f"%{p_indeks}")
    with m2: st.metric("Fizyolojik Yük", f"%{f_indeks}")
    with m3: st.metric("Oksijen Durumu", f"%{spo2}")
    with m4:
        durum_text = "KRİTİK" if risk_skoru > 65 else ("RİSKLİ" if risk_skoru > 40 else "STABİL")
        st.metric("Bütünleşik Risk", f"%{risk_skoru}", delta=durum_text, delta_color="inverse")

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.subheader("📈 Görev Süreci Risk Projeksiyonu")
        # Grafik renkleri POLAR TWIN temasına uygun
        zaman = np.arange(0, 121, 10)
        degerler = [min(100, (x/120)*risk_skoru + np.random.randint(-5, 5)) for x in zaman]
        df_plot = pd.DataFrame({"Gün": zaman, "Risk": degerler})
        fig = px.area(df_plot, x="Gün", y="Risk", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("📋 Durum Özet")
        st.success(f"**Takım:** POLAR TWIN")
        st.write(f"**İzolasyon Günü:** {izolasyon}")
        st.write(f"**Işık Maruziyeti:** {isik_maruziyeti}")
        st.write(f"**Sosyal Etkileşim:** {sosyal_etkilesim}")
        
        if risk_skoru > 60:
            st.error("🚨 KRİTİK: Literatür uyarınca acil müdahale önerilir.")
        else:
            st.info("✅ Operasyonel dayanıklılık normal seviyede.")

# DİĞER SAYFALAR...
elif sayfa_secimi == "📊 Fizyolojik Derin Analiz":
    st.title("📊 Derin Analiz Sayfası")
    st.write("Veriler işleniyor...")

else:
    st.title("🚨 Acil Durum Protokolleri")
    st.write("Müdahale adımları burada listelenecek.")
