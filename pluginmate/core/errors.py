class PluginError(Exception):
    """Exception base class for plugin errors."""

    def __init__(self, value):
        """Constructor, whose argument is the error message"""
        self.value = value

    def __str__(self):
        """Return a string value for this message"""
        return str(self.value)