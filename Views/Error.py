from tkinter import Tk
from Factories import MenuWindow

class Error:
    def __init__(self, parent: Tk, error: Exception):
        print(f'{__name__}: {error}')

        self.error = MenuWindow(
            parent=parent,
            title='Error',
            menu_message='Error',
            error=error,
            image_fn='error.png',
            icon_fn='error_icon.png',
            close_callback=lambda: print(f'{__name__}: closed window'), 
            menu_items={}
        )

        # wait for the user to read the error and close it
        parent.wait_window(self.error.window)
