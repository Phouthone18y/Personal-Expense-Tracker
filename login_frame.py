import tkinter as tk

class LoginFrame(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.master.title("ເຂົ້າສູ່ລະບົບ")
        self.master.geometry("300x200+500+100")
        welcome_label = tk.Label(self, text="ຍິນດີຕອນຮັບ ພູທອນ")
        welcome_label.pack(pady=20)
        password_label = tk.Label(self, text="ລະຫັດຜ່ານ:")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        login_button = tk.Button(self, text="ເຂົ້າສູ່ລະບົບ", command=self.check_password)
        login_button.pack(pady=10)
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()

    def check_password(self):
        if self.password_entry.get() == "12345678":
            self.on_success()
        else:
            self.error_label.config(text="ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ")