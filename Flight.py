class Flight:
    def __init__(self, airline, flight_no, takeoff, landing, cost):
        self.airline = airline
        self.flight_no = flight_no
        self.takeoff = takeoff
        self.landing = landing
        self.cost = cost

    def get_cost(self):
        # format the cost to avoid large decimal places
        return f'{self.cost:.1f}' if self.cost == 0.0 else f'{self.cost:.2f}'

    def listify(self):
        return [self.airline, self.flight_no, self.takeoff, self.landing, self.get_cost()]

    def __str__(self):
        return f'{self.airline} Flight {self.flight_no} from {self.takeoff} to {self.landing} for {self.get_cost()}'

    def to_string(self):
        return self.__str__()
