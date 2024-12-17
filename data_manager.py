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
        entry_to_remove = (date, amount, str(note)) # Modified line
        for entry in self.entries:
           date_str, amount_str, note_str = entry
           if date_str == date and amount_str == amount and str(note_str) == str(note): # Modified line
                self.entries.remove(entry)
                self.save_data()
                self.notify_observers()
                return


    def update_entry(self, old_date_str, old_amount, old_note, new_date, new_amount, new_note):
        new_date_str = new_date.strftime("%Y-%m-%d")
        for i, (date_str, amount, note) in enumerate(self.entries):
            if date_str == old_date_str and amount == old_amount and note == old_note:
                self.entries[i] = (new_date_str, new_amount, new_note)
                self.save_data()
                self.notify_observers()
                return

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
