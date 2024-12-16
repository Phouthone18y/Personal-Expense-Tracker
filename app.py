import tkinter as tk
from input_frame import InputFrame
from table_frame import TableFrame
from graph_frame import GraphFrame
from data_manager import DataManager
from summary_frame import SummaryFrame
from login_frame import LoginFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.show_login_frame()
        self.bind("<Button-1>", self.on_window_click)


    def show_login_frame(self):
        self.login_frame = LoginFrame(self, on_success=self.show_main_frames)
        self.login_frame.pack()


    def show_main_frames(self):
        self.login_frame.destroy()
        self.create_widgets()
        self.update()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.title("ບັນຊີລາຍຮັບລາຍຈ່າຍ")
        self.geometry(f"{int(width * 1)}x{int(height * 0.7)}+{int(width * 0)}+{int(height * 0.1)}")


    def create_widgets(self):
        self.input_frame = InputFrame(self, self.data_manager)
        self.input_frame.grid(row=0, column=0, sticky="w")

        self.table_frame = TableFrame(self, self.data_manager, self.input_frame)
        self.table_frame.grid(row=1, column=0)

        self.input_frame.master = self  # Pass the main app object to InputFrame
        self.table_frame.master = self
        self.summary_frame = SummaryFrame(self, self.data_manager)
        self.summary_frame.grid(row=2, column=0, sticky="w", padx=20)


        self.graph_frame = GraphFrame(self, self.data_manager)
        self.graph_frame.grid(row=0, column=1, rowspan=3)

    def on_window_click(self, event):
        if event.widget not in (self.table_frame.tree,
                                *self.input_frame.winfo_children()):
            self.table_frame.deselect_item()

if __name__ == "__main__":
    app = App()
    app.mainloop()
