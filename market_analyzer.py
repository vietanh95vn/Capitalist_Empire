import sqlite3
import pandas as pd
def analyze_market():
    conn = sqlite3.connect("ebay.db")
    df =pd.read_sql_query("SELECT * FROM data_ebay WHERE price >= 0",conn)
    if not df.empty:
        market_median = df['price'].median()
        print(f"📊 TỔNG SỐ LƯỢNG DATA: {len(df)} máy.")
        print(f"🎯 GIÁ THỊ TRƯỜNG TRUNG VỊ (MEDIAN): {market_median:.2f}VND")
        target_price = market_median * 0.8
        print(f"🔫 NGƯỠNG BÓP CÒ (TARGET THRESHOLD): Mua vào nếu giá <= {target_price:.2f}VND")
    else:
        print("⚠️ Két sắt trống rỗng!")
if __name__ == "__main__":
    analyze_market()