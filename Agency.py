from tkinter import Tk

DEBUG = True # simplify login while testing

class Agency:
    def __init__(self):
        from Administrators import Administrators
        from Destinations import Destinations
        from Flights import Flights
        from Trip import Trip

        self.logged_in_user = None
        self.admins = Administrators()
        self.admins.insert_dummy_data()

        self.flights = Flights(self)

        self.destinations = Destinations(self)
        self.destinations.insert_dummy_data()

        self.trip = Trip(self)

    def is_logged_in(self) -> bool:
        return self.logged_in_user is not None

    def on_auth(self, *args):
        if DEBUG:
            print(f'{__name__}: DEBUG mode! Will login as: "{self.admins.administrators[0].name}"')
            self.logged_in_user = self.admins.administrators[0]
        else:        
            print(f'{__name__}: checking username "{args[0]}"')
            self.logged_in_user = self.admins.get_administrator(*args)
        
        return self.logged_in_user
        

    def get_flight_dataframe(self) -> dict:
        return {
            'columns': ['Airline', 'Flight Number', 'Takeoff Country', 'Landing Country', 'Cost'],
            'rows': [f.listify() for f in self.flights.flights]
        }
    
    def get_destinations_dataframe(self) -> dict:
        return {
            'columns': ['Name', 'Country'],
            'rows': [d.listify() for d in self.destinations.destinations]
        }