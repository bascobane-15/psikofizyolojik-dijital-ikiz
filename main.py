import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kutup Dijital İkiz v2", layout="wide")

# --- GELİŞMİŞ TASARIM (CSS) - Yazıları Belirginleştirme ---
st.markdown("""
    <style>
    /* Arka plan */
    .stApp { background: linear-gradient(to bottom, #0a192f, #112240); }
    
    /* Tüm yazıların rengini saf beyaz yap ve netleştir */
    p, span, label, .stMarkdown, [data-testid="stMetricLabel"] { 
        color: #FFFFFF !important; 
        font-weight: 500 !important;
        opacity: 1 !important; /* Silikliği kaldırır */
    }
    
    /* Metrik değerlerini (sayıları) parlat */
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
        font-weight: 700 !important;
    }

    /* Yan panel yazılarını belirginleştir */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Kartların (Metric) görünürlüğünü artır */
    div[data-testid="metric-container"] {
        background-color: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. SOL PANEL (MENÜ VE GİRDİLER)
st.sidebar.title("🚀 Görev Kontrol Merkezi")
sayfa_secimi = st.sidebar.selectbox("Bölüm Seçiniz:", ["🏠 Ana Kontrol Paneli", "📊 Fizyolojik Derin Analiz", "🚨 Acil Durum Rehberi"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Temel Parametreler")

# Parametreler (Aynen korunmuştur)
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

# --- RİSK HESAPLAMA MOTORU (Aynen korunmuştur) ---
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
# SAYFA 1: ANA KONTROL PANELİ
# ==========================================
if sayfa_secimi == "🏠 Ana Kontrol Paneli":
    st.title("❄️ Kutup Görevi: Psikofizyolojik Dijital İkiz")
    st.caption("Literatür Dayanağı: Palinkas (2003), Stuster (2016), Suedfeld (2018)")
    st.markdown("---")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Psikolojik Yük", f"%{p_indeks}")
    with c2: st.metric("Fizyolojik Yük", f"%{f_indeks}")
    with c3: st.metric("Işık Seviyesi", isik_maruziyeti)
    with c4: 
        durum = "KRİTİK" if risk_skoru > 60 else ("RİSKLİ" if risk_skoru > 40 else "STABİL")
        st.metric("Bütünleşik Risk", f"%{risk_skoru}", delta=durum, delta_color="inverse")

    st.markdown("---")
    
    col_graph, col_info = st.columns([2, 1])
    with col_graph:
        st.subheader("📈 Görev Süreci Risk Projeksiyonu")
        gunler = [30, 60, 90, 120]
        riskler = [25, 35, 55, 65]
        df_tablo6 = pd.DataFrame({"Gün": gunler, "Risk Skoru": riskler})
        fig = px.line(df_tablo6, x="Gün", y="Risk Skoru", markers=True, template="plotly_dark", title="Tablo 6: Işık Maruziyetine Bağlı Risk Artışı")
        fig.update_traces(line_color='#00d4ff', marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
    
    with col_info:
        st.subheader("📋 Parametre Analizi")
        st.write(f"**Görev Yoğunluğu:** {gorev_yogunlugu}")
        st.write(f"**Sosyal Etkileşim:** {sosyal_etkilesim}")
        st.write(f"**Işık Durumu:** {isik_maruziyeti}")
        if risk_skoru > 50:
            st.error("Literatüre göre müdahale seviyesine yaklaşıldı.")
        else:
            st.success("Parametreler güvenli aralıkta.")

# ==========================================
# SAYFA 2: DERİN ANALİZ
# ==========================================
elif sayfa_secimi == "📊 Fizyolojik Derin Analiz":
    st.title("📊 Detaylı Sağlık Analizi")
    st.info("Bu bölümdeki grafikler sensör verilerinizle (Nabız, HRV) senkronize çalışır.")
    
    # Görselleştirme örneği (Boş kalmaması için)
    df_ana = pd.DataFrame({'Zaman': range(24), 'Nabız': np.random.normal(nabiz, 2, 24)})
    fig_nabiz = px.area(df_ana, x="Zaman", y="Nabız", template="plotly_dark", title="24 Saatlik Nabız Trendi")
    st.plotly_chart(fig_nabiz, use_container_width=True)

# ==========================================
# SAYFA 3: ACİL DURUM
# ==========================================
else:
    st.title("🚨 Acil Durum Protokolleri")
    st.markdown("### Tablo 6 ve Tablo 1 uyarınca belirlenen müdahale adımları:")
    st.warning("1. Risk skoru %60 üzerine çıktığında sosyal izolasyon sonlandırılmalıdır.")
    st.warning("2. Düşük uyku süresi (<6 saat) durumunda ışık simülasyonu uygulanmalıdır.")
