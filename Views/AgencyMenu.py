from tkinter import *
from tkinter.ttk import *
from Agency import Agency
from Flight import Flight
from Destination import Destination
from Factories import MainWindow
from Views import Error


GEOM_TABLE_VIEW = "1600x1400"


class AgencyMenu():
    def __init__(self, parent: Tk, agency: Agency):
        '''a simple high-level navigation menu for the agency app'''
        self.agency = agency

        self.main = MainWindow(
            parent=parent,
            menu_message=f'Hi {self.agency.logged_in_user.name}, welcome to the Prog2 Travel Agency',
            menu_items={
                'Explore Flights': self.on_flights,
                'Explore Destinations': self.on_destinations,
                'Book a Trip': self.on_book,
            }
        )

    ##############################################
    # menus
    ##############################################

    def on_flights(self):
        self.main.open_child_menu(
            title='Explore Flights',
            menu_message=f'Hi {self.agency.logged_in_user.name}, welcome to the Flights section',
            image_fn='flight.png',
            icon_fn='flights_icon.png',
            menu_items={
                'View All Flights': self.on_view_flights,
                'View Flights by Country': self.on_filter_flights,
                'Add Flight': self.on_add_flight,
                'Remove Flight': self.on_remove_flight
            }
        )

    def on_destinations(self):
        self.main.open_child_menu(
            title='Explore Destinations',
            menu_message=f'Hi {self.agency.logged_in_user.name}, welcome to the Destinations section',
            image_fn='destination.png',
            icon_fn='destinations_icon.png',
            menu_items={
                'View All Destinations': self.on_view_destinations,
                'View Filtered Destinations': self.on_filter_destinations,
                'Add Destination': self.on_add_destination,
                'Remove Destination': self.on_remove_destination
            }
        )

    def on_book(self):
        self.main.open_child_menu(
            title='Book a Trip',
            menu_message=f'Hi {self.agency.logged_in_user.name}, welcome to the Trip section',
            image_fn='trip.png',
            icon_fn='trip_icon.png',
            menu_items={
                # redirects to the existing destination add/remove forms
                # TODO: check example video if trip/destination photo should show here... :/
                'Add Destination': self.on_add_destination,
                'Remove Destination': self.on_remove_destination,
                # autogenerate the itinerary, this is then visible in 'View Trip'
                'Add Connecting Flights': self.on_add_connecting,
                'View Trip': self.on_view_trip
            }
        )

    ##############################################
    # sub-menu forms
    ##############################################

    def on_view_flights(self):
        self.main.child_menu.open_sub_menu(
            title='Display Flights',
            menu_message='Flights',
            menu_items={},
            table_data=self.agency.get_flight_dataframe(),
            geom=GEOM_TABLE_VIEW
        )

    def on_filter_flights(self):
        form_data = { 'Country': None }
        # TODO: add filter + callback to self.agency.get_filtered_flights
        self.main.child_menu.open_sub_menu(
            title='Display Flights Filtered',
            menu_message='Filtered Flights',
            form_fields=form_data,
            menu_items={},
            geom=GEOM_TABLE_VIEW
        )

    def on_add_flight(self):
        form_data = {
            'Airline': None,
            'Flight Number': None,
            'Takeoff': None,
            'Landing': None,
            'Cost': None
        }

        def on_add():
            try:
                self.agency.flights.add_flight(Flight(
                    # these are tkinter form fields, remember to call get()
                    form_data['Airline'].get(),
                    form_data['Flight Number'].get(),
                    form_data['Takeoff'].get(),
                    form_data['Landing'].get(),
                    form_data['Cost'].get()
                ))
            except Exception as ex:
                Error(self.main, ex)

        self.main.child_menu.open_sub_menu(
            title='Add Flight',
            menu_message='Add a Flight',
            form_fields=form_data,
            menu_items={ 'Add Flight': on_add },
            disable_primary_action=True,
            close_on_submit=True,
            geom="1600x900"
        )

    def on_remove_flight(self):
        form_data = {
            'Takeoff': None,
            'Landing': None,
        }

        def on_remove():
            # given takeoff + landing determine the flight
            # if it exists, remove it, else open the error window
            takeoff = form_data['Takeoff'].get()
            landing = form_data['Landing'].get()
            
            try:
                if self.agency.flights.has_flight(takeoff, landing):
                    f = self.agency.flights.get_flight(takeoff, landing)
                    self.agency.flights.remove_flight(f)
            except Exception as ex:
                Error(self.main, ex)

        self.main.child_menu.open_sub_menu(
            title='Remove Flight',
            menu_message='Remove a Flight',
            form_fields=form_data,
            menu_items={ 'Remove Flight': on_remove },
            disable_primary_action=True,
            close_on_submit=True,
            geom="1600x800"
        )

    def on_view_destinations(self):
        self.main.child_menu.open_sub_menu(
            title='Display Destinations',
            menu_message='Destinations',
            menu_items={},
            table_data=self.agency.get_destinations_dataframe(),
            geom=GEOM_TABLE_VIEW
        )

    def on_filter_destinations(self):
        form_data = { 'Country': None }
        # TODO: add filter + callback to self.agency.get_filtered_flights
        self.main.child_menu.open_sub_menu(
            title='Display Destinations Filtered',
            menu_message='Filtered Flights',
            form_fields=form_data,
            menu_items={},
            geom=GEOM_TABLE_VIEW
        )

    def on_add_destination(self):
        form_data = {
            'Name': None,
            'Country': None
        }

        def on_add():
            try:
                self.agency.destinations.add_destination(Destination(
                    # these are tkinter form fields, remember to call get()
                    form_data['Name'].get(),
                    form_data['Country'].get()
                ))
            except Exception as ex:
                Error(self.main, ex)


        self.main.child_menu.open_sub_menu(
            title='Add Destination',
            menu_message='Add a Destination',
            form_fields=form_data,
            menu_items={ 'Add Destination': on_add },
            disable_primary_action=True,
            close_on_submit=True,
            geom="1600x800"
        )

    def on_remove_destination(self):
        form_data = {
            'Name': None,
            'Country': None
        }

        def on_remove():
            # similar to on_remove for flights
            # if it exists, remove it, else open the error window
            name = form_data['Name'].get()
            country = form_data['Country'].get()
            
            try:
                if self.agency.has_destination(name, country):
                    d = self.agency.get_destination(name, country)
                    self.agency.destinations.remove_destination(d)
            except Exception as ex:
                Error(self.main, ex)

        self.main.child_menu.open_sub_menu(
            title='Remove Destinations',
            menu_message='Remove a Destination',
            form_fields=form_data,
            menu_items={ 'Remove Destination': on_remove },
            disable_primary_action=True,
            close_on_submit=True,
            geom="1600x800"
        )

    def on_add_connecting(self):
        try:
            self.agency.trip.add_connecting_flights()
        except Exception as ex:
            Error(self.main, ex)

    def on_view_trip(self):
        # TODO: determine the value clicked on, use it to switch the redirect
        # TODO: add a list-view (instead of the typical table view)
        # TODO: add "Nothing Yet" default text when there is no trip in the list
        self.main.child_menu.open_sub_menu(
            title='Display Trip',
            menu_message='Your Trip',
            menu_items={
                'View Individual': lambda menu_choice: print(f'go to {menu_choice}'),
            },
            table_data={ 'Itinery': self.trip.get_itinery() }
        )
