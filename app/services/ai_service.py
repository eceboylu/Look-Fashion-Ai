import requests
import logging

#config dosyasını import ediyoruz.
from config import Config

# '__name__' bu dosyanın adını temsil eder, böylece hatanın hangi dosyadan geldiğini anlarız.
logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    pass


class AIService:

    def __init__(self):
        # Ayarlar artık koda gömülü değil, config.py (ve .env) üzerinden geliyor.
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self.url = Config.GROQ_API_URL

    def yanit_uret(self, mesaj, gecmis=None):

        if not self.api_key:
            raise AIServiceError(
                "Groq API anahtarı bulunamadı."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        system_prompt = Config.BUSINESS_CONTEXT

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
            # Satış danışmanında düşük temperature: uydurma fiyat/özellik riskini azaltır.
            "temperature": Config.AI_TEMPERATURE,
            # Cevabın uzayıp reklam metnine dönmesini engeller.
            "max_tokens": Config.AI_MAX_TOKENS
        }

        # reasoning_effort sadece gpt-oss ailesinde geçerli.
        # Boş bırakılırsa gönderilmez, böylece desteklemeyen modellerde
        # istek hata vermez.
        if Config.AI_REASONING_EFFORT:
            payload["reasoning_effort"] = Config.AI_REASONING_EFFORT

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=Config.AI_TIMEOUT
            )

        except requests.RequestException as e:

            logger.error(
                "Groq API bağlantı hatası: %s",
                str(e)
            )

            print("GROQ HATASI:", repr(e))

            raise AIServiceError(
                f"AI bağlantı hatası: {str(e)}"
            )

        if response.status_code == 200:

            data = response.json()

            try:
                # Gelen karmaşık JSON verisi içinden sadece yapay zekanın yazdığı metni çek
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

        print(
            "GROQ HATASI:",
            response.status_code,
            response.text
        )

        raise AIServiceError(
            f"Yapay zeka servisi hata döndürdü ({response.status_code})."
        )


ai_service = AIService()