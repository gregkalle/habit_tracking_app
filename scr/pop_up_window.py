"""
NAME
    pop_up_window - contains the parent for all kind of pop-up windows of the habit tracking app

DESCRIPTION
    Override the destroy method of tkinter.Tk

CLASSES
    tkinter.Tk
        PopUpWindow
"""
from tkinter import Tk

class PopUpWindow(Tk):

    """
    A base class for creating pop-up windows.

    Args:
        main_window (tkinter.Tk): The main application window.
    
    Attributes:
        main_window (tkinter.Tk): The main application window.

    Raises:
        AttributeError: main window has no attribute add_child_window
    """

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        #position of the child window
        position_x = 300 + self.main_window.winfo_x()
        position_y = 300 + self.main_window.winfo_y()
        self.geometry(f"+{position_x}+{position_y}")
        try:
            self.main_window.add_child_window(self)
        except AttributeError as exc:
            self.destroy()
            raise AttributeError("main window has no attribute add_child_window") from exc

    def destroy(self):
        """
        Override the destroy method to remove the child window reference from the main window.

        Raises:
            AttributeError: Main window has no attribut remove_child_window
        """
        try:
            self.main_window.remove_child_window(self)
        except AttributeError as exc:
            raise AttributeError("Main window has no attribut remove_child_window") from exc
        return super().destroy()
