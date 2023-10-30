from tkinter import *
from tkinter.ttk import *
from typing import Callable
import Styles
from Views import Error
from Factories.AssetUtil import load_icon


DEBUG = False # simplify login while testing


class LoginForm():
    def __init__(self, parent: Tk, redirect_win: Tk, on_auth: Callable):
        '''a simple tkinter auth form'''
        self.conf_window(parent)
        self.redirect_win = redirect_win
        self.on_auth = on_auth

        (section_frame, inputs_frame) = self.setup_layout()

        self.add_heading(section_frame)
        self.add_inputs(inputs_frame)
        self.add_actions()

        if DEBUG: self.on_login()

    def conf_window(self, parent: Tk):
        self.window = Toplevel(parent)
        self.window.iconphoto(False, load_icon('login_icon.png'))
        self.window.title('Login')
        self.window.geometry('800x400')
        Styles.setup_styling()

    def setup_layout(self):
        # configure the grid as a 2x4 with equal columns
        for i in range(2):
            self.window.columnconfigure(i, weight=1)

        # equally weight the content rows
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(3, weight=1)

        # setup a frame to hold the form heading and divider
        section_frame = Frame(self.window)
        section_frame.grid(row=0, column=0, columnspan=2)

        # and a further frame for the inputs
        inputs_frame = Frame(self.window)
        inputs_frame.grid(row=3, column=0, columnspan=2)

        return (section_frame, inputs_frame)

    def add_inputs(self, inputs_frame: Frame):
        username_label = Label(inputs_frame, text="Username:")
        password_label = Label(inputs_frame, text="Password:")
        self.username_entry = Entry(inputs_frame)
        self.password_entry = Entry(inputs_frame, show="*")

        # arrange the inputs and labels next to each other
        username_label.grid(row=2, column=0)
        self.username_entry.grid(row=2, column=1)
        password_label.grid(row=3, column=0)
        self.password_entry.grid(row=3, column=1)

        # default focus to the input
        self.username_entry.focus_force()

    def add_actions(self):
        # disabled by default
        self.login_btn = Button(self.window, text="Login",
                                command=self.on_login, state='disabled')

        exit_btn = Button(self.window, text="Exit", command=self.on_exit)
        # flex these buttons and fill the x-axis as per the design spec
        self.login_btn.grid(row=4, column=0, sticky="we")
        exit_btn.grid(row=4, column=1, sticky="we")

        # register validation to toggle the login button state
        self.username_entry.bind('<KeyRelease>', self.validate_entries)
        self.password_entry.bind('<KeyRelease>', self.validate_entries)

    def add_heading(self, section_frame):
        heading_label = Label(section_frame, text="Login")

        divider = Separator(
            master=self.window,
            orient=HORIZONTAL,
            style='TSeparator',
            class_=Separator
        )

        # arrange everything
        heading_label.grid(row=0, column=0)
        divider.grid(row=1, column=0, columnspan=2, sticky="we")

    def validate_entries(self, value):
        # toggle the state if the entries have values
        if bool(self.username_entry.get() and self.password_entry.get()):
            self.login_btn.config(state='normal')
        else:
            self.login_btn.config(state='disabled')
        return True

    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            user = self.on_auth(username, password)
            print(f'{__name__}: user {user.name} logged in, redirecting to agency home')
            self.on_exit()
            self.redirect_win()
        except Exception as ex:
            Error(self.window, ex)
            self.window.destroy()

    def on_exit(self):
        print(f'{__name__}: exiting login')
        self.window.destroy()
