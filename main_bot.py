import telebot
import time
import threading
from config import TOKEN, TREASURE, CHAT_ID
from database import tao_ket_sat, luu_tai_san, lay_gia_cu

# GHI CHÚ: Tôi giả định cậu vẫn để hàm hunt_stock trong file này. 
# Nếu cậu đã chuyển nó sang api_binance.py, thì mới import. 
# Hiện tại Tôi tự viết hàm giả lập ở đây để test.
def hunt_stock(name):
    return 65000 # Giả lập giá

# ==========================================
# ĐẾ CHẾ OOP: BẢN THIẾT KẾ CHÓ SĂN TÀI CHÍNH
# ==========================================
class FinancialWatchdog:
    
    def __init__(self, bot_token, admin_chat_id):
        self.bot = telebot.TeleBot(bot_token)
        self.admin_id = admin_chat_id
        self.is_running = True
        print("[HỆ THỐNG] Chó săn tài chính đã được đúc thành công!")

        # Khai báo các lệnh của Bot ngay trong lúc khởi tạo
        self.setup_routes()

    def setup_routes(self):
        # Mũ bảo hiểm và Đầu phải thẳng hàng với nhau!
        @self.bot.message_handler(commands=['audit'])
        def handle_audit(message):
            # Không có dấu @ ở đây. Và BẮT BUỘC dùng self.bot
            self.bot.reply_to(message, "Đang kiểm tra tài sản...") 
            tao_ket_sat()
            
            for stock in TREASURE:
                real_price = hunt_stock(stock)
                quantity  = TREASURE[stock]
                total_asset = real_price * quantity
                luu_tai_san(stock, real_price, total_asset, quantity)
                
            self.bot.reply_to(message, "✅ Báo cáo CFO: Kế toán đã lưu xong toàn bộ tài sản vào Két sắt!")

    def patrol_market(self):
        # Vòng lặp while phải thụt lề vào trong hàm
        while self.is_running:
            # Ngủ 10 giây để test
            time.sleep(10)
            print("Chó săn đang ngửi mùi thị trường...")
            
            for stock in TREASURE:
                try:
                    gia_moi = hunt_stock(stock)
                    gia_cu = lay_gia_cu(stock)
                    
                    if gia_cu > 0:
                        bien_dong = abs(gia_moi - gia_cu) / gia_cu * 100
                        
                        if bien_dong > 0.01:
                            canh_bao = f"🚨 BÁO ĐỘNG ĐỎ (RED ALERT) 🚨\n"
                            canh_bao += f"Tài sản: {stock}\n"
                            canh_bao += f"Biến động: {bien_dong:.3f}%\n"
                            canh_bao += f"Giá cũ: {gia_cu}$\n"
                            canh_bao += f"Giá mới: {gia_moi}$"
                            
                            # Phải dùng self.bot và tọa độ CFO lưu trong self.admin_id
                            self.bot.send_message(self.admin_id, canh_bao)
                            luu_tai_san(stock, gia_moi, gia_moi * TREASURE[stock], TREASURE[stock])
                except Exception as e:
                    print(f"⚠️ [LỖI HỆ THỐNG] Mất kết nối khi kiểm tra {stock}. Chi tiết: {e}")
                    print("🔄 Chó săn vẫn đang thở. Sẽ thử lại ở vòng lặp sau...")
                    # Hệ thống sẽ bỏ qua vòng lặp bị lỗi này và tự động chạy tiếp!

    def ignite_engine(self):
        print("Đang đánh thức Hệ thống Đa Luồng...")
        watchdog_thread = threading.Thread(target=self.patrol_market)
        watchdog_thread.start()
        self.bot.infinity_polling()

# ==========================================
# KHU VỰC THỰC THI 
# ==========================================
if __name__ == "__main__":
    lo_mo_tu_dong = FinancialWatchdog(TOKEN, CHAT_ID)
    lo_mo_tu_dong.ignite_engine()