import streamlit as st
import pandas as pd
import io
from pathlib import Path

# Import setiap tab analisis
from tabs.tab1_deskriptif import tab1_deskriptif
from tabs.tab2_clustering import tab2_clustering
from tabs.tab3_laporan import tab3_laporan

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Pengelompokan Barang Pasar Kabupaten Sumedang",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header utama
st.markdown('<h2 style="text-align:center">📊 Dashboard Pengelompokan Barang Pasar Kabupaten Sumedang</h2>', unsafe_allow_html=True)

# =============================
# ✅ Sidebar: Upload dan Download
# =============================
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload file CSV", type=['csv'])

# Path ke file contoh asli (untuk di-download)
contoh_path = Path("contoh_dataset.csv")  # Pastikan file ini ada di root folder

if contoh_path.exists():
    st.sidebar.markdown("### 📥 Download Contoh Dataset")
    with open(contoh_path, "rb") as f:
        st.sidebar.download_button(
            label="Download Contoh CSV",
            data=f,
            file_name="contoh_dataset.csv",
            mime="text/csv"
        )
else:
    st.sidebar.warning("⚠ File contoh dataset tidak ditemukan")

# =============================
# ✅ Tab Layout
# =============================
if uploaded_file:
    # Jika ada file yang diupload
    df = pd.read_csv(uploaded_file)
    df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')
    df = df[df['satuan_item'].str.lower() == 'kg']

    tab_home, tab1, tab2, tab3 = st.tabs(["🏠 Beranda", "📈 Analisis Deskriptif", "🔍 K-Means Clustering", "📄 Laporan"])
else:
    # Jika belum upload, hanya tampilkan Beranda
    tab_home = st.tabs(["🏠 Beranda"])[0]

# =============================
# ✅ Konten Tab Beranda
# =============================
with tab_home:
    st.markdown("### 📌 Contoh Dataset")
    contoh_data = {
        "tanggal": ["2024-01-01"] * 5,
        "nama_pasar": ["Pasar Buahdua"] * 5,
        "item_barang": [
            "Beras Medium", "Gula Pasir", "Daging Ayam Ras", "Telur Ayam Ras",
            "Cabe Merah Keriting"
        ],
        "jumlah": [30, 100, 300, 40, 10],
        "kebutuhan": [20, 55, 260, 30, 5],
        "satuan_item": ["kg"] * 5
    }
    contoh_df_static = pd.DataFrame(contoh_data)
    st.dataframe(contoh_df_static, use_container_width=True)

    # ✅ Catatan adaptif (dark mode friendly)
    st.info("""
    **ℹ️ Catatan:**  
    Anda dapat mengunggah data sendiri asalkan memiliki kolom berikut:
    - `tanggal` (format tanggal, contoh: 2024-01-01)
    - `nama_pasar` (nama pasar)
    - `item_barang` (nama barang)
    - `jumlah` (jumlah stok barang)
    - `kebutuhan` (jumlah kebutuhan barang)
    - `satuan_item` (misal: kg)

    Pastikan nama kolom sesuai agar analisis berjalan dengan baik.
    """)

# =============================
# ✅ Konten Tab Lain (jika file diupload)
# =============================
if uploaded_file:
    with tab1:
        tab1_deskriptif(df)

    with tab2:
        tab2_clustering(df)

    with tab3:
        tab3_laporan(df)
