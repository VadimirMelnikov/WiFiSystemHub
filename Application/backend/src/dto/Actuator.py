class Actuator:
    def __init__(self, name, sensor_name):
        self.name = name
        self.sensor_name = sensor_name

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Actuator) and all(getattr(self, attr) == getattr(other, attr) for attr in vars(self))

    def __hash__(self):
        return hash(attr for attr in vars(self))