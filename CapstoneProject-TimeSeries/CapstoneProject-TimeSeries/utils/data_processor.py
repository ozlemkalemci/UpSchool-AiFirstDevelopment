import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns

class DataProcessor:
    def process_file(self, file):
        try:
            # Dosyayı oku, başlık olup olmadığını kontrol et
            data = pd.read_csv(file, sep=';', encoding='utf-8', header=0)

        except Exception as e:
            raise ValueError(f"Dosya okuma hatası: {e}")

        # Dosya formatı kontrolü
        if "Timestamp" not in data.columns or "Energy_Consumption" not in data.columns:
            raise ValueError(
                "Dosya uygun formatta değil. Lütfen 'Timestamp' ve 'Energy_Consumption' sütunlarına sahip bir dosya yükleyin."
            )

        # 'Timestamp' sütununu datetime formatına çevir
        data["Timestamp"] = pd.to_datetime(data["Timestamp"], format="%d.%m.%Y %H:%M")

        # Zamanı indeks olarak ayarla
        data = data.set_index("Timestamp")

        # Verinin ilk 5 satırını göster
        st.write("Verinin ilk 5 satırı:")
        st.write(data.head())

        # Veri türleri ve temel istatistiksel bilgiler
        st.write("Veri Türleri ve Temel İstatistiksel Bilgiler:")
        st.write(data.info())
        st.write(data.describe())

        # Saatlik frekansa göre yeniden örnekle
        dt_range = pd.date_range(data.index.min(), data.index.max(), freq='H')
        dt_range = pd.DataFrame(data=dt_range, columns=["Timestamp"])

        # Mevcut veri ile zaman aralığını birleştir
        missing_dts = pd.DataFrame(dt_range.merge(data,
                                                  indicator=True,
                                                  how='left',
                                                  on="Timestamp").loc[lambda x: x['_merge'] != 'both']).reset_index(
            drop=True)

        st.write("Eksik tarihler:")
        st.write(missing_dts)

        # Eksik veri varsa, eksik olanları veri setine ekle
        df_with_missing = pd.concat([data, missing_dts.set_index('Timestamp')], axis=0).sort_index()

        # Eksik verilerin sayısını al
        missing_data = df_with_missing[df_with_missing["Energy_Consumption"].isna()]
        st.write("Veri setindeki null sayısı:")
        st.write(missing_data.count())
        # Eksik verileri doldur
        df_with_missing["Energy_Consumption"] = df_with_missing["Energy_Consumption"].ffill().bfill()

        missing_info = f"{len(missing_data)} eksik veri dolduruldu." if not missing_data.empty else None

        return df_with_missing, missing_info
