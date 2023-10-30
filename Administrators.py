from Administrator import Administrator


class Administrators:
    def __init__(self):
        self.administrators = []

    def has_administrator(self, username, password):
        for a in self.administrators:
            if a.login == username and a.password == password:
                return True
        raise Exception('cannot find administrator')

    def get_administrator(self, username, password):
        for a in self.administrators:
            if a.login == username and a.password == password:
                return a
        raise Exception('cannot get administrator')

    def insert_dummy_data(self):
        self.administrators.append(Administrator("Davey", "david46", "123"))
        self.administrators.append(Administrator("Angela", "angela123", "mypw"))
        self.administrators.append(Administrator("Rafiqul", "boss", "secure"))
        self.administrators.append(Administrator("Vishesh", "legend", "notsecure"))
        self.administrators.append(Administrator("Zyzz", "1", "1"))
