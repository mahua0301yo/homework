import os
import numpy as np
import datetime
import pandas as pd
import streamlit as st 
import streamlit.components.v1 as stc 
from plotly.subplots import make_subplots
import plotly.graph_objects as go

html_temp = """
\t\t<div style="background-color:#3872fb;padding:10px;border-radius:10px">
\t\t<h1 style="color:white;text-align:center;">金融資料視覺化呈現 (金融看板) </h1>
\t\t<h2 style="color:white;text-align:center;">Financial Dashboard </h2>
\t\t</div>
\t\t"""
stc.html(html_temp)

df_original = pd.read_pickle('kbars_2330_2022-01-01-2022-11-18.pkl')
df_original = df_original.drop('Unnamed: 0', axis=1)

st.subheader("選擇開始與結束的日期, 區間:2022-01-03 至 2022-11-18")
start_date = st.text_input('選擇開始日期 (日期格式: 2022-01-03)', '2022-01-03')
end_date = st.text_input('選擇結束日期 (日期格式: 2022-11-18)', '2022-11-18')
start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
df = df_original[(df_original['time'] >= start_date) & (df_original['time'] <= end_date)]

# Define the MACD calculation function
def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    short_ema = prices.ewm(span=short_period, adjust=False).mean()
    long_ema = prices.ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    hist = macd - signal
    return macd, signal, hist

MACD_short_period = 12  # Example short period for MACD
MACD_long_period = 26   # Example long period for MACD
MACD_signal_period = 9  # Example signal period for MACD

df['MACD'], df['Signal'], df['Hist'] = calculate_macd(df['close'], MACD_short_period, MACD_long_period, MACD_signal_period)

# Your existing plotting code
with st.expander("K線圖, MACD 指標"):
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Candlestick(x=df['time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'], name='K線'), secondary_y=True)
    fig2.add_trace(go.Scatter(x=df['time'], y=df['MACD'], mode='lines', line=dict(color='red', width=2), name='MACD'), secondary_y=False)
    fig2.add_trace(go.Scatter(x=df['time'], y=df['Signal'], mode='lines', line=dict(color='blue', width=2), name='Signal'), secondary_y=False)
    fig2.add_trace(go.Bar(x=df['time'], y=df['Hist'], name='Hist', marker=dict(color='green')), secondary_y=False)
    fig2.layout.yaxis2.showgrid = True
    st.plotly_chart(fig2, use_container_width=True)
