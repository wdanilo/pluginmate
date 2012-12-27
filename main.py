from logging import Formatter
import logging

verboseLevel = logging.DEBUG

formatter = Formatter('[%(levelname)s] %(message)s','%Y:%m:%d:%H:%M:%S')

logger        = logging.root
streamHandler = logging.StreamHandler()

logger.setLevel(verboseLevel)
streamHandler.setFormatter(formatter)
streamHandler.setLevel(verboseLevel)
logger.addHandler(streamHandler)

from utils.printTracer import PrintTracer
PrintTracer.enable()

# -------------------

import pluginmate
from pluginmate import implements, interface, abstract
from pluginmate.core.extensionPoint import ExtensionPoint


pluginmate.env.push('myenv')


@interface
class ITest:
    def f(self): pass
    def g(self, x): pass

@implements(ITest)
class B:
    def f(self):
        print("B f")


b = B()

from inspect import getargspec
print(getargspec(b.g))
'''
print('--------------')
e = ExtensionPoint(ITest)
print(e.plugins())
'''

pluginmate.env.push('myenv2')

print('--------------')
e = ExtensionPoint(ITest)
print(e.plugins())

pluginmate.env.pop()

pluginmate.env.pop()




'''
@interface
class ITest2:
    def f(self): raise NotImplementedError
    def g(self, x): raise NotImplementedError

@implements(ITest, ITest2)
class B:
    def f(self):
        print("B f")


B()
e = ExtensionPoint(ITest2)

print(e.services())


# jak rozwiazac takie cos ze potrzebujemy instancji pluginy kotry nie jest singletonem on demand


#'''




