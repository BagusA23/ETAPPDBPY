# 🌾 API Prediksi Durasi Panen

API sederhana namun powerful yang dibangun dengan **FastAPI** untuk memprediksi estimasi durasi panen berdasarkan jenis bibit dan kondisi cuaca. Proyek ini membungkus **model machine learning** yang sudah dilatih ke dalam sebuah **REST API** yang siap digunakan.

---

## ✨ Fitur Utama

* 🔮 **Prediksi Real-time** – dapatkan estimasi durasi panen secara instan.
* ✅ **Validasi Input** – menggunakan **Pydantic** untuk memastikan data valid.
* ⚡ **Ringan & Cepat** – performa tinggi dengan FastAPI.
* 🚀 **Siap Deploy** – bisa langsung di-deploy ke Railway, Heroku, atau VPS.
* 📖 **Dokumentasi Otomatis** – Swagger UI & ReDoc bawaan FastAPI.

---

## 🚀 Alur Kerja API

```text
Client (Web/Mobile App)         FastAPI Server (Railway)
+-----------------------+       +-------------------------+
| {                     |       |                         |
|  "jenis_bibit": "A",  | ----> |  /predict Endpoint      |
|  "catatan_cuaca":"Cerah"|     |   1. Validasi Data      |
| }                     |       |   2. Preprocessing      |
+-----------------------+       |   3. Model.predict()    |
                                |                         |
+-----------------------+       +-------------------------+
| {                     |       |                         |
| "predicted_duration"| <---- |  Return JSON Response   |
| : 25                  |       |                         |
| }                     |       |                         |
+-----------------------+       +-------------------------+
```

---

## 🛠️ Teknologi yang Digunakan

* **Backend**: FastAPI, Uvicorn
* **Machine Learning**: scikit-learn, pandas
* **Data Handling**: Pydantic
* **Deployment**: Railway / Heroku / VPS

---

## ⚙️ Instalasi & Setup Lokal

1. **Clone repository**

   ```bash
   git clone https://github.com/BagusA23/ETAPPDBPY.git
   cd ETAPPDBPY
   ```

2. **Buat virtual environment**

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependensi**

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan server**

   ```bash
   uvicorn main:app --reload
   ```

👉 Server berjalan di: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔌 Dokumentasi API

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 Endpoint

### `POST /predict`

Kirim data JSON → API mengembalikan estimasi durasi panen.

**Contoh Request**

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "jenis_bibit": "Unggul",
    "catatan_cuaca": "Cerah Berawan"
  }'
```

**Contoh Response**

```json
{
  "predicted_duration_days": 30
}
```

---

## 📂 Struktur Proyek

```text
.
├── harvest_model.pkl       # File model machine learning
├── model_columns.pkl       # File kolom untuk preprocessing
├── main.py                 # Aplikasi FastAPI
├── Procfile                # Perintah deploy Railway/Heroku
├── requirements.txt        # Dependensi Python
└── README.md               # Dokumentasi proyek
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** – lihat file [LICENSE](./LICENSE).
