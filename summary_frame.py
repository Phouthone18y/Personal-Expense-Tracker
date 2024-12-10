import tkinter as tk

class SummaryFrame(tk.Frame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        self.data_manager.observers.append(self.update_summary)
        self.create_widgets()

    def create_widgets(self):
        # สร้าง Frame สำหรับแต่ละ Label เพื่อเพิ่มกรอบและช่องว่าง
        self.income_frame = tk.Frame(self, borderwidth=1, relief="solid", padx=10, pady=5)
        self.income_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.expense_frame = tk.Frame(self, borderwidth=1, relief="solid", padx=10, pady=5)
        self.expense_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.balance_frame = tk.Frame(self, borderwidth=1, relief="solid", padx=10, pady=5)
        self.balance_frame.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        # สร้าง Label โดยให้แสดงใน Frame ที่สร้างไว้
        self.income_label = tk.Label(self.income_frame, text="ລາຍຮັບ: 0.00", fg="blue")
        self.income_label.pack()

        self.expense_label = tk.Label(self.expense_frame, text="ລາຍຈ່າຍ: 0.00", fg="red")
        self.expense_label.pack()

        self.balance_label = tk.Label(self.balance_frame, text="ຍອດເງິນຄົງເຫຼືອ: 0.00", fg="black")
        self.balance_label.pack()

    def update_summary(self):
        data = self.data_manager.get_filtered_data()
        income = sum(amount for _, amount, _ in data if amount > 0)
        expense = abs(sum(amount for _, amount, _ in data if amount < 0))
        balance = income - expense

        # จัดรูปแบบตัวเลขให้มีคอมม่า และไม่มีทศนิยม
        formatted_income = "{:,.0f}".format(income)
        formatted_expense = "{:,.0f}".format(expense)
        formatted_balance = "{:,.0f}".format(balance)

        # อัพเดท Label
        self.income_label.config(text=f"ລາຍຮັບ: {formatted_income}", fg="blue")
        self.expense_label.config(text=f"ລາຍຈ່າຍ: {formatted_expense}", fg="red")

        if balance >= 0:
            self.balance_label.config(text=f"ຍອດເງິນຄົງເຫຼືອ: {formatted_balance}", fg="blue")
        else:
            self.balance_label.config(text=f"ຍອດເງິນຄົງເຫຼືອ: {formatted_balance}", fg="red")