from vault import DataObject
from notifier import TelegramNotifier
from scraper import ObjectScraper
from config import CHAT_ID , key_telegram
import time
def main():
    print("🚀 BẮT ĐẦU CHUỖI KHỞI ĐỘNG HỆ THỐNG...")
    scraper = ObjectScraper()
    db = DataObject()
    bot = TelegramNotifier(token=key_telegram ,chat_id= CHAT_ID)
    print ("⚡ Kích hoạt Mũi khoan Playwright...")
    
    all_data , vip_deals = scraper.fetch_data()
    
    if all_data and len(all_data) > 0:
        print(f"🎯 Đã tóm được {len(all_data)} mục tiêu. Bắt đầu đẩy vào Data Lake!")
        for item in all_data:
            db.save_data(item)
        print("💾 Đã lưu xong toàn bộ sản phẩm vào Data Lake.")
    else:
        print("⚠️ Không lấy được dữ liệu nào từ Mũi khoan.")
        
    if vip_deals and len(vip_deals) > 0:
        print(f"Có {len(vip_deals)} kèo thơm! Đang gọi Telegram báo động...")
        bot.send_report(vip_deals)
    else:
        print("🔕 Không có kèo thơm nào trong chu kỳ này. Telegram tiếp tục ngủ.")
    print("🧹 Kích hoạt Giao thức Dọn dẹp Chiến trường...")
    scraper.stop_engine()
def run_forever():
    print("⚙️ KÍCH HOẠT ĐỘNG CƠ TỰ ĐỘNG HÓA VÔ CỰC...")
    cycle = 1
    while True:
        print(f"\n" + "="*50)
        print(f"🚀 BẮT ĐẦU CHU KỲ QUÉT SỐ {cycle}")
        print("="*50)
        try:
            main()
            print("\n⏳ Chu kỳ hoàn tất. Cỗ máy đi ngủ 60 phút")
            time.sleep(3600)
            cycle += 1
        except Exception as e:
            print(f"🔥 LỖI CHÍ MẠNG TRONG CHU KỲ {cycle}: {e}")
            print("⏳ Cỗ máy bị vấp! Chờ 5 phút rồi tự động thử lại...")
            time.sleep(300)
if __name__ == "__main__":
    run_forever()
    print("🧹 Kích hoạt Giao thức Dọn dẹp Chiến trường...")
    