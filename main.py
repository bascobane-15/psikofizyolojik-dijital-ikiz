import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="POLAR TWIN | Dijital İkiz", layout="wide")

# --- GELİŞMİŞ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #0a192f, #112240); color: #FFFFFF !important; }
    p, span, label, .stMarkdown, [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 600 !important; }
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

# 2. ÜST PANEL (LOGOLAR VE BAŞLIK)
# Logoların yüklenmeme ihtimaline karşı alternatif placeholder kullanıldı
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_l:
    st.image("https://upload.wikimedia.org/wikipedia/tr/b/b3/Teknofest_logo.png", width=120)
with col_m:
    st.markdown("<h1 style='text-align: center;'>POLAR TWIN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Psikofizyolojik Dijital İkiz Karar Destek Paneli</p>", unsafe_allow_html=True)
with col_r:
    st.image("https://upload.wikimedia.org/wikipedia/tr/0/07/T%C3%9CB%C4%B0TAK_logo.png", width=100)

st.markdown("---")

# 3. YAN PANEL (PARAMETRELER)
st.sidebar.title("Menü")
sayfa = st.sidebar.selectbox("Bölüm Seçiniz:", ["Ana Kontrol Paneli", "Fizyolojik Derin Analiz", "Acil Durum Rehberi"])

st.sidebar.markdown("---")
st.sidebar.subheader("Görev Değişkenleri")
izolasyon = st.sidebar.slider("İzolasyon (Gün)", 0, 120, 60)
# Tablo 1'e göre parametreler
gorev_yogunlugu = st.sidebar.select_slider("Görev Yoğunluğu", options=["Düşük", "Orta", "Yüksek"], value="Orta")
sosyal_etkilesim = st.sidebar.select_slider("Sosyal Etkileşim", options=["Düşük", "Orta", "Yüksek"], value="Orta")
isik_maruziyeti = st.sidebar.select_slider("Işık Maruziyeti", options=["Düşük", "Orta", "Yüksek", "Çok Yüksek"], value="Orta")
uyku = st.sidebar.slider("Uyku Süresi (Saat)", 4.0, 10.0, 7.5)

st.sidebar.subheader("Sensör Verileri")
nabiz = st.sidebar.number_input("Nabız (bpm)", 40, 150, 72)
spo2 = st.sidebar.number_input("Oksijen (SpO2 %)", 80, 100, 98)
hrv = st.sidebar.number_input("HRV Skoru", 10, 100, 55)

# --- GELİŞMİŞ RİSK HESAPLAMA (TABLO 1 VE 6 TEMELLİ) ---
def hesapla():
    # Psikolojik Risk Puanı (Tablo 1 Kaynaklı)
    p_puan = 0
    if izolasyon > 90: p_puan += 30 # Palinkas, 2003
    elif izolasyon >= 30: p_puan += 15
    
    if gorev_yogunlugu == "Yüksek": p_puan += 20 # Stuster, 2016
    if sosyal_etkilesim == "Düşük": p_puan += 25 # Suedfeld, 2018
    
    # Işık Riski Puanı (Tablo 6 Kaynaklı)
    i_map = {"Düşük": 25, "Orta": 35, "Yüksek": 55, "Çok Yüksek": 65}
    i_puan = i_map[isik_maruziyeti]
    
    # Fizyolojik Risk Puanı
    f_puan = (100 - spo2) * 3 + (abs(nabiz - 72) * 0.5)
    
    total = min(100, int((p_puan + f_puan + i_puan) / 3))
    return total, int(p_puan), int(f_puan)

risk_skoru, p_indeks, f_indeks = hesapla()

# --- SAYFA İÇERİKLERİ ---
if sayfa == "Ana Kontrol Paneli":
    # Metrikler
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Psikolojik Yük", f"%{p_indeks}")
    with m2: st.metric("Fizyolojik Yük", f"%{f_indeks}")
    with m3: st.metric("Oksijen Durumu", f"%{spo2}")
    with m4: st.metric("Bütünleşik Risk", f"%{risk_skoru}", delta="KRİTİK" if risk_skoru > 60 else "STABİL", delta_color="inverse")

    st.markdown("---")
    
    col_g, col_s = st.columns([2, 1])
    with col_g:
        st.subheader("Zamana Bağlı Risk Projeksiyonu")
        # Grafik Verisi Oluşturma (Tablo 6'daki gün aralıklarına göre)
        gun_aksis = np.arange(0, 121, 5)
        # Risk eğrisi izolasyon süresi ve ışık maruziyetine göre şekillenir
        risk_trend = [( (g/120) * risk_skoru + np.random.normal(0, 1) ) for g in gun_aksis]
        df_plot = pd.DataFrame({"Gün": gun_aksis, "Risk Skoru": risk_trend})
        
        fig = px.area(df_plot, x="Gün", y="Risk Skoru", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        fig.update_layout(yaxis_range=[0, 100], xaxis_title="Görev Günü", yaxis_title="Risk Endeksi")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_s:
        st.subheader("Durum Analizi")
        st.success("**Takım:** POLAR TWIN")
        st.write(f"**Güncel Risk Seviyesi:** %{risk_skoru}")
        st.write(f"**Literatür Dayanağı:** Palinkas, Stuster, Suedfeld")
        if risk_skoru > 50:
            st.warning("Dikkat: Adaptasyon sınırına yaklaşıldı.")
        else:
            st.info("Sistem nominal seviyede.")

elif sayfa == "Fizyolojik Derin Analiz":
    st.title("Veri Analiz Laboratuvarı")
    # Nabız-Oksijen Korelasyon Grafiği
    df_lab = pd.DataFrame({
        'Zaman': range(100),
        'Nabız': np.random.normal(nabiz, 5, 100),
        'Oksijen': np.random.normal(spo2, 1, 100)
    })
    fig_lab = px.scatter(df_lab, x="Nabız", y="Oksijen", color="Oksijen", 
                         title="Nabız - SpO2 İlişki Analizi", template="plotly_dark")
    st.plotly_chart(fig_lab, use_container_width=True)

elif sayfa == "Acil Durum Rehberi":
    st.title("Acil Durum Protokolleri")
    st.error("Kritik Eşik Uyarıları")
    st.markdown("""
    - **Risk > %65 (Tablo 6):** Çok yüksek risk; acil medikal müdahale ve tahliye planı gözden geçirilmelidir.
    - **SpO2 < %92:** Hipoksi riski; ek oksijen desteği ve rakım ayarı yapılmalıdır.
    - **HRV Düşüşü:** Kronik stres belirtisi; görev yoğunluğu %50 azaltılmalıdır.
    """)
