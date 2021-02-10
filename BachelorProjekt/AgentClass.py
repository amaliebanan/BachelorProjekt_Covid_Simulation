from mesa import Agent, Model
import numpy as np


class covid_Agent(Agent):
    def __init__(self,id,infected,model):
        super().__init__(self,id,model)
        self.infected = infected

    def step(self):
        #to be implemented
        #whatever the agent does when activated
        print("what to do?")

agent1 = covid_Agent(0,False)
agent2 = covid_Agent(1,True)

agent1.infected = not agent1.infected


