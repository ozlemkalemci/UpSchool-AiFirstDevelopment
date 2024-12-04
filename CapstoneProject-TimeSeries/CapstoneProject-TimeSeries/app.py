import streamlit as st
from utils.data_processor import DataProcessor
from utils.analysis import TimeSeriesAnalyzer
from utils.gemini_client import GeminiClient
from components.file_upload import file_uploader
from matplotlib import pyplot as plt
from datetime import timedelta

# Başlık
st.title("Enerji Tüketimi Verileri İle Zaman Serisi Analizi")
st.write("Bu uygulama Prophet ile 1 haftalık enerji tüketim verisi tahmin eder ve Gemini kullanarak işletme verimliliği için önerilerde bulunur")

# Ülke ve Şehir Bilgisi
st.sidebar.header("Seçili Ülkenin Tatillerini Dahil Et (Opsiyonel)")
# Holidays kütüphanesinde desteklenen ülkeler
country_codes = {
    "Türkiye": "TR",
    "Amerika Birleşik Devletleri": "US",
    "Almanya": "DE",
    "Fransa": "FR",
    "Birleşik Krallık": "GB"
}

# Ülke seçimi
country_name = st.sidebar.selectbox("Ülke Seçiniz", [None] + list(country_codes.keys()))
country = country_codes.get(country_name) if country_name else None

# Dosya Yükleme
uploaded_file = file_uploader()

if uploaded_file:
    try:
        processor = DataProcessor()
        # Veriyi işle
        data, missing_info = processor.process_file(uploaded_file)
        # Eksik verilerle ilgili bilgi
        if missing_info:
            st.write(missing_info)

    except ValueError as e:
        st.error(f"Hata: {e}")
    try:
        analyzer = TimeSeriesAnalyzer()
        forecast_df = analyzer.run_analysis(data, country)

        # Zaman ve tahmin değerlerini içeren bir DataFrame oluştur
        forecast_df = forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'trend']]
        st.write(forecast_df.head(5))
        st.write(forecast_df.tail(168))

        # Son bir haftayı filtrele
        last_week = forecast_df[forecast_df['ds'] > (forecast_df['ds'].max() - timedelta(weeks=1))]

        # Grafik Gösterimi
        st.subheader("Son Bir Haftalık Zaman Serisi Tahmini")
        st.line_chart(last_week.set_index('ds')['yhat'])

    except Exception as e:
        st.error(f"Zaman Serisi Analizi Hatası: {e}")

    # Gemini API
    try:
        st.subheader("Gemini'den İşletme Kararları")
        gemini = GeminiClient()
        report = gemini.generate_report(forecast_df)
        st.text_area("Rapor:", report)
        st.markdown(report)
    except Exception as e:
        st.error(f"Gemini API Hatası: {e}")
