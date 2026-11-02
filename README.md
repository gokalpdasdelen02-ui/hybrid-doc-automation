# Yapay Zeka Destekli Hibrit Belge Ayrıştırma ve Muhasebe Otomasyon Sistemi

Bu proje, kurumsal işletmelerde kullanılan **e-Fatura, irsaliye ve banka dekontu** gibi farklı mizanpajlara sahip finansal belgelerden Optik Karakter Tanıma (OCR) ve Doğal Dil İşleme (NLP) yöntemleriyle yapılandırılmış veri çıkarımı yapan ve muhasebe sistemlerine entegre eden hibrit bir otomasyon sistemidir.

## Mühendislik Problemi ve Hedefler
* **Problem Tanımı:** Kısıtlı hesaplama ve bellek kaynaklarına sahip düşük güçlü yerel donanım altyapısında, yüksek doğruluk ve hızda finansal belge ayrıştırma.
* **Performans Hedefi:** Belge başına ortalama **≤ 1.5 saniye** işlem süresi.
* **Doğruluk Hedefi:** Temel fatura alanlarında (VKN, Tarih, Fatura No, KDV, Genel Toplam) **≥ %95** çıkarım doğruluğu.
* **İnsan Onayı Döngüsü (Human-in-the-Loop):** Güven skoru %95'in altında kalan belgelerin otomatik olarak manuel doğrulama arayüzüne yönlendirilmesi.

## Sistem Mimarisi ve Klasör Yapısı
* `backend/`: Python (FastAPI, SQLAlchemy, Pydantic) tabanlı REST API, hibrit belge yönlendirici (`router_poc.py`), dijital PDF ayrıştırıcı (`pdf_parser.py`) ve yerel OCR motoru (`ocr_engine.py`).
* `frontend/`: Belge yükleme ve düşük güven skorlu belgeler için kullanıcı doğrulama (Human-in-the-Loop) web arayüzü.
* `dataset/`: Sentetik ve anonimleştirilmiş test belgeleri ile doğrulama şablonları.
