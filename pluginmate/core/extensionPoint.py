import pluginmate

class ExtensionPoint:
    def __init__(self, interface):
        self.__interface = interface
        self.__env = pluginmate.env()

    def __iter__(self):
        return self.services().__iter__()

    def __call__(self, key=None, all=False):
        pass

    def service(self, key=None, all=False):
        pass

    def __len__(self):
        return 0

    def services(self):
        return self.__env.services(self.__interface)

    def plugins(self):
        return self.__env.plugins(self.__interface)

    def __repr__(self):
        return 'TODO'
