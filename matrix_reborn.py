# 1. THỰC THỂ SẦU RIÊNG
import sqlite3
import time
class Durian:
    def __init__(self,item_code,type_durian,weight,price_selling,price_cost):
        self.item_code = item_code
        self.type_durian = type_durian
        self.weight = weight
        self.price_selling = price_selling
        self.price_cost = price_cost
        self.status_code = False
    def calculate_selling(self):
        price_of_durian_selling = self.price_selling * self.weight
        return price_of_durian_selling
    def calculate_cost(self):
        price_of_durian_cost = self.price_cost * self.weight
        return price_of_durian_cost
class Customer:
    def __init__(self,name,phone,address):
        self.name = name
        self.phone = phone
        self.address = address
        self.cart = []
    def add_to_cart(self,durian:Durian):
        if durian.status_code == False:
            self.cart.append(durian)
            durian.status_code = True
            print(f"Succes put {durian.item_code} to customer {self.name}")
        else:
            print(f"❌ FAILED: Cảnh báo! Quả {durian.item_code} đã có người chốt rồi! {self.name} chậm chân quá!")
    def process_payment(self,shipping_fee):
        total_customer_payment = 0
        for item in self.cart:
            item_price = item.calculate_selling()
            total_customer_payment += item_price
        total_payment = total_customer_payment + shipping_fee
        print(f"Shipping fee {shipping_fee}")
        print(f"Total payment {total_payment} - Name Customer : {self.name}")
        
class LiveStream:
    def __init__(self):
        self.inventory = []
        self.cart_customer = []
    def add_to_inventory(self,inventory_durian:Durian):
        self.inventory.append(inventory_durian)
        print(f"📦 Đã nhập kho quả: {inventory_durian.item_code} - {inventory_durian.weight}kg")
    def add_cart_customer(self,cart_customer:Customer):
        self.cart_customer.append(cart_customer)
        print(f"👤 Khách hàng {cart_customer.name} đã vào phiên Live!")
    def process_order(self,customer_order:Customer,request_code:str):
        print(f"🔄 Đang xử lý yêu cầu: {customer_order.name} muốn chốt mã {request_code}...")
        for item in self.inventory:
            if request_code == item.item_code:
                customer_order.add_to_cart(item)
                return
        print(f"❌ THẤT BẠI: Trong kho không có mã {request_code} hoặc đã bị bán mất rồi!")
    def generate_bunisess_report(self):
        total_revenue = 0 # Tổng doanh thu
        total_cost = 0    # Tổng vốn
        total_profit = 0  # Lợi nhuận
        sold_count = 0    # Số quả đã bán
        for item in self.inventory:
            if item.status_code == True:
                sold_count += 1
                total_cost += item.calculate_cost()
                total_revenue += item.calculate_selling()
        total_profit = total_revenue - total_cost
        print("\n" + "="*40)
        print("📊 BÁO CÁO KẾT THÚC PHIÊN LIVE 📊")
        print(f"✅ Đã bán thành công: {sold_count} quả")
        print(f"💰 Tổng Doanh Thu: {total_revenue} VND")
        print(f"📉 Tổng Tiền Vốn: {total_cost} VND")
        print(f"🚀 LỢI NHUẬN RÒNG: {total_profit} VND")
        print("="*40 + "\n")
    def save_to_database(self):
        # 1. Kết nối Két sắt
        conn = sqlite3.connect("durian_database.db")
        cursor = conn.cursor()
        
        # 2. Xây Bảng (Chú ý: ĐÃ THÊM DẤU PHẨY SAU CHỮ REAL)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Doanh_thu(
                id INTEGER PRIMARY KEY,
                item_sell TEXT,
                profit REAL,
                time TEXT
            )
        ''')
        so_qua_da_luu = 0
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        for item in self.inventory:
            # Chỉ lưu những quả ĐÃ BÁN (status_code == True)
            if item.status_code == True:
                # Tự tính lại lợi nhuận của riêng quả này!
                loi_nhuan_qua_nay = item.calculate_selling() - item.calculate_cost()
                
                # Bóp cò: Nhét thông tin của Thực Thể 'item' vào Két Sắt!
                cursor.execute('''
                    INSERT INTO Doanh_thu(item_sell, profit, time)
                    VALUES(?, ?, ?)
                ''', (item.item_code, loi_nhuan_qua_nay, current_time))
                
                so_qua_da_luu += 1
                
        # 5. Khóa Két!
        conn.commit()
        conn.close()
        
        print(f"💾 SYSTEM: Đã sao lưu thành công {so_qua_da_luu} giao dịch vào Database!")
# - Nó cần có: mã, loại, cân nặng, giá bán, giá vốn, trạng thái chưa bán.
# - Nó có thể làm: tính ra tiền bán, tính ra tiền vốn.
item_A1 = Durian(item_code="A1",type_durian="Ri6",weight=3.0,price_selling=80000,price_cost=50000)
item_A2 = Durian(item_code="A2",type_durian="Thai",weight=2.5,price_selling=100000,price_cost=60000)
customer_1 = Customer(name="Linh",phone="93493194",address="CauGiay")
customer_2 = Customer(name="Nga",phone="34235552",address="ThanhXuan")
system_live = LiveStream()
system_live.add_to_inventory(item_A1)
system_live.add_to_inventory(item_A2)
system_live.add_cart_customer(customer_1)
system_live.add_cart_customer(customer_2)
system_live.process_order(customer_1,"A1")
system_live.process_order(customer_2,"A1")
system_live.process_order(customer_2,"A2")
system_live.process_order(customer_2,"A99")

customer_1.process_payment(shipping_fee= 30000)
customer_2.process_payment(shipping_fee= 25000)

system_live.generate_bunisess_report() 
system_live.save_to_database()
# 2. THỰC THỂ KHÁCH HÀNG
# - Nó cần có: tên, sđt, địa chỉ, giỏ hàng.
# - Nó có thể làm: nhặt sầu riêng bỏ vào giỏ, in hóa đơn.

# 3. KỊCH BẢN THỰC CHIẾN (TEST)
# - Tạo ra 2 quả sầu riêng
# - Tạo ra 1 bà khách
# - Bắt bà khách nhặt 1 quả
# - Bắt bà khách in hóa đơn