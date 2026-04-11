import telebot
from key_telegram import TOKEN
# Lát nữa chúng ta sẽ import Playwright và Database sau, giờ lo thằng Bot trước!
from playwright.sync_api import sync_playwright
from saas_database import DataVault

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

# Mở cổng nhận lệnh /track
@bot.message_handler(commands=['track'])
def handle_track_command(message):
    chat_id = message.chat.id
    text = message.text # Lấy toàn bộ tin nhắn (Ví dụ: "/track https://link...")
    
    # Cắt chữ "/track " đi để lấy mỗi cái link
    # (Hàm replace sẽ thay chữ "/track " thành khoảng trắng)
    url_target = text.split(" ")[1]
    
    # Kiểm tra xem link có trống không
    if url_target == "/track":
        bot.reply_to(message, "⚠️ Lỗi: Sai cú pháp. Hãy gõ /track [Link_Sách]")
        return # Dừng lại luôn
        
    # KIỂM TRA TÊN MIỀN QUYỀN LỰC!
    if "books.toscrape.com" not in url_target:
        bot.reply_to(message, "⚠️ Lỗi: Tao chỉ nhận link của trang books.toscrape.com thôi!")
        return # Dừng lại luôn
        
    # Nếu vượt qua 2 lớp bảo vệ trên, nhắn tin báo đang đi cào!
    bot.reply_to(message, f"✅ Đã nhận lệnh! Đang cử Điệp viên đến: {url_target}")
    
    # --- CHỖ NÀY LÁT NỮA SẼ CHÈN CODE PLAYWRIGHT VÀ SQL VÀO ---

    gia_tien = crawl_spy(url_target)
    if gia_tien is not None:
        ket_sat_saas.save_data(gia_tien,chat_id,url_target)
        bot.reply_to(message,f"✅Cướp thành công!\n👉 Giá hiện tại là: £{gia_tien}\n💾 Đã lưu vào Két sắt SaaS của ngài!")
    else:
        bot.reply_to(message,"❌ Điệp viên tử trận! Không thể lấy được giá. Web có thể đang sập.")
print("Dây chuyền Lắp ráp SaaS đã hoàn tất. Chờ lệnh từ Telegram...")
bot.polling()