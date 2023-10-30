from tkinter import *
from tkinter.ttk import *
from typing import Callable
from Factories.LayoutBuilder import LayoutBuilder
from Factories.AssetUtil import load_icon


GEOM = "1600x700"
WINDOW_WIDTH = 1600


class MenuWindow():
    def __init__(self, parent: Tk, title: str, menu_message: str,
                 close_callback: Callable, menu_items: dict, image_fn='',
                 icon_fn='', table_data=None, form_fields=None, 
                 disable_primary_action=False, close_on_submit=False,
                 filters=None, error=None, geom=GEOM):
        '''construct a new window for a menu page'''

        print(f'{__name__}: opened {title}')
        
        self.conf_window(parent, title, close_callback, image_fn, icon_fn, geom)

        # add a default close menu option that returns to the outer menu
        menu_items['Close'] = self.on_close

        if close_on_submit:
            # update the primary action to close after running
            primary_key = list(menu_items.keys())[0]
            original_action = menu_items[primary_key]
            menu_items[primary_key] = lambda: (original_action(), self.on_close())

        # build the layout
        self.layout = LayoutBuilder(self.window, dimms=(len(menu_items), 5))
            
        if len(image_fn) > 0:
            self.layout.add_image(WINDOW_WIDTH, image_fn)
        
        (self.layout
            .add_separator()
            .add_heading(menu_message=menu_message)
            .add_separator()
        )

        if error is not None:
            self.layout.add_error_message(error_message=error)
        
        if form_fields is not None:
            self.layout.add_form(form_fields)

        if table_data is not None:
            self.layout.add_table_data(
                window_width=WINDOW_WIDTH,
                table_data=table_data,
                filters=filters
            )
        
        self.layout.add_menu(menu_items, disable_primary_action)

    def conf_window(self, parent, title, close_callback, image_fn, icon_fn, geom):
        self.window = Toplevel(parent)
        # place this new window on-top of the parent and wait on this window's outcome
        self.window.wm_transient(parent)
        self.window.title(title)
        self.window.iconphoto(False, load_icon(icon_fn))
        self.window.geometry(geom)
        self.close_callback = close_callback
        self.image_fn = image_fn

    def on_close(self):
        print(f'{__name__}: closing menu')
        self.window.destroy()
        self.close_callback()

    def open_sub_menu(self, **kwargs):
        print(f'{__name__}: {kwargs["title"]}')
        sub_menu = MenuWindow(
            self.window,
            # display the same image on sub-menus as their parent
            image_fn=self.image_fn,
            close_callback=lambda: print('closed sub-menu'),
            **kwargs
        ).window

        # wait for this sub-menu to close
        self.window.wait_window(sub_menu)
