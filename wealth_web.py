# ==========================================
# wealth_web.py - Mặt Tiền Của Đế Chế Tư Bản
# ==========================================
import streamlit as st
import pandas as pd
import sqlite3

# Cài đặt giao diện toàn màn hình cho uy lực
st.set_page_config(page_title="CFO Empire Dashboard", layout="wide")

st.title("🏛️ Đế Chế Tài Sản Tư Bản (Capitalist Wealth Empire)")
if st.button("🔄 Cập Nhật Dữ Liệu Mới Nhất (Refresh Data)"):
    st.rerun()

# 1. Gọi Kế toán mở Két sắt lấy sổ sách
conn = sqlite3.connect("wealth_tracking.db")
df = pd.read_sql_query("SELECT * FROM wealth_tracking", conn)
conn.close()

# 2. XỬ LÝ LỖ HỔNG LẠM PHÁT (Fixing the Inflation Flaw)
# Chỉ cắt lấy 4 dòng dữ liệu mới nhất (tương ứng với 4 đồng Coin vừa quét)
df_hien_tai = df.tail(4)

# Tính tổng tài sản dựa trên 4 dòng mới nhất này
tong_tai_san = df_hien_tai['total_asset'].sum()

# 3. Hiển thị Trực quan (Visual Display)
st.metric(label="💰 TỔNG TÀI SẢN THỰC TẾ (REAL TOTAL NET WORTH)", value=f"${tong_tai_san:,.2f}")

# Chia màn hình làm 2 cột cho giống phong cách Thung lũng Silicon



st.subheader("📋 Sổ Cái Kiểm Toán (Audit Ledger)")
# Chỉ in ra 4 dòng mới nhất để CFO khỏi rối mắt
st.dataframe(df_hien_tai)


st.subheader("📊 Phân Bổ Danh Mục (Portfolio Allocation)")
st.bar_chart(data=df_hien_tai, x='name_coin', y='total_asset')