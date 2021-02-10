
import numpy as np


class Agent:
    def __init__(self,infected):
        self.infected = infected

    def step(self):
        #to be implemented
        #whatever the agent does when activated
        print("what to do?")

agent1 = Agent(False)
agent2 = Agent(True)

agent1.infected = not agent1.infected
