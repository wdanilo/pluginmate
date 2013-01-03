class PluginError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class MultiNotImplementedError(NotImplementedError):
    def __init__(self, cls=None, interfaces=None):
        self.cls = cls
        self.interfaces = interfaces

    def __str__(self):
        out = "\nClass %s does not implement all abstract methods:" % self.cls.__name__
        for interface, methods in self.interfaces.items():
            out += '\ninterface %s:\n\t' % interface + '\n\t'.join(methods)
        return out



