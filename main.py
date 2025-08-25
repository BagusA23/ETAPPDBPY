import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import traceback

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Harvest Prediction API",
    description="API untuk memprediksi durasi panen.",
    version="1.0.0"
)

# --- Memuat Model dan Kolom ---
# Model dan kolom dimuat sekali saat startup untuk efisiensi
try:
    model = joblib.load('harvest_model.pkl')
    model_columns = joblib.load('model_columns.pkl')
    print("Model and columns loaded successfully.")
except FileNotFoundError:
    print("Error: Model or column files not found. Make sure 'harvest_model.pkl' and 'model_columns.pkl' exist.")
    model = None
    model_columns = None

# --- Struktur Data Input ---
# Definisikan struktur input data yang akan diterima oleh API
class PredictionInput(BaseModel):
    jenis_bibit: str
    catatan_cuaca: str

# --- Endpoint Aplikasi ---
@app.get("/")
def read_root():
    """Endpoint root untuk mengecek apakah API berjalan."""
    return {"status": "API is running", "message": "Welcome to the Harvest Prediction API!"}

@app.post("/predict")
def predict_harvest(data: PredictionInput):
    """
    Endpoint untuk melakukan prediksi durasi panen.
    Menerima data jenis bibit dan catatan cuaca, lalu mengembalikan prediksi durasi dalam hari.
    """
    if not model or not model_columns:
        # Gunakan HTTPException untuk error yang terkontrol
        raise HTTPException(status_code=503, detail="Model is not loaded, service unavailable.")

    try:
        # Buat DataFrame dari input
        input_df = pd.DataFrame([data.dict()])
        
        # Lakukan One-Hot Encoding sama persis seperti saat training
        input_encoded = pd.get_dummies(input_df)

        # Samakan kolom input dengan kolom saat training
        # Ini penting untuk mengatasi jika ada kategori yang tidak ada di input baru
        input_processed = input_encoded.reindex(columns=model_columns, fill_value=0)

        # Lakukan prediksi
        prediction = model.predict(input_processed)
        
        # Ambil hasil prediksi (durasi dalam hari)
        predicted_duration = int(prediction[0])

        # Kembalikan hasil dalam format JSON
        return {"predicted_duration_days": predicted_duration}
        
    except Exception as e:
        # Tangkap semua jenis error yang mungkin terjadi selama proses prediksi
        print(f"An error occurred during prediction: {e}")
        # Cetak traceback untuk debugging mendalam di log Railway
        traceback.print_exc()
        # Kembalikan response error 500 yang informatif
        return JSONResponse(
            status_code=500,
            content={"error": "An internal error occurred.", "detail": str(e)}
        )


# --- Menjalankan Server ---
# Bagian ini PENTING untuk deployment di Railway
if __name__ == "__main__":
    # Railway akan memberikan port melalui environment variable 'PORT'
    port = int(os.environ.get("PORT", 8080))
    
    # Menjalankan server Uvicorn
    # host="0.0.0.0" berarti server akan menerima koneksi dari mana saja (bukan hanya dari localhost)
    uvicorn.run(app, host="0.0.0.0", port=port)
