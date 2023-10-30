class Destination:
    def __init__(self, name, country):
        self.name = name
        self.country = country

    def listify(self):
        return [self.name, self.country]

    def __str__(self):
        return f"{self.name} in {self.country}"

    def to_string(self):
        return self.__str__()
