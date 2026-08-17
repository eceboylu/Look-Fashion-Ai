import logging
import secrets

from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app,
)

from app.database import (
    lead_ekle,
    tum_leadleri_getir,
)

from app.services.ai_service import (
    ai_service,
    AIServiceError,
)


logger = logging.getLogger(__name__)


# =========================
# BLUEPRINTLER
# =========================

main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")


# =========================
# GÜVENLİK YARDIMCILARI
# =========================

def admin_gerekli(fonksiyon):
    """Yönetim uçlarını ADMIN_API_KEY ile korur.

    İstemci anahtarı 'X-Admin-Key' başlığında gönderir.
    Bu koruma olmadan /api/leads GET ucu, adresi bilen herkese
    müşteri isim ve telefonlarını veriyordu.
    """

    @wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):

        beklenen = current_app.config.get("ADMIN_API_KEY")

        # Anahtar tanımlı değilse ucu AÇIK BIRAKMA.
        # Aksi halde .env'i eksik bir sunucuda koruma sessizce devre dışı kalır.
        if not beklenen:

            logger.error(
                "ADMIN_API_KEY tanımlı değil; yönetim ucu kapatıldı."
            )

            return jsonify({
                "basari": False,
                "mesaj": "Yönetim ucu yapılandırılmamış."
            }), 503

        gonderilen = request.headers.get("X-Admin-Key", "")

        # compare_digest: sabit süreli karşılaştırma, zamanlama saldırısını önler.
        if not secrets.compare_digest(gonderilen, beklenen):

            logger.warning(
                "Yetkisiz lead erişimi denemesi: %s",
                request.remote_addr
            )

            return jsonify({
                "basari": False,
                "mesaj": "Yetkisiz erişim."
            }), 401

        return fonksiyon(*args, **kwargs)

    return sarmalayici


# Sohbet geçmişi sınırları.
# Geçmiş tarayıcıdan geldiği için GÜVENİLMEZ veridir ve doğrudan
# modele gönderilirse "system" rolü enjekte edilip satış promptu ezilebilir.
GECMIS_MAX_MESAJ = 10        # son 5 soru-cevap turu
GECMIS_MAX_KARAKTER = 1000   # tek mesaj başına
MESAJ_MAX_KARAKTER = 2000    # kullanıcının yeni mesajı


def gecmisi_dogrula(gecmis):
    """İstemciden gelen sohbet geçmişini temizler ve sınırlar.

    Sadece 'user' ve 'assistant' rollerine izin verilir; 'system' rolü
    ve bozuk kayıtlar atılır.
    """

    if not isinstance(gecmis, list):
        return []

    temiz = []

    # Sadece son N mesaj: hem token maliyeti hem de istek boyutu kontrol altında.
    for kayit in gecmis[-GECMIS_MAX_MESAJ:]:

        if not isinstance(kayit, dict):
            continue

        rol = kayit.get("role")
        icerik = kayit.get("content")

        if rol not in ("user", "assistant"):
            continue

        if not isinstance(icerik, str) or not icerik.strip():
            continue

        temiz.append({
            "role": rol,
            "content": icerik.strip()[:GECMIS_MAX_KARAKTER]
        })

    return temiz


# =========================
# SAYFALAR
# =========================

@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# =========================
# HEALTH CHECK
# =========================

@api_bp.route("/health", methods=["GET"])
def health_check():

    return jsonify({
        "basari": True,
        "mesaj": "Fashion Look AI API aktif ve çalışıyor!"
    }), 200


# =========================
# AI SOHBET
# =========================

@api_bp.route("/sohbet", methods=["POST"])
def ai_sohbet_route():

    # silent=True: bozuk JSON gelirse 500 yerine None döner.
    data = request.get_json(silent=True) or {}

    mesaj = data.get("mesaj", "")

    # Tip kontrolü: {"mesaj": 123} gibi bir gövde .strip() üzerinde
    # çöküp 500 veriyordu.
    if not isinstance(mesaj, str):
        mesaj = ""

    mesaj = mesaj.strip()[:MESAJ_MAX_KARAKTER]

    # Geçmiş modele gitmeden önce temizlenir (rol enjeksiyonuna karşı).
    gecmis = gecmisi_dogrula(data.get("gecmis", []))

    if not mesaj:

        return jsonify({
            "basari": False,
            "mesaj": "Mesaj boş olamaz!"
        }), 400

    try:

        # AI artık gardırop veya kıyafet verisi almıyor.
        # Sadece kullanıcının mesajı ve konuşma geçmişi gönderiliyor.
        yanit = ai_service.yanit_uret(
            mesaj,
            gecmis
        )

        return jsonify({
            "basari": True,
            "cevap": yanit
        }), 200

    except AIServiceError as e:

        logger.warning(
            "AI servis hatası: %s",
            str(e)
        )

        return jsonify({
            "basari": False,
            "mesaj": (
                "Şu anda yanıt veremiyorum. "
                "Lütfen biraz sonra tekrar deneyin."
            )
        }), 503

    except Exception:

        logger.exception(
            "Sohbet route'unda beklenmeyen hata"
        )

        return jsonify({
            "basari": False,
            "mesaj": "Bir şeyler ters gitti."
        }), 500


# =========================
# LEAD KAYDET
# =========================

@api_bp.route("/leads", methods=["POST"])
def lead_ekle_route():

    data = request.get_json()

    if not data:

        return jsonify({
            "basari": False,
            "mesaj": "Veri gönderilmedi!"
        }), 400

    isim = data.get("isim", "").strip()
    telefon = data.get("telefon", "").strip()
    mesaj = data.get("mesaj", "").strip()

    if not isim or not telefon:

        return jsonify({
            "basari": False,
            "mesaj": "İsim ve telefon alanları zorunludur!"
        }), 400

    try:

        yeni_id = lead_ekle(
            isim,
            telefon,
            mesaj
        )

        return jsonify({
            "basari": True,
            "mesaj": "Bilgileriniz başarıyla kaydedildi!",
            "id": yeni_id
        }), 201

    except Exception:

        logger.exception(
            "Lead eklenirken hata oluştu"
        )

        return jsonify({
            "basari": False,
            "mesaj": (
                "Bilgiler kaydedilemedi. "
                "Lütfen tekrar deneyin."
            )
        }), 500


# =========================
# LEADLERİ GETİR (YÖNETİM)
# =========================
# Müşteri isim/telefon bilgisi döndürdüğü için admin anahtarı zorunlu.

@api_bp.route("/leads", methods=["GET"])
@admin_gerekli
def leads_getir_route():

    try:

        leadler = tum_leadleri_getir()

        return jsonify({
            "basari": True,
            "veri": leadler
        }), 200

    except Exception:

        logger.exception(
            "Leadler getirilirken hata oluştu"
        )

        return jsonify({
            "basari": False,
            "mesaj": "Lead listesi alınamadı."
        }), 500