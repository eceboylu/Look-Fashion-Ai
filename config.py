import os

from dotenv import load_dotenv


# .env dosyasındaki değişkenleri işletim sistemi ortamına yükler.
# Bu satır import anında çalışır, yani Config sınıfı okunmadan önce
# .env değerleri hazır olur.
load_dotenv()


# Bu dosyanın bulunduğu klasör = proje kök dizini.
# Göreli yolları (örn. "wardrobe.db") mutlak yola çevirmek için kullanılır.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Tüm ortamların (development / production) ortak ayarları."""

    # Flask'ın session ve cookie imzalaması için kullandığı anahtar.
    # Production'da MUTLAKA .env üzerinden verilmeli.
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    # SQLite veritabanının yolu.
    # DİKKAT: Burası bir "URL" değil, dosya yolu (sqlite3.connect'e gidiyor).
    # Göreli yol verilirse proje köküne göre mutlak yola çevriliyor; aksi halde
    # uygulama farklı bir klasörden çalıştırıldığında boş bir DB oluşuyordu.
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "wardrobe.db"
    )
    if not os.path.isabs(DATABASE_URL):
        DATABASE_URL = os.path.join(BASE_DIR, DATABASE_URL)

    # =========================================================
    # AI (GROQ) AYARLARI
    # =========================================================

    # Hangi sağlayıcının kullanıldığı (.env: AI_PROVIDER=groq).
    # İleride başka sağlayıcı eklenirse ai_service bu değere bakar.
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

    # Groq API anahtarı. Yoksa AIService anlamlı bir hata fırlatır.
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

    # Model ve endpoint artık koda gömülü değil; .env'den değiştirilebilir.
    #
    # DİKKAT: Önceki değer olan "llama-3.1-8b-instant" Groq hesabında artık
    # YOK (API 404 "model_not_found" dönüyordu) ve sohbet tamamen çalışmıyordu.
    # Groq zaman zaman model kaldırır; sohbet 503 vermeye başlarsa önce
    # https://api.groq.com/openai/v1/models listesinden geçerli model kontrol edilmeli.
    GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
    GROQ_API_URL = os.environ.get(
        "GROQ_API_URL",
        "https://api.groq.com/openai/v1/chat/completions"
    )

    # Yaratıcılık seviyesi. Satış danışmanında çok yüksek olmamalı,
    # yoksa fiyat/özellik uydurmaya başlar.
    AI_TEMPERATURE = float(os.environ.get("AI_TEMPERATURE", "0.6"))

    # API isteğinin saniye cinsinden zaman aşımı.
    AI_TIMEOUT = int(os.environ.get("AI_TIMEOUT", "15"))

    # Cevap uzunluğu sınırı.
    # gpt-oss modellerinde düşünme (reasoning) token'ları da bu limitten
    # düştüğü için düşük değerlerde cevap cümle ortasında kesiliyordu.
    AI_MAX_TOKENS = int(os.environ.get("AI_MAX_TOKENS", "700"))

    # gpt-oss modelleri için düşünme derinliği: low / medium / high.
    # "low" hem daha hızlı hem de token'ı düşünmeye değil cevaba harcıyor.
    # Bu parametreyi desteklemeyen bir modele geçilirse boş bırakılmalı.
    AI_REASONING_EFFORT = os.environ.get("AI_REASONING_EFFORT", "low")

    # =========================================================
    # GÜVENLİK
    # =========================================================

    # Tarayıcıdan API'ye erişebilecek domainler.
    # .env örneği:  CORS_ORIGINS=https://site.com,https://www.site.com
    # Boşluklar temizlenir ve boş elemanlar atılır; aksi halde
    # "a.com, b.com" yazımında ikinci origin " b.com" olarak okunup
    # hiçbir zaman eşleşmiyordu.
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.environ.get("CORS_ORIGINS", "").split(",")
        if origin.strip()
    ]

    # Lead listesini (/api/leads GET) korumak için kullanılacak anahtar.
    # NOT: Şu anda routes.py bu anahtarı kontrol ETMİYOR, yani lead
    # listesi herkese açık. Bu kontrol routes.py'ye eklenmeli.
    ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")

    # =========================================================
    # AI KİMLİĞİ / SATIŞ DAVRANIŞI (SYSTEM PROMPT)
    # =========================================================
    # Bu metin ai_service.py içinde "system" mesajı olarak gönderilir.
    # Yapay zekanın karakterini, sınırlarını ve satış akışını burası belirler.
    #
    # Önceki sürümdeki çelişki giderildi: "her şekilde forma yönlendir"
    # kuralı ile "aynı cümleyi tekrarlama" kuralı birbirini eziyordu ve
    # model her mesaja form linki yapıştırıp reklam gibi konuşuyordu.
    # Yeni akış: önce değer ver, ilgi sinyali gelince yönlendir.

    BUSINESS_CONTEXT = """
Sen Fashion Look AI'ın akıllı satış danışmanısın.

GÖREVİN:
Ziyaretçiye gerçekten işe yarar stil tavsiyesi vermek, ürünün faydasını
hissettirmek ve ilgilenen kişiyi sayfadaki iletişim formuna yönlendirerek
potansiyel müşteriye (lead) dönüştürmek.

ÜRÜN:
Fashion Look AI, kullanıcının kendi kıyafetlerini dijital gardıroba
eklemesini ve yapay zekanın bu kıyafetlerden etkinliğe, mevsime ve renk
uyumuna göre kombin önermesini sağlar.
Faydası: sabah "ne giysem?" derdini bitirir, dolaptaki kıyafetleri daha
çok kullandırır, gereksiz alışverişi azaltır.

ÜRÜN NASIL ÇALIŞIR (bunun dışında mekanizma UYDURMA):
Kullanıcı kıyafetlerini uygulamaya ekleyerek dijital gardırobunu oluşturur.
Yapay zeka bu gardıroptaki parçalar arasından kombin önerir.
Kıyafet ekleme uygulama içinde yapılır; bu sohbet ekranında yapılmaz.
Bu yüzden burada fotoğraf konusunu hiç açma, "fotoğrafsız çalışıyor" gibi
kafa karıştırıcı cümleler kurma.

SATIŞ AKIŞI (her cevapta bu sırayı takip et):
1. ANLA: Kullanıcının ihtiyacını kısaca anla. Gerekirse TEK bir kısa soru
   sor (örn. "Hangi etkinlik için?").
   Soru sorsan bile AYNI mesajda mutlaka bir öneri ver; sadece soru sorup bırakma.
2. DEĞER VER: Önce somut bir stil önerisi ver. Karşılığında bir şey
   vermeden satış yapma.
3. BAĞLA: Verdiğin öneriyi ürünün yaptığı işle ilişkilendir
   ("Bunu senin kendi dolabınla otomatik yapıyoruz").
4. YÖNLENDİR: İlgi sinyali varsa (nasıl çalışır, denemek isterim, fiyat,
   detay sorusu) forma doğal bir cümleyle davet et.

FORM KURALLARI:
- Formu her mesajda değil, ilgi sinyali gördüğünde öner.
- Yönlendirme cümlesini her seferinde farklı kur, ezber cümle tekrarlama.
- Chat içinde telefon, e-posta veya kişisel bilgi İSTEME.
  Bilgiler sadece sayfadaki forma girilir ("aşağıdaki formu doldurman yeterli").
- Kullanıcı bilgilerini bıraktığını söylerse tekrar isteme, teşekkür et.

SINIRLAR:
- Her zaman kullanıcının SON sorusuna cevap ver. Önceki turda verdiğin
  öneriyi tekrar anlatma; konu değiştiyse sen de değiştir.
- Chat'te fotoğraf veya kıyafet listesi isteme; görsel alamazsın.
- "Ne giysem?" sorusunda genel ama uygulanabilir bir öneri ver, sonra
  kendi gardırobuyla kişiselleştirdiğini anlat.
- Fiyat, kampanya, teslim süresi gibi emin olmadığın bilgileri UYDURMA;
  "ekibimiz form üzerinden netleştiriyor" de.
- Moda ve Fashion Look AI dışındaki konularda:
  "Ben Fashion Look AI'ın stil asistanıyım, bu konuda yardımcı olamam.
  Ama stil ve kombin konusunda sana yardımcı olabilirim. ✨"
- Israrcı olma, baskı kurma, abartılı reklam dili kullanma.

ÜSLUP:
- Türkçe, samimi, net; kullanıcıya "sen" diye hitap et.
- 2-4 cümle. Uzun özellik listesi ve madde madde açıklama yapma.
- DÜZ METİN yaz. Markdown kullanma: **kalın**, başlık, madde işareti YOK.
  (Arayüz metni düz gösteriyor, yıldızlar ekranda olduğu gibi görünür.)
- En fazla 1 emoji.
"""


class DevelopmentConfig(Config):
    """Yerel geliştirme: hata detayları görünür, otomatik reload açık."""

    DEBUG = True


class ProductionConfig(Config):
    """Canlı ortam: debug kapalı, kritik ayarlar zorunlu."""

    DEBUG = False

    @classmethod
    def dogrula(cls):
        """Canlıya çıkmadan önce eksik/riskli ayarları yakalar.

        create_app içinde production seçildiğinde çağrılmalı.
        """
        eksikler = []

        if cls.SECRET_KEY == "dev-secret-key-change-in-production":
            eksikler.append("SECRET_KEY (hâlâ geliştirme anahtarı)")

        if not cls.GROQ_API_KEY:
            eksikler.append("GROQ_API_KEY")

        if not cls.CORS_ORIGINS:
            eksikler.append("CORS_ORIGINS")

        if not cls.ADMIN_API_KEY:
            eksikler.append("ADMIN_API_KEY")

        if eksikler:
            raise RuntimeError(
                "Production için eksik ayarlar: " + ", ".join(eksikler)
            )


# create_app(config_name) bu sözlükten sınıfı seçer.
# run.py şu an 'development' değerini sabit geçiyor; canlıda
# 'production' geçilmeli.
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
