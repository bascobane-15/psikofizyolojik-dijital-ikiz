import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Sayfa Ayarları ve Başlık
st.set_page_config(page_title="Dijital İkiz Karar Destek Paneli", layout="wide")

st.title("🔬 Dijital İkiz: Psikofizyolojik Risk Prototipi")
st.markdown("---")

# 2. SOL PANEL: GİRDİ DEĞİŞKENLERİ
st.sidebar.header("📥 Girdi Değişkenleri")

izolasyon = st.sidebar.slider("İzolasyon Süresi (Gün)", 0, 180, 120)
uyku = st.sidebar.slider("Günlük Uyku Süresi (Saat)", 4.0, 9.0, 5.5)
gorev_yogunlugu = st.sidebar.selectbox("Görev Yoğunluğu", ["Düşük", "Orta", "Yüksek"], index=2)
sosyal_etkilesim = st.sidebar.selectbox("Sosyal Etkileşim", ["Günlük", "Sınırlı", "Çok Sınırlı"], index=2)
isik_duzeyi = st.sidebar.selectbox("Işık Maruziyeti (Fotoperiyod)", ["Normal", "Düşük/Düzensiz"], index=1)

# 3. FİZYOLOJİK KATMAN (Sensör Verisi Simülasyonu)
st.sidebar.subheader("⌚ Giyilebilir Sensör Verileri")
hrv = st.sidebar.number_input("Kalp Hızı Değişkenliği (HRV)", 20, 100, 45)
nabiz = st.sidebar.number_input("Nabız (bpm)", 50, 120, 85)

# 4. RİSK HESAPLAMA MOTORU (Algoritma Kısmı)
def risk_hesapla():
    # Psikolojik Stres İndeksi
    p_stres = 0
    if izolasyon > 90: p_stres += 40
    elif izolasyon > 30: p_stres += 20
    
    if gorev_yogunlugu == "Yüksek": p_stres += 30
    if sosyal_etkilesim == "Çok Sınırlı": p_stres += 30
    
    # Fizyolojik Yüklenme İndeksi
    f_yuklenme = 0
    if uyku < 6: f_yuklenme += 40
    if isik_duzeyi == "Düşük/Düzensiz": f_yuklenme += 30
    if hrv < 50: f_yuklenme += 30 
    
    # Bütünleşik Risk Skoru
    total_risk = (p_stres + f_yuklenme) / 2
    return min(total_risk, 100), p_stres, f_yuklenme

butunlesik_skor, p_indeks, f_indeks = risk_hesapla()

# 5. ANA PANEL: GÖRSELLEŞTİRME VE METRİKLER
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Psikolojik Stres İndeksi", f"{p_indeks}%")
with c2:
    st.metric("Fizyolojik Yüklenme İndeksi", f"{f_indeks}%")
with c3:
    durum = "Yüksek" if butunlesik_skor > 70 else ("Orta" if butunlesik_skor > 40 else "Düşük")
    st.metric("Bütünleşik Risk Skoru", f"{butunlesik_skor}%", delta=durum, delta_color="inverse")

st.markdown("---")

# 6. ZAMANA BAĞLI RİSK GRAFİĞİ
st.subheader("📈 Zamana Bağlı Risk Projeksiyonu")
zaman_adimlari = np.arange(0, izolasyon + 10, 10)
risk_egrisi = [ (x/iz
