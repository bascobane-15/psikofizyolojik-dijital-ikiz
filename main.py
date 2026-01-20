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
    
    f_yuklenme = 0
    if uyku < 6: f_yuklenme += 30
    if is_isik := (isik_duzeyi == "Düşük/Düzensiz"): f_yuklenme += 20
    if hrv < 50: f_yuklenme += 20 
    if spo2 < 94: f_yuklenme += 30 
    
    total_risk = (p_stres + f_yuklenme) / 2
    return min(total_risk, 100), p_stres, f_yuklenme

butunlesik_skor, p_indeks, f_indeks = risk_hesapla()

# 5. ANA PANEL
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Psikolojik Stres", f"{p_indeks}%")
with c2:
    st.metric("Fizyolojik Yüklenme", f"{f_indeks}%")
with c3:
    # Oksijen için özel renkli gösterge
    st.metric("Oksijen (SpO2)", f"%{spo2}", delta="Normal" if spo2 >= 94 else "Düşük", delta_color="normal" if spo2 >= 94 else "inverse")
with c4:
    durum = "KRİTİK" if butunlesik_skor > 70 else ("RİSKLİ" if butunlesik_skor > 40 else "STABİL")
    st.metric("Bütünleşik Risk", f"{butunlesik_skor}%", delta=durum, delta_color="inverse")

st.markdown("---")

# 6. GRAFİK
st.subheader("📈 Görev Süreci Risk Tahmini")
zaman_adimlari = np.arange(0, izolasyon + 10, 10)
risk_egrisi = [ (x/izolasyon) * butunlesik_skor for x in zaman_adimlari]

df_graph = pd.DataFrame({"Gün": zaman_adimlari, "Risk Skoru": risk_egrisi})
fig = px.line(df_graph, x="Gün", y="Risk Skoru", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
st.plotly_chart(fig, use_container_width=True)

# 7. UYARILAR
if spo2 < 90:
    st.error("🚨 KRİTİK: Düşük Oksijen Seviyesi! Acil müdahale protokolü (Antarktika Medevac) hazırlığı başlatılmalı.")
elif butunlesik_skor > 70:
    st.error("🔴 KRİTİK: Personel sağlığı tehlikede! İzolasyon etkisi maksimum seviyede.")
elif butunlesik_skor > 40:
    st.warning("🟡 UYARI: Fizyolojik yorgunluk saptandı. Dinlenme süresi artırılmalı.")
else:
    st.success("🟢 DURUM: Sistem ve personel parametreleri nominal.")
