import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, db

# Inisialisasi Firebase (gunakan file JSON kredensial Anda)
if not firebase_admin._apps:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://parking-detection-34614-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Fungsi untuk mendapatkan data dari Firebase
def get_parking_data():
    ref = db.reference('parking')
    return ref.get()

st.title("Status Parkir")

# Placeholder untuk menampilkan data secara real-time
placeholder = st.empty()

# Loop untuk memperbarui data secara real-time
while True:
    # Ambil data terbaru dari Firebase
    data = get_parking_data()

    # Perbarui placeholder dengan data baru
    with placeholder.container():
        if data:
            st.metric("Jumlah Slot Kosong", data['num_free_slots'])
            st.metric("Jumlah Slot Terisi", data['num_occupied_slots'])
            if data['num_free_slots'] == 0:
                st.warning("Parkir Penuh!")
            else:
                st.success("Slot tersedia.")
        else:
            st.warning("Data parkir belum tersedia.")

    # Tunggu 5 detik sebelum mengambil data lagi
    time.sleep(5)
