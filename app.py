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
        # Input Frame
        self.input_frame = InputFrame(self, self.data_manager)
        self.input_frame.grid(row=0, column=0, sticky="ew")

        # Table Frame
        self.table_frame = TableFrame(self, self.data_manager, self.input_frame)
        self.table_frame.grid(row=1, column=0, sticky="nsew",)

        # Graph Frame
        self.graph_frame = GraphFrame(self, self.data_manager)
        self.graph_frame.grid(row=0, column=1, rowspan=3)


        # Summary Frame
        self.summary_frame = SummaryFrame(self, self.data_manager)
        self.summary_frame.grid(row=2, column=0,sticky="ew")

        # Configure grid weights for responsive resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.input_frame.master = self
        self.table_frame.master = self

    def on_window_click(self, event):
        if event.widget not in (self.table_frame.tree,
                                *self.input_frame.winfo_children(),
                                 self.table_frame.delete_button): # Modified line
            self.table_frame.deselect_item()


if __name__ == "__main__":
    app = App()
    app.mainloop()
