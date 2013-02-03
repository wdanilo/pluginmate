"""
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

class option:
    def __set__(self, instance, value):
        print(instance, value)

    def __get__(self, instance, owner):
        print('!!!')

@interface(abstract=False)
class ITest:
    def f(self): pass
    def g(self, x): pass

@implements(ITest)
class B:
    def __init__(self):
        print ('>>>')
        self.x = option()
        print ('<<<')

    def f(self):
        print("B f")



pluginmate.env.push('myenv2')

b = B()
print(b.x)
b.disable()
print('--------------')

e = ExtensionPoint(ITest)


pluginmate.env.pop()

print(e.services())

pluginmate.env.pop()

print (pluginmate.env('myenv'))


#'''
"""

from pluginmate import implements, interface, abstract, ExtensionPoint, Attribute
import pluginmate

from collections import defaultdict
import sys
import inspect


def test(func):
    return test

@interface
class IPerson:
    name  = Attribute('Person name')
    email = Attribute('Person email address')
    phone = Attribute('Person phone number')

    def f(self, x, y=1, *args, **kwargs):
        pass


#print(inspect.getargspec(IPerson.f))
#print(inspect.getargspec(IPerson.g))


@implements(IPerson)
class Person:
    def f(self):
        pass



pluginmate.check_interface(Person, IPerson)

'''
@interface
class IOptionManager:
    pass

@implements(IOptionManager)
class OptionMager:
    def __init__(self):
        self.__values = defaultdict(dict)
        pass

    def get(self, section, name, default):
        data = self.__values[section]
        if not name in data:
            data[name] = default
        return data[name]

    def set(self, section, name, value):
        data = self.__values[section]
        data[name] = value


a = OptionMager()

e = ExtensionPoint(IOptionManager)
print(e.service())


class VirtualOption(object):
    def __init__(self, name, section=None, default=None, static=False):
        self.name = name
        self.static = static
        self.section = section
        self.default = default
        self.data = ExtensionPoint(IOptionManager)
    def __get__(self, instance, owner):
        return self.data.service().get(section=self.section, name=self.name, default=self.default)
        #return getattr(instance,self.name)

    def __set__(self, instance, value):
        return self.data.service().set(section=self.section, name=self.name, value=value)
        #return setattr(instance, self.name, value)

def option(section=None, **kwargs):
    frame   = inspect.stack()[1][0]
    locals_ = frame.f_locals
    if locals_ == frame.f_globals:
        raise SyntaxError('option() can only be used in a class definition')

    if '__module__' in locals_:
        # Class decorator.  Initialize the VirtualOption, and then
        # create a locally-available Option instance.
        for x in inspect.stack():
            print(x)
        print(inspect.stack()[1][0].f_locals)
        for name, value in kwargs.items():
            locals_[name] = VirtualOption(name, section=section, default=value, static=True)

    else:
        # Class constructor.  If a VirtualOption does not exist in this
        # class, create it.  Create an Option instance in this instance.
        for name, value in kwargs.items():
            if not name in locals_["self"].__class__.__dict__:
                setattr(locals_["self"].__class__, name, VirtualOption(name, section=section, default=value, static=False))
            #setattr(locals_["self"], '_'+name,value)

    #print('__module__' in frame.f_locals)

######################################



class SillyWalksMetaClass(type):
    def __init__(self, class_name, bases, namespace):
            print("!!!", class_name)

class X:
    def __init__(self):
        option(y=0, section='x')
        pass

        #print(self.x, self.y, self.z)



x1 = X()
x2 = X()
#x1.x = 5
#x2.x = 6

x1.y = 5
x2.y = 6
#print(x1.x)
#print(x2.x)

print(x1.y)
print(x2.y)

print ('----')

#'''