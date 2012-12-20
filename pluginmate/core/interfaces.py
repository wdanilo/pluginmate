from pluginmate import interface

@interface
class IPluginLoader:
    def load(self, env, path, disable_re, name_re): raise NotImplementedError
