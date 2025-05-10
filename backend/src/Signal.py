class Signal:
    def __init__(self, name, mode, param):
        self.name = name
        self.mode = mode
        self.param = param

    def __str__(self):
        return str(self.__dict__)
