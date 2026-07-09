# 01. IMPOR LIBRARY
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# 02. KONFIGURASI HALAMAN
st.set_page_config(page_title="Analisis Kritik dan Saran")
st.title(":blue[Analisis Kritik dan Saran]", text_alignment="center")


# 03. LOAD DATA
data_sentimen = pd.read_csv('https://drive.google.com/uc?export=download&id=1Ui3FBDoS6ddxqfaqhx7Qsw8IWaHtjE-i', sep=";")
data_topik = pd.read_csv('https://drive.google.com/uc?export=download&id=1Meppim59fyy1pQdMk0wcVSEEZEzkOsCR', sep=";")


# 04. DATA PREPARATION
# Menyesuaikan Data Bulan
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
data_sentimen['Bulan'] = pd.Categorical(data_sentimen['Bulan'], categories=bulan_urut, ordered=True)
data_topik['Bulan'] = pd.Categorical(data_topik['Bulan'], categories=bulan_urut, ordered=True)

# Menyesuaikan Data Unit Eselon II
ue2_urut = (
    "Setditjen",
    "DSSE",
    "DSKPE",
    "DSPPE",
    "DSP",
    "DSPNBP",
    "DSAPBN"
)
data_sentimen['Unit Eselon II'] = pd.Categorical(data_sentimen['Unit Eselon II'], categories=ue2_urut, ordered=True)
data_topik['Unit Eselon II'] = pd.Categorical(data_topik['Unit Eselon II'], categories=ue2_urut, ordered=True)

# Menyesuaikan Data Sentimen
sentimen_kamus = {
    "positive": "Positif",
    "neutral": "Netral",
    "negative": "Negatif"
}
data_sentimen['Sentimen'] = data_sentimen['Sentimen'].str.replace(pat=sentimen_kamus)
sentimen_urut = [
    "Positif",
    "Netral",
    "Negatif"
]
data_sentimen['Sentimen'] = pd.Categorical(data_sentimen['Sentimen'], categories=sentimen_urut, ordered=True)

# Menggabung Tabel
data_sentimen_topik = pd.merge(data_sentimen, data_topik, how='outer')

# Mengurutkan Data Berdasarkan Tanggal Responden Terakhir Mengisi Survei
data_sentimen_topik = data_sentimen_topik.sort_values(by='Last Submitted')

# Tanggal Responden Terakhir Mengisi Survei
st.badge(f"Data Masuk Terakhir: {data_sentimen_topik.loc[data_sentimen_topik.index[-1], 'Last Submitted']}", icon=":material/database:", color="blue")


# 05. FILTER DATA
# Variabel untuk Filter Data
validitas_saring = data_sentimen_topik['Validitas'].sort_values().dropna().unique()
ue2_saring = data_sentimen_topik['Unit Eselon II'].sort_values().dropna().unique()
tahun_saring = data_sentimen_topik['Tahun'].sort_values().dropna().unique()

# Catatan untuk Filter Data
st.write(":orange-badge[Untuk memilih **Layanan**, silakan memilih **Unit Eselon II** terlebih dahulu :smile:]")
st.write(":orange-badge[Untuk memilih **Bulan**, silakan memilih **Tahun** terlebih dahulu :smile:]")
st.write(":orange-badge[Untuk menampilkan **Data Triwulanan**, silakan pilih **Seluruh Bulan** yang termasuk dalam **Triwulan bersangkutan** :smile:]")

# Membuat Kolom Selector untuk Filter Data
col_wks_01, col_wks_02, col_wks_03, col_wks_04, col_wks_05 = st.columns(5)
with col_wks_01:
    validitas_widget = st.multiselect(":material/person_edit: Status Responden:", validitas_saring, default="VALID")
    if validitas_widget:
        data_sentimen_topik = data_sentimen_topik[data_sentimen_topik['Validitas'].isin(validitas_widget)]
with col_wks_02:
    ue2_widget = st.multiselect(":material/moving_ministry: Unit Eselon II:", ue2_saring)
    if ue2_widget:
        data_sentimen_topik = data_sentimen_topik[data_sentimen_topik['Unit Eselon II'].isin(ue2_widget)]
        layanan_saring = data_sentimen_topik['Layanan'].sort_values().dropna().unique()
    else:
        layanan_saring = []
with col_wks_03:
    layanan_widget = st.multiselect(":material/apps: Layanan:", layanan_saring)
    if layanan_widget:
        data_sentimen_topik = data_sentimen_topik[data_sentimen_topik['Layanan'].isin(layanan_widget)]
with col_wks_04:
    tahun_widget = st.multiselect(":material/date_range: Tahun:", tahun_saring)
    if tahun_widget: 
        data_sentimen_topik = data_sentimen_topik[data_sentimen_topik['Tahun'].isin(tahun_widget)]
        periode_saring = data_sentimen_topik['Bulan'].sort_values().dropna().unique()
    else:
        periode_saring = []
with col_wks_05:
    periode_widget = st.multiselect(":material/calendar_month: Bulan:", periode_saring)
    if periode_widget: 
        data_sentimen_topik = data_sentimen_topik[data_sentimen_topik['Bulan'].isin(periode_widget)]


# 06. VISUALISASI DATA
# Tren Sentimen Kritik dan Saran
st.header("Tren Sentimen Kritik dan Saran", text_alignment="center", divider=True)
st.write(":orange-badge[Catatan: **Sentimen Responden** menggunakan ***model library OpenAI***]")

# Membuat Tabel Baru
tabel_sentimen = data_sentimen_topik.groupby(['Tahun', 'Bulan', 'Sentimen']).size().fillna(0).reset_index()
tabel_sentimen.columns = ['Tahun', 'Bulan', 'Sentimen', 'Jumlah']

# Visualisasi Grafik
tren_sentimen = px.line(tabel_sentimen, x='Bulan', y='Jumlah', color='Sentimen', markers=True, symbol='Sentimen', height=500, category_orders={'Bulan': bulan_urut})
tren_sentimen.update_traces(marker=dict(size=7))
st.plotly_chart(tren_sentimen)

# Deteksi Outlier
st.header("Deteksi *Outlier*", text_alignment="center", divider=True)

# Visualisasi Grafik
responden_outlier = px.scatter(data_sentimen_topik, x='Indeks SKM per Responden', y='IPAK per Responden', range_x=[0, 5.5], range_y=[0, 5.5], color='Sentimen', symbol='Sentimen', category_orders={'Sentimen': sentimen_urut})
responden_outlier.update_traces(marker=dict(size=10))
st.plotly_chart(responden_outlier)

# Topik Utama Kritik dan Saran
st.header("Topik Utama Kritik dan Saran", text_alignment="center", divider=True)
st.write(":orange-badge[Catatan: **Ekstraksi Topik** menggunakan ***model library OpenAI***]")

# Impor Library
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Data Preparation
data_sentimen_topik['Topik'] = data_sentimen_topik['Topik'].fillna('').apply(lambda x: x.split())
data_sentimen_topik['Topik'] = data_sentimen_topik['Topik'].astype(str)
data_sentimen_topik['Topik'] = data_sentimen_topik['Topik'].str.lower()
data_sentimen_topik['Topik'] = data_sentimen_topik['Topik'].str.replace(r"\d+", "", regex=True)
data_sentimen_topik['Topik'] = data_sentimen_topik['Topik'].str.replace(r"[^\w\s]", "", regex=True)
data_sentimen_topik['Topik'] = data_sentimen_topik['Topik'].str.strip()

# Visualisasi Data
col_kks_01, col_kks_02, col_kks_03 = st.columns(3)
with col_kks_01:
    st.markdown("Topik Utama dari Sentimen Positif", text_alignment='center')
    tabel_positif = data_sentimen_topik.loc[data_sentimen_topik['Sentimen'] == 'Positif', ['Sentimen', 'Topik']]
    teks_positif = " ".join(map(str, tabel_positif['Topik'].dropna().tolist()))
    if teks_positif and teks_positif.strip():
        wcloud_positif = WordCloud(background_color='white', collocations=False).generate(teks_positif)
        plt.figure(facecolor=None)
        plt.imshow(wcloud_positif)
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.warning("Tidak ada kata POSITIF untuk dibuat WordCloud.")
with col_kks_02:
    st.markdown("Topik Utama dari Sentimen Netral", text_alignment='center')
    tabel_netral = data_sentimen_topik.loc[data_sentimen_topik['Sentimen'] == 'Netral', ['Sentimen', 'Topik']]
    teks_netral = " ".join(map(str, tabel_netral['Topik'].dropna().tolist()))
    if teks_netral and teks_netral.strip():
        wcloud_netral = WordCloud(background_color='white', collocations=False).generate(teks_netral)
        plt.figure(facecolor=None)
        plt.imshow(wcloud_netral)
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.warning("Tidak ada kata NETRAL untuk dibuat WordCloud.")
with col_kks_03:
    st.markdown("Topik Utama dari Sentimen Negatif", text_alignment='center')
    tabel_negatif = data_sentimen_topik.loc[data_sentimen_topik['Sentimen'] == 'Negatif', ['Sentimen', 'Topik']]
    teks_negatif = " ".join(map(str, tabel_negatif['Topik'].dropna().tolist()))
    if teks_negatif and teks_negatif.strip():
        wcloud_negatif = WordCloud(background_color='white', collocations=False).generate(teks_negatif)
        plt.figure(facecolor=None)
        plt.imshow(wcloud_negatif)
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.warning("Tidak ada kata NEGATIF untuk dibuat WordCloud.")

# Menampilkan Tabel Berdasarkan Sentimen
sentimen_saring = data_sentimen_topik['Sentimen'].sort_values().dropna().unique()
sentimen_widget = st.multiselect("Tabel Berdasarkan Sentimen:", sentimen_saring)
if sentimen_widget: 
    data_sentimen_topik = data_sentimen_topik[data_sentimen_topik['Sentimen'].isin(sentimen_widget)]
    st.dataframe(data_sentimen_topik)