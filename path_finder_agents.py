from definitions import Agent
import numpy as np
import heapq
import math

class RandAgent(Agent):
    """
    This class implements an agent that explores the environmente randomly
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        path = self.frontier.pop(0)
        
        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path} 
        # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
        self.percepts = self.env.signal(action)

        # Add visited node 
        self.visited.append(path[-1])

        # From the list of viable neighbors given by the environment
        # Select a random neighbor that has not been visited yet
        
        viable_neighbors =  self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors: 
            # Select random neighbor
            visit = viable_neighbors[np.random.randint(0,len(viable_neighbors))]
            
            # Append neighbor to the path and add it to the frontier
            self.frontier = [path + [visit]] + self.frontier

    def run(self):
        """Keeps the agent acting until it finds the target
        """

        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])


class DFSAgent(Agent):
    """
    This class implements an agent that explores the environmente doing an depth-first search
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier (last added)
        path = self.frontier.pop(0)
        
        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path} 
        # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
        self.percepts = self.env.signal(action)

        # Add visited node 
        self.visited.append(path[-1])

        # From the list of viable neighbors given by the environment
        # Select a neighbor that has not been visited yet
        
        viable_neighbors =  self.percepts['neighbors']
        visit = []

        for i in viable_neighbors:
            # If it is not on the list of visited nodes
            if not any(np.equal(self.visited,i).all(1)):
                visit = i.tolist()
                break

        # If the agent is not stuck
        if visit:
            # Append neighbor to the path and add it to the frontier
            self.frontier = [path + [visit]] + self.frontier
        else:
            # Remove the node from the path and add it to the frontier
            # if it is not empty
            path.pop()
            if path:
                self.frontier = [path] + self.frontier


    def run(self):
        """Keeps the agent acting until it finds the target
        """

        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])

class BFSAgent(Agent):
    """
    This class implements an agent that explores the environmente doing an depth-first search
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        path = self.frontier.pop()

        # Visit the last node in the path if it is not on the list of visited nodes
        if not self.visited or not any(np.equal(self.visited,path[-1]).all(1)):
            action = {'visit_position': path[-1], 'path': path} 
            # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
            self.percepts = self.env.signal(action)

            # Add visited node 
            self.visited.append(path[-1])

            # From the list of viable neighbors given by the environment
            # Select a neighbor that has not been visited yet
            
            viable_neighbors =  self.percepts['neighbors']

            if viable_neighbors:
                for i in viable_neighbors:
                    # If it is not on the list of visited nodes
                    if not any(np.equal(self.visited,i).all(1)):
                        self.frontier = [path + [i]] + self.frontier

    def run(self):
        """Keeps the agent acting until it finds the target
        """

        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])


def calc_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class AStarAgent(Agent):
    """
    This class implements an agent that explores the environmente doing an depth-first search
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = []
        heapq.heappush(self.frontier, (0, [self.percepts['current_position']], 0)) #(f(p), path, cost(p))
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        _, path, path_cost = heapq.heappop(self.frontier)
 
        # Visit the last node in the path if it is not on the list of visited nodes
        if not self.visited or not any(np.equal(self.visited,path[-1]).all(1)):
            action = {'visit_position': path[-1], 'path': path} 
            # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
            self.percepts = self.env.signal(action)

            # Add visited node 
            self.visited.append(path[-1])

            # From the list of viable neighbors given by the environment
            # Select a neighbor that has not been visited yet
            
            viable_neighbors =  self.percepts['neighbors']

            if viable_neighbors:
                for i in viable_neighbors:
                    # If it is not on the list of visited nodes
                    if not any(np.equal(self.visited,i).all(1)):
                        # Calc the cost of path from start to the new node (cost(p))
                        new_path_cost = path_cost + calc_dist(path[-1], i)
                        # Calc the estimated total cost of the path (f(p) = cost(p) + h(p))
                        f = new_path_cost + calc_dist(i, self.percepts['target'])
                        # Add it to the frontier
                        heapq.heappush(self.frontier, (f, path + [i.tolist()], new_path_cost))

    def run(self):
        """Keeps the agent acting until it finds the target
        """

        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])

class GreedyAgent(Agent):
    """
    This class implements an agent that explores the environmente doing an depth-first search
    until it reaches the target
    """

    def __init__(self, env):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = []
        heapq.heappush(self.frontier, (0, [self.percepts['current_position']])) #(h(p), path)
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        _, path = heapq.heappop(self.frontier)
 
        # Visit the last node in the path if it is not on the list of visited nodes
        if not self.visited or not any(np.equal(self.visited,path[-1]).all(1)):
            action = {'visit_position': path[-1], 'path': path} 
            # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
            self.percepts = self.env.signal(action)

            # Add visited node 
            self.visited.append(path[-1])

            # From the list of viable neighbors given by the environment
            # Select a neighbor that has not been visited yet
            
            viable_neighbors =  self.percepts['neighbors']

            if viable_neighbors:
                for i in viable_neighbors:
                    # If it is not on the list of visited nodes
                    if not any(np.equal(self.visited,i).all(1)):
                        # Calc the estimated cost to the target (h(p))
                        h = calc_dist(i, self.percepts['target'])
                        # Add it to the frontier
                        heapq.heappush(self.frontier, (h, path + [i.tolist()]))

    def run(self):
        """Keeps the agent acting until it finds the target
        """

        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])