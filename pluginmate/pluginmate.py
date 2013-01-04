import inspect
from decorator import decorator
from collections import defaultdict
from .core.errors import MultiNotImplementedError
from .core.interface import Interface
from .core.plugin import Plugin
from .core.environment import Environment
from .core.envmanager import EnvManager


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
                    abstract = getattr(func, '__abstract__', None)
                    if not abstract: continue
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


def __abstract(func, *args, **kwargs):
    raise NotImplementedError

def abstract(func):
    func.__abstract__ = True
    return decorator(__abstract, func)


__g_abstract = abstract # not to collide with argument name
def interface(cls=None, abstract=True):
    def decorator(cls):
        newcls = type(cls.__name__, (Interface, cls), {})
        def init(self):
            if self.__class__ == newcls:
                raise TypeError('Interface cannot be initialized')
        newcls.__init__ = init

        # substitute all methods with abstract ones
        if abstract:
            for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
                if name[0] == '_': continue
                setattr(cls, name, __g_abstract(func))
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

