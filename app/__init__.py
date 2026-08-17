from flask import Flask
from flask_cors import CORS
from config import config_dict
from app.database import init_db
import logging

def create_app(config_name='default'):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    app = Flask(__name__)
    ...
def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config_dict[config_name])

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