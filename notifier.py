import requests
from config import CHAT_ID,key_telegram
from vault import Object
class TelegramNotifier:
    def __init__(self,token,chat_id):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
    def send_report(self,list_item:list[Object]):
        report ="Report Object On eBay\n" + "0" + "\n"
        for s in list_item[:10]:
            short_name = s.name[:50] + "....." if len(s.name) > 50 else s.name  
            report += f"{short_name}:{s.price}\n"
        pay_load = {
            "chat_id":self.chat_id,
            "text": report
        }
        try:
            response = requests.post(self.api_url, data=pay_load)
            if response.status_code == 200:
                print("🚀 TELEGRAM: Đã bắn tin nhắn báo cáo thành công!")
            else:
                print(f"❌ LỖI API TELEGRAM: {response.text}")
        except Exception as e:
            print(f"❌ LỖI TELEGRAM: Không thể bắn tin nhắn! {e}")
            
        