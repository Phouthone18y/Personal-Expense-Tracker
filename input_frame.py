import tkinter as tk
from tkcalendar import DateEntry
import datetime

class InputFrame(tk.Frame):
    def __init__(self, master, data_manager=None):
        super().__init__(master)
        self.data_manager = data_manager
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="ວັນທີ:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.set_date(datetime.date.today())
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self, text="ຈຳນວນເງິນ:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self, text="ໝາຍເຫດ:").grid(row=2, column=0, padx=5, pady=5)
        self.note_entry = tk.Entry(self)
        self.note_entry.grid(row=2, column=1, padx=5, pady=5)
        add_button = tk.Button(self, text="ເພີ່ມຂໍ້ມູນ", command=self.add_entry)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_entry(self):
        date = self.date_entry.get_date()
        try:
            amount = float(self.amount_entry.get())
            note = self.note_entry.get()
            if self.data_manager:
                self.data_manager.add_entry(date, amount, note)
            self.amount_entry.delete(0, tk.END)
            self.note_entry.delete(0, tk.END)
        except ValueError:
            print("ກະລຸນາໃສ່ຈຳນວນເງິນເປັນຕົວເລກ")