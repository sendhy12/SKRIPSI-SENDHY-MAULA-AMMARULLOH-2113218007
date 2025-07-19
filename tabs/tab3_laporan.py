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

def tab3_laporan(df):
            st.markdown('<h2 class="section-header">📄 Laporan Profesional</h2>', unsafe_allow_html=True)
            
            if st.button("📊 Generate Laporan PDF Lengkap"):
                # Ambil periode lengkap dari df
                min_date = df['tanggal'].min()
                max_date = df['tanggal'].max()

                # Tambahkan kolom 'bulan' dalam format YYYY-MM
                df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)

                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Buat buffer untuk PDF
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(
                    buffer,
                    pagesize=A4,
                    rightMargin=2*cm,
                    leftMargin=2*cm,
                    topMargin=2*cm,
                    bottomMargin=2*cm
                )
                
                # Style
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'TitleStyle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=30,
                    alignment=1,  # Center
                    textColor=colors.darkblue
                )
                
                heading_style = ParagraphStyle(
                    'HeadingStyle',
                    parent=styles['Heading2'],
                    fontSize=14,
                    spaceAfter=12,
                    textColor=colors.darkblue
                )
                
                subheading_style = ParagraphStyle(
                    'SubheadingStyle',
                    parent=styles['Heading3'],
                    fontSize=12,
                    spaceAfter=8,
                    textColor=colors.darkgreen
                )
                
                normal_style = styles['Normal']
                normal_style.fontSize = 10
                normal_style.spaceAfter = 6

                # Style teks instansi (rata tengah)
                instansi_style = ParagraphStyle(
                    'InstansiStyle',
                    parent=styles['Normal'],
                    fontSize=10,
                    spaceAfter=2,
                    alignment=1  # Center
                )

                # Story (konten PDF)
                story = []

                # === LOGO DAN HEADER INSTANSI ===
                logo_path = "logo.png"  # Pastikan file tersedia di folder proyek
                
                instansi_text = """
                <font size="14">PEMERINTAH KABUPATEN SUMEDANG<br/>
                <b>DINAS KOPERASI, USAHA KECIL, MENENGAH, PERDAGANGAN DAN PERINDUSTRIAN</b></font><br/>
                Alamat : JL. Mayor Abdul Rachman No.107, Kotakaler, Kec. Sumedang Utara, Kabupaten Sumedang, Jawa Barat 45621, No. Tlp: (0261) 201238,<br/>
                Website : disperindag.sumedangkab.go.id E-mail : diskopukmpp@sumedangkab.go.id, 45621
                """

                header_table = Table(
                    data=[[
                        Image(logo_path, width=2.5*cm, height=2.5*cm),
                        Paragraph(instansi_text, instansi_style)
                    ]],
                    colWidths=[3*cm, 13*cm]
                )

                header_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))

                story.append(header_table)
                story.append(Spacer(1, 12))

                # Garis bawah pemisah
                line = Table([[""]], colWidths=[16*cm], rowHeights=[0.5])
                line.setStyle(TableStyle([
                    ('LINEABOVE', (0, 0), (-1, -1), 1, colors.darkblue),
                    ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.darkblue)
                ]))
                story.append(line)
                story.append(Spacer(1, 20))
                
                # Informasi laporan
                story.append(Paragraph("LAPORAN ANALISIS PENGELOMPOKAN BARANG PASAR KABUPATEN SUMEDANG", heading_style))
                story.append(Paragraph(f"Tanggal Laporan Dibuat: {datetime.now().strftime('%d %B %Y')}", normal_style))
                story.append(Paragraph(f"Periode Data: {min_date.strftime('%d %B %Y')} - {max_date.strftime('%d %B %Y')}", normal_style))
                story.append(Paragraph(f"Total Data: {len(df)} records", normal_style))
                story.append(Paragraph(f"Total Pasar: {df['nama_pasar'].nunique()} pasar", normal_style))
                story.append(Paragraph(f"Total Jenis Barang: {df['item_barang'].nunique()} jenis", normal_style))
                story.append(Spacer(1, 20))
                
                status_text.text("Generating statistik deskriptif...")
                progress_bar.progress(10)
                
                # 1. STATISTIK DESKRIPTIF
                story.append(Paragraph("1. STATISTIK DESKRIPTIF", heading_style))
                
                # Tabel statistik deskriptif
                story.append(Paragraph("1.1 Ringkasan Statistik", subheading_style))
                
                stats_data = [
                    ['Metrik', 'Jumlah (kg)', 'Kebutuhan (kg)'],
                    ['Mean', f"{df['jumlah'].mean():.2f}", f"{df['kebutuhan'].mean():.2f}"],
                    ['Median', f"{df['jumlah'].median():.2f}", f"{df['kebutuhan'].median():.2f}"],
                    ['Std Dev', f"{df['jumlah'].std():.2f}", f"{df['kebutuhan'].std():.2f}"],
                    ['Min', f"{df['jumlah'].min():.2f}", f"{df['kebutuhan'].min():.2f}"],
                    ['Max', f"{df['jumlah'].max():.2f}", f"{df['kebutuhan'].max():.2f}"]
                ]
                
                stats_table = Table(stats_data, colWidths=[4*cm, 4*cm, 4*cm])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(stats_table)
                story.append(Spacer(1, 20))
                
                # Generate dan simpan grafik tren global
                status_text.text("Generating grafik tren global...")
                progress_bar.progress(20)
                
                df_global = df.groupby('bulan').agg({
                    'jumlah': 'mean',
                    'kebutuhan': 'mean'
                }).reset_index()
                
                df_global['bulan'] = pd.to_datetime(df_global['bulan'])
                df_global = df_global.sort_values('bulan')
                
                # Grafik tren global
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
                
                ax1.plot(df_global['bulan'], df_global['jumlah'], marker='o', color='blue', linewidth=2)
                ax1.set_title('Tren Rata-rata Jumlah per Bulan (Global)', fontsize=14, fontweight='bold')
                ax1.set_ylabel('Jumlah (kg)')
                ax1.grid(True, alpha=0.3)
                ax1.tick_params(axis='x', rotation=45)
                
                ax2.plot(df_global['bulan'], df_global['kebutuhan'], marker='o', color='green', linewidth=2)
                ax2.set_title('Tren Rata-rata Kebutuhan per Bulan (Global)', fontsize=14, fontweight='bold')
                ax2.set_xlabel('Bulan')
                ax2.set_ylabel('Kebutuhan (kg)')
                ax2.grid(True, alpha=0.3)
                ax2.tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                
                # Simpan grafik sebagai image
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                # Tambahkan grafik ke PDF
                story.append(Paragraph("1.2 Tren Global 12 Bulan Terakhir", subheading_style))
                story.append(Image(img_buffer, width=15*cm, height=10*cm))
                story.append(Spacer(1, 10))
                
                # Insight tren global
                jumlah_trend = "meningkat" if df_global['jumlah'].iloc[-1] > df_global['jumlah'].iloc[0] else "menurun"
                kebutuhan_trend = "meningkat" if df_global['kebutuhan'].iloc[-1] > df_global['kebutuhan'].iloc[0] else "menurun"
                
                story.append(Paragraph("Insight Tren Global:", subheading_style))
                story.append(Paragraph(f"• Tren Jumlah: Secara keseluruhan menunjukkan tren {jumlah_trend}", normal_style))
                story.append(Paragraph(f"• Tren Kebutuhan: Secara keseluruhan menunjukkan tren {kebutuhan_trend}", normal_style))
                story.append(Paragraph(f"• Rata-rata Jumlah: {df_global['jumlah'].mean():.1f} kg per bulan", normal_style))
                story.append(Paragraph(f"• Rata-rata Kebutuhan: {df_global['kebutuhan'].mean():.1f} kg per bulan", normal_style))
                story.append(Spacer(1, 20))
                
                # 2. ANALISIS PER PASAR (SEMUA PASAR)
                story.append(Paragraph("2. ANALISIS PER PASAR", heading_style))
                
                daftar_pasar = sorted(df['nama_pasar'].dropna().unique())
                
                for idx, pasar in enumerate(daftar_pasar):
                    status_text.text(f"Generating analisis pasar {idx+1}/{len(daftar_pasar)}: {pasar}")
                    progress_bar.progress(30 + (idx * 20 // len(daftar_pasar)))
                    
                    story.append(Paragraph(f"2.{idx+1} Pasar: {pasar}", subheading_style))
                    
                    # Data pasar
                    df_pasar = df[df['nama_pasar'] == pasar]
                    df_grouped = df_pasar.groupby('bulan').agg({
                        'jumlah': 'mean',
                        'kebutuhan': 'mean'
                    }).reset_index()
                    
                    df_grouped['bulan'] = pd.to_datetime(df_grouped['bulan'])
                    df_grouped = df_grouped.sort_values('bulan')
                    
                    # Grafik pasar
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.plot(df_grouped['bulan'], df_grouped['jumlah'], marker='o', label='Rata-rata Jumlah', color='blue', linewidth=2)
                    ax.plot(df_grouped['bulan'], df_grouped['kebutuhan'], marker='o', label='Rata-rata Kebutuhan', color='green', linewidth=2)
                    ax.set_title(f'Tren Pasar {pasar}', fontsize=14, fontweight='bold')
                    ax.set_xlabel('Bulan')
                    ax.set_ylabel('Nilai (kg)')
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    
                    # Simpan grafik
                    img_buffer = io.BytesIO()
                    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                    img_buffer.seek(0)
                    plt.close()
                    
                    story.append(Image(img_buffer, width=15*cm, height=7*cm))
                    story.append(Spacer(1, 5))
                    
                    # Insight pasar
                    story.append(Paragraph(f"Insight Pasar {pasar}:", normal_style))
                    story.append(Paragraph(f"• Rata-rata Jumlah: {df_grouped['jumlah'].mean():.1f} kg", normal_style))
                    story.append(Paragraph(f"• Rata-rata Kebutuhan: {df_grouped['kebutuhan'].mean():.1f} kg", normal_style))
                    story.append(Paragraph(f"• Jumlah Tertinggi: {df_grouped['jumlah'].max():.1f} kg", normal_style))
                    story.append(Paragraph(f"• Kebutuhan Tertinggi: {df_grouped['kebutuhan'].max():.1f} kg", normal_style))
                    story.append(Paragraph(f"• Jenis Barang: {df_pasar['item_barang'].nunique()} jenis", normal_style))
                    story.append(Spacer(1, 15))
                
                # 3. ANALISIS PER BARANG (SEMUA BARANG)
                story.append(Paragraph("3. ANALISIS PER BARANG", heading_style))
                
                unique_items = sorted(df['item_barang'].unique())
                
                for idx, item in enumerate(unique_items):
                    status_text.text(f"Generating analisis barang {idx+1}/{len(unique_items)}: {item}")
                    progress_bar.progress(50 + (idx * 30 // len(unique_items)))
                    
                    story.append(Paragraph(f"3.{idx+1} Barang: {item}", subheading_style))
                    
                    # Data barang
                    df_item = df[df['item_barang'] == item]
                    df_grouped = df_item.groupby('bulan').agg({
                        'jumlah': 'mean',
                        'kebutuhan': 'mean'
                    }).reset_index()
                    
                    df_grouped['bulan'] = pd.to_datetime(df_grouped['bulan'])
                    df_grouped = df_grouped.sort_values('bulan')
                    
                    # Grafik barang
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
                    
                    ax1.plot(df_grouped['bulan'], df_grouped['jumlah'], marker='o', color='blue', linewidth=2)
                    ax1.set_title(f'Tren Jumlah - {item}', fontsize=12, fontweight='bold')
                    ax1.set_ylabel('Jumlah (kg)')
                    ax1.grid(True, alpha=0.3)
                    ax1.tick_params(axis='x', rotation=45)
                    
                    ax2.plot(df_grouped['bulan'], df_grouped['kebutuhan'], marker='o', color='green', linewidth=2)
                    ax2.set_title(f'Tren Kebutuhan - {item}', fontsize=12, fontweight='bold')
                    ax2.set_xlabel('Bulan')
                    ax2.set_ylabel('Kebutuhan (kg)')
                    ax2.grid(True, alpha=0.3)
                    ax2.tick_params(axis='x', rotation=45)
                    
                    plt.tight_layout()
                    
                    # Simpan grafik
                    img_buffer = io.BytesIO()
                    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                    img_buffer.seek(0)
                    plt.close()
                    
                    story.append(Image(img_buffer, width=15*cm, height=10*cm))
                    story.append(Spacer(1, 5))
                    
                    # Insight barang
                    story.append(Paragraph(f"Insight {item}:", normal_style))
                    story.append(Paragraph(f"• Rata-rata Jumlah: {df_grouped['jumlah'].mean():.1f} kg", normal_style))
                    story.append(Paragraph(f"• Rata-rata Kebutuhan: {df_grouped['kebutuhan'].mean():.1f} kg", normal_style))
                    story.append(Paragraph(f"• Variabilitas Jumlah: {df_grouped['jumlah'].std():.1f} kg", normal_style))
                    story.append(Paragraph(f"• Variabilitas Kebutuhan: {df_grouped['kebutuhan'].std():.1f} kg", normal_style))
                    story.append(Paragraph(f"• Tersedia di: {df_item['nama_pasar'].nunique()} pasar", normal_style))
                    story.append(Spacer(1, 15))
                
                # 4. RANKING BARANG
                status_text.text("Generating ranking barang...")
                progress_bar.progress(80)
                
                story.append(Paragraph("4. RANKING BARANG", heading_style))
                
                df_summary = df.groupby('item_barang').agg({
                    'jumlah': 'mean',
                    'kebutuhan': 'mean'
                }).reset_index()
                
                # Grafik ranking
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
                
                # Ranking jumlah
                df_summary_sorted_jumlah = df_summary.sort_values(by='jumlah', ascending=True)
                bars1 = ax1.barh(df_summary_sorted_jumlah['item_barang'], df_summary_sorted_jumlah['jumlah'], color='skyblue')
                ax1.set_xlabel('Rata-rata Jumlah (kg)')
                ax1.set_title('Ranking Berdasarkan Jumlah', fontweight='bold')
                ax1.grid(True, axis='x', alpha=0.3)
                
                # Ranking kebutuhan
                df_summary_sorted_kebutuhan = df_summary.sort_values(by='kebutuhan', ascending=True)
                bars2 = ax2.barh(df_summary_sorted_kebutuhan['item_barang'], df_summary_sorted_kebutuhan['kebutuhan'], color='lightgreen')
                ax2.set_xlabel('Rata-rata Kebutuhan (kg)')
                ax2.set_title('Ranking Berdasarkan Kebutuhan', fontweight='bold')
                ax2.grid(True, axis='x', alpha=0.3)
                
                plt.tight_layout()
                
                # Simpan grafik
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                story.append(Image(img_buffer, width=16*cm, height=8*cm))
                story.append(Spacer(1, 10))
                
                # Insight ranking
                top_jumlah = df_summary_sorted_jumlah.iloc[-1]['item_barang']
                top_kebutuhan = df_summary_sorted_kebutuhan.iloc[-1]['item_barang']
                
                story.append(Paragraph("Insight Ranking:", subheading_style))
                story.append(Paragraph(f"• Barang dengan Jumlah Tertinggi: {top_jumlah}", normal_style))
                story.append(Paragraph(f"• Barang dengan Kebutuhan Tertinggi: {top_kebutuhan}", normal_style))
                story.append(Paragraph(f"• Total Jenis Barang: {len(df_summary)} jenis", normal_style))
                story.append(Spacer(1, 20))
                
                # 5. DIVERSITAS BARANG PER PASAR
                story.append(Paragraph("5. DIVERSITAS BARANG PER PASAR", heading_style))
                
                jumlah_item_per_pasar = df.groupby('nama_pasar')['item_barang'].nunique().reset_index()
                jumlah_item_per_pasar.columns = ['Nama Pasar', 'Jumlah Item Unik']
                jumlah_item_per_pasar = jumlah_item_per_pasar.sort_values(by='Jumlah Item Unik', ascending=True)
                
                # Grafik diversitas
                fig, ax = plt.subplots(figsize=(12, 8))
                bars = ax.barh(jumlah_item_per_pasar['Nama Pasar'], jumlah_item_per_pasar['Jumlah Item Unik'], color='coral')
                ax.set_xlabel('Jumlah Item Unik')
                ax.set_title('Diversitas Barang per Pasar', fontsize=14, fontweight='bold')
                ax.grid(True, axis='x', alpha=0.3)
                
                plt.tight_layout()
                
                # Simpan grafik
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                story.append(Image(img_buffer, width=15*cm, height=10*cm))
                story.append(Spacer(1, 10))
                
                # Insight diversitas
                pasar_terdiversifikasi = jumlah_item_per_pasar.iloc[-1]['Nama Pasar']
                pasar_terbatas = jumlah_item_per_pasar.iloc[0]['Nama Pasar']
                
                story.append(Paragraph("Insight Diversitas:", subheading_style))
                story.append(Paragraph(f"• Pasar Paling Terdiversifikasi: {pasar_terdiversifikasi} ({jumlah_item_per_pasar.iloc[-1]['Jumlah Item Unik']} jenis)", normal_style))
                story.append(Paragraph(f"• Pasar Paling Terbatas: {pasar_terbatas} ({jumlah_item_per_pasar.iloc[0]['Jumlah Item Unik']} jenis)", normal_style))
                story.append(Paragraph(f"• Rata-rata Diversitas: {jumlah_item_per_pasar['Jumlah Item Unik'].mean():.1f} jenis per pasar", normal_style))
                story.append(Spacer(1, 20))
                
                # 6. K-MEANS CLUSTERING (jika ada hasil)
                if 'clustering_results' in st.session_state:
                    status_text.text("Generating hasil clustering...")
                    progress_bar.progress(90)
                    
                    story.append(Paragraph("6. HASIL K-MEANS CLUSTERING", heading_style))
                    
                    results = st.session_state.clustering_results
                    labels = results['labels']
                    centroids = results['centroids']
                    evaluasi_list = results['evaluasi_list']
                    df_summary_cluster = results['df_summary_cluster']
                    X = results['X']
                    
                    # Tambahkan label cluster
                    df_summary_cluster['Cluster'] = labels
                    df_summary_cluster['Cluster_Label'] = df_summary_cluster['Cluster'].map({0: 'C1', 1: 'C2'})
                    
                    # Grafik clustering
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
                    ax.set_title('Hasil K-Means Clustering', fontsize=14, fontweight='bold')
                    ax.legend(fontsize=10)
                    ax.grid(True, alpha=0.3)
                    
                    plt.tight_layout()
                    
                    # Simpan grafik
                    img_buffer = io.BytesIO()
                    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                    img_buffer.seek(0)
                    plt.close()
                    
                    story.append(Image(img_buffer, width=15*cm, height=12*cm))

                    # Tabel hasil clustering
                    df_sorted = df_summary_cluster.sort_values(by=['Cluster_Label', 'Barang'])
                    table_data = [['Barang', 'Rata-Rata Jumlah', 'Rata-Rata Kebutuhan', 'Cluster']]
                    for _, row in df_sorted.iterrows():
                        table_data.append([
                            row['Barang'],
                            f"{row['Rata-Rata Jumlah']:.1f}",
                            f"{row['Rata-Rata Kebutuhan']:.1f}",
                            row['Cluster_Label']
                        ])

                    # Format tabel PDF
                    table = Table(table_data, repeatRows=1, hAlign='LEFT')
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                    ]))

                    story.append(Spacer(1, 10))
                    story.append(Paragraph("6.1 Tabel Hasil Clustering per Barang:", subheading_style))
                    story.append(table)
                    story.append(Spacer(1, 20))

                    story.append(Spacer(1, 10))
                    
                    # Tabel evaluasi clustering
                    story.append(Paragraph("6.2 Evaluasi Clustering", subheading_style))
                    
                    eval_data = [['Iterasi', 'WCV', 'BCV', 'Rasio BCV/WCV']]
                    for eval_item in evaluasi_list:
                        eval_data.append([
                            str(eval_item['Iterasi']),
                            f"{eval_item['WCV']:.1f}",
                            f"{eval_item['BCV']:.1f}",
                            f"{eval_item['Rasio BCV/WCV']:.8f}"
                        ])
                    
                    eval_table = Table(eval_data, colWidths=[3*cm, 3*cm, 3*cm, 4*cm])
                    eval_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 8)
                    ]))
                    
                    story.append(eval_table)
                    story.append(Spacer(1, 15))
                    
                    # Interpretasi cluster
                    story.append(Paragraph("6.3 Interpretasi Cluster", subheading_style))
                    
                    cluster_range = df_summary_cluster.groupby('Cluster_Label')[['Rata-Rata Jumlah', 'Rata-Rata Kebutuhan']].agg(['min', 'max']).reset_index()
                    cluster_range.columns = ['Cluster_Label', 'Jumlah_Min', 'Jumlah_Max', 'Kebutuhan_Min', 'Kebutuhan_Max']
                    
                    for idx, row in cluster_range.iterrows():
                        cluster = row['Cluster_Label']
                        j_min, j_max = row['Jumlah_Min'], row['Jumlah_Max']
                        k_min, k_max = row['Kebutuhan_Min'], row['Kebutuhan_Max']
                        
                        items_in_cluster = df_summary_cluster[df_summary_cluster['Cluster_Label'] == cluster]['Barang'].tolist()
                        
                        story.append(Paragraph(f"Karakteristik Cluster {cluster}:", normal_style))
                        story.append(Paragraph(f"• Rata-rata Jumlah: {j_min:.1f} - {j_max:.1f} kg", normal_style))
                        story.append(Paragraph(f"• Rata-rata Kebutuhan: {k_min:.1f} - {k_max:.1f} kg", normal_style))
                        story.append(Paragraph(f"• Jumlah Barang: {len(items_in_cluster)}", normal_style))
                        story.append(Paragraph(f"• Daftar Barang: {', '.join(items_in_cluster)}", normal_style))
                        story.append(Spacer(1, 10))
                
                # 7. KESIMPULAN
                story.append(Paragraph("7. KESIMPULAN DAN REKOMENDASI", heading_style))
                
                story.append(Paragraph("Berdasarkan analisis yang telah dilakukan, dapat disimpulkan:", normal_style))
                story.append(Paragraph(f"• Total {df['nama_pasar'].nunique()} pasar telah dianalisis dengan {df['item_barang'].nunique()} jenis barang", normal_style))
                story.append(Paragraph(f"• Rata-rata jumlah barang keseluruhan: {df['jumlah'].mean():.1f} kg", normal_style))
                story.append(Paragraph(f"• Rata-rata kebutuhan barang keseluruhan: {df['kebutuhan'].mean():.1f} kg", normal_style))
                story.append(Paragraph("• Analisis clustering menunjukkan pengelompokan barang berdasarkan karakteristik jumlah dan kebutuhan", normal_style))
                story.append(Paragraph("• Rekomendasi: Fokus pada barang dengan permintaan tinggi dan optimalkan distribusi di pasar yang kurang terdiversifikasi", normal_style))
                
                # Build PDF
                status_text.text("Finalizing PDF...")
                progress_bar.progress(100)
                
                doc.build(story)
                buffer.seek(0)
                
                # Download button
                st.download_button(
                    label="📥 Download Laporan PDF Lengkap",
                    data=buffer,
                    file_name=f"Laporan_Analisis_Pasar_Kabupaten_Sumedang_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
                
                progress_bar.empty()
                status_text.empty()
                
                st.success("✅ Laporan PDF berhasil dibuat!")
                st.info("📋 Laporan mencakup: Statistik Deskriptif, Analisis per Pasar, Analisis per Barang, Ranking, Diversitas, dan K-Means Clustering")
            
            else:
                st.info("📊 Klik tombol di atas untuk generate laporan PDF lengkap yang mencakup semua analisis")
                st.markdown("""
                **Laporan akan mencakup:**
                - Statistik Deskriptif Lengkap
                - Tren Global
                - **Analisis per Pasar (Semua Pasar dengan Grafik & Insight)**
                - **Analisis per Barang (Semua Barang dengan Grafik & Insight)**
                - Ranking Barang
                - Diversitas Barang per Pasar
                - K-Means Clustering
                - Kesimpulan & Rekomendasi

                📌 **Catatan**:
                - Proses pembuatan laporan membutuhkan waktu beberapa detik tergantung jumlah pasar dan barang.
                - Pastikan data sudah terupdate sebelum generate laporan.
                """)
