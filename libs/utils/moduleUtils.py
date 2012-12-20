from types import ModuleType
import inspect
import sys

def override_module(name, *module_args, **module_kwargs):
    def decorator(cls):
        class MetaModule(ModuleType):
            def __init__(self):
                super().__init__(name)
            def __new__(cls, *args, **kwargs):
                new_module = super().__new__(cls, *args, **kwargs)
                new_module.__name__ = name
                if not name in sys.modules:
                    raise ImportError
                module = sys.modules[name]
                new_module.__path__ = module.__path__
                new_module.__file__ = inspect.getfile(cls)
                sys.modules[name] = new_module
                return new_module
        newcls = type(cls.__name__, (cls,MetaModule,), {})
        newcls(*module_args, **module_kwargs)
        return newcls
    return decorator