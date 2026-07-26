import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Dashboard", layout="wide")
st.title(":blue[Data Anak-Anak Persatuan 2 KDW]", text_alignment="center")

conn_anak = st.connection("gsheets_anak", type=GSheetsConnection, ttl=120)
data_anak = conn_anak.read()
jalan_saring = data_anak['JALAN PERSATUAN'].sort_values().dropna().unique()
jalan_widget = st.multiselect(":material/home: Lokasi Tinggal:", jalan_saring)
if jalan_widget:
    data_anak = data_anak[data_anak['JALAN PERSATUAN'].isin(jalan_widget)]
st.dataframe(data_anak, hide_index=True)
with st.expander("Sebaran Usia"):
    usia_kolom = pd.DataFrame(data_anak['USIA (TAHUN)'])
    usia_hitung = usia_kolom['USIA (TAHUN)'].value_counts().reset_index()
    usia_hitung.rename(columns={'count': 'JUMLAH ANAK'}, inplace=True)
    usia_hitung = usia_hitung.sort_values(by="USIA (TAHUN)", ascending=True)
    st.dataframe(usia_hitung, hide_index=True)
