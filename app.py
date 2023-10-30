import tkinter as tk
from Agency import Agency
from Forms.Login import LoginForm
from Views.AgencyMenu import AgencyMenu


class FlightsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.agency = Agency()

        LoginForm(
            self,
            redirect_win=lambda: AgencyMenu(self.agency),
            on_auth=self.agency.on_auth
        )


if __name__ == "__main__":
    app = FlightsApp()
    app.mainloop()
