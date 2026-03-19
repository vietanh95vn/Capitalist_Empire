# Tên Class phải viết HOA (PascalCase)
class Order:
    def __init__(self, code_order, price_order):
        self.code_order = code_order
        self.price_order = price_order
        
    # Hàm này CHỈ TÍNH TIỀN và GIAO LẠI TIỀN (Return), không la hét!
    def calculate_total(self):
        return self.price_order

    # Thêm một hàm riêng chuyên để In Hóa Đơn (Print)
    def print_bill(self):
        # Tự nó gọi hàm tính tiền của chính nó (self.calculate_total())
        tong_tien = self.calculate_total()
        print(f"[{self.code_order}] Mức giá gốc: {self.price_order}$")
        print(f"[{self.code_order}] TỔNG TIỀN PHẢI THANH TOÁN: {tong_tien}$\n")

# Kế thừa
class GlobalOrder(Order):
    def __init__(self, code_order, price_order, customs_tax):
        super().__init__(code_order, price_order)
        self.customs_tax = customs_tax
        
    # GHI ĐÈ hàm tính tiền: Giá gốc + Thuế
    def calculate_total(self):
        sum_total = self.price_order + self.customs_tax
        return sum_total
    
    # GHI ĐÈ hàm in hóa đơn để hiển thị thêm dòng Thuế
    def print_bill(self):
        tong_tien = self.calculate_total()
        print(f"[{self.code_order}] Mức giá gốc: {self.price_order}$")
        print(f"[{self.code_order}] Thuế hải quan: {self.customs_tax}$")
        print(f"[{self.code_order}] TỔNG TIỀN PHẢI THANH TOÁN: {tong_tien}$\n")

# ====================
# KIỂM THỬ SẢN PHẨM
# ====================
print("\n-------- HỆ THỐNG KẾ TOÁN QUỐC TẾ -----------")
new_order = Order("VN01", 500)
new_global_order = GlobalOrder("US02", 800, 150)

# Ra lệnh in hóa đơn. Gọn gàng, thanh lịch!
new_order.print_bill()
new_global_order.print_bill()