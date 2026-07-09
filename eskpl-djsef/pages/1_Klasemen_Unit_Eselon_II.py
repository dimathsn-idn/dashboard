# 01. IMPOR LIBRARY
import numpy as np
import pandas as pd
import streamlit as st


# 02. KONFIGURASI HALAMAN
st.set_page_config(page_title="Klasemen Unit Eselon II")
st.title(":blue[Klasemen Unit Eselon II]", text_alignment="center")


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
tahun_saring = data['Tahun'].sort_values().dropna().unique()

# Catatan untuk Filter Data
st.write(":orange-badge[Untuk menampilkan **Data Triwulanan**, silakan pilih **Seluruh Bulan** yang termasuk dalam **Triwulan bersangkutan** :smile:]")

# Membuat Kolom Selector untuk Filter Data
col_wf_01, col_wf_02, col_wf_03 = st.columns(3)
with col_wf_01:
    validitas_widget = st.multiselect(":material/person_edit: Status Responden:", validitas_saring, default="VALID")
    if validitas_widget:
        data = data[data['Validitas'].isin(validitas_widget)]
with col_wf_02:
    tahun_widget = st.multiselect(":material/date_range: Tahun:", tahun_saring)
    if tahun_widget:
        data = data[data['Tahun'].isin(tahun_widget)]
        periode_saring = data['Bulan'].sort_values().dropna().unique()
    else:
        periode_saring = []
with col_wf_03:
    periode_widget = st.multiselect(":material/calendar_month: Bulan:", periode_saring)
    if periode_widget:
        data = data[data['Bulan'].isin(periode_widget)]


# 05. VISUALISASI DATA
# Membuat Kolom Tabel Klasemen Indeks SKM per Unit Eselon II
col_suk_01, col_suk_02, col_suk_03 = st.columns(3)
with col_suk_01:
    st.subheader("Indeks SKM", text_alignment="center", divider=True)
    skm_jumlah = data.groupby(['Unit Eselon II'])[['Aspek Kejelasan Informasi Biaya/Tarif', 'Aspek Kemudahan Persyaratan', 'Aspek Kemudahan Prosedur', 'Aspek Kesesuaian Produk', 'Aspek Ketepatan Waktu', 'Aspek Kompetensi Petugas', 'Aspek Media atau Tempat Pengaduan', 'Aspek Perilaku Petugas', 'Aspek Sarana dan Prasarana', 'E-service - Kualitas informasi', 'E-service - Kualitas bantuan', 'E-service - Kemudahaan penggunaan', 'E-service - Privasi dan Keamanan data', 'aspek_kecepatan_e-service']].agg('sum')
    skm_jumlah['Jumlah Skor'] = skm_jumlah['Aspek Kejelasan Informasi Biaya/Tarif'] + skm_jumlah['Aspek Kemudahan Persyaratan'] + skm_jumlah['Aspek Kemudahan Prosedur'] + skm_jumlah['Aspek Kesesuaian Produk'] + skm_jumlah['Aspek Ketepatan Waktu'] + skm_jumlah['Aspek Kompetensi Petugas'] + skm_jumlah['Aspek Media atau Tempat Pengaduan'] + skm_jumlah['Aspek Perilaku Petugas'] + skm_jumlah['Aspek Sarana dan Prasarana'] + skm_jumlah['E-service - Kualitas informasi'] + skm_jumlah['E-service - Kualitas bantuan'] + skm_jumlah['E-service - Kemudahaan penggunaan'] + skm_jumlah['E-service - Privasi dan Keamanan data'] + skm_jumlah['aspek_kecepatan_e-service']
    skm_banyak = data.groupby(['Unit Eselon II'])[['Aspek Kejelasan Informasi Biaya/Tarif', 'Aspek Kemudahan Persyaratan', 'Aspek Kemudahan Prosedur', 'Aspek Kesesuaian Produk', 'Aspek Ketepatan Waktu', 'Aspek Kompetensi Petugas', 'Aspek Media atau Tempat Pengaduan', 'Aspek Perilaku Petugas', 'Aspek Sarana dan Prasarana', 'E-service - Kualitas informasi', 'E-service - Kualitas bantuan', 'E-service - Kemudahaan penggunaan', 'E-service - Privasi dan Keamanan data', 'aspek_kecepatan_e-service']].agg('count')
    skm_banyak['Banyak Data'] = skm_banyak['Aspek Kejelasan Informasi Biaya/Tarif'] + skm_banyak['Aspek Kemudahan Persyaratan'] + skm_banyak['Aspek Kemudahan Prosedur'] + skm_banyak['Aspek Kesesuaian Produk'] + skm_banyak['Aspek Ketepatan Waktu'] + skm_banyak['Aspek Kompetensi Petugas'] + skm_banyak['Aspek Media atau Tempat Pengaduan'] + skm_banyak['Aspek Perilaku Petugas'] + skm_banyak['Aspek Sarana dan Prasarana'] + skm_banyak['E-service - Kualitas informasi'] + skm_banyak['E-service - Kualitas bantuan'] + skm_banyak['E-service - Kemudahaan penggunaan'] + skm_banyak['E-service - Privasi dan Keamanan data'] + skm_banyak['aspek_kecepatan_e-service']
    skm_rata = (skm_jumlah['Jumlah Skor'] / skm_banyak['Banyak Data']).round(2).sort_values(ascending=False)
    st.table(skm_rata.to_frame().style.format("{:.2f}"), border=False, hide_header=True)
with col_suk_02:
    st.subheader("IPAK", text_alignment="center", divider=True)
    ipak_jumlah = data.groupby(['Unit Eselon II'])[['Persepsi - Tidak ada diskriminasi pelayanan', 'Persepsi - Tidak ada pelayanan di luar prosedur', 'Persepsi - Tidak ada pencaloan', 'Persepsi - Tidak ada penerimaan imbalan', 'Persepsi - Tidak ada pungutan liar']].agg('sum')
    ipak_jumlah['Jumlah Skor'] = ipak_jumlah['Persepsi - Tidak ada diskriminasi pelayanan'] + ipak_jumlah['Persepsi - Tidak ada pelayanan di luar prosedur'] + ipak_jumlah['Persepsi - Tidak ada pencaloan'] + ipak_jumlah['Persepsi - Tidak ada penerimaan imbalan'] + ipak_jumlah['Persepsi - Tidak ada pungutan liar']
    ipak_banyak = data.groupby(['Unit Eselon II'])[['Persepsi - Tidak ada diskriminasi pelayanan', 'Persepsi - Tidak ada pelayanan di luar prosedur', 'Persepsi - Tidak ada pencaloan', 'Persepsi - Tidak ada penerimaan imbalan', 'Persepsi - Tidak ada pungutan liar']].agg('count')
    ipak_banyak['Banyak Data'] = ipak_banyak['Persepsi - Tidak ada diskriminasi pelayanan'] + ipak_banyak['Persepsi - Tidak ada pelayanan di luar prosedur'] + ipak_banyak['Persepsi - Tidak ada pencaloan'] + ipak_banyak['Persepsi - Tidak ada penerimaan imbalan'] + ipak_banyak['Persepsi - Tidak ada pungutan liar']
    ipak_rata = (ipak_jumlah['Jumlah Skor'] / ipak_banyak['Banyak Data']).round(2).sort_values(ascending=False)
    st.table(ipak_rata.to_frame().style.format("{:.2f}"), border=False, hide_header=True)
with col_suk_03:
    st.subheader("Indeks Inklusivitas", text_alignment="center", divider=True)
    inklusivitas_jumlah = data.groupby(['Unit Eselon II'])[['Sarana dan Prasarana Khusus']].agg('sum')
    inklusivitas_jumlah['Jumlah Skor'] = inklusivitas_jumlah['Sarana dan Prasarana Khusus']
    inklusivitas_banyak = data.groupby(['Unit Eselon II'])[['Sarana dan Prasarana Khusus']].agg('count')
    inklusivitas_banyak['Banyak Data'] = inklusivitas_banyak['Sarana dan Prasarana Khusus']
    inklusivitas_rata = (inklusivitas_jumlah['Jumlah Skor'] / inklusivitas_banyak['Banyak Data']).round(2).sort_values(ascending=False)
    st.table(inklusivitas_rata.to_frame().style.format("{:.2f}"), border=False, hide_header=True)