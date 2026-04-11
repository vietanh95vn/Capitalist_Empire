import telebot
import time
import threading
from config import TOKEN, TREASURE, CHAT_ID
from database import tao_ket_sat, luu_tai_san, lay_gia_cu
from main_bot import hunt_stock # Giả sử cậu có file này chứa hàm lấy giá

# ==========================================
# ĐẾ CHẾ OOP: BẢN THIẾT KẾ CHÓ SĂN TÀI CHÍNH
# ==========================================
class FinancialWatchdog:
    
    # 1. KỸ NĂNG KHỞI TẠO: Nạp đạn và chìa khóa cho Thực thể
    def __init__(self, bot_token, admin_chat_id):
        self.bot = telebot.TeleBot(bot_token) # Gắn con Bot vào bụng nó
        self.admin_id = admin_chat_id         # Gắn tọa độ GPS của CFO vào bụng nó
        self.is_running = True
        print("[HỆ THỐNG] Chó săn tài chính đã được đúc thành công!")

        # Khai báo các lệnh của Bot ngay trong lúc khởi tạo
        self.setup_routes()

    # 2. ĐỊNH TUYẾN LỆNH (Routing): Gắn tai nghe cho Lễ tân
    def setup_routes(self):
        @self.bot.message_handler(commands=['audit'])
        def handle_audit(self,message):
            # Cậu sẽ tự copy logic lệnh /audit cũ của cậu vào đây!
            self.bot.reply_to(message, "Đang kiểm tra tài sản...") 
            tao_ket_sat()
            for stock in TREASURE:
                real_price = hunt_stock(stock)
                quantity  = TREASURE[stock]
                total_asset = real_price * quantity
                luu_tai_san(stock,real_price,total_asset,quantity)
            self.bot.reply_to(message,"✅ Báo cáo CFO: Kế toán đã lưu xong toàn bộ tài sản vào Két sắt!")
            

    # 3. KỸ NĂNG ĐI TUẦN TRA (Chạy ngầm)
    def patrol_market(self):
        while self.is_running:

            print("Đang quét radar thị trường...")
        # Cậu sẽ tự copy logic vòng lặp tính % Biến động và Gửi Cảnh báo vào đây!

        # Cứ 10 giây báo cáo 1 lần (Để test cho nhanh, thực tế sẽ là 3600 giây)
            time.sleep(10)
            print("Chó săn đang ngửi mùi thị trường...")
            for stock in TREASURE:
                gia_moi = hunt_stock(stock)
                gia_cu = lay_gia_cu(stock)
                if gia_cu > 0:
                    bien_dong = abs(gia_moi-gia_cu)/gia_cu * 100
                    if bien_dong > 0.01:
                        canh_bao = f"🚨 BÁO ĐỘNG ĐỎ (RED ALERT) 🚨\n"
                        canh_bao += f"Tài sản: {stock}\n"
                        canh_bao += f"Biến động: {bien_dong:.3f}%\n"
                        canh_bao += f"Giá cũ: {gia_cu}$\n"
                        canh_bao += f"Giá mới: {gia_moi}$"
                        bot.send_message(CHAT_ID,canh_bao)
                        luu_tai_san(stock, gia_moi, gia_moi * TREASURE[stock], TREASURE[stock])
                pass

    # 4. KỸ NĂNG KÍCH HOẠT TOÀN HỆ THỐNG (Khởi động)
    def ignite_engine(self):
        print("Đang đánh thức Hệ thống Đa Luồng...")
        # Tạo luồng cho Chó săn đi tuần
        watchdog_thread = threading.Thread(target=self.patrol_market)
        watchdog_thread.start()
        
        # Thằng Lễ tân đứng canh cửa
        self.bot.infinity_polling()

# ==========================================
# KHU VỰC THỰC THI (CHỈ TỐN ĐÚNG 2 DÒNG CODE)
# ==========================================
if __name__ == "__main__":
    # Đúc ra 1 con Chó săn Bất tử từ Bản thiết kế
    lo_mo_tu_dong = FinancialWatchdog(TOKEN, CHAT_ID)
    
    # Bấm nút Khởi động!
    lo_mo_tu_dong.ignite_engine()