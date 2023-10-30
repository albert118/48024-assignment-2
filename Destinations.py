from Destination import Destination
from Agency import Agency
from Utils import Utils


class Destinations:
    def __init__(self, agency: Agency):
        self.agency = agency
        self.destinations = []

    def add_destination(self, destination: Destination):
        if self.has_destination(destination.name, destination.country):
            raise Exception('cannot add destination (already exists)')
        self.destinations.append(destination)

    def remove_destination(self, destination: Destination):
        if self.has_destination(destination.name, destination.country) == False:
            raise Exception('cannot remove destination (does not exist)')
        self.destinations.remove(destination)

    def has_destination(self, name, country):
        for d in self.destinations:
            if d.name == name and d.country == country:
                return True
        return False

    def get_destination(self, name, country):
        if not self.has_destination(name, country):
            raise Exception('cannot get destination (does not exist)')
        for d in self.destinations:
            if d.name == name and d.country == country:
                return d
        return None

    def insert_dummy_data(self):
        self.destinations.append(Destination("Eiffel Tower", "France"))
        self.destinations.append(Destination("Opera House", "Australia"))
        self.destinations.append(Destination("Uluru", "Australia"))
        self.destinations.append(Destination("Machu Picchu", "Peru"))
        self.destinations.append(Destination("Great Pyramids", "Egypt"))
        self.destinations.append(Destination("Niagara Falls", "Canada"))

        for d in self.destinations:
            Utils.add_flights_for_destination(d, self.agency)
