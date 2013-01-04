from pluginmate import implements
from test.interfaces.i1 import ITest

@implements(ITest)
class B:
    def f(self):
        print("B f")