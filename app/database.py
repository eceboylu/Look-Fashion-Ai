import sqlite3
from flask import g, current_app


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE_URL'])
        db.row_factory = sqlite3.Row  # Sütun adlarıyla erişim sağlar
    return db


def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clothes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tur TEXT NOT NULL,
                kategori TEXT NOT NULL,
                renk TEXT NOT NULL,
                stil TEXT NOT NULL,
                mevsim TEXT NOT NULL,
                durum TEXT DEFAULT 'aktif',
                fotograf_url TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outfits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                etkinlik TEXT,
                kombin_detayi TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                favori INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

    # DB bağlantısını her istek sonunda kapat (artık burada, routes.py'de değil)
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()


def kiyafet_ekle(tur, kategori, renk, stil, mevsim, fotograf_url=''):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO clothes (tur, kategori, renk, stil, mevsim, fotograf_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tur, kategori, renk, stil, mevsim, fotograf_url))
    db.commit()
    return cursor.lastrowid


def tum_kiyafetleri_getir(sadece_aktif=False):
    db = get_db()
    cursor = db.cursor()
    if sadece_aktif:
        cursor.execute("SELECT * FROM clothes WHERE durum = 'aktif'")
    else:
        cursor.execute("SELECT * FROM clothes ORDER BY id DESC")
    return [dict(row) for row in cursor.fetchall()]


def kiyafet_durum_guncelle(kiyafet_id, yeni_durum):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE clothes SET durum = ? WHERE id = ?", (yeni_durum, kiyafet_id))
    db.commit()


def kombin_kaydet(etkinlik, kombin_detayi, favori=0):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO outfits (etkinlik, kombin_detayi, favori)
        VALUES (?, ?, ?)
    ''', (etkinlik, kombin_detayi, favori))
    db.commit()
    return cursor.lastrowid


def lead_ekle(isim, telefon, mesaj):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
    ''', (isim, telefon, mesaj))
    db.commit()
    return cursor.lastrowid


def tum_leadleri_getir():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY id DESC")
    rows = cursor.fetchall()

    lead_listesi = []
    for row in rows:
        d = dict(row)
        d['_id'] = str(d['id'])  # Wix Repeater için zorunlu
        lead_listesi.append(d)
    return lead_listesi