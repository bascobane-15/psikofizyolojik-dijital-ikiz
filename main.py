import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Sayfa Ayarlarını En Başta Yapmalıyız (Beyaz şeridi engellemek için)
st.set_page_config(page_title="Dijital İkiz Paneli", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ KARANLIK TEMA VE TASARIM ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(to bottom, #0a0f1e, #16213e, #0f3460);
        color: white;
    }
    /* Üstteki beyaz şeridi ve boşlukları kapat */
    header {visibility: hidden;}
    .main .block-container {padding-top: 2rem;}
    
    /* Yan Panel (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0a0c10 !important;
        border-right: 1px solid #1e272e;
    }
    
    /* Metrik Kutuları Tasarımı */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("❄️ Kutup Görevi: Psikofizyolojik Dijital İkiz")
st.markdown("---")

# 2. SOL PANEL (GİRDİLER)
st.sidebar.header("📥 Görev Parametreleri")

izolasyon = st.sidebar.slider("İzolasyon Süresi (Gün)", 0, 180, 60)
uyku = st.sidebar.slider("Günlük Uyku Süresi (Saat)", 4.0, 9.0, 7.0)
gorev_yogunlugu = st.sidebar.selectbox("Görev Yoğunluğu", ["Düşük", "Orta", "Yüksek"], index=1)
sosyal_etkilesim = st.sidebar.selectbox("Sosyal Etkileşim", ["Günlük", "Sınırlı", "Çok Sınırlı"], index=0)
isik_duzeyi = st.sidebar.selectbox("Işık Maruziyeti", ["Normal", "Düşük/Düzensiz"], index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("⌚ Sensör Verileri")
hrv = st.sidebar.number_input("HRV (Kalp Değişkenliği)", 20, 100, 55)
nabiz = st.sidebar.number_input("Nabız (bpm)", 50, 120, 72)
spo2 = st.sidebar.number_input("Oksijen (SpO2 %)", 80, 100, 98)

# 3. HESAPLAMA MOTORU
def risk_hesapla():
    p_stres = 0
    if izolasyon > 90: p_stres += 40
    elif izolasyon > 30: p_stres += 20
    if gorev_yogunlugu == "Yüksek": p_stres += 30
    if sosyal_etkilesim == "Çok Sınırlı": p_stres += 30
    
    f_yuklenme = 0
    if uyku < 6: f_yuklenme += 30
    if isik_duzeyi == "Düşük/Düzensiz": f_yuklenme += 20
    if hrv < 50: f_yuklenme += 20 
    if spo2 < 94: f_yuklenme += 30 
    
    total_risk = (p_stres + f_yuklenme) / 2
    return min(total_risk, 100), p_stres, f_yuklenme

risk_skoru, p_indeks, f_indeks = risk_hesapla()

# 4. ANA PANEL: 4 SÜTUNLU METRİKLER (Sağ tarafın dolması için)
# Sütunları net bir şekilde tanımlıyoruz
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Psikolojik Stres", f"{p_indeks}%")
with col2:
    st.metric("Fizyolojik Yük", f"{f_indeks}%")
with col3:
    st.metric("Oksijen (SpO2)", f"%{spo2}")
with col4:
    durum = "KRİTİK" if risk_skoru > 70 else ("RİSKLİ" if risk_skoru > 40 else "STABİL")
    st.metric("Genel Risk", f"{risk_skoru}%", delta=durum, delta_color="inverse")

st.markdown("---")

# 5. GRAFİK VE UYARILAR
c_left, c_right = st.columns([2, 1]) # Sol geniş (grafik), sağ dar (uyarılar)

with c_left:
    st.subheader("📈 Risk Projeksiyonu")
    zaman = np.arange(0, 101, 10)
    degerler = [(x/100) * risk_skoru for x in zaman]
    df = pd.DataFrame({"İlerleme (%)": zaman, "Risk": degerler})
    fig = px.area(df, x="İlerleme (%)", y="Risk", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.subheader("🚨 Sistem Notları")
    if spo2 < 94:
        st.error(f"Düşük Oksijen: %{spo2}! Hemen dinlenmeye geçilmeli.")
    if risk_skoru > 50:
        st.warning("Yüksek Risk: Psikolojik destek protokolü öneriliyor.")
    else:
        st.info("Sistem Durumu: Tüm parametreler görev için uygun.")
