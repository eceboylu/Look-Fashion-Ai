import sqlite3

from flask import g, current_app


def get_db():
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = sqlite3.connect(
            current_app.config["DATABASE_URL"]
        )

        db.row_factory = sqlite3.Row

    return db


def init_db(app):

    with app.app_context():

        db = get_db()
        cursor = db.cursor()

        # =========================
        # LEADS
        # =========================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()

    # Her istek sonunda database bağlantısını kapat.
    @app.teardown_appcontext
    def close_connection(exception):

        db = getattr(g, "_database", None)

        if db is not None:
            db.close()


# =========================
# LEAD EKLE
# =========================

def lead_ekle(isim, telefon, mesaj=""):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO leads (
            isim,
            telefon,
            mesaj
        )
        VALUES (?, ?, ?)
    """, (
        isim,
        telefon,
        mesaj
    ))

    db.commit()

    return cursor.lastrowid


# =========================
# TÜM LEADLERİ GETİR
# =========================

def tum_leadleri_getir():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM leads
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    lead_listesi = []

    for row in rows:

        d = dict(row)

        # Wix / dashboard tarafında kullanılabilecek ID
        d["_id"] = str(d["id"])

        lead_listesi.append(d)

    return lead_listesi