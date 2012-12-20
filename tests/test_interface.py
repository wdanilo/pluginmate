import sys
import os

dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(dir, os.path.pardir))
sys.path.append(os.path.join(parent_dir, 'libs'))
sys.path.append(parent_dir)

import pluginmate

print(sys.modules['pluginmate'])

class TestInterface:
    def test_simple(self):
        assert 1 == 1
