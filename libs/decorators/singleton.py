class singleton:
    def __init__(self, decorated):
        self.__decorated = decorated
        self.__instance = decorated()

    def __call__(self):
        return self.__instance

    def __instancecheck__(self, inst):
        return isinstance(inst, self.__decorated)