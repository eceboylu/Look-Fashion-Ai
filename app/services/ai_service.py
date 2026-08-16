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

    def yanit_uret(self, mesaj, gecmis=None):

        if not self.api_key:
            raise AIServiceError(
                "Groq API anahtarı bulunamadı."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Satış asistanının tüm davranış kuralları
        system_prompt = Config.BUSINESS_CONTEXT

        # Groq'a gönderilecek mesajlar:
        # 1. Sistem talimatı
        # 2. Önceki konuşma geçmişi
        # 3. Yeni kullanıcı mesajı
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        if gecmis:
            messages.extend(gecmis)

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
                print("GROQ HATASI:", repr(e))
    return f"AI hatası: {str(e)}"
            )

        if response.status_code == 200:

            data = response.json()

            try:
                return data["choices"][0]["message"]["content"]

            except (KeyError, IndexError, TypeError):

                logger.error(
                    "Groq API beklenmeyen cevap döndürdü: %s",
                    data
                )

                raise AIServiceError(
                    "Yapay zeka geçerli bir cevap oluşturamadı."
                )

        logger.error(
            "Groq API hatası: %s - %s",
            response.status_code,
            response.text
        )

        raise AIServiceError(
            f"Yapay zeka servisi hata döndürdü ({response.status_code})."
        )


ai_service = AIService()