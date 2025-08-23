from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Definisikan struktur input data yang akan dikirim Laravel
class PredictionInput(BaseModel):
    jenis_bibit: str
    catatan_cuaca: str

# Muat model dan kolom yang sudah disimpan
model = joblib.load('harvest_model.pkl')
model_columns = joblib.load('model_columns.pkl')

@app.post("/predict")
def predict_harvest(data: PredictionInput):
    # Buat DataFrame dari input
    input_df = pd.DataFrame([data.dict()])

    # Lakukan One-Hot Encoding sama persis seperti saat training
    input_encoded = pd.get_dummies(input_df)

    # Samakan kolom input dengan kolom saat training
    # Ini untuk mengatasi jika ada kategori yang tidak ada di input
    input_processed = input_encoded.reindex(columns=model_columns, fill_value=0)

    # Lakukan prediksi
    prediction = model.predict(input_processed)
    
    # Ambil hasil prediksi (durasi dalam hari)
    predicted_duration = int(prediction[0])

    # Kembalikan hasil dalam format JSON
    return {"predicted_duration_days": predicted_duration}