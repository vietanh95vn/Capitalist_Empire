import sqlite3
import time
import telebot
from playwright.sync_api import sync_playwright
from key_telegram import TOKEN
class DataVault:
    def __init__(self,db_name = "saas_database.db"):
        self.db_name = db_name
        self.create_table()
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS client_data(
                           id INTEGER PRIMARY KEY,
                           chat_id ,
                           url TEXT,
                           time TEXT,
                           price REAL
                       )
                       ''')
    def save_data(self,price,chat_id,url):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        current_time = time.strftime("%Y %m %d - %H:%M:%S")
        cursor.execute('''
                       INSERT INTO client_data(chat_id ,url ,price ,time)
                       VALUES(?,?,?,?)
                       ''',(chat_id,url,price,current_time))
        conn.commit()
        print(f"✅ Đã cất vào két:")
        
#Playwright crawl data       
def crawl_data(url_target):
    try:
        with sync_playwright() as p:
            brower = p.chromium.launch(headless=True)
            page = brower.new_page()
            page.goto(url_target,timeout= 30000)
            text_price = page.locator("p.price_color").first.inner_text()
            float_price = float(text_price.replace("£",""))
            name_data = page.locator(".product_main h1").inner_text()
            return float_price,name_data
    except Exception as e:
        print(f"Error {e}")
        return None
bot = telebot.TeleBot(TOKEN)
ket_sat_saas = DataVault()
def crawl_spy(url_target):
    try:
        with sync_playwright() as p:
            brower = p.chromium.launch(headless=True)
            page = brower.new_page()
            page.goto(url_target,timeout= 30000)
            text_price = page.locator("p.price_color").first.inner_text()
            float_price = float(text_price.replace("£",""))
            brower.close()
            return float_price
    except Exception as e:
        print("Error")
        return None
@bot.message_handler(commands=['track'])
def handle_track_command(message):
    chat_id = message.chat.id
    text = message.text # Lấy toàn bộ tin nhắn (Ví dụ: "/track https://link...")
    

    url_target = text.split(" ")[1]
    
    # Kiểm tra xem link có trống không
    if url_target == "/track":
        bot.reply_to(message, "⚠️ Lỗi: Sai cú pháp. Hãy gõ /track [Link_Sách]")
        return # Dừng lại luôn
        

    if "books.toscrape.com" not in url_target:
        bot.reply_to(message, "⚠️ Lỗi: Tao chỉ nhận link của trang books.toscrape.com thôi!")
        return # Dừng lại luôn
        
    bot.reply_to(message, f"✅ Đã nhận lệnh! Đang cử Điệp viên đến: {url_target}")
    

    gia_tien = crawl_spy(url_target)
    if gia_tien is not None:
        ket_sat_saas.save_data(gia_tien,chat_id,url_target)
        bot.reply_to(message,f"✅Cướp thành công!\n👉 Giá hiện tại là: £{gia_tien}\n💾 Đã lưu vào Két sắt SaaS của ngài!")
    else:
        bot.reply_to(message,"❌ Điệp viên tử trận! Không thể lấy được giá. Web có thể đang sập.")
print("Dây chuyền Lắp ráp SaaS đã hoàn tất. Chờ lệnh từ Telegram...")
bot.polling()
