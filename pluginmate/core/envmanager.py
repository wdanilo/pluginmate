class EnvManager:
    def __init__(self, envroot):
        self.root = envroot
        self.__envs = []

    def push(self, name):
        env = self.current().child(name)
        self.__envs.append(env)
        return env

    def pop(self):
        env = self.__envs.pop()

    def current(self):
        if self.__envs:
            env = self.__envs[-1]
        else:
            env = self.root
        return env

    def __call__(self, name=None):
        env = self.current()
        if name:
            env = env.child(name)
        return env

