import streamlit as st
import sqlite3
import pandas as pd
st.set_page_config(page_title="CEO Dashbroad",page_icon="📈",layout="wide")
def load_data():
    conn=sqlite3.connect("competior.db")
    df = pd.read_sql_query("SELECT * FROM price_history",conn)
    return df

st.title("📊 HỆ THỐNG TÌNH BÁO THỊ TRƯỜNG (MARKET INTELLIGENCE)")
st.markdown("----")
data = load_data()
if data.empty:
    st.warning("⚠️ Két sắt đang trống! Hãy chạy file intelligence.py để thả Điệp viên đi cào dữ liệu trước!")
else:
    st.subheader("Sổ Cái Kế Toán (Raw Data)")
    st.dataframe(data,use_container_width=True)
    st.subheader("Biểu Đồ Biến Động Giá (Price Trend)")
    chart_data = data.set_index('time')
    st.line_chart(chart_data['price'])
    st.success("✅ Dữ liệu được trích xuất trực tiếp từ Két sắt SQLite!")
    