# 01. IMPOR LIBRARY
import numpy as np
import pandas as pd
import streamlit as st


# 02. KONFIGURASI HALAMAN
st.set_page_config(page_title="Klasemen Layanan")
st.title(":blue[Klasemen Layanan]", text_alignment="center")


# 03. LOAD DATA
if "data" in st.session_state:
    data = st.session_state["data"]
else:
    st.error("Data tidak ditemukan!")


# 04. FILTER DATA
# Tanggal Responden Terakhir Mengisi Survei
st.badge(f"Data Masuk Terakhir: {data.loc[data.index[-1], 'Last Submitted']}", icon=":material/database:", color="blue")

# Variabel untuk Filter Data
validitas_saring = data['Validitas'].sort_values().dropna().unique()
ue2_saring = data['Unit Eselon II'].sort_values().dropna().unique()
tahun_saring = data['Tahun'].sort_values().dropna().unique()

# Catatan untuk Filter Data
st.write(":orange-badge[Untuk memilih **Bulan**, silakan memilih **Tahun** terlebih dahulu :smile:]")
st.write(":orange-badge[Untuk menampilkan **Data Triwulanan**, silakan pilih **Seluruh Bulan** yang termasuk dalam **Triwulan bersangkutan** :smile:]")

# Menyalin Data
data = data.copy()

# Membuat Kolom Selector untuk Filter Data
col_wf_01, col_wf_02, col_wf_03, col_wf_04 = st.columns(4)
with col_wf_01:
    validitas_widget = st.multiselect(":material/person_edit: Status Responden:", validitas_saring, default="VALID")
    if validitas_widget:
        data = data[data['Validitas'].isin(validitas_widget)]
with col_wf_02:
    ue2_widget = st.multiselect(":material/moving_ministry: Unit Eselon II:", ue2_saring)
    if ue2_widget:
        data = data[data['Unit Eselon II'].isin(ue2_widget)]
with col_wf_03:
    tahun_widget = st.multiselect(":material/date_range: Tahun:", tahun_saring)
    if tahun_widget:
        data = data[data['Tahun'].isin(tahun_widget)]
        periode_saring = data['Bulan'].sort_values().dropna().unique()
    else:
        periode_saring = []
with col_wf_04:
    periode_widget = st.multiselect(":material/calendar_month: Bulan:", periode_saring)
    if periode_widget:
        data = data[data['Bulan'].isin(periode_widget)]


# 05. VISUALISASI DATA
# Membuat Kolom Tabel Klasemen Frekuensi Layanan dan Indeks SKM per Layanan
col_sl_01, col_sl_02 = st.columns(2)
with col_sl_01:
    st.subheader("Layanan Populer", text_alignment="center", divider=True)
    populer_summary = data.groupby(['Layanan']).size()
    populer_klasemen = populer_summary.sort_values(ascending=False)
    st.table(populer_klasemen, border=False, hide_header=True)
with col_sl_02:
    st.subheader("Indeks SKM Layanan", text_alignment="center", divider=True)
    skm_jumlah = data.groupby(['Layanan'])[['Aspek Kejelasan Informasi Biaya/Tarif', 'Aspek Kemudahan Persyaratan', 'Aspek Kemudahan Prosedur', 'Aspek Kesesuaian Produk', 'Aspek Ketepatan Waktu', 'Aspek Kompetensi Petugas', 'Aspek Media atau Tempat Pengaduan', 'Aspek Perilaku Petugas', 'Aspek Sarana dan Prasarana', 'E-service - Kualitas informasi', 'E-service - Kualitas bantuan', 'E-service - Kemudahaan penggunaan', 'E-service - Privasi dan Keamanan data', 'aspek_kecepatan_e-service']].agg('sum')
    skm_jumlah['Jumlah Skor'] = skm_jumlah['Aspek Kejelasan Informasi Biaya/Tarif'] + skm_jumlah['Aspek Kemudahan Persyaratan'] + skm_jumlah['Aspek Kemudahan Prosedur'] + skm_jumlah['Aspek Kesesuaian Produk'] + skm_jumlah['Aspek Ketepatan Waktu'] + skm_jumlah['Aspek Kompetensi Petugas'] + skm_jumlah['Aspek Media atau Tempat Pengaduan'] + skm_jumlah['Aspek Perilaku Petugas'] + skm_jumlah['Aspek Sarana dan Prasarana'] + skm_jumlah['E-service - Kualitas informasi'] + skm_jumlah['E-service - Kualitas bantuan'] + skm_jumlah['E-service - Kemudahaan penggunaan'] + skm_jumlah['E-service - Privasi dan Keamanan data'] + skm_jumlah['aspek_kecepatan_e-service']
    skm_banyak = data.groupby(['Layanan'])[['Aspek Kejelasan Informasi Biaya/Tarif', 'Aspek Kemudahan Persyaratan', 'Aspek Kemudahan Prosedur', 'Aspek Kesesuaian Produk', 'Aspek Ketepatan Waktu', 'Aspek Kompetensi Petugas', 'Aspek Media atau Tempat Pengaduan', 'Aspek Perilaku Petugas', 'Aspek Sarana dan Prasarana', 'E-service - Kualitas informasi', 'E-service - Kualitas bantuan', 'E-service - Kemudahaan penggunaan', 'E-service - Privasi dan Keamanan data', 'aspek_kecepatan_e-service']].agg('count')
    skm_banyak['Banyak Data'] = skm_banyak['Aspek Kejelasan Informasi Biaya/Tarif'] + skm_banyak['Aspek Kemudahan Persyaratan'] + skm_banyak['Aspek Kemudahan Prosedur'] + skm_banyak['Aspek Kesesuaian Produk'] + skm_banyak['Aspek Ketepatan Waktu'] + skm_banyak['Aspek Kompetensi Petugas'] + skm_banyak['Aspek Media atau Tempat Pengaduan'] + skm_banyak['Aspek Perilaku Petugas'] + skm_banyak['Aspek Sarana dan Prasarana'] + skm_banyak['E-service - Kualitas informasi'] + skm_banyak['E-service - Kualitas bantuan'] + skm_banyak['E-service - Kemudahaan penggunaan'] + skm_banyak['E-service - Privasi dan Keamanan data'] + skm_banyak['aspek_kecepatan_e-service']
    skm_rata = (skm_jumlah['Jumlah Skor'] / skm_banyak['Banyak Data']).round(2).sort_values(ascending=False)
    st.table(skm_rata.to_frame().style.format("{:.2f}"), border=False, hide_header=True)