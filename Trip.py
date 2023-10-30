from Agency import Agency
from Flights import Flights
from Destinations import Destinations

DEBUG = True # for mocking data while testing

class Trip:
    def __init__(self, agency: Agency):
        self.agency = agency
        self.flights = Flights(self)
        self.destinations = Destinations(self)

        if DEBUG:
            from Destination import Destination
            self.destinations.destinations.append(Destination("Eiffel Tower", "France"))
            self.destinations.destinations.append(Destination("Uluru", "Australia"))
            self.destinations.destinations.append(Destination("Machu Picchu", "Peru"))
            self.destinations.destinations.append(Destination("Great Pyramids", "Egypt"))
            self.destinations.destinations.append(Destination("Niagara Falls", "Canada"))
            # auto-connect when testing
            self.add_connecting_flights()

    def add_connecting_flights(self):
        if len(self.destinations.destinations) <= 1:
            raise Exception('cannot add connecting flights (no destinations exist)')

        self.flights.flights.clear()
        current_destination = None
        next_destination = None

        for i in range(len(self.destinations.destinations)):
            if i == (len(self.destinations.destinations) - 1):
                return

            current_destination = self.destinations.destinations[i]
            next_destination = self.destinations.destinations[i + 1]

            if current_destination == next_destination or current_destination.country == next_destination.country:
                raise Exception('cannot add connecting flights (invalid destinations)')

            for f in self.agency.flights.flights:
                if f.takeoff == current_destination.country and f.landing == next_destination.country:
                    try:
                        self.flights.add_flight(f)
                    except Exception as ex:
                        raise Exception('error adding flight: ' + str(ex))
                    break

    def get_itinery(self):
        objects = []
        for i in range(len(self.destinations.destinations)):
            objects.append(self.destinations.destinations[i])
            if i < len(self.flights.flights):
                objects.append(self.flights.flights[i])
        return objects
