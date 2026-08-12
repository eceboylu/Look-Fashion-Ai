Fashion Look Ai — Akıllı Gardırop ve Kişisel Stil Asistanı

Fashion Look Ai, kullanıcıların yapay zekâ ile konuşup kişiye özel stil ve kombin önerileri almasını sağlayan bir stil asistanıdır.

##  Proje Bağlantıları

* Canlı Backend (Render): https://look-fashion-ai.onrender.com
* Wix Canlı Arayüz: https://eceboylu.wixstudio.com/fashion-look-ai

## Proje Özellikleri

*  Yapay zekâ destekli stil asistanı
*  Kişiselleştirilmiş kombin önerileri
*  Renk ve stil uyumu önerileri
*  Mevsim ve hava koşullarına göre kombin önerileri
*  Türkçe doğal dil ile AI sohbeti
*  İletişim formu
*  Yönetim paneli
*  Wix Studio ve Wix Velo entegrasyonu
*  Render üzerinde canlı backend
*  Güvenli API anahtarı yönetimi

## Proje Mimarisi

Proje, **Separation of Concerns** prensibine göre tasarlandı.

```text
AI-Wardrobe/
│
├── run.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
└── app/
├── __init__.py
├── database.py
├── routes.py
│
├── services/
│ ├── __init__.py
│ └── ai_service.py
│
└── templates/
├── index.html
└── dashboard.html
```

### Katmanlar

**config.py**

Uygulamanın ayarlarını ve ortam değişkenlerini yönetir.

**database.py**

Veritabanı işlemlerini yönetir.

**ai_service.py**

Yapay zekâ API bağlantısını yönetir.

**routes.py**

HTTP isteklerini alır ve ilgili katmanları çağırır.

**app/**init**.py**

Flask, uygulama fabrikası yapısını kurar.

**run.py**

Uygulamanın başlangıç noktasıdır.

## Yapay Zekâ Asistanı

AI Wardrobe'un temel özelliği, yapay zekâ destekli stil danışmanıdır.

Kullanıcı örneğin:

> "Bugün ne giysem?"

veya

"Siyah pantolonumu nasıl kombinleyebilirim?"

gibi sorular sorabilir.

Asistan, renk, stil, mevsim, kullanım amacı ve mevcut bilgilere göre Türkçe ve uygulanabilir kombin önerileri sunar.

Yapay zekâ hizmetinde **Groq API** kullanılır.

Kullanılan model:

```text
llama-3.1-8b-instant
```

AI davranışı, `BUSINESS_CONTEXT` üzerinden tanımlandı.
### Kullanıcı Akışı

```text
Kullanıcı
↓
Wix Studio
↓
AI mesajı
↓
Wix Velo
↓
Flask API
↓
AI Service
↓
Groq API
↓
AI cevabı
↓
Wix Studio
↓
Kullanıcı
```

Kullanıcı, istediği zaman stil asistanına sorular sorabilir. AI tarafından oluşturulan yanıtları doğrudan arayüzde görebilir.

##  İletişim Formu

Daha fazla destek almak isteyen kullanıcı, iletişim formunu doldurarak:

* İsim
* Telefon
* Mesaj

bilgilerini bırakabilir. Bu bilgiler backend'e gönderilir ve kaydedilir.

##  Yönetim Paneli

You can view incoming contact records in the project's management panel. In the panel:

* İsim
* Telefon
* Mesaj
* Tarih

Bilgiler listelenir. Lead kayıtları, Wix Repeater ile yönetim panelinde gösterilir.

##  Wix Studio Entegrasyonu

Frontend tarafında **Wix Studio + Wix Velo** kullanıldı. Wix, backend ile bağlantı kurar ve:

* AI sohbet isteklerini
* AI cevaplarını
* İletişim formu gönderimlerini
* Yönetim panelindeki kayıtları

yönetmektedir.

## 🔌 Backend API

### Health Check

```text
GET /api/health
```

Backend'in çalışıp çalışmadığını kontrol eder.

### AI Sohbet

```text
POST /api/sohbet
```

Kullanıcının mesajını AI servisine yollar.

### Lead Kaydetme

```text
POST /api/leads
```

İletişim formundan gelen kullanıcı bilgilerini kaydeder.

### Lead Listeleme

```text
GET /api/leads
```

Kayıtlı iletişim bilgilerini yönetim paneline yollar.

##  Güvenlik

* API anahtarları `.env` dosyası ile yönetiliyor.
* `.env` dosyası GitHub'a yüklenmez.
* SQL sorgularında parametreli sorgular kullanılır.
* API ve veritabanı hataları `try-except` ile kontrol ediliyor.
