import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    def __init__(self):

        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

    def generate_report(self, forecast_df):
        prompt = f"""
        Aşağıda saatlik olarak enerji tüketimi verileri verilmiştir. Bu verilerin son bir haftası Prophet tarafından tahminlenmiş verilerdir. "ds" kolonu saat ve tarih bilgisini tutmaktadır. İşletme verimliliği için önerilerde bulunduğun ve enerji tasarrufu sağlamak amacıyla stratejik tavsiyeler verdiğin bir rapor oluştur. Yanıtı Markdown formatında oluştur ve Türkçe yaz.

        {forecast_df.to_string(index=False)}
        """

        generation_config = {
            "temperature": 0.8,  # Yanıtın çeşitliliğini etkiler
            "top_p": 0.9,  # Yanıtın olasılık kesim parametresi
            "max_output_tokens": 500,  # Maksimum çıktı uzunluğu
            "response_mime_type": "text/plain",  # Yanıt formatı
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            safety_settings=safety_settings,
            generation_config=generation_config,
        )

        # Modelden içerik üretme
        response = model.generate_content(prompt)

        # Raporu döndürüyoruz
        return response.text
