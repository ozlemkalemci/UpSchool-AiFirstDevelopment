from matplotlib import pyplot as plt
from prophet import Prophet
import pandas as pd
import streamlit as st
class TimeSeriesAnalyzer:
    def run_analysis(self, data, country=None):
        # Prophet modelini başlat
        st.write("Prophet başlatılıyor...")
        model = Prophet()

        # Eğer ülke sağlanmışsa, tatil günlerini modele ekle
        if country:
            model.add_country_holidays(country_name=country)

        model.add_seasonality(name='hourly', period=24, fourier_order=3)

        # Veriyi hazırlamak: "Timestamp" sütununu "ds", "Energy_Consumption" sütununu "y" olarak yeniden adlandır
        data = data.reset_index().rename(columns={"Timestamp": "ds", "Energy_Consumption": "y"})

        data['ds'] = pd.to_datetime(data['ds'])
        st.write(data.head())
        st.write(data.tail())

        color_pal = ["#F8766D", "#D39200", "#93AA00", "#00BA38",
                     "#00C19F", "#00B9E3", "#619CFF", "#DB72FB"]


        st.line_chart(data.set_index('ds')['y'])

        progress = st.progress(0)  # Başlangıçta %0

        st.write("Model eğitiliyor...")

        model.fit(data)

        progress.progress(50)  # Eğitim tamamlandığında %50'ye güncelle

        st.write("Tahmin modeli oluşturuluyor...")

        # 7 gün * 24 saatlik bir geleceğe yönelik tahmin oluştur
        future = model.make_future_dataframe(periods=168, freq="H")  # 7 gün * 24 saat

        progress.progress(75)  # Tahminler oluşturuluyor, %75


        forecast = model.predict(future)

        progress.progress(100)
        st.write("Tahmin modeli oluşturuldu...")
        return forecast
