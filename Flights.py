from Agency import Agency
from Flight import Flight


class Flights:
    def __init__(self, agency: Agency):
        self.agency = agency
        self.flights = []

    def add_flight(self, flight: Flight):
        if self.has_flight(flight.takeoff, flight.landing):
            raise Exception('cannot add flight (flight already exists)')
        self.flights.append(flight)

    def remove_flight(self, flight: Flight):
        if self.has_flight(flight.takeoff, flight.landing) == False:
            raise Exception('cannot remove flight (flight does not exist)')
        self.flights.append(flight)

    def has_flight(self, takeoff, landing):
        for f in self.flights:
            if f.takeoff == takeoff and f.landing == landing:
                return True
        return False

    def get_flight(self, takeoff, landing):
        for f in self.flights:
            if f.takeoff == takeoff and f.landing == landing:
                return f
        return None

    def get_filtered_flights(self, country):
        filtered = []
        for f in self.flights:
            if f.landing.lower().contains(country.lower()) or f.takeoff.lower().contains(country.lower()):
                filtered.append(f)
        return filtered

    def get_total_cost(self):
        cost = 0.0
        for f in self.flights:
            cost = cost + f.cost
        return cost
