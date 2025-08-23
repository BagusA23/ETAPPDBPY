import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# 1. Baca Data
data = pd.read_csv('data_panen.csv')

# 2. Feature Engineering (mengubah data jadi angka yang dimengerti model)
# Ubah kolom tanggal menjadi tipe datetime
data['Tanggal Tanam'] = pd.to_datetime(data['Tanggal Tanam'])
data['Tanggal Panen Aktual'] = pd.to_datetime(data['Tanggal Panen Aktual'])

# Buat target prediksi: Durasi Panen dalam Hari
data['durasi_panen_hari'] = (data['Tanggal Panen Aktual'] - data['Tanggal Tanam']).dt.days

# Ubah data kategori (teks) menjadi angka dengan One-Hot Encoding
data = pd.get_dummies(data, columns=['Jenis Bibit', 'Catatan Cuaca'], drop_first=True)

# 3. Pisahkan Fitur (X) dan Target (y)
# Hapus kolom yang tidak relevan/sudah diolah
features = data.drop(columns=['Tanggal Tanam', 'Tanggal Panen Aktual', 'durasi_panen_hari'])
target = data['durasi_panen_hari']

# Simpan nama kolom fitur, ini PENTING untuk tahap prediksi nanti
model_columns = features.columns
joblib.dump(model_columns, 'model_columns.pkl')

# 4. Latih Model
# RandomForest adalah model yang bagus dan serbaguna
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(features, target)

print("Model berhasil dilatih!")

# 5. Simpan model yang sudah dilatih ke file
joblib.dump(model, 'harvest_model.pkl')
print("Model berhasil disimpan ke harvest_model.pkl!")