from Agency import Agency
from Flights import Flights
from Destinations import Destinations


class Trip:
    def __init__(self, agency: Agency):
        self.agency = agency
        self.flights = Flights(self)
        self.destinations = Destinations(self)

    def add_connecting_flights(self):
        if len(self.destinations) <= 1:
            raise Exception('cannot add connecting flights (no destinations exist)')

        self.flights.clear()
        current_destination = None
        next_destination = None

        for i in range(len(self.destinations)):
            if i == (len(self.destinations) - 1):
                return

            current_destination = self.destinations[i]
            next_destination = self.destinations[i + 1]

            if current_destination == next_destination or current_destination.country == next_destination.country:
                raise Exception('cannot add connecting flights (invalid destinations)')

            for f in self.agency.flights:
                if f.takeoff == current_destination.country and f.landing == next_destination.country:
                    try:
                        self.flights.add_flight(f)
                    except Exception as ex:
                        raise Exception('error adding flight: ' + str(ex))
                    break

    def get_itinery(self):
        objects = []
        for i in range(len(self.destinations)):
            objects.append(self.destinations[i])
            if i < len(self.flights):
                objects.append(self.flights[i])
        return objects
