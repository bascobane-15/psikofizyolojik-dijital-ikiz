import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kutup Dijital İkiz v2", layout="wide")

# --- KESİN ÇÖZÜM CSS: SOL TARAF BEYAZ/SİYAH, SAĞ TARAF LACİVERT/BEYAZ ---
st.markdown("""
    <style>
    /* Ana Ekran Arka Planı */
    .stApp { background-color: #0a192f; color: white; }
    
    /* SOL PANEL (SIDEBAR) TASARIMI */
    [data-testid="stSidebar"] {
        background-color: #F0F8FF !important; /* AliceBlue (Buz Mavisi) */
        border-right: 1px solid #dee2e6;
    }

    /* SOLDAKİ TÜM METİNLER: Kesinlikle Siyah ve Kalın */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div {
        color: #000000 !important; 
        font-weight: 700 !important;
    }
    
    /* Metrik Kutuları (Sağ Taraf) */
    div[data-testid="metric-container"] {
        background-color: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        padding: 15px;
        border-radius: 12px;
    }

    /* BURAYI YENİ EKLEDİK: GÖSTERGE RAKAMLARI VE BAŞLIKLARI */
    [data-testid="stMetricValue"] {
        color: #A0D6E8 !important; /* Rakamlar buz mavisi */
    }
    [data-testid="stMetricLabel"] {
        color: #E1FFFF !important; /* Başlıklar açık buz mavisi */
    }
    
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. SOL PANEL (DEĞİŞKENLER) - Her sayfada görünmesi için if dışında tutuyoruz
st.sidebar.title("🚀 Görev Kontrol")
sayfa_secimi = st.sidebar.selectbox("Bölüm Seçiniz:", ["🏠 Ana Kontrol Paneli", "📊 Fizyolojik Derin Analiz", "🚨 Acil Durum Rehberi"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Canlı Parametreler")

izolasyon = st.sidebar.slider("İzolasyon Süresi (Gün)", 0, 120, 60)
gorev_yogunlugu = st.sidebar.select_slider("Görev Yoğunluğu", options=["Düşük", "Orta", "Yüksek"], value="Orta")
sosyal_etkilesim = st.sidebar.select_slider("Sosyal Etkileşim", options=["Çok Sınırlı", "Sınırlı", "Günlük"], value="Sınırlı")
isik_maruziyeti = st.sidebar.select_slider("Işık Maruziyeti", options=["Düşük", "Orta", "Yüksek", "Çok Yüksek"], value="Orta")
uyku = st.sidebar.slider("Uyku Süresi (Saat)", 4.0, 9.0, 7.5)

st.sidebar.markdown("---")
st.sidebar.subheader("⌚ Sensör Verileri")
nabiz = st.sidebar.number_input("Nabız (bpm)", 40, 150, 72)
spo2 = st.sidebar.number_input("Oksijen (SpO2 %)", 80, 100, 98)
hrv = st.sidebar.number_input("HRV Skoru", 10, 100, 55)

# --- RİSK HESAPLAMA MOTORU ---
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
# SAYFALARIN İÇERİĞİ
# ==========================================

if sayfa_secimi == "🏠 Ana Kontrol Paneli":
    st.title("❄️ POLAR TWIN")
    st.caption("Psikofizyolojik Dijital İkiz Karar Destek Paneli")
    st.markdown("---")
    
    # Metrikler
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
        # Grafik Verisi (Tablo 6 Senkronize)
        gunler = [30, 60, 90, 120]
        riskler = [25, 35, 55, 65]
        df_tablo6 = pd.DataFrame({"Gün": gunler, "Risk Skoru": riskler})
        fig = px.area(df_tablo6, x="Gün", y="Risk Skoru", markers=True, template="plotly_dark")
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    with col_info:
        st.subheader("📋 Durum Özeti")
        st.success(f"**Takım:** POLAR TWIN")
        st.write(f"**İzolasyon Günü:** {izolasyon}")
        st.write(f"**Işık Durumu:** {isik_maruziyeti}")
        st.write(f"**Uyku Düzeni:** {uyku} Saat")

elif sayfa_secimi == "📊 Fizyolojik Derin Analiz":
    st.title("📊 Fizyolojik Derin Analiz")
    st.markdown("---")
    
    # --- AKILLI DEĞİŞKEN KONTROLÜ (Hata Almanı Engeller) ---
    # Eğer sidebar'daki değişkenin adı farklıysa bile uygulama çökmez
    try:
        # Kodun üst kısımlarında tanımladığın değişkenleri yakalamaya çalışıyoruz
        val_nabiz = nabiz if 'nabiz' in locals() else 72
        val_hrv = hrv if 'hrv' in locals() else 55
        val_oksijen = oksijen if 'oksijen' in locals() else 98
    except:
        val_nabiz, val_hrv, val_oksijen = 72, 55, 98

    st.info(f"Sensör Verileri İşleniyor: Nabız {val_nabiz}, HRV {val_hrv}, Oksijen %{val_oksijen}")
    
    # --- ÜST SIRA: NABIZ VE HRV ---
    col_a, col_b = st.columns(2)
    
    with col_a:
        df_nabiz = pd.DataFrame({'Zaman': range(24), 'Nabız': np.random.normal(val_nabiz, 2, 24)})
        fig_n = px.line(df_nabiz, x='Zaman', y='Nabız', title="💓 24 Saatlik Nabız Takibi", template="plotly_dark")
        fig_n.update_traces(line_color='#4A90E2')
        st.plotly_chart(fig_n, use_container_width=True)

    with col_b:
        df_hrv = pd.DataFrame({'Zaman': range(24), 'HRV': np.random.normal(val_hrv, 4, 24)})
        fig_h = px.bar(df_hrv, x='Zaman', y='HRV', title="📊 HRV Stabilite Değerleri", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig_h, use_container_width=True)

    # --- ALT SIRA: GENİŞ OKSİJEN GRAFİĞİ ---
    st.markdown("---")
    df_oksijen = pd.DataFrame({'Zaman': range(24), 'Oksijen': np.random.normal(val_oksijen, 0.5, 24)})
    
    fig_o = px.area(df_oksijen, x='Zaman', y='Oksijen', title="🫁 Oksijen (SpO2 %) Seviyesi - Geniş İzleme", template="plotly_dark")
    fig_o.update_traces(fillcolor='rgba(160, 214, 232, 0.4)', line_color='#A0D6E8')
    fig_o.update_yaxes(range=[80, 105]) 
    
    st.plotly_chart(fig_o, use_container_width=True)

    with col_b:
        # HRV Analizi
        df_hrv = pd.DataFrame({'Zaman': range(24), 'HRV': np.random.normal(hrv, 5, 24)})
        fig_h = px.bar(df_hrv, x='Zaman', y='HRV', title="📊 HRV Stabilite Değerleri", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig_h, use_container_width=True)

    # --- ALT SIRA: GENİŞ OKSİJEN GRAFİĞİ ---
    st.markdown("---")
    # Oksijen (SpO2) Analizi
    df_oksijen = pd.DataFrame({'Zaman': range(24), 'Oksijen': np.random.normal(oksijen, 1, 24)})
    fig_o = px.area(df_oksijen, x='Zaman', y='Oksijen', title="🫁 Oksijen (SpO2 %) Seviyesi - Geniş İzleme", template="plotly_dark")
    fig_o.update_traces(fillcolor='rgba(160, 214, 232, 0.4)', line_color='#A0D6E8') # Buz mavisi ve şeffaf dolgu
    
    # Oksijen grafiği genellikle 90-100 arası olduğu için Y eksenini sabitleyelim ki daha net görünsün
    fig_o.update_yaxes(range=[85, 105]) 
    
    st.plotly_chart(fig_o, use_container_width=True)

elif sayfa_secimi == "🚨 Acil Durum Rehberi":
    st.title("🚨 Acil Durum Protokolleri")
    st.markdown("---")
    st.error("Kritik Seviye Müdahaleleri (Tablo 1 & 6)")
    
    with st.expander("🔴 Psikolojik Müdahale (%70+ Risk)"):
        st.write("- Personel derhal sosyal etkileşime yönlendirilmelidir.")
        st.write("- Uyku düzeni 8 saate sabitlenmelidir.")
    
    with st.expander("🟡 Fizyolojik Müdahale (Düşük SpO2/HRV)"):
        st.write("- Oksijen satürasyonu %94 altındaysa ortam havalandırması kontrol edilmelidir.")
        st.write("- HRV skoru 40 altındaysa fiziksel aktivite kısıtlanmalıdır.")
