import pytest
import sys
import os

import logging

dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(dir, os.path.pardir))
sys.path.append(os.path.join(parent_dir, 'libs'))
sys.path.append(parent_dir)

from pluginmate import implements, interface, abstract

print(sys.modules['pluginmate'])

@pytest.fixture(scope="module")
def IAbstract():
    @interface
    class Interface:
        def f    (self):       pass
        def f_x  (self, x):    pass
        def f_xy (self, x, y): pass
    return Interface

@pytest.fixture(scope="module")
def INotAbstract():
    @interface(abstract=False)
    class Interface:
        def f    (self):       pass
        def f_x  (self, x):    pass
        def f_xy (self, x, y): pass
    return Interface

# interface initialization test
def test_initialize():
    @interface
    class Interface:
        pass
    with pytest.raises(TypeError):
        Interface()

def test_abstract(IAbstract, INotAbstract):
    with pytest.raises(NotImplementedError):
        @implements(IAbstract)
        class X:
            pass

    @implements(INotAbstract)
    class X:
        pass

def test_abstract_explicite():
    @interface(abstract=False)
    class Interface:
        @abstract
        def f(self):pass

    with pytest.raises(NotImplementedError):
        @implements(Interface)
        class X:
            pass

def test_strict(IAbstract):
    @implements(IAbstract, strict=False)
    class A:
        pass

def test_implementance(INotAbstract):
    @implements(INotAbstract)
    class A:
        pass
    a = A()
    assert a.f() == None

def test_signature(INotAbstract):
    @implements(INotAbstract)
    class X:
        pass
    x = X()
    with pytest.raises(TypeError):
        x.f_x()
