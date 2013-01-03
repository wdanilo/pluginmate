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
def interface1():
    @interface
    class I_1:
        def f(self): pass
        def g(self, x): pass
    return I_1

class TestInterface:
    def test_simple(self):
        @interface
        class Interface:
            pass
        with pytest.raises(TypeError):
            Interface()


