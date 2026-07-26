import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Dashboard", layout="wide")
st.title(":blue[Laporan Keuangan Kegiatan 17an Persatuan 2 KDW]", text_alignment="center")

conn_uang = st.connection("gsheets_uang", type=GSheetsConnection)
data_uang = conn_uang.read()
st.badge(f"Data Masuk Terakhir: {data_uang.loc[data_uang.index[-1], 'TANGGAL']}", icon=":material/database:", color="blue")
pemasukan = pd.DataFrame(data_uang['PEMASUKAN']).sum()
pengeluaran = pd.DataFrame(data_uang['PENGELUARAN']).sum()
total_pemasukan = pemasukan['PEMASUKAN']
total_pengeluaran = pengeluaran["PENGELUARAN"]
saldo = (total_pemasukan - total_pengeluaran)
col_nf_01, col_nf_02 = st.columns(2)
col_nf_03, col_nf_04 = st.columns(2)
with col_nf_01:
    col_nf_01.metric("PEMASUKAN", total_pemasukan, border=True, format="%,d")
with col_nf_02:
    col_nf_02.metric("PENGELUARAN", total_pengeluaran, border=True, format="%,d")
with col_nf_03:
    col_nf_03.metric("SALDO", saldo, border=True, format="%,d")
with st.expander("Detil Transaksi"):
    st.dataframe(data_uang)
