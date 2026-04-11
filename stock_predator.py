import sqlite3
import time
import requests
from playwright.sync_api import sync_playwright
from config import CHAT_ID ,key_telegram

class Stock:
    def __init__(self,name_stock , price_stock , change_stock):
        self.name_stock = name_stock
        self.price_stock = price_stock
        self.change_stock = change_stock
class StockScraper:
    def __init__(self):
        print("🚀 Bơm nhiên liệu cho Động cơ Playwright MỘT LẦN DUY NHẤT...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page() 
    
    def fetch_data(self):
        print("🔍 Đang khởi động Mũi khoan Playwright...")
        scrap_data = []
        
        try:
            self.page.goto("https://finance.yahoo.com/trending-tickers",timeout=60000, wait_until="domcontentloaded")
            self.page.wait_for_selector("table tbody tr")
            rows = self.page.locator("table tbody tr").all()
            print(f"🎯 Đã khóa mục tiêu: {len(rows)} mã chứng khoán!")
            for row in rows:
                name_symbol = row.locator('td:nth-child(1)').inner_text().strip()
                price_stock = row.locator("td:nth-child(3)").inner_text().strip()
                percent_change_stock = row.locator("td:nth-child(5)").inner_text().strip()
                new_stock = Stock(name_stock=name_symbol,price_stock=price_stock,change_stock=percent_change_stock)
                scrap_data.append(new_stock)
            self.browser.close()
            return scrap_data
        except Exception as e:
            print(f"Error {e}")
            return []

        
class StockDatabase:
    def __init__(self,db_name = "stock.db"):
        self.db_name = db_name
        self.create_table()
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS stock_data(
                           id INTEGER PRIMARY KEY,
                           symbol TEXT,
                           price REAL,
                           change REAL,
                           time TEXT
                       )
                       ''')
        conn.commit()
        conn.close()
    def save_stock(self,data_stock:Stock):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d  %H:%M:%S")
        cursor.execute('''
                       INSERT INTO stock_data(symbol,price,change,time)
                       VALUES(?,?,?,?)
                       ''',(data_stock.name_stock,data_stock.price_stock,data_stock.change_stock,current_time))
        conn.commit()
        conn.close()
        print(f"💾 DATABASE: Đã lưu mã {data_stock.name_stock} vào Két Sắt!")
    def get_last_price(self,symbol):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT price FROM stock_data
                       WHERE symbol = ?
                       ORDER BY time DESC
                       LIMIT 1
                       ''',(symbol,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return str(result[0])
        else:
            return None    
class TelegramNotifier:
    def __init__(self,token , chat_id):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
    def send_report(self,stocks):
        report = "📊 BÁO CÁO MÃ CHỨNG KHOÁN:\n" + "-"*20 + "\n"
        for s in stocks:
            report += f"🔹 {s.name_stock}: {s.price_stock} ({s.change_stock})\n"
        payload = {
        "chat_id": self.chat_id,
        "text": report
        }
        
        # 3. Kích nổ! Ném thùng hàng vào mặt thằng Telegram!
        try:
            requests.post(self.api_url, data=payload)
            print("🚀 TELEGRAM: Đã bắn tin nhắn báo cáo thành công!")
        except Exception as e:
            print(f"❌ LỖI TELEGRAM: Không thể bắn tin nhắn! {e}")
    
def main():
    scaper = StockScraper()
    db = StockDatabase()
    bot = TelegramNotifier(token=key_telegram,chat_id=CHAT_ID)
    while True:
        stocks = scaper.fetch_data()
        changed_stock = []
        
        for s in stocks:
            old_price = db.get_last_price(s.name_stock)
            if old_price != s.price_stock:
                print(f"Biến Động {s.name_stock}| Cũ {old_price} -> Mới {s.price_stock} ")
                db.save_stock(s)
                changed_stock.append(s)
            else:
                print(f"Sleep {s.name_stock} nothing change")
            if len(changed_stock)>0:
                print(f"🔥 Phát hiện {len(changed_stock)}")
                bot.send_report(changed_stock)
            else:
                print("💤 Thị trường đóng băng. Không làm phiền Boss.")
            bot.send_report(stocks)
            print("💤 Đã xử lý xong. Nghỉ ngơi 10s...")
            time.sleep(10)

if __name__ == "__main__":
    main()