import streamlit as st
import Orange
import pandas as pd
import pickle

st.title("🩺 Prediksi Risiko Diabetes (Model dari Orange)")
st.write("Masukkan data pasien untuk memprediksi apakah berisiko diabetes atau tidak.")

# ===== Load model hasil dari Orange =====
try:
    with open("model.pkcls", "rb") as f:
        model = pickle.load(f)
    st.success("✅ Model berhasil dimuat dari file 'model.pkcls'")
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.stop()

# ===== Input dari pengguna =====
age = st.number_input("Umur", 1, 120, 30)
bmi = st.number_input("BMI", 10.0, 70.0, 25.0)
glucose = st.number_input("Kadar Glukosa", 50, 300, 120)
blood_pressure = st.number_input("Tekanan Darah", 0, 200, 70)
insulin = st.number_input("Kadar Insulin", 0, 900, 80)
hba1c = st.number_input("HbA1c Level", 3.0, 20.0, 5.5)
hypertension = st.selectbox("Hipertensi", ["No", "Yes"])
heart_disease = st.selectbox("Penyakit Jantung", ["No", "Yes"])
smoking = st.selectbox("Riwayat Merokok", ["never", "former", "current"])
gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])

# ===== Buat DataFrame dari input =====
data_input = pd.DataFrame({
    'Age': [age],
    'BMI': [bmi],
    'Blood_Glucose_Level': [glucose],
    'BloodPressure': [blood_pressure],
    'Insulin': [insulin],
    'HbA1c_Level': [hba1c],
    'Hypertension': [hypertension],
    'Heart_Disease': [heart_disease],
    'Smoking_History': [smoking],
    'Gender': [gender]
})

# ===== Konversi ke format Orange =====
try:
    domain = model.domain

    # Ambil semua fitur dari domain (tanpa class variable)
    features = [var.name for var in domain.attributes]

    # Ambil nilai dari DataFrame sesuai urutan fitur domain
    row = [data_input.iloc[0].get(col, 0) for col in features]

    # Buat Table Orange dari satu baris data
    orange_data = Orange.data.Table(domain, [row])

except Exception as e:
    st.error(f"Gagal mengubah data ke format Orange: {e}")
    st.stop()

# ===== Prediksi =====
if st.button("Prediksi"):
    try:
        pred = model(orange_data)
        pred_value = str(pred[0])

        st.write("**Hasil mentah prediksi:**", pred_value)

        if pred_value.lower() in ["1", "yes", "true", "diabetes", "positive"]:
            st.error("⚠️ Pasien berisiko diabetes.")
        else:
            st.success("✅ Pasien tidak berisiko diabetes.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")
