import logging
from flask import Blueprint, render_template, request, jsonify, current_app

from app.database import (
    kiyafet_ekle,
    tum_kiyafetleri_getir,
    kiyafet_durum_guncelle,
    kombin_kaydet,
    lead_ekle,
    tum_leadleri_getir,
)
from app.services.ai_service import ai_service, AIServiceError

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')



@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"basari": True, "mesaj": "AI Wardrobe API aktif ve çalışıyor!"}), 200


@api_bp.route('/kiyafetler', methods=['POST'])
def kiyafet_ekle_route():
    data = request.get_json()
    if not data or not all(k in data for k in ('tur', 'kategori', 'renk', 'stil', 'mevsim')):
        return jsonify({"basari": False, "mesaj": "Eksik veri gönderildi!"}), 400

    try:
        yeni_id = kiyafet_ekle(
            data['tur'], data['kategori'], data['renk'],
            data['stil'], data['mevsim'], data.get('fotograf_url', '')
        )
        return jsonify({"basari": True, "mesaj": "Kıyafet başarıyla dolaba eklendi!", "id": yeni_id}), 201
    except Exception:
        logger.exception("Kiyafet eklenirken hata olustu")
        return jsonify({"basari": False, "mesaj": "Kıyafet eklenemedi, lütfen tekrar deneyin."}), 500


@api_bp.route('/kiyafetler', methods=['GET'])
def kiyafetleri_getir_route():
    try:
        sadece_aktif = request.args.get('aktif', 'false').lower() == 'true'
        kiyafetler = tum_kiyafetleri_getir(sadece_aktif=sadece_aktif)
        return jsonify({"basari": True, "veri": kiyafetler}), 200
    except Exception:
        logger.exception("Kiyafetler getirilirken hata olustu")
        return jsonify({"basari": False, "mesaj": "Kıyafetler alınamadı."}), 500


@api_bp.route('/kiyafetler/<int:kiyafet_id>/durum', methods=['PUT'])
def durum_guncelle_route(kiyafet_id):
    data = request.get_json()
    yeni_durum = data.get('durum') if data else None
    if yeni_durum not in ['aktif', 'kirli']:
        return jsonify({"basari": False, "mesaj": "Geçersiz durum!"}), 400

    try:
        kiyafet_durum_guncelle(kiyafet_id, yeni_durum)
        return jsonify({"basari": True, "mesaj": f"Kıyafet durumu {yeni_durum} olarak güncellendi."}), 200
    except Exception:
        logger.exception("Durum guncellenirken hata olustu")
        return jsonify({"basari": False, "mesaj": "Durum güncellenemedi."}), 500


@api_bp.route('/sohbet', methods=['POST'])
def ai_sohbet_route():
    data = request.get_json()
    mesaj = data.get('mesaj', '') if data else ''
    if not mesaj:
        return jsonify({"basari": False, "mesaj": "Mesaj boş olamaz!"}), 400

    try:
        # Sadece dolapta aktif (kirli olmayan) kıyafetleri AI'a bağlam olarak ver
        aktif_dolap = tum_kiyafetleri_getir(sadece_aktif=True)
        dolap_ozeti = ", ".join([f"{k['tur']} ({k['renk']}, {k['stil']})" for k in aktif_dolap])

        yanit = ai_service.yanit_uret(mesaj, dolap_ozeti)
        return jsonify({"basari": True, "cevap": yanit}), 200
    except AIServiceError as e:
        logger.warning("AI servis hatasi: %s", str(e))
        return jsonify({"basari": False, "mesaj": "Şu anda yanıt veremiyorum, lütfen daha sonra tekrar deneyin."}), 503
    except Exception:
        logger.exception("Sohbet route'unda beklenmeyen hata")
        return jsonify({"basari": False, "mesaj": "Bir şeyler ters gitti."}), 500


@api_bp.route('/leads', methods=['POST'])
def lead_ekle_route():
    data = request.get_json()
    if not data or not all(k in data for k in ('isim', 'telefon')):
        return jsonify({"basari": False, "mesaj": "İsim ve telefon alanları zorunludur!"}), 400

    try:
        yeni_id = lead_ekle(data['isim'], data['telefon'], data.get('mesaj', ''))
        return jsonify({"basari": True, "mesaj": "Lead başarıyla kaydedildi!", "id": yeni_id}), 201
    except Exception:
        logger.exception("Lead eklenirken hata olustu")
        return jsonify({"basari": False, "mesaj": "Kayıt yapılamadı, lütfen tekrar deneyin."}), 500


@api_bp.route('/leads', methods=['GET'])
def leads_getir_route():
    try:
        leadler = tum_leadleri_getir()
        return jsonify({"basari": True, "veri": leadler}), 200
    except Exception:
        logger.exception("Leadler getirilirken hata olustu")
        return jsonify({"basari": False, "mesaj": "Lead listesi alınamadı."}), 500
    try:
        leadler = tum_leadleri_getir()
        return jsonify({"basari": True, "veri": leadler}), 200
    except Exception:
        logger.exception("Leadler getirilirken hata olustu")
        return jsonify({"basari": False, "mesaj": "Lead listesi alınamadı."}), 500