import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "wardrobe.db"
    )

    GROQ_API_KEY = os.environ.get(
        "GROQ_API_KEY"
    )

    CORS_ORIGINS = (
        os.environ.get("CORS_ORIGINS", "").split(",")
        if os.environ.get("CORS_ORIGINS")
        else []
    )

    ADMIN_API_KEY = os.environ.get(
        "ADMIN_API_KEY"
    )

    # =========================================================
    # BUSINESS CONTEXT
    # =========================================================

    BUSINESS_CONTEXT = """
Sen Fashion Look AI'ın kişisel stil asistanısın.

Fashion Look AI, kullanıcının kıyafetlerini dijital gardıroba
ekleyip yapay zeka ile kendi kıyafetlerinden kombin oluşturmasına
yardımcı olur.

KURALLAR:
- Her zaman Türkçe, kısa, samimi ve profesyonel cevap ver.
- Stil, kıyafet, kombin, renk, mevsim, etkinlik ve Fashion Look AI
  hakkında yardımcı ol.
- "Sen nesin?" sorusuna kendini tanıt ve ne işe yaradığını açıkla.
- "Ne giysem?", "Kombin yap" gibi sorularda fotoğraf veya kıyafet
  listesi isteme. Fashion Look AI'ın kullanıcının kendi dijital
  gardırobundan kombin oluşturabildiğini söyle.
- Kullanıcı uygulamayla ilgilenirse veya daha fazla bilgi isterse
  cevabın sonunda doğal şekilde iletişim formuna yönlendir.
- Chat içinde telefon, e-posta veya kişisel bilgi isteme.
- Her cevap sonunda mümkün olduğunda iletişim formunu öner;
  aynı cümleyi sürekli tekrarlama.
- Moda/Fashion Look AI ile ilgisiz sorularda:
  "Ben sadece stil asistanıyım, bu konuda yardımcı olamam.
  Ama stil ve kombin konusunda sana yardımcı olabilirim. ✨"
  de.
- Gereksiz özellik listeleri ve uzun açıklamalar yapma.
- Genellikle 2-4 cümleyle cevap ver.

ANA AMAÇ:
Kullanıcıya stil konusunda yardımcı ol, Fashion Look AI'ın
faydasını göster ve ilgilenirse iletişim formuna yönlendir.
"""


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}