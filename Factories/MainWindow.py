from tkinter import *
from tkinter.ttk import *
from typing import Callable
from Factories.MenuWindow import MenuWindow
from Factories.LayoutBuilder import LayoutBuilder
from Factories.AssetUtil import load_icon


class MainWindow:
    def __init__(self, parent: Tk, menu_message: str, menu_items: dict,
                 on_close: Callable, title='Prog2 Travel Agency', icon_fn='agency_icon.png', 
                 image_fn='agency.png', geom="1600x700"):
        '''construct a new window with some common config'''
        print(f'{__name__}: created main window')

        self.on_close = on_close
        self._title = title

        self.conf_window(parent, title, icon_fn, geom)
        self.child_menu = None

        # add the app's exit condition
        menu_items['Exit'] = self.on_exit

        # build the layout
        (LayoutBuilder(self.window, dimms=(len(menu_items), 5))
            .add_image(window_width=1600, image_fn=image_fn)
            .add_separator()
            .add_heading(menu_message=menu_message,)
            .add_separator()
            .add_menu(menu_items)
        )

    def conf_window(self, parent, title, icon_fn, geom):
        self.window = Toplevel(parent)
        self.window.title(self._title)
        self.window.iconphoto(False, load_icon(icon_fn))
        self.window.geometry(geom)

    def on_exit(self):
        print(f'{__name__}: exiting {self._title}')
        self.window.destroy()
        self.on_close()

    def cleanup_child(self):
        self.child_menu = None

    def open_child_menu(self, **kwargs):
        self.child_menu = MenuWindow(self.window, close_callback=self.cleanup_child, **kwargs)
        # wait for this menu to close
        self.window.wait_window(self.child_menu.window)
