import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- ARKA PLAN VE TEMA AYARI (YENİ EKLENDİ) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #1a2a6c, #b21f1f, #fdbb2d); /* Kutup gecesi efekti */
        background-color: #0e1117; /* Koyu lacivert/siyah zemin */
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #1c2331; /* Yan panel koyu mavi */
    }
    h1, h2, h3, p {
        color: #e0e0e0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Sayfa Ayarları
st.set_page_config(page_title="Dijital İkiz Karar Destek Paneli", layout="wide")

st.title("❄️ Kutup Görevi: Psikofizyolojik Dijital İkiz")
st.markdown("---")

# 2. SOL PANEL
st.sidebar.header("📥 Girdi Değişkenleri")

izolasyon = st.sidebar.slider("İzolasyon Süresi (Gün)", 0, 180, 120)
uyku = st.sidebar.slider("Günlük Uyku Süresi (Saat)", 4.0, 9.0, 5.5)
gorev_yogunlugu = st.sidebar.selectbox("Görev Yoğunluğu", ["Düşük", "Orta", "Yüksek"], index=2)
sosyal_etkilesim = st.sidebar.selectbox("Sosyal Etkileşim", ["Günlük", "Sınırlı", "Çok Sınırlı"], index=2)
isik_duzeyi = st.sidebar.selectbox("Işık Maruziyeti", ["Normal", "Düşük/Düzensiz"], index=1)

# 3. FİZYOLOJİK KATMAN
st.sidebar.subheader("⌚ Sensör Verileri")
hrv = st.sidebar.number_input("Kalp Hızı Değişkenliği (HRV)", 20, 100, 45)
nabiz = st.sidebar.number_input("Nabız (bpm)", 50, 120, 85)

# 4. RİSK HESAPLAMA MOTORU
def risk_hesapla():
    p_stres = 0
    if izolasyon > 90: p_stres += 40
    elif izolasyon > 30: p_stres += 20
    if gorev_yogunlugu == "Yüksek": p_stres += 30
    if sosyal_etkilesim == "Çok Sınırlı": p_stres += 30
    
    f_yuklenme = 0
    if uyku < 6: f_yuklenme += 40
    if isik_duzeyi == "Düşük/Düzensiz": f_yuklenme += 30
    if hrv < 50: f_yuklenme += 30 
    
    total_risk = (p_stres + f_yuklenme) / 2
    return min(total_risk, 100), p_stres, f_yuklenme

butunlesik_skor, p_indeks, f_indeks = risk_hesapla()

# 5. ANA PANEL
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Psikolojik Stres", f"{p_indeks}%")
with c2:
    st.metric("Fizyolojik Yüklenme", f"{f_indeks}%")
with c3:
    durum = "KRİTİK" if butunlesik_skor > 70 else ("RİSKLİ" if butunlesik_skor > 40 else "STABİL")
    st.metric("Bütünleşik Risk", f"{butunlesik_skor}%", delta=durum)

st.markdown("---")

# 6. GRAFİK (Koyu Temaya Uygun)
st.subheader("📈 Risk Projeksiyonu")
zaman_adimlari = np.arange(0, izolasyon + 10, 10)
risk_egrisi = [ (x/izolasyon) * butunlesik_skor for x in zaman_adimlari]

df_graph = pd.DataFrame({"Gün": zaman_adimlari, "Risk Skoru": risk_egrisi})
fig = px.line(df_graph, x="Gün", y="Risk Skoru", template="plotly_dark") # Koyu tema grafiği
st.plotly_chart(fig, use_container_width=True)

# 7. UYARILAR
if butunlesik_skor > 70:
    st.error("🚨 KRİTİK SEVİYE: Personel tahliyesi değerlendirilmeli!")
elif butunlesik_skor > 40:
    st.warning("⚠️ UYARI: Psikolojik destek protokolü başlatılmalı.")
else:
    st.success("✅ DURUM: Operasyonel dayanıklılık ideal seviyede.")
