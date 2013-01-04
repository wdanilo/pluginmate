import pluginmate
from utils.collections import AssociationMap
from .interface import Interface

import logging
logger = logging.getLogger(__name__)

class Environment:
    def __init__(self, name, *bases):
        self.name = name
        self.__bases = bases
        self.children           = {}
        self.__interfaces       = AssociationMap()
        self.__plugins          = AssociationMap()
        self.__services         = AssociationMap()
        self.__enabled_services = set()

    def child(self, name):
        if not name in self.children:
            self.children[name] = Environment(name, self)
        return self.children[name]

    def interfaces(self, obj):
        return self.__interfaces.values(obj)

    def register_plugin (self, plugin):
        name = plugin.__name__
        interfaces = []
        for base in plugin.mro():
            if Interface in base.__bases__:
                interfaces.append(base)
                self.__interfaces.bind(plugin, base)
                self.__plugins.bind(base, plugin)
        logger.debug("Registering plugin '%s' with interfaces %s in environment '%s'"
                     % (name, ', '.join(["'%s'" % interface.__name__ for interface in interfaces]), self.name))

    def register_service(self, service):
        name = service.__class__.__name__
        logger.debug("Registering %s in %s" % (repr(service), repr(self)))
        plugin = service.__class__
        self.__plugins.bind(service, plugin)
        self.__services.bind(plugin, service)
        interfaces = pluginmate.interfaces(plugin)
        if not interfaces:
            logger.error("No matching interface was found for %s" % repr(service))
            raise Exception()
        for interface in interfaces:
            self.__interfaces.bind(service, interface)
            self.__services.bind(interface, service)
        self.enable(service)

    def services(self, interface=None, inherit=True, all=False):
        services = set()
        services |= self.__services.values(interface)
        services &= self.__enabled_services
        if inherit and self.__bases:
            for parent in self.__bases:
                services.update(parent.services(interface, inherit=inherit, all=all))
        return services

    def plugins(self, interface=None, inherit=True):
        plugins = set()
        plugins |= self.__plugins.values(interface)
        if inherit and self.__bases:
            for parent in self.__bases:
                plugins.update(parent.plugins(interface, inherit=inherit))
        return plugins

    def enable(self, service):
        self.__enabled_services.add(service)

    def disable(self, service):
        self.__enabled_services.remove(service)

    def __str__(self):
        return "environment '%s'"%self.name

    def __repr__(self):
        return str(self)