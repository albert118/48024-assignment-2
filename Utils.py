import random
from Agency import Agency
from Destination import Destination
from Flight import Flight


class Utils:
    @staticmethod
    def add_flights_for_destination(destination: Destination, agency: Agency):
        country = destination.country
        airlines = ["American Airlines", "QANTAS", "JetStar", "Tiger Airways", "United Airlines",
                    "Egypt Air", "Etihad", "Singapore Airlines", "British Air", "Cathay Dragon"]
        flight_min = 11
        flight_max = 999

        cost_min = 49.99
        cost_max = 999.99

        countries = []
        # a few variables here refer to agency.attribute and directly expected the underlying collection
        # this differs from assignment 1, and what I'm reading the skeleton code-style as
        # this could absolutely be simplified. However, I'm attempting to keep with the existing style by fixing this area
        # instead of re-writing the whole project
        for d in agency.destinations.destinations:
            countries.append(d.country)

        for s in countries:
            try:
                agency.flights.add_flight(Flight(airlines[random.randint(0, (len(airlines) - 1))], random.randint(
                    flight_min, flight_max), country, s, random.uniform(cost_min, cost_max)))
                agency.flights.add_flight(Flight(airlines[random.randint(0, (len(airlines) - 1))], random.randint(
                    flight_min, flight_max), s, country, random.uniform(cost_min, cost_max)))
            except:
                continue
