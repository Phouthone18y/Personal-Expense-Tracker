import tkinter as tk
from tkcalendar import DateEntry
import datetime

class InputFrame(tk.Frame):
    def __init__(self, master, data_manager=None):
        super().__init__(master)
        self.data_manager = data_manager
        self.editing_item = None
        self.edit_mode = False  # Track if in edit mode
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="ວັນທີ:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = DateEntry(self, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.set_date(datetime.date.today())
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="ຈຳນວນເງິນ:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="ໝາຍເຫດ:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.note_entry = tk.Entry(self)
        self.note_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.add_button = tk.Button(self, text="ເພີ່ມຂໍ້ມູນ", command=self.add_entry)
        self.add_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")
        self.edit_button = tk.Button(self, text="ບັນທຶກການແກ້ໄຂ", command=self.update_entry, state=tk.DISABLED)
        self.edit_button.grid(row=3, column=2, padx=5, pady=10, sticky="e")

    def add_entry(self):
        date = self.date_entry.get_date()
        try:
            amount = float(self.amount_entry.get())
            note = self.note_entry.get()
            if self.data_manager:
                self.data_manager.add_entry(date, amount, note)
                self.set_input_values(date.strftime("%Y-%m-%d"), amount, note)
            self.clear_input()
        except ValueError:
            print("ກະລຸນາໃສ່ຈຳນວນເງິນເປັນຕົວເລກ")

    def update_entry(self):
        date = self.date_entry.get_date()
        try:
            amount = float(self.amount_entry.get())
            note = self.note_entry.get()
            if self.data_manager and self.master.table_frame.selected_item:
                old_date_str, old_amount_str, old_note = self.master.table_frame.tree.item(self.master.table_frame.selected_item)['values']
                old_amount_str = old_amount_str.replace(",", "")
                old_amount = float(old_amount_str)

                self.data_manager.update_entry(old_date_str, old_amount, old_note, date, amount, note)
                self.master.table_frame.update_table()
                self.clear_input()
                self.enable_edit_mode(False)
        except ValueError:
            print("ກະລຸນາໃສ່ຈຳນວນເງິນເປັນຕົວເລກ")

    def enable_edit_mode(self, enable):
        self.edit_mode = enable
        if enable:
            self.add_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.NORMAL)
        else:
            self.add_button.config(state=tk.NORMAL)
            self.edit_button.config(state=tk.DISABLED)

    def set_input_values(self, date_str, amount, note):
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        self.date_entry.set_date(date_obj)
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(amount))
        self.note_entry.delete(0, tk.END)
        self.note_entry.insert(0, note)

    def clear_input(self):
        self.date_entry.set_date(datetime.date.today())
        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        self.editing_item = None
