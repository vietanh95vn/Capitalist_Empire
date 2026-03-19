# ==========================================
# database.py - Phòng Kế Toán Cấp Cao
# ==========================================
import sqlite3

# Nghiệp vụ 1: Đúc Két sắt (Chỉ chạy 1 lần khi bắt đầu)
def tao_ket_sat():
    conn = sqlite3.connect("wealth_tracking.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wealth_tracking(
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            name_coin TEXT,
            real_price REAL,
            total_asset REAL,
            quantity REAL
        )
    ''')
    conn.commit()
    conn.close()

# Nghiệp vụ 2: Ghi chép Sổ sách (Nhét tiền vào Két)
def luu_tai_san(name_coin, real_price, total_asset, quantity):
    conn = sqlite3.connect("wealth_tracking.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO wealth_tracking(name_coin, real_price, total_asset, quantity)
        VALUES(?,?,?,?)
    ''', (name_coin, real_price, total_asset, quantity))
    conn.commit()
    conn.close()
def lay_gia_cu(name_coin):
    conn= sqlite3.connect("wealth_tracking.db")
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT real_price FROM wealth_tracking WHERE name_coin = ?
                   ORDER BY time DESC LIMIT 1
                   ''',(name_coin,))
    ket_qua = cursor.fetchone()
    conn.close()
    if ket_qua:
        return ket_qua[0]
    return 0.0
    