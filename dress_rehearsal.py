import sqlite3
from playwright.sync_api import sync_playwright
import time


class DataVault:
    def __init__(self,db_name = "secret_file.db"):
        self.db_name = db_name
        self.create_table()
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS history_price(
                           id INTEGER PRIMARY KEY,
                           time TEXT,
                           price REAL
                       )
                       ''')
    def save_price(self,price):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
                       INSERT INTO history_price(time,price)
                       VALUES (?,?)
                       ''', (current_time,price))
        conn.commit()
        print(f"✅ Đã cất vào két:")
class WebSpy:
    def __init__(self,url,Data):
        self.url = url
        self.data = Data
    def extract_price(self):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url,timeout= 30000)
                text_price = page.locator("p.price_color").first.inner_text()
                float_price = float(text_price.replace("£",""))
                self.data.save_price(float_price)
                print(f"✅ Báo cáo: Đã cướp được dữ liệu giá là £{float_price}")
                browser.close()
                
        except Exception as e:
            print(f"Fall Back {e}")
            return 0.0
aim_url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
safe_box = DataVault()
hunt_price = WebSpy(aim_url,safe_box)
hunt_price.extract_price()