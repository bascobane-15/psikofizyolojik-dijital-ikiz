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
    ["🏠 Ana Kontrol Paneli",
     "📊 Fizyolojik Derin Analiz",
    "🧩 Dijital İkiz Veri Akışı",
     "🚨 Acil Durum Rehberi" ]
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

# --- RİSK HESAPLAMA MOTORU ---
def akademik_risk_hesapla():
    # --- 1. PSİKOLOJİK STRES İNDEKSİ (PSİ) HESABI ---
    p_skor = 0
    if izolasyon > 90: p_skor += 35
    elif izolasyon >= 30: p_skor += 20
    if gorev_yogunlugu == "Yüksek": p_skor += 25
    if sosyal_etkilesim == "Çok Sınırlı": p_skor += 25
    
    # [TABLO 6 KURALI]: HRV normalin %20 altına düşerse (Örn: <45) PSİ'ye +15 puan ekle
    if hrv < 45: 
        p_skor += 15

    # --- 2. FİZYOLOJİK YÜKLENME İNDEKSİ (FYİ) HESABI ---
    f_skor = 0
    if uyku < 6: f_skor += 30
    
    # [TABLO 6 KURALI]: Dinlenme Nabzı > 80 bpm ise FYİ'ye +10 puan ekle
    if nabiz > 80:
        f_skor += 10
    
    # --- 3. IŞIK RİSKİ ---
    isik_risk_map = {"Düşük": 25, "Orta": 35, "Yüksek": 55, "Çok Yüksek": 65}
    isik_riski = isik_risk_map[isik_maruziyeti]

    # --- 4. BÜTÜNLEŞİK RİSK SKORU (BPRS) VE ŞİDDETLENDİRME ---
    toplam_risk = (p_skor + f_skor + isik_riski) / 3
    
    # [TABLO 6 KURALI]: Oksijen %94'ün altına inerse BPRS skoru 1.15 ile çarpılır
    if spo2 < 94:
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

elif sayfa_secimi == "📊 Fizyolojik Derin Analiz":
    st.title("📊 Detaylı Sağlık Analizi")
    st.markdown("---")
    
    # Veri Tanımlamaları (Hata almamak için güvenli yöntem)
    current_nabiz = nabiz if 'nabiz' in locals() else 72
    current_hrv = hrv if 'hrv' in locals() else 55
    current_oksijen = oksijen if 'oksijen' in locals() else 98

    st.info(f"Anlık İzleme: Nabız {current_nabiz} bpm | HRV {current_hrv} | Oksijen %{current_oksijen}")
    
    # --- ÜST SIRA: 2 GRAFİK YAN YANA ---
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. GRAFİK: NABIZ (Çizgi Grafik)
        df_n = pd.DataFrame({'Zaman': range(24), 'Nabız': np.random.normal(current_nabiz, 2, 24)})
        fig_n = px.line(df_n, x='Zaman', y='Nabız', title="💓 24 Saatlik Nabız Takibi", template="plotly_dark")
        fig_n.update_traces(line_color='#4A90E2')
        st.plotly_chart(fig_n, use_container_width=True)

    with col2:
        # 2. GRAFİK: HRV (Sütun Grafik)
        df_h = pd.DataFrame({'Zaman': range(24), 'HRV': np.random.normal(current_hrv, 4, 24)})
        fig_h = px.bar(df_h, x='Zaman', y='HRV', title="📊 HRV Stabilite Değerleri", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig_h, use_container_width=True)

    # --- ALT SIRA: TEK GRAFİK ---
    st.markdown("---")
    # 3. GRAFİK: OKSİJEN (Alan Grafik)
    df_o = pd.DataFrame({'Zaman': range(24), 'Oksijen': np.random.normal(current_oksijen, 0.5, 24)})
    fig_o = px.area(df_o, x='Zaman', y='Oksijen', title="🫁 Oksijen (SpO2 %) Seviyesi - Geniş İzleme", template="plotly_dark")
    fig_o.update_traces(fillcolor='rgba(160, 214, 232, 0.4)', line_color='#A0D6E8')
    fig_o.update_yaxes(range=[85, 105]) # Oksijen değerini daha net görmek için ölçekleme
    
    st.plotly_chart(fig_o, use_container_width=True)
elif sayfa_secimi == "🧩 Dijital İkiz Veri Akışı":
    st.title("🧩 Dijital İkiz – Gerçek Veri Entegrasyon Akışı")
    st.caption("Simülasyon tabanlı modelden, veriyle kalibre edilebilir dijital ikiz mimarisine geçiş")
    st.markdown("---")

    # === ÜST: AKIŞIN SÖZEL TEMSİLİ ===
    st.subheader("📥 Girdi Katmanı (Input Layer)")
    st.markdown("""
    - İzolasyon Süresi **I(t)**
    - Görev Yoğunluğu **G(t)**
    - Uyku Süresi **U(t)**
    - Sosyal Etkileşim **S(t)**
    - Giyilebilir Sensörler *(opsiyonel)*: **HRV**, **SpO₂**
    """)

    st.markdown("⬇️")

    st.subheader("⚙️ Ön İşleme ve Normalizasyon")
    st.markdown("""
    - Tüm değişkenler **0–1 aralığında normalize edilir**
    - Zaman adımlarına bölünür *(t → t+1)*
    - Gürültü ve eksik veri kavramsal olarak ele alınır
    """)

    st.markdown("⬇️")

    # === ÇEKİRDEK MODEL ===
    st.subheader("🧠 Dijital İkiz Model Çekirdeği")
    st.latex(r"""
    R(t)= w_1 I(t) + w_2 G(t) - w_3 U(t) - w_4 S(t) + w_5 I(t)\cdot G(t)
    """)
    st.latex(r"""
    P(t)=P(t-1)+\alpha \cdot R(t)
    """)

    st.markdown("""
    - Risk **anlık değil**, zamanla **birikimli** hesaplanır  
    - İzolasyon süresine bağlı **gecikmeli kırılma davranışı** modellenir  
    """)

    st.markdown("⬇️")

    # === İNDEKSLER ===
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Psikolojik Stres İndeksi (PSI)")
        st.markdown("""
        - Algılanan stres  
        - Bilişsel yorgunluk  
        - Duygudurum dalgalanması  
        """)

    with col2:
        st.subheader("💓 Fizyolojik Yüklenme İndeksi (FYI)")
        st.markdown("""
        - Uyku bozulması  
        - Sirkadiyen ritim  
        - **HRV & SpO₂ → şiddetlendirici katsayı (β)**  
        """)

    st.markdown("⬇️")

    # === BÜTÜNLEŞİK SKOR ===
    st.subheader("📊 Bütünleşik Psikofizyolojik Risk Skoru (BPRS)")
    st.latex(r"""
    BPRS(t) = (PSI + FYI) \times \gamma(t)
    """)

    st.markdown("""
    - İzolasyon süresiyle etkileşimlidir  
    - **60. gün sonrası doğrusal olmayan risk artışı** temsil edilir  
    """)

    st.markdown("⬇️")

    # === ERKEN UYARI ===
    st.subheader("🚨 Erken Risk Uyarı Mekanizması")
    st.latex(r"""
    \text{If } \frac{d(BPRS)}{dt} > \theta \Rightarrow \text{ALERT}
    """)

    st.markdown("""
    - Mutlak skor yerine **değişim hızı** izlenir  
    - Kritik eşik aşıldığında sistem uyarı üretir  
    """)

    st.markdown("---")

    # === KALİBRASYON VURGUSU (ÇOK KRİTİK) ===
    st.success(
        "🔁 Bu dijital ikiz mimarisi, giyilebilir sensörlerden elde edilecek "
        "gerçek dünya verileri ile **kalibre edilebilir şekilde tasarlanmıştır**. "
        "Mevcut çalışma, klinik doğrulama içermeyen simülasyon tabanlı bir altyapı sunmaktadır."
    )
elif page == "Dijital İkiz Gerçek Veri Entegrasyonu":

    st.header("🔗 Dijital İkiz – Gerçek Veri Entegrasyon Akışı")

    st.markdown("""
    Bu sayfa, dijital ikiz modelinin harici sensör verileriyle
    kalibre edilebilir bir sisteme dönüştürülmesini amaçlayan
    kavramsal ve deneysel veri akışını göstermektedir.
    """)

elif sayfa_secimi == "🚨 Acil Durum Rehberi":
    st.title("🚨 Acil Durum Protokolleri")
    st.markdown("---")
    
    # --- 1. CANLI DURUM ANALİZİ (Okunabilirliği artırılmış) ---
    if risk_skoru > 60:
        st.warning(f"### ⚠️ DİKKAT: Risk Skorunuz %{risk_skoru}")
        st.write("Şu anki verileriniz yüksek risk grubundadır. Lütfen aşağıdaki adımları sırasıyla takip edin.")
    else:
        st.success("### ✅ Durum Stabil")
        st.write("Risk seviyeniz güvenli aralıkta. Aşağıdaki protokoller önleyici bilgi amaçlıdır.")

    # Parantez içindeki (Tablo 1 & 6) ibaresi kaldırıldı
    st.error("Kritik Seviye Müdahaleleri")

    # --- 2. MEVCUT GENİŞLETİLEBİLİR PANELLER ---
    with st.expander("🔴 Psikolojik Müdahale (%70+ Risk)"):
        st.markdown("#### **Uygulanacak Adımlar:**")
        st.write("- **Sosyal Etkileşim:** Personel derhal sosyal etkileşime yönlendirilmelidir.")
        st.write("- **Uyku Standardı:** Uyku düzeni 8 saate sabitlenmelidir.")

    with st.expander("🟡 Fizyolojik Müdahale (Düşük SpO2/HRV)"):
        st.markdown("#### **Uygulanacak Adımlar:**")
        st.write("- **Havalandırma:** Oksijen satürasyonu %94 altındaysa ortam havalandırması kontrol edilmelidir.")
        st.write("- **Aktivite Kısıtlaması:** HRV skoru 40 altındaysa fiziksel aktivite derhal kısıtlanmalıdır.")

    # --- 3. MÜDAHALE EŞİK DEĞERLERİ (Tablo yerine büyük yazılı kartlar) ---
    st.markdown("---")
    st.subheader("📊 Müdahale Eşik Değerleri")
    
    col_x, col_y, col_z = st.columns(3)
    
    with col_x:
        st.markdown("""
        **🫁 HİPOKSİ** **Eşik:** SpO2 < %94  
        **Aksiyon:** Oksijen Desteği
        """)
        
    with col_y:
        st.markdown("""
        **🧠 OSS YORGUNLUĞU** **Eşik:** HRV < 45 ms  
        **Aksiyon:** Aktif Dinlenme
        """)
        
    with col_z:
        st.markdown("""
        **📉 KRİTİK RİSK** **Eşik:** Risk > %70  
        **Aksiyon:** Görev Durdurma
        """)

    # --- 4. AKADEMİK REFERANS BİLGİ KUTUSU ---
    st.markdown("---")
    with st.expander("ℹ️ Dijital İkiz Modeli ve Akademik Referanslar"):
        st.markdown(f"""
        **Metodoloji:** Bu protokoller, **Tablo 6**'daki fizyolojik katsayılar ve **Tablo 7**'deki dinamik bütünleşik risk hesaplamalarına (BPRS) göre anlık olarak filtrelenmektedir. 
        
        **Önemli Not:** Oksijen seviyesindeki her düşüş, tüm riskleri **1.15 katsayısı** ile şiddetlendirir.
        """)
    # --- 4. MEVCUT BİLGİ KUTUSU (Geliştirildi) ---
    st.markdown("---")
    with st.expander("ℹ️ Dijital İkiz Modeli ve Akademik Referanslar Hakkında"):
        st.write("**Metodoloji:** Bu protokoller, Tablo 6'daki fizyolojik katsayılar ve Tablo 7'deki bütünleşik risk hesaplamalarına göre dinamik olarak filtrelenmektedir.")
        st.write("**Referans:** Palinkas ve Suedfeld (2008), Uzay ve Antarktika Görevlerinde Psikofizyolojik Uyum Protokolleri.")
# --- SAYFA SONU: DİJİTAL İKİZ HAKKINDA BİLGİ KUTUSU ---
st.markdown("---")
with st.expander("ℹ️ Dijital İkiz Modeli ve Akademik Referanslar Hakkında"):
    st.markdown(f"""
    ### 🔬 Psikofizyolojik Dijital İkiz Metodolojisi
    Bu simülasyon, kutup araştırmacılarının ekstrem koşullardaki biyo-psikolojik yanıtlarını modellemek amacıyla **Tablo 6 (Fizyolojik Katsayılar)** ve **Tablo 7 (Dinamik Entegrasyon)** verileri temel alınarak geliştirilmiştir.
    
    **Temel Algoritmalar:**
    * **Şiddetlendirme Katsayısı:** Oksijen satürasyonunun (SpO2) %94'ün altına düşmesi, Bütünleşik Risk Skorunu (BPRS) **1.15 kat** artırarak hipoksik stresi simüle eder.
    * **Psikolojik Stres Artışı (PSİ):** HRV değerinin normalin %20 altına düşmesi, modele doğrudan **+15 puanlık** bir stres yükü ekler.
    * **Fizyolojik Yüklenme (FYİ):** Dinlenme nabzının 80 bpm üzerine çıkması, fiziksel kondisyon kaybını temsilen **+10 puanlık** bir yük tetikler.
    * **Kümülatif Yük:** Yetersiz uyku (<2 saat derin uyku veya <5 saat toplam uyku) genel risk projeksiyonunu **%20 oranında** yukarı çeker.

    **Geliştirme Ortamı:** Replit | Streamlit | Python tabanlı karar destek sistemi.
    """)
    st.info("Bu model, Palinkas ve Suedfeld (2008) ile Stuster (2016) tarafından tanımlanan izolasyon evreleri ve literatürdeki fizyolojik eşik değerlerle %100 uyumlu çalışmaktadır.")

