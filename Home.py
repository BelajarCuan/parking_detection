import streamlit as st

# Set konfigurasi halaman di awal
st.set_page_config(page_title="Sistem Deteksi Slot Parkir", layout="wide")

# Fungsi untuk berpindah halaman
def navigate_page(page):
    st.session_state['current_page'] = page

# Inisialisasi halaman aktif jika belum ada
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'

# Sidebar navigasi untuk Admin dan User
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ("Home", "Admin", "User"))

# Simpan pilihan halaman di session_state
if page == "Admin":
    navigate_page("Admin")
elif page == "User":
    navigate_page("User")

# Tampilkan halaman berdasarkan pilihan tanpa reload paksa
if st.session_state['current_page'] == "Home":
    st.title("Selamat Datang di Sistem Deteksi Slot Parkir")
    st.write("Pilih halaman dari sidebar untuk melanjutkan.")
elif st.session_state['current_page'] == "Admin":
    st.title("Halaman Admin")
    # Anda bisa memuat isi dari Admin.py di sini atau menggunakan streamlit page-multipage system
    exec(open("Admin.py").read())
elif st.session_state['current_page'] == "User":
    st.title("Halaman User")
    # Anda bisa memuat isi dari User.py di sini atau menggunakan streamlit page-multipage system
    exec(open("User.py").read())
