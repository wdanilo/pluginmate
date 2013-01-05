import pluginmate

class ExtensionPoint:
    def __init__(self, interface):
        self.__interface = interface
        self.__env = pluginmate.env()

    def __iter__(self):
        return self.services().__iter__()

    def __call__(self, key=None, all=False):
        pass

    def service(self, all=False):
        services = list(self.services(all=all))
        servicenum = len(services)
        if servicenum != 1:
            raise LookupError('The ExtensionPoint does not have a unique service. %d services are defined for interface %s.' % (servicenum, self.__interface.__name__))
        return services[0]

    def __len__(self):
        return 0

    def services(self, all=False):
        return self.__env.services(self.__interface, all=all)

    def plugins(self):
        return self.__env.plugins(self.__interface)

    def __repr__(self):
        return 'TODO'
