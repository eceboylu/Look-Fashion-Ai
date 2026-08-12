import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'wardrobe.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',') if os.environ.get('CORS_ORIGINS') else []

    ADMIN_API_KEY = os.environ.get('ADMIN_API_KEY')

    BUSINESS_CONTEXT = """
    Sen AI Wardrobe kişisel stil asistanısın. Kullanıcılara dijital gardırop,
    kombin önerileri, kıyafet analizi, hava durumu ve etkinlik bazlı stil
    önerileri konusunda yardımcı ol. Sorularını Türkçe, kibar ve profesyonel
    bir şekilde yanıtla. Kullanıcı ilgisini belirttiğinde, ona daha detaylı
    bilgi ve destek sunabilmek için adını ve telefon numarasını paylaşmaya yönlendir.
    """


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}