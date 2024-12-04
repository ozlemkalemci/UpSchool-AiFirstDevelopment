import holidays
import pandas as pd


class HolidayChecker:
    def check_holidays(self, country, year=None):
        holiday_list = []

        # Eğer yıl verilmediyse, mevcut yıl alınır
        if year is None:
            year = pd.Timestamp.today().year

        # Ülkeye göre tatil günlerini al
        for holiday in holidays.CountryHoliday(country=country, years=[year]).items():
            holiday_list.append(holiday)

        # Tatil günlerini bir DataFrame'e dönüştür
        holidays_df = pd.DataFrame(holiday_list, columns=["Datetime", "Holiday"])
        holidays_df = holidays_df.set_index('Datetime')  # Tarihi index olarak ayarla

        return holidays_df

