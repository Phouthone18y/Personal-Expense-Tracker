import tkinter as tk
from tkinter import ttk


class TableFrame(tk.Frame):
    def __init__(self, master, data_manager, input_frame):
        super().__init__(master)
        self.data_manager = data_manager
        self.input_frame = input_frame
        self.data_manager.observers.append(self.update_table)
        self.selected_item = None
        self.create_widgets()


    def create_widgets(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="ກັ່ນຕອງເດືອນ:").pack(side=tk.LEFT, padx=5)
        self.all_months = ["ທັງໝົດ"] + [str(i) for i in range(1, 13)]
        self.current_month = tk.StringVar(value="ທັງໝົດ")
        self.month_cb = ttk.Combobox(filter_frame, values=self.all_months, textvariable=self.current_month, state="readonly", width=10)
        self.month_cb.pack(side=tk.LEFT)
        self.month_cb.current(0)
        self.month_cb.bind("<<ComboboxSelected>>", self.filter_data)
        self.tree = ttk.Treeview(self, columns=("Date", "Amount", "Note"), show='headings')
        self.tree.heading("Date", text="ວັນທີ")
        self.tree.heading("Amount", text="ຈຳນວນເງິນ")
        self.tree.heading("Note", text="ໝາຍເຫດ")
        self.tree.pack(padx=5, pady=5)


        # กำหนด tags สำหรับค่าบวก (สีน้ำเงิน) และค่าลบ (สีแดง)
        self.tree.tag_configure("positive", foreground="blue")
        self.tree.tag_configure("negative", foreground="red")


        delete_button = tk.Button(self, text="ລຶບຂໍ້ມູນ", command=self.delete_entry)
        delete_button.pack(pady=10)


        self.tree.bind("<ButtonRelease-1>", self.on_item_selected)
        self.update_table()


    def on_item_selected(self, event):
        self.selected_item = self.tree.selection()
        if self.selected_item:
            item = self.tree.item(self.selected_item)
            date_str, amount_str, note = item['values']
            amount_str = amount_str.replace(",", "")
            amount = float(amount_str)
            self.input_frame.set_input_values(date_str, amount, note)
            self.input_frame.enable_edit_mode(True)
        else:
           self.input_frame.enable_edit_mode(False)


    def deselect_item(self):
        if self.selected_item:
            self.tree.selection_remove(self.selected_item)
            self.selected_item = None
        self.input_frame.clear_input()
        self.input_frame.enable_edit_mode(False)


    def delete_entry(self):
       selected_item = self.tree.selection()
       if selected_item:
           date_str, amount_str, note = self.tree.item(selected_item)['values']
           # แก้ไข: ลบคอมม่าออกจาก amount_str ก่อนแปลงเป็น float
           amount_str = amount_str.replace(",", "")
           amount = float(amount_str)
           self.data_manager.delete_entry(date_str, amount, note)


    def filter_data(self, event=None):
        selected_month = self.current_month.get()
        if selected_month != "ທັງໝົດ":
            selected_month = f"{int(selected_month):02}"
        self.data_manager.filter_data(selected_month)
        self.update_table()


    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        data = self.data_manager.get_filtered_data()
        for date_str, amount, note in data:
            # จัดรูปแบบตัวเลขให้มีคอมม่าคั่น
            formatted_amount = "{:,}".format(amount)


            # กำหนด tag ตามค่า amount
            if amount >= 0:
                tag = "positive"
            else:
                tag = "negative"


            # แทรกข้อมูลโดยกำหนด tag เฉพาะคอลัมน์ที่ 2 (Amount)
            item_id = self.tree.insert("", tk.END, values=(date_str, formatted_amount, note))
            self.tree.item(item_id, tags=(tag,))
