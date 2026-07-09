# 01. IMPOR LIBRARY
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_gsheets import GSheetsConnection


# 02. KONFIGURASI HALAMAN
st.set_page_config(page_title="Dashboard", layout="wide")
st.title(":blue[e-SKPL (Survei Kepuasan Pengguna Layanan) DJSEF]")


# 03. LOAD DATA
conn_dash = st.connection("gsheets_data", type=GSheetsConnection, ttl=120)
data = conn_dash.read()


# 04. DATA PREPARATION
# Menyesuaikan Data Tanggal
data['Last Submitted'] = pd.to_datetime(data['Last Submitted'], dayfirst=True)
data['Tahun'] = data['Last Submitted'].dt.year
data['Bulan ke-'] = data['Last Submitted'].dt.month
data['Bulan'] = data['Bulan ke-'].astype(str)
bulan_kamus = {
    "1":"Januari",
    "2":"Februari",
    "3":"Maret",
    "4":"April",
    "5":"Mei",
    "6":"Juni",
    "7":"Juli",
    "8":"Agustus",
    "9":"September",
    "10":"Oktober",
    "11":"November",
    "12":"Desember"
}
data['Bulan'] = data['Bulan'].str.replace(pat=bulan_kamus)
bulan_urut = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember"
]
data['Bulan'] = pd.Categorical(data['Bulan'], categories=bulan_urut, ordered=True)

# Menyesuaikan Data Unit Eselon II
data['Unit Eselon II'] = data['Unit Kerja']
ue2_kamus = {
    "Sekretariat Direktorat Jenderal Strategi Ekonomi Dan Fiskal":"Setditjen",
    "Direktorat Strategi Stabilisasi Ekonomi":"DSSE",
    "Direktorat Strategi Kesejahteraan dan Pemerataan Ekonomi":"DSKPE",
    "Direktorat Strategi Produktivitas dan Pertumbuhan Ekonomi":"DSPPE",
    "Direktorat Strategi Perpajakan":"DSP",
    "Direktorat Strategi Penerimaan Negara Bukan Pajak":"DSPNBP",
    "Direktorat Strategi Anggaran Pendapatan dan Belanja Negara":"DSAPBN"
}
data['Unit Eselon II'] = data['Unit Eselon II'].str.replace(pat=ue2_kamus)
ue2_urut = (
    "Setditjen",
    "DSSE",
    "DSKPE",
    "DSPPE",
    "DSP",
    "DSPNBP",
    "DSAPBN"
)
data['Unit Eselon II'] = pd.Categorical(data['Unit Eselon II'], categories=ue2_urut, ordered=True)

# Menyesuaikan Data Layanan
data['detil_kategori_layanan_input'] = data['detil_kategori_layanan_input'].str.replace("Pelayanan Dokumen Kerangka Ekonomi Makro dan Pokok-Pokok Kebijakan Fiskal/ KEMPPKF", "Pelayanan Dokumen Kerangka Ekonomi Makro dan Pokok-Pokok Kebijakan Fiskal (KEM PPKF)", regex=False)
data['Layanan'] = data['detil_kategori_layanan_input']
layanan_kamus = {
    "Pelayanan Riset dan/atau Wawancara":"Riset/Wawancara",
    "Pelayanan Magang Mahasiswa":"Magang Mahasiswa",
    "Pelayanan Informasi Publik (Pejabat Pengelola Informasi dan Dokumentasi/PPID)":"PPID",
    "Pelayanan Application Programming Interface (API) Nilai Kurs":"API Nilai Kurs",
    "Pelayanan Dokumen Kerangka Ekonomi Makro dan Pokok-Pokok Kebijakan Fiskal (KEM PPKF)":"KEM PPKF",
    "Pelayanan Informasi Nilai Kurs Perpajakan":"Informasi Kurs Perpajakan",
    "Pelayanan Informasi Tarif Bunga":"Informasi Tarif Bunga",
    "Pelayanan Diskusi Strategi Kesejahteraan dan Pemerataan Ekonomi":"Diskusi Strategi KPE",
    "Pelayanan Kelas GrowLab":"GrowLab",
    "Pelayanan Audiensi dan/atau Diskusi Kebijakan Perpajakan":"Aud./Dis. Perpajakan",
    "Pelayanan Audiensi dan/atau Diskusi Kebijakan Penerimaan Negara Bukan Pajak (PNBP)":"Aud./Dis. PNBP",
    "Pelayanan Kelas Skenario Fiskal":"Skenario Fiskal"
}
data['Layanan'] = data['Layanan'].str.replace(pat=layanan_kamus)

# Menghitung Data Indeks SKM
data['Jumlah Skor SKM'] = data[['Aspek Kejelasan Informasi Biaya/Tarif', 'Aspek Kemudahan Persyaratan', 'Aspek Kemudahan Prosedur', 'Aspek Kesesuaian Produk', 'Aspek Ketepatan Waktu', 'Aspek Kompetensi Petugas', 'Aspek Media atau Tempat Pengaduan', 'Aspek Perilaku Petugas', 'Aspek Sarana dan Prasarana', 'E-service - Kualitas informasi', 'E-service - Kualitas bantuan', 'E-service - Kemudahaan penggunaan', 'E-service - Privasi dan Keamanan data', 'aspek_kecepatan_e-service']].sum(axis=1)
data['Banyak Data SKM'] = data[['Aspek Kejelasan Informasi Biaya/Tarif', 'Aspek Kemudahan Persyaratan', 'Aspek Kemudahan Prosedur', 'Aspek Kesesuaian Produk', 'Aspek Ketepatan Waktu', 'Aspek Kompetensi Petugas', 'Aspek Media atau Tempat Pengaduan', 'Aspek Perilaku Petugas', 'Aspek Sarana dan Prasarana', 'E-service - Kualitas informasi', 'E-service - Kualitas bantuan', 'E-service - Kemudahaan penggunaan', 'E-service - Privasi dan Keamanan data', 'aspek_kecepatan_e-service']].count(axis=1)
data['Indeks SKM per Responden'] = (data['Jumlah Skor SKM'] / data['Banyak Data SKM'])

# Menghitung Data Indeks Aspek e-Services
data['Jumlah Skor e-Services'] = data[['E-service - Kualitas informasi', 'E-service - Kualitas bantuan', 'E-service - Kemudahaan penggunaan', 'E-service - Privasi dan Keamanan data', 'aspek_kecepatan_e-service']].sum(axis=1)
data['Banyak Data e-Services'] = data[['E-service - Kualitas informasi', 'E-service - Kualitas bantuan', 'E-service - Kemudahaan penggunaan', 'E-service - Privasi dan Keamanan data', 'aspek_kecepatan_e-service']].count(axis=1)
data['Indeks e-Services per Responden'] = (data['Jumlah Skor e-Services'] / data['Banyak Data e-Services'])

# Menghitung Data IPAK
data['Jumlah Skor IPAK'] = data[['Persepsi - Tidak ada diskriminasi pelayanan', 'Persepsi - Tidak ada pelayanan di luar prosedur', 'Persepsi - Tidak ada pencaloan', 'Persepsi - Tidak ada penerimaan imbalan', 'Persepsi - Tidak ada pungutan liar']].sum(axis=1)
data['Banyak Data IPAK'] = data[['Persepsi - Tidak ada diskriminasi pelayanan', 'Persepsi - Tidak ada pelayanan di luar prosedur', 'Persepsi - Tidak ada pencaloan', 'Persepsi - Tidak ada penerimaan imbalan', 'Persepsi - Tidak ada pungutan liar']].count(axis=1)
data['IPAK per Responden'] = (data['Jumlah Skor IPAK'] / data['Banyak Data IPAK'])

# Menghitung Data Indeks Inklusivitas
data['Jumlah Skor Inklusivitas'] = data[['Sarana dan Prasarana Khusus']].sum(axis=1)
data['Banyak Data Inklusivitas'] = data[['Sarana dan Prasarana Khusus']].count(axis=1)
data['Indeks Inklusivitas per Responden'] = (data['Jumlah Skor Inklusivitas'] / data['Banyak Data Inklusivitas'])

# Menentukan Validitas Responden
data['Validitas'] = ""
data.loc[data['akurasi_pengisian'] == 3, 'Validitas'] = 'VALID'
data.loc[data['akurasi_pengisian'] != 3, 'Validitas'] = 'INVALID'

# Mengurutkan Data Berdasarkan Tanggal Responden Terakhir Mengisi Survei
data = data.sort_values(by='Last Submitted')


# 05. PENYIMPANAN DATA
if "data" not in st.session_state:
    st.session_state["data"] = data


# 06. VISUALISASI DATA JUMLAH SELURUH RESPONDEN
# Membuat Kolom Data Responden
col_dr_01, col_dr_02, col_dr_03, col_dr_04 = st.columns(4)
with col_dr_01:
    st.write(f":blue-badge[:material/done_all: Total SELURUH Responden:] {len(data)}")
with col_dr_02:
    st.write(f":green-badge[:material/person_check: Total Responden VALID:] {(data['Validitas'] == 'VALID').sum()}")
with col_dr_03:
    st.write(f":red-badge[:material/person_off: Total Responden INVALID:] {(data['Validitas'] == 'INVALID').sum()}")
with col_dr_04:
    st.write(f":blue-badge[:material/apps: Jumlah LAYANAN:] {data['Layanan'].nunique()}")

# Tanggal Responden Terakhir Mengisi Survei
st.badge(f"Data Masuk Terakhir: {data.loc[data.index[-1], 'Last Submitted']}", icon=":material/database:", color="blue")


# 07. FILTER DATA
# Variabel untuk Filter Data
validitas_saring = data['Validitas'].sort_values().dropna().unique()
ue2_saring = data['Unit Eselon II'].sort_values().dropna().unique()
tahun_saring = data['Tahun'].sort_values().dropna().unique()

# Catatan untuk Filter Data
st.write(":orange-badge[Untuk memilih **Layanan**, silakan memilih **Unit Eselon II** terlebih dahulu :smile:]")
st.write(":orange-badge[Untuk memilih **Bulan**, silakan memilih **Tahun** terlebih dahulu :smile:]")
st.write(":orange-badge[Untuk menampilkan **Data Triwulanan**, silakan pilih **Seluruh Bulan** yang termasuk dalam **Triwulan bersangkutan** :smile:]")

# Membuat Kolom Selector untuk Filter Data
col_wf_01, col_wf_02, col_wf_03, col_wf_04, col_wf_05 = st.columns(5)
with col_wf_01:
    validitas_widget = st.multiselect(":material/person_edit: Status Responden:", validitas_saring, default="VALID")
    if validitas_widget:
        data = data[data['Validitas'].isin(validitas_widget)]
with col_wf_02:
    ue2_widget = st.multiselect(":material/moving_ministry: Unit Eselon II:", ue2_saring)
    if ue2_widget:
        data = data[data['Unit Eselon II'].isin(ue2_widget)]
        layanan_saring = data['Layanan'].sort_values().dropna().unique()
    else:
        layanan_saring = []
with col_wf_03:
    layanan_widget = st.multiselect(":material/apps: Layanan:", layanan_saring)
    if layanan_widget:
        data = data[data['Layanan'].isin(layanan_widget)]
with col_wf_04:
    tahun_widget = st.multiselect(":material/date_range: Tahun:", tahun_saring)
    if tahun_widget:
        data = data[data['Tahun'].isin(tahun_widget)]
        periode_saring = data['Bulan'].sort_values().dropna().unique()
    else:
        periode_saring = []
with col_wf_05:
    periode_widget = st.multiselect(":material/calendar_month: Bulan:", periode_saring)
    if periode_widget:
        data = data[data['Bulan'].isin(periode_widget)]

# Visualisasi Jumlah Responden dan Layanan Berdasarkan Hasil Filter Data
# Membuat Kolom Jumlah Responden dan Layanan Berdasarkan Hasil Filter Data
col_uw_01, col_uw_02, col_uw_03, col_uw_04 = st.columns(4)
#with col_uw_01:
#    st.write(f":blue-badge[:material/done_all: SELURUH Responden:] {len(data)}")
with col_uw_02:
    st.write(f":green-badge[:material/person_check: Responden VALID:] {(data['Validitas'] == 'VALID').sum()}")
#with col_uw_03:
#    st.write(f":red-badge[:material/person_off: Responden INVALID:] {(data['Validitas'] == 'INVALID').sum()}")
with col_uw_04:
    st.write(f":blue-badge[:material/apps: Jumlah LAYANAN:] {data['Layanan'].nunique()}")


# 08. VISUALISASI DATA
# Skor Indeks
st.header("Skor Indeks", text_alignment="center", divider=True)

# Menghitung Indeks SKM Saat Ini
nilai_skm = np.sum(data['Jumlah Skor SKM'])
terisi_skm = np.sum(data['Banyak Data SKM'])
rata_skm = (nilai_skm / terisi_skm).round(2) # Skala 5
rata_skm_s4 = rata_skm * 0.8 # Skala 4
rata_skm_s100 = rata_skm * 20 # Skala 100

# Menghitung IPAK Saat Ini
nilai_ipak = np.sum(data['Jumlah Skor IPAK'])
terisi_ipak = np.sum(data['Banyak Data IPAK'])
rata_ipak = (nilai_ipak / terisi_ipak).round(2) # Skala 5
rata_ipak_s4 = rata_ipak * 0.8 # Skala 4
rata_ipak_s100 = rata_ipak * 20 # Skala 100

# Menghitung Indeks Inklusivitas Saat Ini
nilai_inklusivitas = data['Sarana dan Prasarana Khusus'].sum()
terisi_inklusivitas = data['Sarana dan Prasarana Khusus'].count()
rata_inklusivitas = (nilai_inklusivitas / terisi_inklusivitas).round(2) # Skala 5
rata_inklusivitas_s4 = rata_inklusivitas * 0.8 # Skala 4
rata_inklusivitas_s100 = rata_inklusivitas * 20 # Skala 100

# Visualisasi Indeks SKM, IPAK, dan Indeks Inklusivitas Beserta Kenaikan/Penurunan
# Membuat Kolom Indeks SKM, IPAK, dan Indeks Inklusivitas Beserta Kenaikan/Penurunan
col_nf_01, col_nf_02, col_nf_03 = st.columns(3)
with col_nf_01:
    st.subheader("SKM", text_alignment="center", divider="orange")
    col_nf_01_a, col_nf_01_b = st.columns(2)
    col_nf_01_c, col_nf_01_d = st.columns(2)
    col_nf_01_a.metric("Skala 5", rata_skm, border=True, format="%.2f")
    col_nf_01_b.metric("Skala 4", rata_skm_s4, border=True, format="%.2f")
    col_nf_01_c.metric("Skala 100", rata_skm_s100, border=True, format="%.2f")
with col_nf_02:
    st.subheader("IPAK", text_alignment="center", divider="green")
    col_nf_02_a, col_nf_02_b = st.columns(2)
    col_nf_02_c, col_nf_02_d = st.columns(2)
    col_nf_02_a.metric("Skala 5", rata_ipak, border=True, format="%.2f")
    col_nf_02_b.metric("Skala 4", rata_ipak_s4, border=True, format="%.2f")
    col_nf_02_c.metric("Skala 100", rata_ipak_s100, border=True, format="%.2f")
with col_nf_03:
    st.subheader("Inklusivitas", text_alignment="center", divider="blue")
    col_nf_03_a, col_nf_03_b = st.columns(2)
    col_nf_03_c, col_nf_03_d = st.columns(2)
    col_nf_03_a.metric("Skala 5", rata_inklusivitas, border=True, format="%.2f")
    col_nf_03_b.metric("Skala 4", rata_inklusivitas_s4, border=True, format="%.2f")
    col_nf_03_c.metric("Skala 100", rata_inklusivitas_s100, border=True, format="%.2f")

# Tren Indeks
st.header("Tren Indeks SKM", text_alignment="center", divider=True)

# Membuat Tabel Baru
tren_kolom = data[['Bulan', 'Unit Eselon II', 'Jumlah Skor SKM', 'Banyak Data SKM']]
tren_jumlah = tren_kolom.groupby(['Unit Eselon II', 'Bulan'])[['Jumlah Skor SKM']].sum().reset_index()
tren_banyak = tren_kolom.groupby(['Unit Eselon II', 'Bulan'])[['Banyak Data SKM']].sum().reset_index()
tren_tabel = pd.merge(tren_jumlah, tren_banyak, how='outer')
tren_tabel['Kumulatif Jumlah Skor SKM'] = tren_tabel.groupby('Unit Eselon II')['Jumlah Skor SKM'].cumsum()
tren_tabel['Kumulatif Banyak Data SKM'] = tren_tabel.groupby('Unit Eselon II')['Banyak Data SKM'].cumsum()
tren_tabel['Indeks SKM'] = (tren_tabel['Kumulatif Jumlah Skor SKM'] / tren_tabel['Kumulatif Banyak Data SKM']).round(2)
tren_tabel.columns = ['Unit Eselon II', 'Bulan', 'Jumlah Skor SKM', 'Banyak Data SKM', 'Kumulatif Jumlah Skor SKM', 'Kumulatif Banyak Data SKM', 'Indeks SKM']

# Visualisasi Tren Indeks SKM
tren_skm = px.line(tren_tabel, x='Bulan', y='Indeks SKM', color='Unit Eselon II', markers=True, symbol='Unit Eselon II', height=450, category_orders={'Bulan': bulan_urut})
tren_skm.add_hline(y=4.36, line_dash="dash", line_color='violet', annotation_text="Garis - - - adalah Target Indeks = 4.36", annotation_position="bottom left")
tren_skm.update_traces(marker=dict(size=7.5))
st.plotly_chart(tren_skm)

# Statistik Responden
st.header("Statistik Responden", text_alignment="center", divider=True)

# Visualisasi Statistik Responden
# Membuat Kolom Grafik Statistik Responden
col_sr_01, col_sr_02, col_sr_03 = st.columns(3)
col_sr_04, col_sr_05, col_sr_06 = st.columns(3)
col_sr_07, col_sr_08, col_sr_09 = st.columns(3)
col_sr_10, col_sr_11, col_sr_12 = st.columns(3)
with col_sr_01:
    # Membuat Tabel Baru
    kelamin_kolom = pd.DataFrame(data['Jenis Kelamin'])
    kelamin_hitung = kelamin_kolom['Jenis Kelamin'].value_counts().reset_index()
    kelamin_hitung.columns = ['Jenis Kelamin', 'Jumlah']
    # Visualisasi Grafik
    kelamin_grafik = px.pie(kelamin_hitung, names='Jenis Kelamin', values='Jumlah', title="Jenis Kelamin", width=300, height=300)
    st.plotly_chart(kelamin_grafik)
with col_sr_02:
    # Membuat Tabel Baru
    usia_kolom = pd.DataFrame(data['Usia'])
    usia_hitung = usia_kolom['Usia'].value_counts().reset_index()
    usia_hitung.columns = ['Usia', 'Jumlah']
    # Visualisasi Grafik
    usia_grafik = px.pie(usia_hitung, names='Usia', values='Jumlah', title="Usia", width=300, height=300)
    st.plotly_chart(usia_grafik)
with col_sr_03:
    # Membuat Tabel Baru
    pendidikan_kolom = pd.DataFrame(data['Pendidikan Terakhir'])
    pendidikan_hitung = pendidikan_kolom['Pendidikan Terakhir'].value_counts().reset_index()
    pendidikan_hitung.columns = ['Pendidikan Terakhir', 'Jumlah']
    # Visualisasi Grafik
    pendidikan_grafik = px.pie(pendidikan_hitung, names='Pendidikan Terakhir', values='Jumlah', title="Pendidikan Terakhir", width=300, height=300)
    st.plotly_chart(pendidikan_grafik)
with col_sr_04:
    # Membuat Tabel Baru
    pekerjaan_kolom = pd.DataFrame(data['Pekerjaan'])
    pekerjaan_hitung = pekerjaan_kolom['Pekerjaan'].value_counts().reset_index()
    pekerjaan_hitung.columns = ['Pekerjaan', 'Jumlah']
    # Visualisasi Grafik
    pekerjaan_grafik = px.pie(pekerjaan_hitung, names='Pekerjaan', values='Jumlah', title="Pekerjaan", width=300, height=300)
    st.plotly_chart(pekerjaan_grafik)
with col_sr_05:
    # Membuat Tabel Baru
    terakhir_kolom = pd.DataFrame(data['Kapan terakhir kali Anda menerima Layanan ini ?'])
    terakhir_hitung = terakhir_kolom['Kapan terakhir kali Anda menerima Layanan ini ?'].value_counts().reset_index()
    terakhir_hitung.columns = ['Terakhir Dilayani', 'Jumlah']
    # Visualisasi Grafik
    terakhir_grafik = px.pie(terakhir_hitung, names='Terakhir Dilayani', values='Jumlah', title="Terakhir Kali Menerima Layanan", width=300, height=300)
    st.plotly_chart(terakhir_grafik)
with col_sr_06:
    # Membuat Tabel Baru
    frekuensi_kolom = pd.DataFrame(data['Seberapa sering Anda menggunakan layanan ini ?'])
    frekuensi_hitung = frekuensi_kolom['Seberapa sering Anda menggunakan layanan ini ?'].value_counts().reset_index()
    frekuensi_hitung.columns = ['Frekuensi Dilayani', 'Jumlah']
    # Visualisasi Grafik
    frekuensi_grafik = px.pie(frekuensi_hitung, names='Frekuensi Dilayani', values='Jumlah', title="Frekuensi Menerima Layanan", width=300, height=300)
    st.plotly_chart(frekuensi_grafik)
with col_sr_07:
    # Membuat Tabel Baru
    media_kolom = pd.DataFrame(data['mekanisme_layanan'])
    media_hitung = media_kolom['mekanisme_layanan'].value_counts().reset_index()
    media_hitung.columns = ['Media Layanan', 'Jumlah']
    # Visualisasi Grafik
    media_grafik = px.pie(media_hitung, names='Media Layanan', values='Jumlah', title="Mekanisme Layanan", width=300, height=300)
    st.plotly_chart(media_grafik)
with col_sr_08:
    # Membuat Tabel Baru
    komplain_kolom = pd.DataFrame(data['Apakah Anda PERNAH melakukan pengaduan (complain) terkait pelayanan ini ?'])
    komplain_hitung = komplain_kolom['Apakah Anda PERNAH melakukan pengaduan (complain) terkait pelayanan ini ?'].value_counts().reset_index()
    komplain_hitung.columns = ['Pernah Komplain', 'Jumlah']
    # Visualisasi Grafik
    komplain_grafik = px.pie(komplain_hitung, names='Pernah Komplain', values='Jumlah', title="Pernah Komplain?", width=300, height=300)
    st.plotly_chart(komplain_grafik)
with col_sr_09:
    # Membuat Tabel Baru
    komplain_media_kolom = pd.DataFrame(data['Media apa yang menjadi sarana pengaduan Anda?'])
    komplain_media_hitung = komplain_media_kolom['Media apa yang menjadi sarana pengaduan Anda?'].value_counts().reset_index()
    komplain_media_hitung.columns = ['Media Komplain', 'Jumlah']
    # Visualisasi Grafik
    komplain_media_grafik = px.pie(komplain_media_hitung, names='Media Komplain', values='Jumlah', title="Media Komplain", width=300, height=300)
    st.plotly_chart(komplain_media_grafik)
with col_sr_10:
    # Membuat Tabel Baru
    disabilitas_kolom = pd.DataFrame(data['disabilitas'])
    disabilitas_hitung = disabilitas_kolom['disabilitas'].value_counts().reset_index()
    disabilitas_hitung.columns = ['Disabilitas', 'Jumlah']
    # Visualisasi Grafik
    disabilitas_grafik = px.pie(disabilitas_hitung, names='Disabilitas', values='Jumlah', title="Penyandang Disabilitas", width=300, height=300)
    st.plotly_chart(disabilitas_grafik)

# Membuat Variabel Urutan Skor Survei (Tertinggi ke Terendah)
skor_urut = [5, 4, 3, 2, 1]

# Hasil SKM
st.header("Hasil SKM (Survei Kepuasan Masyarakat)", text_alignment="center", divider=True)

# Menghitung Jumlah Skor Saat Ini dari Setiap Aspek
jumlah_persyaratan = data['Aspek Kemudahan Persyaratan'].sum()
jumlah_prosedur = data['Aspek Kemudahan Prosedur'].sum()
jumlah_waktu = data['Aspek Ketepatan Waktu'].sum()
jumlah_biaya = data['Aspek Kejelasan Informasi Biaya/Tarif'].sum()
jumlah_produk = data['Aspek Kesesuaian Produk'].sum()
jumlah_kompetensi = data['Aspek Kompetensi Petugas'].sum()
jumlah_perilaku = data['Aspek Perilaku Petugas'].sum()
jumlah_sarpras = data['Aspek Sarana dan Prasarana'].sum()
jumlah_penanganan = data['Aspek Media atau Tempat Pengaduan'].sum()

# Menghitung Banyak Data Saat Ini dari Setiap Aspek
banyak_persyaratan = data['Aspek Kemudahan Persyaratan'].count()
banyak_prosedur = data['Aspek Kemudahan Prosedur'].count()
banyak_waktu = data['Aspek Ketepatan Waktu'].count()
banyak_biaya = data['Aspek Kejelasan Informasi Biaya/Tarif'].count()
banyak_produk = data['Aspek Kesesuaian Produk'].count()
banyak_kompetensi = data['Aspek Kompetensi Petugas'].count()
banyak_perilaku = data['Aspek Perilaku Petugas'].count()
banyak_sarpras = data['Aspek Sarana dan Prasarana'].count()
banyak_penanganan = data['Aspek Media atau Tempat Pengaduan'].count()

# Menghitung Skor Rata-Rata Saat Ini dari Setiap Aspek
rata_persyaratan = (jumlah_persyaratan / banyak_persyaratan).round(2) # Skala 5
rata_persyaratan_s4 = rata_persyaratan * 0.8 # Skala 4
rata_persyaratan_s100 = rata_persyaratan * 20 # Skala 100
rata_prosedur = (jumlah_prosedur / banyak_prosedur).round(2) # Skala 5
rata_prosedur_s4 = rata_prosedur * 0.8 # Skala 4
rata_prosedur_s100 = rata_prosedur * 20 # Skala 100
rata_waktu = (jumlah_waktu / banyak_waktu).round(2) # Skala 5
rata_waktu_s4 = rata_waktu * 0.8 # Skala 4
rata_waktu_s100 = rata_waktu * 20 # Skala 100
rata_biaya = (jumlah_biaya / banyak_biaya).round(2) # Skala 5
rata_biaya_s4 = rata_biaya * 0.8 # Skala 4
rata_biaya_s100 = rata_biaya * 20 # Skala 100
rata_produk = (jumlah_produk / banyak_produk).round(2) # Skala 5
rata_produk_s4 = rata_produk * 0.8 # Skala 4
rata_produk_s100 = rata_produk * 20 # Skala 100
rata_kompetensi = (jumlah_kompetensi / banyak_kompetensi).round(2) # Skala 5
rata_kompetensi_s4 = rata_kompetensi * 0.8 # Skala 4
rata_kompetensi_s100 = rata_kompetensi * 20 # Skala 100
rata_perilaku = (jumlah_perilaku / banyak_perilaku).round(2) # Skala 5
rata_perilaku_s4 = rata_perilaku * 0.8 # Skala 4
rata_perilaku_s100 = rata_perilaku * 20 # Skala 100
rata_sarpras = (jumlah_sarpras / banyak_sarpras).round(2) # Skala 5
rata_sarpras_s4 = rata_sarpras * 0.8 # Skala 4
rata_sarpras_s100 = rata_sarpras * 20 # Skala 100
rata_penanganan = (jumlah_penanganan / banyak_penanganan).round(2) # Skala 5
rata_penanganan_s4 = rata_penanganan * 0.8 # Skala 4
rata_penanganan_s100 = rata_penanganan * 20 # Skala 100

# Membuat Kolom Grafik Setiap Aspek SKM
col_dskm_01, col_dskm_02, col_dskm_03 = st.columns(3)
col_dskm_04, col_dskm_05, col_dskm_06 = st.columns(3)
col_dskm_07, col_dskm_08, col_dskm_09 = st.columns(3)
with col_dskm_01:
    # Membuat Tabel Baru
    persyaratan_kolom = pd.DataFrame(data['Aspek Kemudahan Persyaratan'])
    persyaratan_hitung = persyaratan_kolom['Aspek Kemudahan Persyaratan'].value_counts().reset_index()
    persyaratan_hitung.rename(columns={'Aspek Kemudahan Persyaratan': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    persyaratan_grafik = px.bar(persyaratan_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Kemudahan Persyaratan", subtitle=f"Indeks: {rata_persyaratan}", height=300, text_auto=True)
    persyaratan_grafik.update_xaxes(type='category')
    persyaratan_grafik.update_traces(textangle=0)
    st.plotly_chart(persyaratan_grafik)
with col_dskm_02:
    # Membuat Tabel Baru
    prosedur_kolom = pd.DataFrame(data['Aspek Kemudahan Prosedur'])
    prosedur_hitung = prosedur_kolom['Aspek Kemudahan Prosedur'].value_counts().reset_index()
    prosedur_hitung.rename(columns={'Aspek Kemudahan Prosedur': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    prosedur_grafik = px.bar(prosedur_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Kemudahan Prosedur", subtitle=f"Indeks: {rata_prosedur}", height=300, text_auto=True)
    prosedur_grafik.update_xaxes(type='category')
    prosedur_grafik.update_traces(textangle=0)
    st.plotly_chart(prosedur_grafik)
with col_dskm_03:
    # Membuat Tabel Baru
    waktu_kolom = pd.DataFrame(data['Aspek Ketepatan Waktu'])
    waktu_hitung = waktu_kolom['Aspek Ketepatan Waktu'].value_counts().reset_index()
    waktu_hitung.rename(columns={'Aspek Ketepatan Waktu': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    waktu_grafik = px.bar(waktu_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Ketepatan Waktu", subtitle=f"Indeks: {rata_waktu}", height=300, text_auto=True)
    waktu_grafik.update_xaxes(type='category')
    waktu_grafik.update_traces(textangle=0)
    st.plotly_chart(waktu_grafik)
with col_dskm_04:
    # Membuat Tabel Baru
    biaya_kolom = pd.DataFrame(data['Aspek Kejelasan Informasi Biaya/Tarif'])
    biaya_hitung = biaya_kolom['Aspek Kejelasan Informasi Biaya/Tarif'].value_counts().reset_index()
    biaya_hitung.rename(columns={'Aspek Kejelasan Informasi Biaya/Tarif': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    biaya_grafik = px.bar(biaya_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Kejelasan Informasi Biaya/Tarif", subtitle=f"Indeks: {rata_biaya}", height=300, text_auto=True)
    biaya_grafik.update_xaxes(type='category')
    biaya_grafik.update_traces(textangle=0)
    st.plotly_chart(biaya_grafik)
with col_dskm_05:
    # Membuat Tabel Baru
    produk_kolom = pd.DataFrame(data['Aspek Kesesuaian Produk'])
    produk_hitung = produk_kolom['Aspek Kesesuaian Produk'].value_counts().reset_index()
    produk_hitung.rename(columns={'Aspek Kesesuaian Produk': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    produk_grafik = px.bar(produk_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Kesesuaian Produk", subtitle=f"Indeks: {rata_produk}", height=300, text_auto=True)
    produk_grafik.update_xaxes(type='category')
    produk_grafik.update_traces(textangle=0)
    st.plotly_chart(produk_grafik)
with col_dskm_06:
    # Membuat Tabel Baru
    kompetensi_kolom = pd.DataFrame(data['Aspek Kompetensi Petugas'])
    kompetensi_hitung = kompetensi_kolom['Aspek Kompetensi Petugas'].value_counts().reset_index()
    kompetensi_hitung.rename(columns={'Aspek Kompetensi Petugas': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    kompetensi_grafik = px.bar(kompetensi_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Kompetensi Petugas", subtitle=f"Indeks: {rata_kompetensi}", height=300, text_auto=True)
    kompetensi_grafik.update_xaxes(type='category')
    kompetensi_grafik.update_traces(textangle=0)
    st.plotly_chart(kompetensi_grafik)
with col_dskm_07:
    # Membuat Tabel Baru
    perilaku_kolom = pd.DataFrame(data['Aspek Perilaku Petugas'])
    perilaku_hitung = perilaku_kolom['Aspek Perilaku Petugas'].value_counts().reset_index()
    perilaku_hitung.rename(columns={'Aspek Perilaku Petugas': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    perilaku_grafik = px.bar(perilaku_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Perilaku Petugas", subtitle=f"Indeks: {rata_perilaku}", height=300, text_auto=True)
    perilaku_grafik.update_xaxes(type='category')
    perilaku_grafik.update_traces(textangle=0)
    st.plotly_chart(perilaku_grafik)
with col_dskm_08:
    # Membuat Tabel Baru
    sarpras_kolom = pd.DataFrame(data['Aspek Sarana dan Prasarana'])
    sarpras_hitung = sarpras_kolom['Aspek Sarana dan Prasarana'].value_counts().reset_index()
    sarpras_hitung.rename(columns={'Aspek Sarana dan Prasarana': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    sarpras_grafik = px.bar(sarpras_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Sarana dan Prasarana", subtitle=f"Indeks: {rata_sarpras}", height=300, text_auto=True)
    sarpras_grafik.update_xaxes(type='category')
    sarpras_grafik.update_traces(textangle=0)
    st.plotly_chart(sarpras_grafik)
with col_dskm_09:
    # Membuat Tabel Baru
    penanganan_kolom = pd.DataFrame(data['Aspek Media atau Tempat Pengaduan'])
    penanganan_hitung = penanganan_kolom['Aspek Media atau Tempat Pengaduan'].value_counts().reset_index()
    penanganan_hitung.rename(columns={'Aspek Media atau Tempat Pengaduan': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    penanganan_grafik = px.bar(penanganan_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Aspek Media atau Tempat Pengaduan", subtitle=f"Indeks: {rata_penanganan}", height=300, text_auto=True)
    penanganan_grafik.update_xaxes(type='category')
    penanganan_grafik.update_traces(textangle=0)
    st.plotly_chart(penanganan_grafik)

# Visualisasi Spider Plot
radar_skm = px.line_polar(data, r=[rata_persyaratan_s4, rata_prosedur_s4, rata_waktu_s4, rata_biaya_s4, rata_produk_s4, rata_kompetensi_s4, rata_perilaku_s4, rata_sarpras_s4, rata_penanganan_s4], theta=['Kemudahan Persyaratan', 'Kemudahan Prosedur', 'Ketepatan Waktu', 'Kejelasan Informasi Biaya/Tarif', 'Kesesuaian Produk', 'Kompetensi Petugas', 'Perilaku Petugas', 'Sarana dan Prasarana', 'Media/Tempat Pengaduan'], line_close=True, markers=True, height=500, width=500)
radar_skm.update_polars(angularaxis=dict(ticks='outside', tickfont_size=20, showgrid=False), radialaxis=dict(dtick=1, tick0=0, range=[0, 4], gridcolor='gray', showline=False, tickfont_size=20, tickfont_color='darkorange'), bgcolor="rgba(0,0,0,0)")
radar_skm.update_traces(mode='lines+markers+text', line=dict(color='navy', width=5), marker=dict(size=15, color='navy'), text=[rata_persyaratan_s4, rata_prosedur_s4, rata_waktu_s4, rata_biaya_s4, rata_produk_s4, rata_kompetensi_s4, rata_perilaku_s4, rata_sarpras_s4, rata_penanganan_s4], texttemplate='%{text:.2f}', textfont_size=20, textfont_color='darkorange', textfont_weight='bold', textposition='bottom center', fill='toself')
st.plotly_chart(radar_skm, theme='streamlit')

# Hasil Aspek e-Services
st.header("Hasil Aspek e-Services", text_alignment="center", divider=True)

# Menghitung Jumlah Skor Saat Ini dari Setiap Aspek
jumlah_eservice_informasi = data['E-service - Kualitas informasi'].sum()
jumlah_eservice_bantuan = data['E-service - Kualitas bantuan'].sum()
jumlah_eservice_kemudahan = data['E-service - Kemudahaan penggunaan'].sum()
jumlah_eservice_privasi = data['E-service - Privasi dan Keamanan data'].sum()
jumlah_eservice_kecepatan = data['aspek_kecepatan_e-service'].sum()

# Menghitung Banyak Data Saat Ini dari Setiap Aspek
banyak_eservice_informasi = data['E-service - Kualitas informasi'].count()
banyak_eservice_bantuan = data['E-service - Kualitas bantuan'].count()
banyak_eservice_kemudahan = data['E-service - Kemudahaan penggunaan'].count()
banyak_eservice_privasi = data['E-service - Privasi dan Keamanan data'].count()
banyak_eservice_kecepatan = data['aspek_kecepatan_e-service'].count()

# Menghitung Skor Rata-Rata Saat Ini dari Setiap Aspek
rata_eservice_informasi = (jumlah_eservice_informasi / banyak_eservice_informasi).round(2)
rata_eservice_bantuan = (jumlah_eservice_bantuan / banyak_eservice_bantuan).round(2)
rata_eservice_kemudahan = (jumlah_eservice_kemudahan / banyak_eservice_kemudahan).round(2)
rata_eservice_privasi = (jumlah_eservice_privasi / banyak_eservice_privasi).round(2)
rata_eservice_kecepatan = (jumlah_eservice_kecepatan / banyak_eservice_kecepatan).round(2)

# Menghitung Indeks Aspek e-Services Saat Ini
nilai_eservice = np.sum(data['Jumlah Skor e-Services'])
terisi_eservice = np.sum(data['Banyak Data e-Services'])
rata_eservice = (nilai_eservice / terisi_eservice).round(2) # Skala 5
rata_eservice_s4 = rata_eservice * 0.8 # Skala 4
rata_eservice_s100 = rata_eservice * 20 # Skala 100

# Subjudul dan Skor Rata-Rata Aspek e-Services
st.subheader(f"Indeks Aspek e-Services: {rata_eservice}")

# Membuat Kolom Grafik Setiap Aspek e-Services
col_des_01, col_des_02, col_des_03, col_des_04, col_des_05 = st.columns(5)
with col_des_01:
    # Membuat Tabel Baru
    informasi_kolom = pd.DataFrame(data['E-service - Kualitas informasi'])
    informasi_hitung = informasi_kolom['E-service - Kualitas informasi'].value_counts().reset_index()
    informasi_hitung.rename(columns={'E-service - Kualitas informasi': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    informasi_grafik = px.bar(informasi_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Kualitas Informasi", subtitle=f"Indeks: {rata_eservice_informasi}", height=300, text_auto=True)
    informasi_grafik.update_xaxes(type='category')
    informasi_grafik.update_traces(textangle=0)
    st.plotly_chart(informasi_grafik)
with col_des_02:
    # Membuat Tabel Baru
    bantuan_kolom = pd.DataFrame(data['E-service - Kualitas bantuan'])
    bantuan_hitung = bantuan_kolom['E-service - Kualitas bantuan'].value_counts().reset_index()
    bantuan_hitung.rename(columns={'E-service - Kualitas bantuan': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    bantuan_grafik = px.bar(bantuan_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Kualitas Bantuan", subtitle=f"Indeks: {rata_eservice_bantuan}", height=300, text_auto=True)
    bantuan_grafik.update_xaxes(type='category')
    bantuan_grafik.update_traces(textangle=0)
    st.plotly_chart(bantuan_grafik)
with col_des_03:
    # Membuat Tabel Baru
    kemudahan_kolom = pd.DataFrame(data['E-service - Kemudahaan penggunaan'])
    kemudahan_hitung = kemudahan_kolom['E-service - Kemudahaan penggunaan'].value_counts().reset_index()
    kemudahan_hitung.rename(columns={'E-service - Kemudahaan penggunaan': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    kemudahan_grafik = px.bar(kemudahan_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Kemudahan Penggunaan", subtitle=f"Indeks: {rata_eservice_kemudahan}", height=300, text_auto=True)
    kemudahan_grafik.update_xaxes(type='category')
    kemudahan_grafik.update_traces(textangle=0)
    st.plotly_chart(kemudahan_grafik)
with col_des_04:
    # Membuat Tabel Baru
    privasi_kolom = pd.DataFrame(data['E-service - Privasi dan Keamanan data'])
    privasi_hitung = privasi_kolom['E-service - Privasi dan Keamanan data'].value_counts().reset_index()
    privasi_hitung.rename(columns={'E-service - Privasi dan Keamanan data': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    privasi_grafik = px.bar(privasi_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Privasi & Keamanan Data", subtitle=f"Indeks: {rata_eservice_privasi}", height=300, text_auto=True)
    privasi_grafik.update_xaxes(type='category')
    privasi_grafik.update_traces(textangle=0)
    st.plotly_chart(privasi_grafik)
with col_des_05:
    # Membuat Tabel Baru
    kecepatan_kolom = pd.DataFrame(data['aspek_kecepatan_e-service'])
    kecepatan_hitung = kecepatan_kolom['aspek_kecepatan_e-service'].value_counts().reset_index()
    kecepatan_hitung.rename(columns={'aspek_kecepatan_e-service': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    kecepatan_grafik = px.bar(kecepatan_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Kecepatan", subtitle=f"Indeks: {rata_eservice_kecepatan}", height=300, text_auto=True)
    kecepatan_grafik.update_xaxes(type='category')
    kecepatan_grafik.update_traces(textangle=0)
    st.plotly_chart(kecepatan_grafik)

# Hasil IPAK
st.header("Hasil IPAK (Indeks Persepsi Anti Korupsi)", text_alignment='center', divider=True)

# Menghitung Jumlah Skor Saat Ini dari Setiap Aspek
jumlah_diskriminasi = data['Persepsi - Tidak ada diskriminasi pelayanan'].sum()
jumlah_kecurangan = data['Persepsi - Tidak ada pelayanan di luar prosedur'].sum()
jumlah_imbalan = data['Persepsi - Tidak ada penerimaan imbalan'].sum()
jumlah_pungli = data['Persepsi - Tidak ada pungutan liar'].sum()
jumlah_calo = data['Persepsi - Tidak ada pencaloan'].sum()

# Menghitung Banyak Data Saat Ini dari Setiap Aspek
banyak_diskriminasi = data['Persepsi - Tidak ada diskriminasi pelayanan'].count()
banyak_kecurangan = data['Persepsi - Tidak ada pelayanan di luar prosedur'].count()
banyak_imbalan = data['Persepsi - Tidak ada penerimaan imbalan'].count()
banyak_pungli = data['Persepsi - Tidak ada pungutan liar'].count()
banyak_calo = data['Persepsi - Tidak ada pencaloan'].count()

# Menghitung Skor Rata-Rata Saat Ini dari Setiap Aspek
rata_diskriminasi = (jumlah_diskriminasi / banyak_diskriminasi).round(2) # Skala 5
rata_diskriminasi_s4 = rata_diskriminasi * 0.8 # Skala 4
rata_diskriminasi_s100 = rata_diskriminasi * 20 # Skala 100
rata_kecurangan = (jumlah_kecurangan / banyak_kecurangan).round(2) # Skala 5
rata_kecurangan_s4 = rata_kecurangan * 0.8 # Skala 4
rata_kecurangan_s100 = rata_kecurangan * 20 # Skala 100
rata_imbalan = (jumlah_imbalan / banyak_imbalan).round(2) # Skala 5
rata_imbalan_s4 = rata_imbalan * 0.8 # Skala 4
rata_imbalan_s100 = rata_imbalan * 20 # Skala 100
rata_pungli = (jumlah_pungli / banyak_pungli).round(2) # Skala 5
rata_pungli_s4 = rata_pungli * 0.8 # Skala 4
rata_pungli_s100 = rata_pungli * 20 # Skala 100
rata_calo = (jumlah_calo / banyak_calo).round(2) # Skala 5
rata_calo_s4 = rata_calo * 0.8 # Skala 4
rata_calo_s100 = rata_calo * 20 # Skala 100

# Membuat Kolom Grafik IPAK
col_dipak_01, col_dipak_02, col_dipak_03, col_dipak_04, col_dipak_05 = st.columns(5)
with col_dipak_01:
    # Membuat Tabel Baru
    diskriminasi_kolom = pd.DataFrame(data['Persepsi - Tidak ada diskriminasi pelayanan'])
    diskriminasi_hitung = diskriminasi_kolom['Persepsi - Tidak ada diskriminasi pelayanan'].value_counts().reset_index()
    diskriminasi_hitung.rename(columns={'Persepsi - Tidak ada diskriminasi pelayanan': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    diskriminasi_grafik = px.bar(diskriminasi_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Tidak Ada Diskriminasi", subtitle=f"Indeks: {rata_diskriminasi}", height=300, text_auto=True)
    diskriminasi_grafik.update_xaxes(type='category')
    diskriminasi_grafik.update_traces(textangle=0)
    st.plotly_chart(diskriminasi_grafik)
with col_dipak_02:
    # Membuat Tabel Baru
    kecurangan_kolom = pd.DataFrame(data['Persepsi - Tidak ada pelayanan di luar prosedur'])
    kecurangan_hitung = kecurangan_kolom['Persepsi - Tidak ada pelayanan di luar prosedur'].value_counts().reset_index()
    kecurangan_hitung.rename(columns={'Persepsi - Tidak ada pelayanan di luar prosedur': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    kecurangan_grafik = px.bar(kecurangan_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Tidak Ada Kecurangan", subtitle=f"Indeks: {rata_kecurangan}", height=300, text_auto=True)
    kecurangan_grafik.update_xaxes(type='category')
    kecurangan_grafik.update_traces(textangle=0)
    st.plotly_chart(kecurangan_grafik)
with col_dipak_03:
    # Membuat Tabel Baru
    imbalan_kolom = pd.DataFrame(data['Persepsi - Tidak ada penerimaan imbalan'])
    imbalan_hitung = imbalan_kolom['Persepsi - Tidak ada penerimaan imbalan'].value_counts().reset_index()
    imbalan_hitung.rename(columns={'Persepsi - Tidak ada penerimaan imbalan': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    imbalan_grafik = px.bar(imbalan_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Tidak Ada Imbalan", subtitle=f"Indeks: {rata_imbalan}", height=300, text_auto=True)
    imbalan_grafik.update_xaxes(type='category')
    imbalan_grafik.update_traces(textangle=0)
    st.plotly_chart(imbalan_grafik)
with col_dipak_04:
    # Membuat Tabel Baru
    pungli_kolom = pd.DataFrame(data['Persepsi - Tidak ada pungutan liar'])
    pungli_hitung = pungli_kolom['Persepsi - Tidak ada pungutan liar'].value_counts().reset_index()
    pungli_hitung.rename(columns={'Persepsi - Tidak ada pungutan liar': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    pungli_grafik = px.bar(pungli_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Tidak Ada Pungutan Liar", subtitle=f"Indeks: {rata_pungli}", height=300, text_auto=True)
    pungli_grafik.update_xaxes(type='category')
    pungli_grafik.update_traces(textangle=0)
    st.plotly_chart(pungli_grafik)
with col_dipak_05:
    # Membuat Tabel Baru
    pencaloan_kolom = pd.DataFrame(data['Persepsi - Tidak ada pencaloan'])
    pencaloan_hitung = pencaloan_kolom['Persepsi - Tidak ada pencaloan'].value_counts().reset_index()
    pencaloan_hitung.rename(columns={'Persepsi - Tidak ada pencaloan': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)
    # Visualisasi Grafik
    pencaloan_grafik = px.bar(pencaloan_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Tidak Ada Pencaloan", subtitle=f"Indeks: {rata_calo}", height=300, text_auto=True)
    pencaloan_grafik.update_xaxes(type='category')
    pencaloan_grafik.update_traces(textangle=0)
    st.plotly_chart(pencaloan_grafik)

# Visualisasi Spider Plot
radar_ipak = px.line_polar(data, r=[rata_diskriminasi_s4, rata_kecurangan_s4, rata_imbalan_s4, rata_pungli_s4, rata_calo_s4], theta=['Tidak ada Diskriminasi', 'Tidak ada Kecurangan', 'Tidak ada Imbalan', 'Tidak ada Pungli', 'Tidak ada Pencaloan'], line_close=True, markers=True, height=500, width=500)
radar_ipak.update_polars(angularaxis=dict(ticks='outside', tickfont_size=20, showgrid=False), radialaxis=dict(dtick=1, tick0=0, range=[0, 4], gridcolor='gray', showline=False, tickfont_size=20, tickfont_color='darkorange'), bgcolor="rgba(0,0,0,0)")
radar_ipak.update_traces(mode='lines+markers+text', line=dict(color='navy', width=5), marker=dict(size=15, color='navy'), text=[rata_diskriminasi_s4, rata_kecurangan_s4, rata_imbalan_s4, rata_pungli_s4, rata_calo_s4], texttemplate='%{text:.2f}', textfont_size=20, textfont_color='darkorange', textfont_weight='bold', textposition='middle center', fill='toself')
st.plotly_chart(radar_ipak, theme='streamlit')

# Hasil Inklusivitas
st.header("Hasil Inklusivitas", text_alignment="center", divider=True)

# Membuat Tabel Baru
inklusivitas_kolom = pd.DataFrame(data['Sarana dan Prasarana Khusus'])
inklusivitas_hitung = inklusivitas_kolom['Sarana dan Prasarana Khusus'].value_counts().reset_index()
inklusivitas_hitung.rename(columns={'Sarana dan Prasarana Khusus': 'Skor', 'count': 'Jumlah Responden'}, inplace=True)

# Visualisasi Grafik Indeks Inklusivitas
inklusivitas_grafik = px.bar(inklusivitas_hitung, x='Skor', y='Jumlah Responden', category_orders={'Skor': skor_urut}, title="Sarana dan Prasarana Khusus", subtitle=f"Indeks: {rata_inklusivitas}", height=300, text_auto=True)
inklusivitas_grafik.update_xaxes(type='category')
st.plotly_chart(inklusivitas_grafik)


# DATA MENTAH
with st.expander("Sumber Data"):
    st.write("https://dashboard.kemenkeu.go.id/t/SETJEN-BIROORGANTA/views/eSKPLUE1DJSEF2026/DashboardUE12026?%3Aembed=y&%3Aiid=6&%3AisGuestRedirectFromVizportal=y")