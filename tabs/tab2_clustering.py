import streamlit as st
import pandas as pd

# === Library Utama ===
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io
import base64

# === ReportLab untuk PDF ===
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def tab2_clustering(df):
        st.markdown('<h2 class="section-header">🔍 K-Means Clustering</h2>', unsafe_allow_html=True)
        
        # Persiapan data untuk clustering
        df['jumlah'] = pd.to_numeric(df['jumlah'], errors='coerce')
        df['kebutuhan'] = pd.to_numeric(df['kebutuhan'], errors='coerce')
        
        df_summary_cluster = df.groupby('item_barang').agg({
            'jumlah': 'mean',
            'kebutuhan': 'mean'
        }).reset_index()
        
        df_summary_cluster.columns = ['Barang', 'Rata-Rata Jumlah', 'Rata-Rata Kebutuhan']
        df_summary_cluster = df_summary_cluster.sort_values(by='Barang')
        
        X = df_summary_cluster[['Rata-Rata Jumlah', 'Rata-Rata Kebutuhan']].values
        
        # Pengaturan centroid
        st.markdown("### ⚙️ Pengaturan Centroid Awal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            centroid_option = st.radio("Pilih metode centroid:", ["Manual", "Random"])
        
        with col2:
            if st.button("🎲 Generate Random Centroid"):
                st.session_state.random_m1_x = np.random.uniform(X[:, 0].min(), X[:, 0].max())
                st.session_state.random_m1_y = np.random.uniform(X[:, 1].min(), X[:, 1].max())
                st.session_state.random_m2_x = np.random.uniform(X[:, 0].min(), X[:, 0].max())
                st.session_state.random_m2_y = np.random.uniform(X[:, 1].min(), X[:, 1].max())
        
        if centroid_option == "Manual":
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Centroid M1")
                m1_x = st.number_input("M1 - Rata-Rata Jumlah", value=112.058564231738, key="m1_x")
                m1_y = st.number_input("M1 - Rata-Rata Kebutuhan", value=103.372941700045, key="m1_y")
            
            with col2:
                st.markdown("#### Centroid M2")
                m2_x = st.number_input("M2 - Rata-Rata Jumlah", value=389.15220293725, key="m2_x")
                m2_y = st.number_input("M2 - Rata-Rata Kebutuhan", value=530.673533363189, key="m2_y")
            
            centroids = np.array([[m1_x, m1_y], [m2_x, m2_y]])
        
        else:  # Random
            if 'random_m1_x' in st.session_state:
                centroids = np.array([
                    [st.session_state.random_m1_x, st.session_state.random_m1_y],
                    [st.session_state.random_m2_x, st.session_state.random_m2_y]
                ])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Centroid M1 (Random)")
                    st.write(f"Rata-Rata Jumlah: {st.session_state.random_m1_x:.2f}")
                    st.write(f"Rata-Rata Kebutuhan: {st.session_state.random_m1_y:.2f}")
                
                with col2:
                    st.markdown("#### Centroid M2 (Random)")
                    st.write(f"Rata-Rata Jumlah: {st.session_state.random_m2_x:.2f}")
                    st.write(f"Rata-Rata Kebutuhan: {st.session_state.random_m2_y:.2f}")
            else:
                centroids = np.array([[75.9, 56.6], [323.8, 86.7]])
                st.info("Klik tombol 'Generate Random Centroid' untuk mendapatkan centroid random")
        
        # Jalankan K-Means
        if st.button("🚀 Jalankan K-Means Clustering"):
            # Proses clustering
            max_iter = 10
            evaluasi_list = []
            centroid_list = []
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(max_iter):
                status_text.text(f'Iterasi {i+1}/{max_iter}')
                progress_bar.progress((i+1)/max_iter)
                
                # Hitung jarak Euclidean
                distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
                labels = np.argmin(distances, axis=1)
                jarak_terdekat = np.min(distances, axis=1)
                
                # Simpan centroid lama
                old_centroids = centroids.copy()
                
                # Update centroid
                centroids = np.array([
                    X[labels == k].mean(axis=0) if np.any(labels == k) else old_centroids[k]
                    for k in range(2)
                ])
                
                # Hitung WCV dan BCV
                wcv = np.sum(jarak_terdekat ** 2)
                if i == 0:
                    bcv = np.linalg.norm(old_centroids[0] - old_centroids[1])
                else:
                    bcv = np.linalg.norm(centroids[0] - centroids[1])
                
                rasio = bcv / wcv if wcv != 0 else np.nan
                
                evaluasi_list.append({
                    'Iterasi': i + 1,
                    'WCV': round(wcv, 1),
                    'BCV': round(bcv, 1),
                    'Rasio BCV/WCV': float(f"{rasio:.8f}")
                })
                
                centroid_list.append(centroids.copy())
                
                # Cek konvergensi
                if np.allclose(centroids, old_centroids):
                    status_text.text(f'Konvergen pada iterasi ke-{i+1}')
                    break
            
            progress_bar.empty()
            status_text.empty()
            
            # Simpan hasil ke session state
            st.session_state.clustering_results = {
                'labels': labels,
                'centroids': centroids,
                'evaluasi_list': evaluasi_list,
                'df_summary_cluster': df_summary_cluster,
                'X': X
            }

            # Tambahkan label cluster ke df_summary (copy dari df_summary_cluster agar aman)
            df_summary = df_summary_cluster.copy()
            df_summary['Cluster'] = labels
            df_summary['Cluster_Label'] = df_summary['Cluster'].map({0: 'C1', 1: 'C2'})
            df_sorted = df_summary.sort_values(by=['Cluster_Label', 'Barang'])

            # Tampilkan DataFrame hasil clustering
            st.markdown('<h3 class="section-header">📄 DataFrame Hasil Cluster</h3>', unsafe_allow_html=True)
            st.dataframe(df_sorted[['Barang', 'Rata-Rata Jumlah', 'Rata-Rata Kebutuhan', 'Cluster_Label']], use_container_width=True)
            
            st.success("✅ Clustering selesai!")
        
        # Tampilkan hasil clustering jika sudah ada
        if 'clustering_results' in st.session_state:
            results = st.session_state.clustering_results
            labels = results['labels']
            centroids = results['centroids']
            evaluasi_list = results['evaluasi_list']
            df_summary_cluster = results['df_summary_cluster']
            X = results['X']
            
            # 1. Visualisasi Hasil Clustering
            st.markdown('<h3 class="section-header">📊 Visualisasi Hasil Clustering</h3>', unsafe_allow_html=True)
            
            cluster_colors = {0: 'green', 1: 'orange'}
            cluster_names = {0: 'Cluster C1', 1: 'Cluster C2'}
            
            fig, ax = plt.subplots(figsize=(10, 8))
            
            for c in [0, 1]:
                cluster_points = X[labels == c]
                ax.scatter(
                    cluster_points[:, 0], cluster_points[:, 1],
                    c=cluster_colors[c], label=cluster_names[c],
                    s=100, alpha=0.7, edgecolors='black', linewidth=1
                )
            
            ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=300, marker='X', 
                      label='Centroid', edgecolors='black', linewidth=2)
            
            ax.set_xlabel('Rata-Rata Jumlah (kg)', fontsize=12)
            ax.set_ylabel('Rata-Rata Kebutuhan (kg)', fontsize=12)
            ax.set_title('Hasil Akhir K-Means Clustering', fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # 2. Tabel Evaluasi
            st.markdown('<h3 class="section-header">📋 Tabel Evaluasi K-Means</h3>', unsafe_allow_html=True)

            df_evaluasi = pd.DataFrame(evaluasi_list)
            st.dataframe(df_evaluasi, use_container_width=True)

            # Penjelasan cara membaca hasil evaluasi
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("### 💡 Cara Membaca Evaluasi K-Means")
            st.write("""
            - **WCV (Within-Cluster Variation)**: Mengukur seberapa padat data dalam setiap cluster. Semakin kecil, semakin baik karena artinya data dalam cluster mirip satu sama lain.
            - **BCV (Between-Cluster Variation)**: Mengukur seberapa jauh antar pusat cluster. Semakin besar, semakin baik karena menunjukkan perbedaan antar cluster yang jelas.
            - **Rasio BCV/WCV**: Metrik evaluasi utama. Semakin besar rasio ini, semakin optimal jumlah cluster tersebut, karena cluster saling berbeda (BCV tinggi) dan padat (WCV rendah).

            """)
            st.markdown('</div>', unsafe_allow_html=True)

            # 3. Interpretasi Cluster
            st.markdown('<h3 class="section-header">🔍 Interpretasi Cluster</h3>', unsafe_allow_html=True)

            # Tambahkan label cluster ke dataframe summary
            df_summary_cluster['Cluster'] = labels
            df_summary_cluster['Cluster_Label'] = df_summary_cluster['Cluster'].map({0: 'C1', 1: 'C2'})
            df_sorted = df_summary_cluster.sort_values(by=['Cluster_Label', 'Barang'])

            # Hitung range tiap cluster
            cluster_range = df_summary_cluster.groupby('Cluster_Label')[['Rata-Rata Jumlah', 'Rata-Rata Kebutuhan']].agg(['min', 'max']).reset_index()
            cluster_range.columns = ['Cluster_Label', 'Jumlah_Min', 'Jumlah_Max', 'Kebutuhan_Min', 'Kebutuhan_Max']

            st.write("Range Nilai per Cluster (Minimum - Maksimum):")
            st.dataframe(cluster_range)

            # Interpretasi dalam teks
            for idx, row in cluster_range.iterrows():
                cluster = row['Cluster_Label']
                j_min, j_max = row['Jumlah_Min'], row['Jumlah_Max']
                k_min, k_max = row['Kebutuhan_Min'], row['Kebutuhan_Max']

                items_in_cluster = df_summary_cluster[df_summary_cluster['Cluster_Label'] == cluster]['Barang'].tolist()

                st.markdown(f"""
                **Karakteristik Cluster {cluster}:**
                - Rata-rata Jumlah: {j_min:.1f} s.d. {j_max:.1f} KG
                - Rata-rata Kebutuhan: {k_min:.1f} s.d. {k_max:.1f} KG
                - Jumlah Barang: {len(items_in_cluster)}
                - Daftar Barang: {', '.join(items_in_cluster)}
                """)

            # 4. Download CSV hasil clustering
            csv = df_sorted[['Barang', 'Rata-Rata Jumlah', 'Rata-Rata Kebutuhan', 'Cluster_Label']].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Hasil Clustering (CSV)",
                data=csv,
                file_name='hasil_kmeans.csv',
                mime='text/csv'
            )