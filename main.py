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

import os

'''
from pluginmate.loader.importLoader import ImportLoader

loader = ImportLoader()
install_dir = os.path.dirname(__file__)
test_dir = os.path.join(install_dir, 'test')
plug_dir = os.path.join(test_dir, 'plugins')

loader.load([plug_dir])
#'''


import pluginmate
from pluginmate import implements, interface, abstract
from pluginmate.core.extensionPoint import ExtensionPoint


pluginmate.env.push('myenv')

@interface(abstract=False)
class ITest:
    def f(self): pass
    def g(self, x): pass

@implements(ITest)
class B:
    def f(self):
        print("B f")



pluginmate.env.push('myenv2')

b = B()
b.disable()
print('--------------')

e = ExtensionPoint(ITest)


pluginmate.env.pop()

print(e.services())

pluginmate.env.pop()

print (pluginmate.env('myenv'))


#'''