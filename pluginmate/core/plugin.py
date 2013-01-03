import pluginmate

class Plugin(object):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        pluginmate.register_service(obj)
        return obj

    def enable(self):
        pass

    def disable(self):
        pass

    def __repr__(self):
        return "service '%s' (%s)" % (self.__class__.__name__, id(self))