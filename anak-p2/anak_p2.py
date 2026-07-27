import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn_anak = st.connection("gsheets_anak", type=GSheetsConnection, ttl=120)
data_anak = conn_anak.read()

st.set_page_config(page_title="Dashboard", layout="wide")
st.title(":blue[Data Anak-Anak dan Remaja Persatuan 2 KDW]", text_alignment="center")

nama_terdata = data_anak['NAMA'].count()
usia_terdata = data_anak['USIA (TAHUN)'].count()
st.badge(f"Total Anak/Remaja yang Namanya telah Terdata: {nama_terdata}", icon=":material/emoji_people:", color="blue")
st.badge(f"Total Anak/Remaja yang Usianya telah Terdata: {usia_terdata}", icon=":material/event_repeat:", color="blue")

usia_kolom = pd.DataFrame(data_anak['USIA (TAHUN)'])
usia_hitung = usia_kolom['USIA (TAHUN)'].value_counts().reset_index()
usia_hitung.rename(columns={'count': 'JUMLAH ANAK'}, inplace=True)
usia_hitung = usia_hitung.sort_values(by="USIA (TAHUN)", ascending=True)

jalan_saring = data_anak['JALAN PERSATUAN'].sort_values().dropna().unique()
jalan_widget = st.multiselect(":material/home: Lokasi Tinggal:", jalan_saring)
if jalan_widget:
    data_anak = data_anak[data_anak['JALAN PERSATUAN'].isin(jalan_widget)]
st.dataframe(data_anak, hide_index=True)

st.header(":blue[Rekapitulasi per Kategori Usia]")
interval = [0, 2, 5, 8, 12, 17, 26]
label = ['0 s.d. 2 Tahun', '3 s.d. 5 Tahun', '6 s.d. 8 Tahun', '9 s.d. 12 Tahun', '13 s.d. 17 Tahun', '17 Tahun ke atas']
usia_hitung['KATEGORI USIA'] = pd.cut(usia_hitung['USIA (TAHUN)'], bins=interval, labels=label)
usia_kategori = usia_hitung.groupby('KATEGORI USIA')['JUMLAH ANAK'].sum().reset_index()
usia_0002 = usia_kategori.iloc[0,1]
usia_0305 = usia_kategori.iloc[1,1]
usia_0608 = usia_kategori.iloc[2,1]
usia_0912 = usia_kategori.iloc[3,1]
usia_1317 = usia_kategori.iloc[4,1]
usia_17xx = usia_kategori.iloc[5,1]
col_nf_01, col_nf_02 = st.columns(2)
col_nf_03, col_nf_04 = st.columns(2)
col_nf_05, col_nf_06 = st.columns(2)
with col_nf_01:
    col_nf_01.metric("Usia 0 s.d. 2 Tahun (orang)", usia_0002, border=True)
with col_nf_02:
    col_nf_02.metric("Usia 3 s.d. 5 Tahun (orang)", usia_0305, border=True)
with col_nf_03:
    col_nf_03.metric("Usia 6 s.d. 8 Tahun (orang)", usia_0608, border=True)
with col_nf_04:
    col_nf_04.metric("Usia 9 s.d. 12 Tahun (orang)", usia_0912, border=True)
with col_nf_05:
    col_nf_05.metric("Usia 13 s.d. 17 Tahun (orang)", usia_1317, border=True)
with col_nf_06:
    col_nf_06.metric("Usia 17 Tahun ke atas (orang)", usia_17xx, border=True)

with st.expander("Rekapitulasi per Usia"):
    usia_rekap = usia_hitung[['USIA (TAHUN)', 'JUMLAH ANAK']]
    st.dataframe(usia_rekap, hide_index=True)
