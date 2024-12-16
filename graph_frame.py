import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class GraphFrame(tk.Frame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        self.data_manager.observers.append(self.update_graph)
        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()
        self.update_graph()

    def update_graph(self):
        self.ax.clear()
        data = self.data_manager.get_filtered_data()
        month_name = {
            '01': 'ມັງກອນ', '02': 'ກຸມພາ', '03': 'ມີນາ', '04': 'ເມສາ',
            '05': 'ພຶດສະພາ', '06': 'ມິຖຸນາ', '07': 'ກໍລະກົດ', '08': 'ສິງຫາ',
            '09': 'ກັນຍາ', '10': 'ຕຸລາ', '11': 'ພະຈິກ', '12': 'ທັນວາ',
            'ທັງໝົດ': 'All'
        }

        if self.data_manager.current_month == "ທັງໝົດ":
            self.ax.text(0.5, 0.5,
                         "ຮອງຮັບສະເພາະການເບິ່ງລາຍເດືອນເທົ່ານັ້ນ.\nກະລຸນາເລືອກເດືອນໃດນຶ່ງ.",
                         horizontalalignment='center',
                         verticalalignment='center',
                         fontsize=12,
                         color='gray',
                         transform=self.ax.transAxes)
            self.ax.set_title("ຍັງບໍ່ຮອງຮັບສຳຫຼັບໝວດ:ທັງໝົດ")
            self.fig.canvas.draw()
            return

        if not data:
            self.ax.set_title(f"ບໍ່ມີຂໍ້ມູນສຳລັບ {month_name[self.data_manager.current_month]}")
            self.fig.canvas.draw()
            return

        daily_positive_sums = {}
        daily_negative_sums = {}

        for date_str, amount, note in data:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date().day
            if amount >= 0:
                daily_positive_sums[date] = daily_positive_sums.get(date, 0) + amount
            else:
                daily_negative_sums[date] = daily_negative_sums.get(date, 0) + amount

        all_dates = sorted(set(daily_positive_sums.keys()) | set(daily_negative_sums.keys()))

        positive_amounts = [daily_positive_sums.get(date, 0) for date in all_dates]
        negative_amounts = [daily_negative_sums.get(date, 0) for date in all_dates]

        self.ax.bar(all_dates, positive_amounts, label='ລາຍຮັບ', color='blue')
        self.ax.bar(all_dates, negative_amounts, label='ລາຍຈ່າຍ', color='red')

        self.ax.set_xlabel('ວັນ')
        self.ax.set_title(f'ລາຍຮັບລາຍຈ່າຍສຳລັບເດືອນ: {month_name[self.data_manager.current_month]}')
        self.ax.set_xticks(all_dates)
        self.ax.legend()

        self.fig.canvas.draw()
