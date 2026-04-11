import sqlite3
class Durian:
    def __init__(self,item_code,variety,weight,selling_price_per_kg,cost_price_per_kg):
        self.item_code = item_code
        self.variety = variety
        self.weight = weight
        self.selling_price_per_kg = selling_price_per_kg
        self.cost_price_per_kg = cost_price_per_kg
        self.is_sold = False
        
    def calculate_selling_price(self):
        selling_price = self.selling_price_per_kg * self.weight
        return selling_price
    def calculate_cost_price(self):
        cost_price = self.cost_price_per_kg * self.weight
        return cost_price
class Customer:
    def __init__(self,name , phone ,address):
        self.name = name
        self.phone = phone
        self.address = address
        self.cart = []
    def add_to_cart(self ,durian_item:Durian):
        if durian_item.is_sold == False:
            self.cart.append(durian_item)
            durian_item.is_sold =True
            print(f"✅ SUCCESS: Đã bỏ quả {durian_item.item_code} vào giỏ của {self.name}!")
        else:
            print(f"❌ FAILED: Cảnh báo! Quả {durian_item.item_code} đã có người chốt rồi! {self.name} chậm chân quá!")
            
    def generate_invoice(self,shipping_fee):
        total_durian_price = 0
        print(f"--- INVOICE FOR CUSTOMER: {self.name} ---")
        for item in self.cart:
            item_price = item.calculate_selling_price()
            print(f"- Item Code {item.item_code} ({item.variety} - {item.weight}kg): {item_price} VND")
            total_durian_price += item_price
        total_payment = total_durian_price + shipping_fee
        print(f"Shipping Fee: {shipping_fee} VND")
        print(f"💰 TOTAL PAYMENT: {total_payment} VND\n")
class LiveStream:
    def __init__(self):
        self.inventory = []
        self.customer = []
    def add_to_inventory(self,durian_item:Durian):
        self.inventory.append(durian_item)
        print(f"📦 Đã nhập kho quả: {durian_item.item_code} - {durian_item.weight}kg")
    def register_customer(self,customer:Customer):
        self.customer.append(customer)
        print(f"👤 Khách hàng {customer.name} đã vào phiên Live!")
    def process_order(self,customer:Customer,request_code:str):
        print(f"🔄 Đang xử lý yêu cầu: {customer.name} muốn chốt mã {request_code}...")
        for item in self.inventory:
            if item.item_code == request_code:
                customer.add_to_cart(item)
                return 
        print(f"❌ THẤT BẠI: Trong kho không có mã {request_code} hoặc đã bị bán mất rồi!")
    def generate_bunisess_report(self):
        total_revenue = 0 # Tổng doanh thu
        total_cost = 0    # Tổng vốn
        total_profit = 0  # Lợi nhuận
        sold_count = 0    # Số quả đã bán
        for item in self.inventory:
            if item.is_sold == True:
                sold_count += 1
                total_cost += item.calculate_cost_price()
                total_revenue += item.calculate_selling_price()
        total_profit = total_revenue - total_cost
        print("\n" + "="*40)
        print("📊 BÁO CÁO KẾT THÚC PHIÊN LIVE 📊")
        print(f"✅ Đã bán thành công: {sold_count} quả")
        print(f"💰 Tổng Doanh Thu: {total_revenue} VND")
        print(f"📉 Tổng Tiền Vốn: {total_cost} VND")
        print(f"🚀 LỢI NHUẬN RÒNG: {total_profit} VND")
        print("="*40 + "\n")
        
# -------- CHẠY THỬ HỆ THỐNG ---------

# 1. Tạo Thực thể
item_A1 = Durian(item_code="A1", variety="Ri6", weight=3.0, selling_price_per_kg=100000, cost_price_per_kg=60000)
item_A2 = Durian(item_code="A2", variety="Thai", weight=4.0, selling_price_per_kg=150000, cost_price_per_kg=80000)
customer_1 = Customer("Lan", "090330978", "CauGiay")
customer_2 = Customer("Diep", "09134578", "ThanhXuan")

# 2. Bật Hệ Thống LiveStream
he_thong = LiveStream()

# 3. Nạp đạn (Nhập kho & Điểm danh)
he_thong.add_to_inventory(item_A1)
he_thong.add_to_inventory(item_A2)
he_thong.register_customer(customer_1)
he_thong.register_customer(customer_2)

# 4. Phiên Live Bắt Đầu! Các thực thể tương tác thông qua Bộ Quản Lý!
he_thong.process_order(customer_1, "A1")  # Bà Lan chốt A1 -> THÀNH CÔNG
he_thong.process_order(customer_2, "A1")  # Bà Điệp chốt cướp A1 -> THẤT BẠI
he_thong.process_order(customer_2, "A2")  # Bà Điệp chuyển sang chốt A2 -> THÀNH CÔNG
he_thong.process_order(customer_1, "A99") # Bà Lan đòi mã ảo -> THẤT BẠI

# 5. In báo cáo cuối ngày
customer_1.generate_invoice(30000)
customer_2.generate_invoice(30000)
he_thong.generate_bunisess_report()

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
