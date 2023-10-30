from tkinter import ttk


LIGHT_BLUE = '#168FC1'
ACCENT_BLUE = '#0B729C'
GREY_BLUE = '#E2f3ff' # converted background color from RGB > HEX to avoid Tkinter issues
TABLE_GRAY = '#d1d0d0'
LIGHT_GRAY = '#f2f1f1'

FONT_PRIMARY = ("Arial Narrow", 11, "bold")
FONT_LABEL = ("Helvetica", 10, "bold")

@staticmethod
def setup_styling():
    style = ttk.Style()
    style.configure('TSeparator', background='grey')

    style.configure('TButton', background=LIGHT_BLUE, foreground='white', border=LIGHT_BLUE, padding=6, font=FONT_PRIMARY)
    style.map('TButton', background=[('active', ACCENT_BLUE)])

    style.configure('TEntry', padding=6, font=("Arial", 11), background=GREY_BLUE)

    # TODO: fix the TEntry style to show the border color when focussed (currently does not show)
    style.map('TEntry', bordercolor=[('focus', ACCENT_BLUE)], relief=[('focus', 'solid')])

    style.configure('TLabel', foreground=LIGHT_BLUE, font=FONT_LABEL)

    style.configure('ExceptionType.TLabel', foreground='red', font=FONT_LABEL)
    style.configure('ExceptionMessage.TLabel', foreground=LIGHT_BLUE, font=FONT_LABEL)

    style.configure('Treeview', rowheight=40)
    style.configure("Treeview.Heading", background=TABLE_GRAY, foreground=LIGHT_BLUE, font=FONT_LABEL, padding=(10, 5))

