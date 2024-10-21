import tkinter as tk
from tkinter import ttk

class PopUpWindow(tk.Tk):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.add_child_window(self)


    def destroy(self):
        try:
            self.master.remove.child_window()
        except:
            pass
        return super().destroy()
