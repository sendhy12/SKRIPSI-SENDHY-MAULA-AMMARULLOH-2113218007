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

def tab1_deskriptif(df):
                        
                # --- Ringkasan Umum Data ---
                        st.markdown('<h2 class="section-header">📅 Ringkasan Dataset</h2>', unsafe_allow_html=True)

                        # Pastikan tanggal dalam format datetime
                        df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')

                        periode_awal = df['tanggal'].min().strftime('%d %B %Y')
                        periode_akhir = df['tanggal'].max().strftime('%d %B %Y')
                        total_data = len(df)
                        total_pasar = df['nama_pasar'].nunique()
                        total_barang = df['item_barang'].nunique()

                        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                        st.write(f"- **Periode Data**: {periode_awal} — {periode_akhir}")
                        st.write(f"- **Total Data**: {total_data:,} baris")
                        st.write(f"- **Total Pasar**: {total_pasar} pasar")
                        st.write(f"- **Total Barang**: {total_barang} jenis")
                        st.markdown('</div>', unsafe_allow_html=True)

                # Statistik Deskriptif
                        st.markdown('<h2 class="section-header">📊 Statistik Deskriptif</h2>', unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("### Kolom 'Jumlah'")
                            st.dataframe(df['jumlah'].describe())
                        
                        with col2:
                            st.markdown("### Kolom 'Kebutuhan'")
                            st.dataframe(df['kebutuhan'].describe())
                        
                        with col3:
                            st.markdown("### Kolom 'Item Barang'")
                            st.dataframe(df['item_barang'].describe())

                        # 1. Line Chart Rata-rata Jumlah dan Kebutuhan (Global)
                        st.markdown('<h2 class="section-header">📈 Tren Global</h2>', unsafe_allow_html=True)
                        
                        df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)

                        df_global = df.groupby('bulan').agg({
                            'jumlah': 'mean',
                            'kebutuhan': 'mean'
                        }).reset_index()
                        
                        df_global['bulan'] = pd.to_datetime(df_global['bulan'])
                        df_global = df_global.sort_values('bulan')
                        
                        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
                        
                        ax1.plot(df_global['bulan'], df_global['jumlah'], marker='o', color='blue', linewidth=2)
                        ax1.set_title('Rata-rata Jumlah per Bulan (Semua Pasar dan Barang)', fontsize=14, fontweight='bold')
                        ax1.set_ylabel('Jumlah (kg)')
                        ax1.grid(True, alpha=0.3)
                        ax1.tick_params(axis='x', rotation=45)
                        
                        ax2.plot(df_global['bulan'], df_global['kebutuhan'], marker='o', color='green', linewidth=2)
                        ax2.set_title('Rata-rata Kebutuhan per Bulan (Semua Pasar dan Barang)', fontsize=14, fontweight='bold')
                        ax2.set_xlabel('Bulan')
                        ax2.set_ylabel('Kebutuhan (kg)')
                        ax2.grid(True, alpha=0.3)
                        ax2.tick_params(axis='x', rotation=45)
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Insight untuk tren global
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown("### 💡 Insight: Tren Global")
                        
                        jumlah_trend = "meningkat" if df_global['jumlah'].iloc[-1] > df_global['jumlah'].iloc[0] else "menurun"
                        kebutuhan_trend = "meningkat" if df_global['kebutuhan'].iloc[-1] > df_global['kebutuhan'].iloc[0] else "menurun"
                        
                        st.write(f"- **Tren Jumlah**: Secara keseluruhan, rata-rata jumlah barang menunjukkan tren {jumlah_trend}")
                        st.write(f"- **Tren Kebutuhan**: Rata-rata kebutuhan barang menunjukkan tren {kebutuhan_trend}")
                        st.write(f"- **Rata-rata Jumlah**: {df_global['jumlah'].mean():.1f} kg per bulan")
                        st.write(f"- **Rata-rata Kebutuhan**: {df_global['kebutuhan'].mean():.1f} kg per bulan")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 2. Line Chart per Pasar
                        st.markdown('<h2 class="section-header">🏪 Analisis per Pasar</h2>', unsafe_allow_html=True)
                        
                        daftar_pasar = sorted(df['nama_pasar'].dropna().unique())
                        selected_pasar = st.selectbox("Pilih Pasar untuk Analisis Detail:", daftar_pasar)
                        
                        if selected_pasar:
                            df_pasar = df[df['nama_pasar'] == selected_pasar]
                            df_grouped = df_pasar.groupby('bulan').agg({
                                'jumlah': 'mean',
                                'kebutuhan': 'mean'
                            }).reset_index()
                            
                            df_grouped['bulan'] = pd.to_datetime(df_grouped['bulan'])
                            df_grouped = df_grouped.sort_values('bulan')
                            
                            fig, ax = plt.subplots(figsize=(12, 6))
                            ax.plot(df_grouped['bulan'], df_grouped['jumlah'], marker='o', label='Rata-rata Jumlah', color='blue', linewidth=2)
                            ax.plot(df_grouped['bulan'], df_grouped['kebutuhan'], marker='o', label='Rata-rata Kebutuhan', color='green', linewidth=2)
                            ax.set_title(f'Pasar: {selected_pasar} — Rata-rata Jumlah & Kebutuhan per Bulan', fontsize=14, fontweight='bold')
                            ax.set_xlabel('Bulan')
                            ax.set_ylabel('Nilai (kg)')
                            ax.legend()
                            ax.grid(True, alpha=0.3)
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            st.pyplot(fig)
                            
                            # Insight untuk pasar
                            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                            st.markdown(f"### 💡 Insight: {selected_pasar}")
                            st.write(f"- **Rata-rata Jumlah**: {df_grouped['jumlah'].mean():.1f} kg")
                            st.write(f"- **Rata-rata Kebutuhan**: {df_grouped['kebutuhan'].mean():.1f} kg")
                            st.write(f"- **Jumlah Tertinggi**: {df_grouped['jumlah'].max():.1f} kg")
                            st.write(f"- **Kebutuhan Tertinggi**: {df_grouped['kebutuhan'].max():.1f} kg")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 3. Line Chart per Barang
                        st.markdown('<h2 class="section-header">🥬 Analisis per Barang</h2>', unsafe_allow_html=True)
                        
                        unique_items = sorted(df['item_barang'].unique())
                        selected_item = st.selectbox("Pilih Barang untuk Analisis Detail:", unique_items)
                        
                        if selected_item:
                            df_item = df[df['item_barang'] == selected_item]
                            df_grouped = df_item.groupby('bulan').agg({
                                'jumlah': 'mean',
                                'kebutuhan': 'mean'
                            }).reset_index()
                            
                            df_grouped['bulan'] = pd.to_datetime(df_grouped['bulan'])
                            df_grouped = df_grouped.sort_values('bulan')
                            
                            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
                            
                            ax1.plot(df_grouped['bulan'], df_grouped['jumlah'], marker='o', color='blue', linewidth=2)
                            ax1.set_title(f'Rata-rata Jumlah per Bulan - {selected_item}', fontsize=14, fontweight='bold')
                            ax1.set_ylabel('Jumlah (kg)')
                            ax1.grid(True, alpha=0.3)
                            ax1.tick_params(axis='x', rotation=45)
                            
                            ax2.plot(df_grouped['bulan'], df_grouped['kebutuhan'], marker='o', color='green', linewidth=2)
                            ax2.set_title(f'Rata-rata Kebutuhan per Bulan - {selected_item}', fontsize=14, fontweight='bold')
                            ax2.set_xlabel('Bulan')
                            ax2.set_ylabel('Kebutuhan (kg)')
                            ax2.grid(True, alpha=0.3)
                            ax2.tick_params(axis='x', rotation=45)
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                            
                            # Insight untuk barang
                            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                            st.markdown(f"### 💡 Insight: {selected_item}")
                            st.write(f"- **Rata-rata Jumlah**: {df_grouped['jumlah'].mean():.1f} kg")
                            st.write(f"- **Rata-rata Kebutuhan**: {df_grouped['kebutuhan'].mean():.1f} kg")
                            st.write(f"- **Variabilitas Jumlah**: {df_grouped['jumlah'].std():.1f} kg")
                            st.write(f"- **Variabilitas Kebutuhan**: {df_grouped['kebutuhan'].std():.1f} kg")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 4. Bar Chart Jumlah & Kebutuhan per Barang
                        st.markdown('<h2 class="section-header">📊 Ranking Barang</h2>', unsafe_allow_html=True)
                        
                        df_summary = df.groupby('item_barang').agg({
                            'jumlah': 'mean',
                            'kebutuhan': 'mean'
                        }).reset_index()
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            df_summary_sorted_jumlah = df_summary.sort_values(by='jumlah', ascending=True)
                            
                            fig, ax = plt.subplots(figsize=(10, max(6, len(df_summary_sorted_jumlah)*0.3)))
                            bars = ax.barh(df_summary_sorted_jumlah['item_barang'], df_summary_sorted_jumlah['jumlah'], color='skyblue')
                            ax.set_xlabel('Rata-rata Jumlah (kg)')
                            ax.set_title('Rata-rata Jumlah per Barang (12 Bulan Terakhir)', fontweight='bold')
                            ax.grid(True, axis='x', alpha=0.3)
                            
                            # Tambahkan value di ujung bar
                            for bar in bars:
                                width = bar.get_width()
                                ax.text(width + 0.01 * max(df_summary_sorted_jumlah['jumlah']), 
                                    bar.get_y() + bar.get_height()/2, 
                                    f'{width:.1f}', ha='left', va='center', fontsize=8)
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                        
                        with col2:
                            df_summary_sorted_kebutuhan = df_summary.sort_values(by='kebutuhan', ascending=True)
                            
                            fig, ax = plt.subplots(figsize=(10, max(6, len(df_summary_sorted_kebutuhan)*0.3)))
                            bars = ax.barh(df_summary_sorted_kebutuhan['item_barang'], df_summary_sorted_kebutuhan['kebutuhan'], color='lightgreen')
                            ax.set_xlabel('Rata-rata Kebutuhan (kg)')
                            ax.set_title('Rata-rata Kebutuhan per Barang (12 Bulan Terakhir)', fontweight='bold')
                            ax.grid(True, axis='x', alpha=0.3)
                            
                            # Tambahkan value di ujung bar
                            for bar in bars:
                                width = bar.get_width()
                                ax.text(width + 0.01 * max(df_summary_sorted_kebutuhan['kebutuhan']), 
                                    bar.get_y() + bar.get_height()/2, 
                                    f'{width:.1f}', ha='left', va='center', fontsize=8)
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                        
                        # Insight untuk ranking
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown("### 💡 Insight: Ranking Barang")
                        top_jumlah = df_summary_sorted_jumlah.iloc[-1]['item_barang']
                        top_kebutuhan = df_summary_sorted_kebutuhan.iloc[-1]['item_barang']
                        st.write(f"- **Barang dengan Jumlah Tertinggi**: {top_jumlah}")
                        st.write(f"- **Barang dengan Kebutuhan Tertinggi**: {top_kebutuhan}")
                        st.write(f"- **Total Jenis Barang**: {len(df_summary)} jenis")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 5. Jumlah Barang Unik per Pasar
                        st.markdown('<h2 class="section-header">🏪 Diversitas Barang per Pasar</h2>', unsafe_allow_html=True)
                        
                        jumlah_item_per_pasar = df.groupby('nama_pasar')['item_barang'].nunique().reset_index()
                        jumlah_item_per_pasar.columns = ['Nama Pasar', 'Jumlah Item Unik']
                        jumlah_item_per_pasar = jumlah_item_per_pasar.sort_values(by='Jumlah Item Unik', ascending=True)
                        
                        fig, ax = plt.subplots(figsize=(12, 8))
                        bars = ax.barh(jumlah_item_per_pasar['Nama Pasar'], jumlah_item_per_pasar['Jumlah Item Unik'], color='coral')
                        ax.set_xlabel('Jumlah Item Unik')
                        ax.set_title('Jumlah Barang Unik di Setiap Pasar', fontsize=14, fontweight='bold')
                        ax.grid(True, axis='x', alpha=0.3)
                        
                        # Tambahkan value di ujung bar
                        for bar in bars:
                            width = bar.get_width()
                            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                                f'{int(width)}', ha='left', va='center', fontsize=10)
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Insight untuk diversitas
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown("### 💡 Insight: Diversitas Barang")
                        pasar_terdiversifikasi = jumlah_item_per_pasar.iloc[-1]['Nama Pasar']
                        pasar_terbatas = jumlah_item_per_pasar.iloc[0]['Nama Pasar']
                        st.write(f"- **Pasar Paling Terdiversifikasi**: {pasar_terdiversifikasi} ({jumlah_item_per_pasar.iloc[-1]['Jumlah Item Unik']} jenis barang)")
                        st.write(f"- **Pasar Paling Terbatas**: {pasar_terbatas} ({jumlah_item_per_pasar.iloc[0]['Jumlah Item Unik']} jenis barang)")
                        st.write(f"- **Rata-rata Diversitas**: {jumlah_item_per_pasar['Jumlah Item Unik'].mean():.1f} jenis barang per pasar")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 6. Summary Data
                        st.markdown('<h2 class="section-header">📋 Summary Data</h2>', unsafe_allow_html=True)
                        
                        # Hitung rata-rata untuk setiap item
                        df['jumlah'] = pd.to_numeric(df['jumlah'], errors='coerce')
                        df['kebutuhan'] = pd.to_numeric(df['kebutuhan'], errors='coerce')
                        
                        df_summary_final = df.groupby('item_barang').agg({
                            'jumlah': 'mean',
                            'kebutuhan': 'mean'
                        }).reset_index()
                        
                        df_summary_final.columns = ['Barang', 'Rata-Rata Jumlah', 'Rata-Rata Kebutuhan']
                        df_summary_final = df_summary_final.sort_values(by='Barang')
                        
                        st.dataframe(df_summary_final, use_container_width=True)
                        
                        # Insight untuk summary
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown("### 💡 Insight: Summary Data")
                        st.write(f"- **Total Barang**: {len(df_summary_final)} jenis")
                        st.write(f"- **Rata-rata Jumlah Keseluruhan**: {df_summary_final['Rata-Rata Jumlah'].mean():.1f} kg")
                        st.write(f"- **Rata-rata Kebutuhan Keseluruhan**: {df_summary_final['Rata-Rata Kebutuhan'].mean():.1f} kg")
                        st.write(f"- **Variabilitas Jumlah**: {df_summary_final['Rata-Rata Jumlah'].std():.1f} kg")
                        st.write(f"- **Variabilitas Kebutuhan**: {df_summary_final['Rata-Rata Kebutuhan'].std():.1f} kg")
                        st.markdown('</div>', unsafe_allow_html=True)
                    