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
            raise AIServiceError("Groq API anahtarı bulunamadı.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        system_prompt = f"""
Sen "AI Wardrobe" adlı dijital gardırop uygulamasının
kişisel stil asistanısın.

GÖREVİN:
Kullanıcıya kişisel stil, kombin, kıyafet ve gardırop konusunda
yardımcı olmak.

KULLANICININ DOLABINDAKİ MEVCUT KIYAFETLER:
{dolap_listesi if dolap_listesi else "Henüz dolaba kıyafet eklenmemiş."}

TEMEL KURALLAR:

1. Kullanıcı bir kombin istediğinde mümkün olduğunca
   kullanıcının dolabındaki mevcut kıyafetleri kullan.

2. Kullanıcı dolabında bulunan kıyafetlerden kombin oluşturabiliyorsan
   doğrudan kombin öner. Gereksiz yere kullanıcıdan kıyafetlerinin
   listesini tekrar isteme.

3. Dolapta yeterli kıyafet yoksa bunu kısa ve doğal şekilde belirt.
   Ardından kullanıcıya elindeki bilgilerle mümkün olan en iyi
   öneriyi sun.

4. Kullanıcı hava durumundan bahsediyorsa mevsim ve hava koşullarını
   dikkate al.

5. Kullanıcı belirli bir kıyafet hakkında soru sorarsa doğrudan
   o kıyafet üzerinden öneri yap.

6. Renk uyumu, stil uyumu, mevsim, kullanım amacı ve genel görünümü
   dikkate al.

7. Kullanıcı "ne giyebilirim?", "kombin öner", "bugün ne giysem?"
   gibi genel bir soru sorarsa önce mevcut dolaptaki kıyafetleri
   değerlendir ve mümkünse doğrudan 1-3 kombin öner.

8. Kullanıcıya gereksiz uzun sorular sorma.
   Cevapların doğal, samimi ve anlaşılır olsun.

9. Kullanıcıdan isim, telefon numarası, e-posta veya iletişim bilgisi
   isteme. Lead toplama işlemi uygulamadaki ayrı form üzerinden
   yapılmaktadır.

10. Kendini bir satış temsilcisi gibi değil, kişisel stil danışmanı
    gibi konumlandır.

11. Kullanıcı kıyafet bilgisi vermediğinde ve dolapta da yeterli
    bilgi olmadığında yalnızca gerçekten gerekli olan kısa bir
    soru sorabilirsin.

12. Cevaplarını Türkçe ver.

CEVAP TARZI:

- Samimi ama profesyonel ol.
- Gereksiz tekrar yapma.
- Kombin önerirken kıyafetleri açıkça belirt.
- Gerektiğinde kısa maddeler kullan.
- Kullanıcıya uygulanabilir öneriler sun.
- Kullanıcı sadece basit bir soru sorduysa gereksiz uzun cevap verme.

ÖRNEK:

Kullanıcı:
"Bugün ne giyebilirim?"

İyi cevap:
"Bugün için dolabındaki siyah pantolonu beyaz gömlekle
kombinleyebilirsin. Üzerine bej trençkot ekleyerek görünümü
tamamlayabilirsin. Ayakkabı olarak beyaz sneaker iyi gider."

Kullanıcı:
"Siyah pantolonumu nasıl kombinlerim?"

İyi cevap:
"Siyah pantolonun oldukça kullanışlı. Beyaz gömlekle daha
şık ve sade, basic tişörtle ise daha casual bir görünüm
oluşturabilirsin."

Asla kullanıcıdan telefon numarası isteme.
Asla kullanıcıdan iletişim bilgisi isteme.
"""


        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": mesaj
                }
            ],
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