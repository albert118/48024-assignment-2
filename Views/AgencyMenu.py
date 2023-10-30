from tkinter import *
from tkinter.ttk import *
from typing import Callable
from Agency import Agency
from Flight import Flight
from Destination import Destination
from Factories import MainWindow
from Views.Error import Error


GEOM_TABLE_VIEW = "1600x1400"


class AgencyMenu():
    def __init__(self, parent: Tk, agency: Agency, on_close: Callable):
        '''a simple high-level navigation menu for the agency app'''
        self.agency = agency

        self.main = MainWindow(
            parent=parent,
            on_close=on_close,
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
                'Add Destination': self.on_book_destination,
                'Remove Destination': self.on_unbook_destination,
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
        self.main.child_menu.open_sub_menu(
            title='Display Flights Filtered',
            menu_message='Filtered Flights',
            filters={ 
                'Country': lambda *args: on_filter_flights(self.agency.get_flight_dataframe()['rows'], *args)
            },
            menu_items={},
            table_data=self.agency.get_flight_dataframe(),
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
            f_no = None
            
            try:
                f_no = int(form_data['Flight Number'].get())
            except ValueError:
                Error(self.main.window, Exception('cannot add flight, flight number invalid'))
                return

            f_cost = None
            try:
                f_cost = float(form_data['Cost'].get())
            except ValueError:
                Error(self.main.window, Exception('cannot add flight, cost invalid'))
                return

            try:
                self.agency.flights.add_flight(Flight(
                    # these are tkinter form fields, remember to call get()
                    form_data['Airline'].get(),
                    f_no,
                    form_data['Takeoff'].get(),
                    form_data['Landing'].get(),
                    f_cost
                ))
            except Exception as ex:
                Error(self.main.window, ex)
                return

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
                Error(self.main.window, ex)

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
        self.main.child_menu.open_sub_menu(
            title='Display Destinations Filtered',
            menu_message='Filtered Flights',
            filters={ 
                'Country': lambda *args: on_filter_destinations(self.agency.get_destinations_dataframe()['rows'], *args)
            },
            menu_items={},
            table_data=self.agency.get_destinations_dataframe(),
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
                Error(self.main.window, ex)

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
                d = self.agency.destinations.get_destination(name, country)
                self.agency.destinations.remove_destination(d)
            except Exception as ex:
                Error(self.main.window, ex)

        self.main.child_menu.open_sub_menu(
            title='Remove Destinations',
            menu_message='Remove a Destination',
            form_fields=form_data,
            menu_items={ 'Remove Destination': on_remove },
            disable_primary_action=True,
            close_on_submit=True,
            geom="1600x800"
        )

    def on_book_destination(self):
        form_data = {
            'Name': None,
            'Country': None
        }

        def on_add():
            try:
                self.agency.trip.destinations.add_destination(Destination(
                    form_data['Name'].get(),
                    form_data['Country'].get()
                ))
            except Exception as ex:
                Error(self.main.window, ex)

        self.main.child_menu.open_sub_menu(
            title='Add Destination',
            menu_message='Add a Destination',
            form_fields=form_data,
            menu_items={ 'Add Destination': on_add },
            disable_primary_action=True,
            close_on_submit=True,
            geom="1600x800"
        )

    def on_unbook_destination(self):
        form_data = {
            'Name': None,
            'Country': None
        }

        def on_remove():
            name = form_data['Name'].get()
            country = form_data['Country'].get()
            
            try:
                d = self.agency.trip.destinations.get_destination(name, country)
                self.agency.trip.destinations.remove_destination(d)
            except Exception as ex:
                Error(self.main.window, ex)

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
            Error(self.main.window, ex)

    def on_view_trip(self):
        def redirect(choice: str):
            if choice == 'destination':
                self.on_view_destinations()
                return
            elif choice == 'flight':
                self.on_view_flights()
                return
            else:
                Error(self.main.window, Exception('cannot navigate to both a flight and destination (choose one)'))
                return
            
        itinery = []
        try:
            itinery = self.agency.trip.get_itinery()
        except:
            pass

        self.main.child_menu.open_sub_menu(
            title='Display Trip',
            menu_message='Your Trip',
            menu_items={
                'View Individual': lambda menu_choice: redirect(menu_choice),
            },
            list_data={ 'data': itinery, 'default': 'Nothing yet' }
        )

###########################
# helpers
###########################

def on_filter_destinations(rows: list, value: str, table: Treeview):
    # remove the old table
    table.delete(*table.get_children())

    if len(value.strip()) == 0:
        rebuild_table(table, rows)

    # and rebuild it from scratch - this is very brute force
    # listified data is a tuple, second elem is 'Country'
    filtered_rows = [r for r in rows if r[1].lower() == value.lower()]
    rebuild_table(table, filtered_rows)

def on_filter_flights(rows: list, value: str, table: Treeview):
    # remove the old table
    table.delete(*table.get_children())

    if len(value.strip()) == 0:
        rebuild_table(table, rows)

    # and rebuild it from scratch - this is very brute force
    # listified data is a tuple, third elem is 'takeoff country', fourth is 'landing country'
    filtered_rows = [r for r in rows if r[2].lower() == value.lower() or r[3].lower() == value.lower()]
    rebuild_table(table, filtered_rows)

def rebuild_table(table, rows):
    for idx, row in enumerate(rows):
        tags = ('evenrow',) if idx % 2 == 0 else ('oddrow',)
        table.insert('', 'end', values=row, tags=tags, iid=idx)