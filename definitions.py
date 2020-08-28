class Environment:
    """
    This class implements an interface for an Environment
    """
    def initial_percepts(self):
        raise NotImplementedError('initial_percepts')
    def signal(self, action):
        raise NotImplementedError('signal')

class Agent:
    """
    This class implements an interface for an agent
    """
    def __init__(self, env):
        self.env = env
    def act(self):
        raise NotImplementedError('act')
