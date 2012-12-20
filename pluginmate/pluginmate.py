import logging

from utils.moduleUtils import override_module
logger = logging.getLogger(__name__)

@override_module('pluginmate')
class PluginMate:
    def __init__(self):
        from .core.environment import Environment
        from .core.envmanager import EnvManager
        self.__environments = {}
        self.env = EnvManager(Environment('global'))

    def interfaces_of(self, obj):
        env = self.environment_of(obj)
        return env.interfaces_of(obj)

    def environment_of(self, obj):
        return self.__environments[obj]

    def implements(self, *interfaces):
        def decorator(cls):
            bases = (cls,)+interfaces
            if not issubclass(cls, Plugin):
                bases = (Plugin,)+bases
            newcls = type(cls.__name__, bases, {})
            self.register_plugin(newcls)
            return newcls
        return decorator

    def interface(self, cls):
        newcls = type(cls.__name__, (Interface, cls), {})
        def init(self):
            if self.__class__ == newcls:
                raise TypeError('Interface cannot be initialized')
        newcls.__init__ = init
        return newcls

    def register_service(self, service, env=None):
        env = self.env()
        env.register_service(service)
        self.__environments[service] = env

    def register_plugin(self, plugin):
        env = self.env()
        env.register_plugin(plugin)
        self.__environments[plugin] = env

    def service_env(self, service):
        return self.__environments[service]

    def services(self, interface):
        return self.env.root.services(interface)


from .core.interface import Interface
from .core.plugin import Plugin
