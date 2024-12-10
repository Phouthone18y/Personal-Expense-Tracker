import json
import datetime

class DataManager:
    def __init__(self):
        self.entries = []
        self.observers = []
        self.current_month = "ທັງໝົດ"
        self.data_file = "account_data.json"
        self.load_data()

    def add_entry(self, date, amount, note):
        date_str = date.strftime("%Y-%m-%d")
        self.entries.append((date_str, amount, note))
        self.save_data()
        self.notify_observers()

    def delete_entry(self, date, amount, note):
        entry_to_remove = (date, amount, note)
        if entry_to_remove in self.entries:
            self.entries.remove(entry_to_remove)
            self.save_data()
            self.notify_observers()

    def filter_data(self, month):
        self.current_month = month
        self.notify_observers()

    def get_filtered_data(self):
        if self.current_month == "ທັງໝົດ":
            return self.entries
        filtered = []
        for date_str, amount, note in self.entries:
            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                if f"{date_obj.month:02}" == self.current_month:
                    filtered.append((date_str, amount, note))
            except ValueError:
                print(f"ຮູບແບບວັນທີບໍ່ຖືກຕ້ອງ: {date_str}")
        return filtered

    def notify_observers(self):
        for observer in self.observers:
            observer()

    def save_data(self):
        new_entries = []
        for date_str, amount, note in self.entries:
            try:
                amount_str = str(amount)
                new_entries.append((date_str, amount_str, note))
            except (TypeError, ValueError):
                print(f"ຈຳນວນເງິນບໍ່ຖືກຕ້ອງສຳລັບການບັນທຶກ: {amount}")
        with open(self.data_file, 'w') as f:
            json.dump(new_entries, f, indent=4)

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                loaded_entries = json.load(f)
            new_entries = []
            for date_str, amount_str, note in loaded_entries:
                try:
                    amount = float(amount_str)
                    new_entries.append((date_str, amount, note))
                except ValueError as e:
                    print(f"ຂໍ້ຜິດພາດໃນການແປງຈຳນວນເງິນ: {amount_str}")
            self.entries = new_entries
        except FileNotFoundError:
            pass