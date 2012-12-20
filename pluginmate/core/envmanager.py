class EnvManager:
    def __init__(self, envroot):
        self.root = envroot
        self.__envs = ListDict()

    def push(self, name):
        env = self.current().child(name)
        self.__envs.push(env.name, env)
        return env

    def pop(self):
        env = self.__envs.pop()

    def current(self):
        if self.__envs:
            env = self.__envs.val[-1]
        else:
            env = self.root
        return env

    def __call__(self, name=None):
        if name is None:
            return self.current()
        return self.__envs[name]


from utils.collections import ListDict