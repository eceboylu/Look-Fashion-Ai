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

    def yanit_uret(self, mesaj, dolap_listesi=""):
        if not self.api_key:
            raise AIServiceError("Groq API anahtari bulunamadi.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        system_prompt = (
            Config.BUSINESS_CONTEXT
            + f"\nKullanicinin Dolabindaki Mevcut Kiyafetler: {dolap_listesi}"
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mesaj}
            ],
            "temperature": 0.7
        }

        # Ağ/bağlantı hatalarını ayrı yakala
        try:
            response = requests.post(
                self.url, json=payload, headers=headers, timeout=15
            )
        except requests.RequestException as e:
            logger.error("Groq API baglanti hatasi: %s", str(e))
            raise AIServiceError("Yapay zeka servisine ulasilamadi.")

        # HTTP durumunu ayrı değerlendir — artık aynı try bloğunda değil,
        # bu yüzden alttaki except tarafından tekrar sarılmıyor
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]

        logger.error("Groq API hatasi: %s - %s", response.status_code, response.text)
        raise AIServiceError(f"Yapay zeka servisi hata dondurdu ({response.status_code}).")


ai_service = AIService()