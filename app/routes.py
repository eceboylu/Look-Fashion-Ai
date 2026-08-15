import logging

from flask import Blueprint, render_template, request, jsonify

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

    data = request.get_json()

    mesaj = data.get("mesaj", "") if data else ""
    gecmis = data.get("gecmis", []) if data else []

    mesaj = mesaj.strip()

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
# LEADLERİ GETİR
# =========================

@api_bp.route("/leads", methods=["GET"])
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