import inspect
from decorator import decorator
from collections import defaultdict
from .core.errors import MultiNotImplementedError
from .core.interface import Interface
from .core.plugin import Plugin
from .core.environment import Environment
from .core.envmanager import EnvManager

from abc import ABCMeta
from abc import abstractmethod as abstract


import logging
logger = logging.getLogger(__name__)

__environments = {}
env = EnvManager(Environment('global'))

def interfaces(obj):
    env = environment(obj)
    return env.interfaces(obj)

def environment(obj):
    return __environments[obj]

def implements(*interfaces, **kwargs):
    strict = kwargs.get('strict', True)
    def decorator(cls):
        # check if all interface methods are implemented
        if strict:
            not_implemented = defaultdict(list)
            for interface in interfaces:
                interface_name = interface.__name__
                for name, func in inspect.getmembers(interface, predicate=inspect.isfunction):
                    impl_func = getattr(cls, name, None)
                    if impl_func is None or not inspect.isfunction(impl_func):
                        not_implemented[interface_name].append(name)
            if not_implemented:
                raise MultiNotImplementedError(cls, not_implemented)

        # create new class inheriting interface
        bases = (cls,)+interfaces
        if not issubclass(cls, Plugin):
            bases = (Plugin,)+bases
        newcls = type(cls.__name__, bases, {})
        register_plugin(newcls)
        return newcls
    return decorator

def check_interface(cls, interface):
    functions         = inspect.getmembers(interface, predicate=inspect.isfunction) #(name, func)
    methoddescriptors = inspect.getmembers(interface, predicate=inspect.ismethoddescriptor)
    not_implemented = set()
    print (methoddescriptors)


def enable(service):
    env = environment(service)
    env.enable(service)

def disable(service):
    env = environment(service)
    env.disable(service)

__g_abstract = abstract
def interface(cls=None, abstract=True):
    def decorator(cls):
        # substitute all methods with abstract ones
        if abstract:
            for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
                setattr(cls, name, __g_abstract(func))
        newcls = ABCMeta(cls.__name__, (Interface, cls), dict(cls.__dict__))
        return newcls
    if cls is not None:
        return decorator(cls)
    else:
        return decorator


def register_service(service):
    nenv = env()
    nenv.register_service(service)
    __environments[service] = nenv

def register_plugin(plugin):
    nenv = env()
    nenv.register_plugin(plugin)
    __environments[plugin] = nenv

def services(interface):
    return env.root.services(interface)

