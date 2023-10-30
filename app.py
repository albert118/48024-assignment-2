from tkinter import *
from Agency import Agency
from Forms.Login import LoginForm
from Views.AgencyMenu import AgencyMenu


class App:
    def __init__(self, root: Tk):
        self.root = root
        self.agency = Agency()
        self.show_login_form()

    def show_login_form(self):
        LoginForm(
            self.root,
            redirect_win=lambda: AgencyMenu(self.root, self.agency, on_close=self.root.destroy),
            on_auth=self.agency.on_auth
        )

        # hide the root after leaving the login form
        self.root.withdraw()


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
