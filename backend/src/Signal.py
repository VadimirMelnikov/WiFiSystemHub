class Signal:
    def __init__(self, name, param, time_stamp):
        self.name = name
        self.param = param
        self.time_stamp = time_stamp

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Signal) and all(getattr(self, attr) == getattr(other, attr) for attr in vars(self))

    def __hash__(self):
        return hash(attr for attr in vars(self))