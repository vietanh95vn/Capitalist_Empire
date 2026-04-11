import requests
class TelegramNotifier: # config Telegram bot

    def __init__(self,token:str , chat_id:str):

        self.token = token

        self.chat_id =chat_id

        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_report(self,message:str):
    
        pay_load = {
            "chat_id":self.chat_id,
            "text":message,
            "parse_mode":"HTML"
        }
        try:
            response = requests.post(self.api_url,data=pay_load)
            if response.status_code == 200:
                print("🚀 [TELEGRAM] Đã bắn tin nhắn Cảnh báo thành công!")
               
            else:
                print(f"🔥 [TELEGRAM] Bắn xịt! Lỗi từ Server: {response.text}")
        except Exception as e:
            print(f"🔥 Lỗi hạ tầng mạng: {e}")