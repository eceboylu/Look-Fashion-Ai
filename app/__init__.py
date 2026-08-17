import logging

from flask import Flask
from flask_cors import CORS

from config import config_dict, ProductionConfig
from app.database import init_db


def create_app(config_name='default'):
    """Flask uygulamasını oluşturur ve yapılandırır.

    NOT: Bu dosyada daha önce create_app İKİ KEZ tanımlıydı. Python ikinci
    tanımı geçerli saydığı için ilk tanımdaki logging.basicConfig hiç
    çalışmıyordu ve loglar formatsız kalıyordu. İki tanım burada birleştirildi.
    """

    # Log ayarı: uygulama ayağa kalkarken bir kez yapılır.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    app = Flask(__name__)

    # Bilinmeyen bir isim gelirse KeyError yerine 'default' kullanılır.
    config_class = config_dict.get(config_name, config_dict['default'])

    app.config.from_object(config_class)

    # Canlı ortamda eksik/riskli ayarlarla açılmayı engelle
    # (dev SECRET_KEY, eksik GROQ_API_KEY, eksik ADMIN_API_KEY vb.).
    if issubclass(config_class, ProductionConfig):
        config_class.dogrula()

    # CORS: sadece config'de tanımlı origin'lere izin ver
    CORS(app, origins=app.config['CORS_ORIGINS'] or [])

    # Veritabanını başlat
    init_db(app)

    from app.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.route('/health')
    def health():
        return {"durum": "aktif", "proje": "Look Fashion AI"}, 200

    return app
