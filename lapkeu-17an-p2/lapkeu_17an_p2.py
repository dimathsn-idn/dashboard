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
st.badge(f"SALDO: {data_uang.loc[data_uang.index[-1], 'SALDO']}", icon=":material/money:", color="blue")
data_transaksi = data_uang.melt(value_vars=['PEMASUKAN', 'PENGELUARAN'], var_name='TRANSAKSI', value_name='NILAI TRANSAKSI')
transaksi_grafik = px.bar(data_transaksi, x='TRANSAKSI', y='NILAI TRANSAKSI', color='TRANSAKSI', text_auto=True)
transaksi_grafik.update_xaxes(tickfont_size=20)
transaksi_grafik.update_yaxes(tickformat=",", tickfont_size=20)
transaksi_grafik.update_layout(yaxis_title="TOTAL")
transaksi_grafik.update_traces(width=0.5, textposition='outside', textfont_size=20, textfont_weight=500, textfont_color='blue')
st.plotly_chart(transaksi_grafik)
with st.expander("Detil Transaksi"):
    st.dataframe(data_uang)
