'''import pluginmate
from .errors import PluginError

class InterfaceMeta(type):
    def __new__(cls, name, bases, d):
        new_class = type.__new__(cls, name, bases, d)
        if bases:
            pluginmate.env().register_interface(new_class)
        return new_class


class Interface(metaclass=InterfaceMeta):
    """
    Marker base class for extension point interfaces.  This class
    is not intended to be instantiated.  Instead, the declaration
    of subclasses of Interface are recorded, and these
    classes are used to define extension points.
    """


'''


class Interface:
    pass