 Fashion Look Ai — Akıllı Gardırop ve Kişisel Stil Asistanı

Fashion Look Ai, kullanıcıların yapay zekâ ile etkileşimde bulunarak kişiselleştirilmiş stil ve kombin önerileri almasına olanak tanıyan bir stil asistanıdır.

##  Proje Bağlantıları

* Canlı Backend (Render): https://look-fashion-ai.onrender.com
* Wix Canlı Arayüz: https://eceboylu.wixstudio.com/fashion-look-ai

## ✨ Proje Özellikleri

* 🤖 Yapay zekâ destekli stil asistanı
* 👗 Kişiselleştirilmiş kombin önerileri
* 🎨 Renk ve stil uyumu önerileri
* 🌤️ Mevsim ve hava koşullarına göre kombin önerileri
* 💬 Türkçe doğal dil ile AI sohbeti
* 📋 İletişim formu
* 📊 Yönetim paneli
* 🔗 Wix Studio ve Wix Velo entegrasyonu
* 🚀 Render üzerinde canlı backend
* 🔐 Güvenli API anahtarı yönetimi

## 🏗️ Proje Mimarisi

Proje, **Separation of Concerns** prensibine göre tasarlanmıştır.

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

Yapay zekâ API bağlantısından sorumludur.

**routes.py**

HTTP isteklerini karşılar ve ilgili katmanları çağırır.

**app/**init**.py**

Flask uygulama fabrikası yapısını oluşturur.

**run.py**

Uygulamanın başlangıç noktasıdır.

## 🤖 Yapay Zekâ Asistanı

AI Wardrobe'un temel özelliği yapay zekâ destekli stil danışmanıdır.

Kullanıcı örneğin:

> "Bugün ne giysem?"

veya

> "Siyah pantolonumu nasıl kombinleyebilirim?"

gibi sorular sorabilir.

Asistan; renk, stil, mevsim, kullanım amacı ve mevcut bilgiler doğrultusunda Türkçe ve uygulanabilir kombin önerileri sunar.

Yapay zekâ servisinde **Groq API** kullanılmaktadır.

Kullanılan model:

```text
llama-3.1-8b-instant
```

AI davranışı `BUSINESS_CONTEXT` üzerinden tanımlanmıştır.
### 💬 Kullanıcı Akışı

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

Kullanıcı, istediği zaman stil asistanına sorular sorabilir ve AI tarafından oluşturulan yanıtları doğrudan arayüzde görebilir.

## 📋 İletişim Formu

Daha fazla destek almak isteyen kullanıcı, iletişim formunu doldurarak:

* İsim
* Telefon
* Mesaj

bilgilerini bırakabilir. Bu bilgiler, backend'e gönderilerek kaydedilir.

## 📊 Yönetim Paneli

Projenin yönetim panelinde gelen iletişim kayıtları görüntülenebilir. Panelde:

* İsim
* Telefon
* Mesaj
* Tarih

bilgileri listelenmektedir. Lead kayıtları, Wix Repeater kullanılarak yönetim panelinde gösterilmektedir.

## 🌐 Wix Studio Entegrasyonu

Frontend tarafında **Wix Studio + Wix Velo** kullanılmıştır. Wix, backend ile bağlantı kurarak:

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

Backend'in aktif olup olmadığını kontrol eder.

### AI Sohbet

```text
POST /api/sohbet
```

Kullanıcının mesajını AI servisine gönderir.

### Lead Kaydetme

```text
POST /api/leads
```

İletişim formundan gelen kullanıcı bilgilerini kaydeder.

### Lead Listeleme

```text
GET /api/leads
```

Kayıtlı iletişim bilgilerini yönetim paneline gönderir.

## 🔐 Güvenlik

* API anahtarları `.env` dosyası üzerinden yönetilmektedir.
* `.env` dosyası GitHub'a yüklenmemektedir.
* SQL sorgularında parametreli sorgular kullanılmaktadır.
* API ve veritabanı hataları `try-except` ile yönetilmektedir.
