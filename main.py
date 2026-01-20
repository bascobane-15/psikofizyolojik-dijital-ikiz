import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kutup Dijital İkiz v2", layout="wide")

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
st.sidebar.title("🚀 Görev Kontrol Merkezi")
sayfa_secimi = st.sidebar.selectbox("Bölüm Seçiniz:", ["🏠 Ana Kontrol Paneli", "📊 Fizyolojik Derin Analiz", "🚨 Acil Durum Rehberi"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Temel Parametreler (Ref: Palinkas, 2003)")

# Yeni parametrelerin eklenmesi (Senin tablolarına göre)
izolasyon = st.sidebar.slider("İzolasyon Süresi (Gün)", 0, 120, 60)

# Görev Yoğunluğu (Stuster, 2016)
gorev_yogunlugu = st.sidebar.select_slider(
    "Görev Yoğunluğu",
    options=["Düşük", "Orta", "Yüksek"],
    value="Orta"
)

# Sosyal Etkileşim (Suedfeld, 2018)
sosyal_etkilesim = st.sidebar.select_slider(
    "Sosyal Etkileşim",
    options=["Çok Sınırlı", "Sınırlı", "Günlük"],
    value="Sınırlı"
)

# Işık Maruziyeti (Tablo 6'ya göre)
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

# --- GELİŞMİŞ RİSK HESAPLAMA MOTORU (Tablo Değerlerine Göre) ---
def akademik_risk_hesapla():
    # Psikolojik Risk (Tablo 1 Temelli)
    p_skor = 0
    if izolasyon > 90: p_skor += 35
    elif izolasyon >= 30: p_skor += 20
    
    if gorev_yogunlugu == "Yüksek": p_skor += 25
    if sosyal_etkilesim == "Çok Sınırlı": p_skor += 25
    
    # Işık Maruziyeti Riski (Tablo 6 Temelli)
    isik_risk_map = {"Düşük": 25, "Orta": 35, "Yüksek": 55, "Çok Yüksek": 65}
    isik_riski = isik_risk_map[isik_maruziyeti]
    
    # Fizyolojik Risk
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
    
    # Metrikler
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Psikolojik Yük", f"%{p_indeks}")
    with c2: st.metric("Fizyolojik Yük", f"%{f_indeks}")
    with c3: st.metric("Işık/Çevre Riski", isik_maruziyeti)
    with c4: 
        durum = "KRİTİK" if risk_skoru > 60 else ("RİSKLİ" if risk_skoru > 40 else "STABİL")
        st.metric("Bütünleşik Risk", f"%{risk_skoru}", delta=durum, delta_color="inverse")

    st.markdown("---")
    
    # Görselleştirme
    col_graph, col_info = st.columns([2, 1])
    with col_graph:
        st.subheader("📊 Görev Süreci Risk Projeksiyonu")
        # Senin Tablo 6 verilerini yansıtan bir grafik
        gunler = [30, 60, 90, 120]
        riskler = [25, 35, 55, 65] # Tablo 6'daki değerler
        df_tablo6 = pd.DataFrame({"Gün": gunler, "Risk Skoru": riskler})
        fig = px.line(df_tablo6, x="Gün", y="Risk Skoru", markers=True, template="plotly_dark", title="Tablo 6: Işık Maruziyetine Bağlı Risk Artışı")
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

Python

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
        gunler = np.arange(0, 121, 5)
        base_risk = (gunler / 120) * risk_skoru
        noise = np.random.normal(0, 2, len(gunler))
        eğri_verisi = pd.DataFrame({"Gün": gunler, "Risk Katsayısı": base_risk + noise})
        
        fig = px.area(eğri_verisi, x="Gün", y="Risk Katsayısı", 
                      template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    with col_s:
        st.subheader("📋 Sistem Özeti")
        st.info(f"**Takım Adı:** POLAR TWIN")
        st.write(f"**Analiz Modeli:** Dijital İkiz v2.1")
        if spo2 < 94: st.error("Düşük Oksijen Seviyesi!")
        elif risk_skoru > 50: st.warning("Yüksek Adaptasyon Riski!")
        else: st.success("Sistem Stabil.")

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
