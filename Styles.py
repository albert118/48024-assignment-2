from tkinter import ttk


LIGHT_BLUE = '#168FC1'
ACCENT_BLUE = '#0B729C'
GREY_BLUE = '#E2f3ff' # converted background color from RGB > HEX to avoid Tkinter issues
TABLE_GRAY = '#d1d0d0'

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

    # TODO: rowheight should work here
    style.configure('TreeView', background=LIGHT_BLUE, anchor="w", rowheight=20)
    style.configure("Treeview.Heading", background=TABLE_GRAY, border=LIGHT_BLUE, foreground=LIGHT_BLUE, padding=6, font=FONT_LABEL)
    style.map('Treeview.Heading', background=[('active', TABLE_GRAY)]) # disable active header styling

    # TODO: fix the below to show borders (borders not appearing)
    style.configure('Treeview.Cell', bordercolor='black', borderwidth=1, padding=(10, 5), rowheight=50, font=("Arial", 8))

    style.configure('ExceptionType.TLabel', foreground='red', font=FONT_LABEL)
    style.configure('ExceptionMessage.TLabel', foreground=LIGHT_BLUE, font=FONT_LABEL)




