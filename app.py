import streamlit as st
import pandas as pd
import io
from pathlib import Path

# Import setiap tab
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
# ✅ Contoh tabel statis
# =============================
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

st.markdown("### 📌 Contoh Dataset")
st.dataframe(contoh_df_static, use_container_width=True)

# ✅ Catatan adaptif (pakai st.info agar mendukung dark mode)
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
# ✅ Sidebar: Upload dan Download
# =============================
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload file CSV", type=['csv'])

# Path ke file contoh asli (untuk di-download)
contoh_path = Path("contoh_dataset.csv")  # Ubah sesuai lokasi file Anda

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
# ✅ Jika file diupload, tampilkan tab analisis
# =============================
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')
    df = df[df['satuan_item'].str.lower() == 'kg']

    tab1, tab2, tab3 = st.tabs(["📈 Analisis Deskriptif", "🔍 K-Means Clustering", "📄 Laporan"])

    with tab1:
        tab1_deskriptif(df)

    with tab2:
        tab2_clustering(df)

    with tab3:
        tab3_laporan(df)
