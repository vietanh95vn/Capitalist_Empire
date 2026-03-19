import sqlite3
from playwright.sync_api import sync_playwright
import time

class DataVault:
    def __init__(self,db_name = "competior.db"):
        self.db_name = db_name
        self.create_table()
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS price_history(
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
                       INSERT INTO price_history(time , price)
                       VALUES(?,?)
                       ''',(current_time,price))
        conn.commit()
        print(f"✅ Đã cất vào két:")
        
class WebSpy:
    def __init__(self, taget_url , vault_object):
        self.url = taget_url
        self.vault = vault_object
    def extract_price(self):
        print(f"🕵️‍♂️ Điệp viên đang xâm nhập:{self.url}....")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url , timeout= 30000)
                text_price  = page.locator("p.price_color").inner_text()
                real_price = float(text_price.replace('£',""))
                self.vault.save_price(real_price)
                print(f"✅ Báo cáo: Đã cướp được dữ liệu giá là £{real_price}")
                browser.close()
                
                
            
        except Exception as e:
            print(f"⚠️ ĐIỆP VIÊN BỊ TẤN CÔNG! Rút lui an toàn. Lỗi: {e}")
if __name__  == "__main__":
    AIM_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    safe_box = DataVault()
    spy_007 = WebSpy(AIM_URL,safe_box)
    spy_007.extract_price()