import requests
import logging
from config import Config

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    pass


class AIService:

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "llama-3.1-8b-instant"
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def yanit_uret(self, mesaj, dolap_listesi="", gecmis=None):

        if not self.api_key:
            raise AIServiceError("Groq API anahtarı bulunamadı.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        system_prompt = Config.BUSINESS_CONTEXT.format(
    dolap_listesi=(
        dolap_listesi
        if dolap_listesi
        else "Henüz dolaba kıyafet eklenmemiş."
    )
)

        # Groq'a gönderilecek mesaj listesi.
        # Önce sistem talimatı, sonra geçmiş konuşmalar,
        # en son yeni kullanıcı mesajı gönderilir.
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Önceki konuşma geçmişini ekle.
        if gecmis:
            messages.extend(gecmis)

        # Yeni kullanıcı mesajını konuşmanın en sonuna ekle.
        messages.append({
            "role": "user",
            "content": mesaj
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        try:

            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=15
            )

        except requests.RequestException as e:

            logger.error(
                "Groq API bağlantı hatası: %s",
                str(e)
            )

            raise AIServiceError(
                "Yapay zeka servisine ulaşılamadı."
            )

        if response.status_code == 200:

            data = response.json()

            return data["choices"][0]["message"]["content"]

        logger.error(
            "Groq API hatası: %s - %s",
            response.status_code,
            response.text
        )

        raise AIServiceError(
            f"Yapay zeka servisi hata döndürdü ({response.status_code})."
        )


ai_service = AIService()
