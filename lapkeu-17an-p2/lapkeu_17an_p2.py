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

total_pemasukan = data_uang['PEMASUKAN'].sum()
total_pengeluaran = data_uang['PENGELUARAN'].sum()
saldo = total_pemasukan-total_pengeluaran
col_nf_01, col_nf_02 = st.columns(2)
col_nf_03, col_nf_04 = st.columns(2)
with col_nf_01:
    col_nf_01.metric("PEMASUKAN (Rp)", total_pemasukan, border=True, format="%,d")
with col_nf_02:
    col_nf_02.metric("PENGELUARAN (Rp)", total_pengeluaran, border=True, format="%,d")
with col_nf_03:
    col_nf_03.metric("SALDO (Rp)", saldo, border=True, format="%,d")

with st.expander("Detil Transaksi"):
    st.dataframe(data_uang)
