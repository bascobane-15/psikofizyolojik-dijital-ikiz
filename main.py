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
sayfa_secimi = st.sidebar.selectbox(
    "Bölüm Seçiniz:",
    [
        "🏠 Ana Kontrol Paneli",
        "📊 Fizyolojik Derin Analiz",
        "🚨 Acil Durum Rehberi",
        "🧩 Dijital İkiz Veri Mimarisi",
        "📡 Gerçek Veri Entegrasyonu"
    ]
)

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

# ==========================================
# 📡 AKTİF VERİ KAYNAĞI SEÇİMİ (CSV > Sidebar)
# ==========================================

if uploaded_file is not None:
    # CSV'den son satırı al (en güncel veri varsayımı)
    aktif_hrv = int(df_sensor["HRV"].iloc[-1])
    aktif_spo2 = int(df_sensor["SpO2"].iloc[-1])
    aktif_nabiz = int(df_sensor["Nabiz"].iloc[-1])

    st.success("📡 Aktif veri kaynağı: CSV dosyası")

else:
    # CSV yoksa sidebar değerlerini kullan
    aktif_hrv = hrv
    aktif_spo2 = spo2
    aktif_nabiz = nabiz

    st.info("⌚ Aktif veri kaynağı: Manuel giriş (Sidebar)")


# --- RİSK HESAPLAMA MOTORU ---
def akademik_risk_hesapla():
    # --- 1. PSİKOLOJİK STRES İNDEKSİ (PSİ) HESABI ---
    p_skor = 0
    if izolasyon > 90: p_skor += 35
    elif izolasyon >= 30: p_skor += 20
    if gorev_yogunlugu == "Yüksek": p_skor += 25
    if sosyal_etkilesim == "Çok Sınırlı": p_skor += 25
    
    # [TABLO 6 KURALI]: HRV normalin %20 altına düşerse (Örn: <45) PSİ'ye +15 puan ekle
    if aktif_hrv < 45: 
        p_skor += 15

    # --- 2. FİZYOLOJİK YÜKLENME İNDEKSİ (FYİ) HESABI ---
    f_skor = 0
    if uyku < 6: f_skor += 30
    
    # [TABLO 6 KURALI]: Dinlenme Nabzı > 80 bpm ise FYİ'ye +10 puan ekle
    if aktif_nabiz > 80:
        f_skor += 10
    
    # --- 3. IŞIK RİSKİ ---
    isik_risk_map = {"Düşük": 25, "Orta": 35, "Yüksek": 55, "Çok Yüksek": 65}
    isik_riski = isik_risk_map[isik_maruziyeti]

    # --- 4. BÜTÜNLEŞİK RİSK SKORU (BPRS) VE ŞİDDETLENDİRME ---
    toplam_risk = (p_skor + f_skor + isik_riski) / 3
    
    # [TABLO 6 KURALI]: Oksijen %94'ün altına inerse BPRS skoru 1.15 ile çarpılır
    if aktif_spo2 < 94:
        toplam_risk = toplam_risk * 1.15
        
    # [TABLO 6 KURALI]: Uyku kalitesi (derin uyku) düşükse genel risk %20 artar
    # Not: Eğer derin uyku verisi yoksa genel uyku üzerinden simüle ediyoruz
    if uyku < 5:
        toplam_risk *= 1.20

    return min(100, int(toplam_risk)), p_skor, f_skor

risk_skoru, p_indeks, f_indeks = akademik_risk_hesapla()
# --- GELİŞMİŞ SENARYO VE KARAR DESTEK MODÜLÜ ---
st.sidebar.markdown("---")

# ÖNCELİKLİ DURUM 1: Hipoksik Stres (Oksijen)
if spo2 < 94:
    st.sidebar.error(f"🚨 **HİPOKSİK STRES:** Oksijen %{spo2}! Kandaki düşük oksijen, fiziksel bitkinliği ve bilişsel hataları hızlandırır [Tablo 6].")
    st.sidebar.caption("💡 **Öneri:** Derin nefes egzersizi yapın ve kabin basıncını kontrol edin.")

# DURUM 2: Otonom Sinir Sistemi Yorgunluğu (HRV)
elif hrv < 45:
    st.sidebar.info("🧠 **OTONOM YORGUNLUK:** HRV değeriniz (%45) kritik eşiğin altında! Vücudunuzun strese karşı toleransı düşmüş durumda [Tablo 7].")
    st.sidebar.caption("💡 **Öneri:** Kısa süreli dinlenme (power-nap) veya meditasyon önerilir.")

# DURUM 3: Sirkadiyen Ritim Bozulması (Nabız & Uyku)
elif nabiz > 80 and uyku < 5:
    st.sidebar.warning("⚠️ **SİRKADİYEN RİSK:** Yüksek nabız ve yetersiz uyku kombinasyonu tespit edildi! Fizyolojik yüklenme (FYİ) artıyor [Tablo 6].")
    st.sidebar.caption("💡 **Öneri:** Acil olmayan görevleri erteleyin ve uyku periyoduna geçin.")

# DURUM 4: Yüksek Kümülatif Risk (BPRS)
elif risk_skoru > 65:
    st.sidebar.warning(f"📈 **KÜMÜLATİF YÜK:** Bütünleşik risk skoru %{risk_skoru}! Psikolojik ve çevresel faktörler güvenli sınırı aştı [Tablo 7].")
    st.sidebar.caption("💡 **Öneri:** İzolasyon etkisini azaltmak için sosyal etkileşim kurun.")

# DURUM 5: İdeal Durum
else:
    st.sidebar.success("✅ **SİSTEM STABİL:** Fizyolojik ve psikolojik parametreler nominal değerlerde. Görev icrası için uygunsunuz.")
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
elif sayfa_secimi == "📡 Gerçek Veri Entegrasyonu":
    st.title("📡 Gerçek Veri Entegrasyonu")
    
    # Metodolojindeki Tablo 6 ve 7 Katsayıları
    GAMMA_HYPOXIC = 1.15  # SpO2 < 94 için şiddetlendirme
    
    uploaded_file = st.file_uploader("Sensör verisi yükle (CSV)", type=["csv"])

    if uploaded_file is not None:
        try:
            # ÖNEMLİ: sep=None ve engine='python' sayesinde CSV'deki ; veya , ayrımını otomatik çözer
            df_sensor = pd.read_csv(uploaded_file, sep=None, engine='python')
            
            # Sütun isimlerini temizle (boşlukları sil ve küçük harf yap)
            df_sensor.columns = [c.strip().lower() for c in df_sensor.columns]
            
            # --- DİJİTAL İKİZ HESAPLAMA MOTORU ---
            def hesapla_bprs(row):
                # PSI: HRV < 45 ise +15 puan stres yükü
                psi = 20 + (15 if float(row['hrv']) < 45 else 0)
                # FYI: Nabız > 80 ise +10 puan fiziksel yük
                fyi = 10 + (10 if float(row['nabiz']) > 80 else 0)
                # Gamma: SpO2 < 94 ise %15 artış
                gamma = GAMMA_HYPOXIC if float(row['spo2']) < 94 else 1.0
                
                return (psi + fyi) * gamma

            # Hesaplamayı yap ve yeni sütun ekle
            df_sensor['risk_skoru'] = df_sensor.apply(hesapla_bprs, axis=1)

            # --- EKRANDA DEĞİŞİKLİĞİ GÖSTERECEK ALAN ---
            st.success("✅ Veriler Başarıyla Ayrıştırıldı ve BPRS Hesaplandı!")
            
            # Üst tarafa özet metrikler ekleyelim (Bu kısım görseli değiştirir)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Analiz Edilen Kayıt", len(df_sensor))
            with col2:
                st.metric("Ortalama Risk", f"%{df_sensor['risk_skoru'].mean():.1f}")
            with col3:
                anlik_risk = df_sensor['risk_skoru'].iloc[-1]
                st.metric("Anlık Risk Durumu", f"%{anlik_risk:.1f}")

            # Risk Grafiği (Bu en büyük görsel değişikliktir)
            st.subheader("📈 Bütünleşik Risk Projeksiyonu (BPRS)")
            st.area_chart(df_sensor['risk_skoru'])

            # Tabloyu göster
            with st.expander("Hesaplanan Ham Verileri İncele"):
                st.dataframe(df_sensor)

        except Exception as e:
            st.error(f"⚠️ Dosya İşleme Hatası: {e}")
            st.info("Lütfen CSV dosyasının 'hrv', 'spo2' ve 'nabiz' başlıklarını içerdiğinden emin olun.")


   

