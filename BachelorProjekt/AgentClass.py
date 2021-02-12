from mesa import Agent, Model
import random
import numpy as np


class covid_Agent(Agent):
    def __init__(self,id, model):
        super().__init__(id, model)
        self.infected = 0 #0 for False, 1 for True
        self.pos = 0
        self.infection_period = 9
        self.id = id

    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):
        #whatever the agent does when activated
        #print("ID",self.id, "Status:", self.infected)
        #Infect another agent random
        if self.infected == 0:
            return


        #Generate random int and infect a new agent if int = 1. If other_agent is already infected, find a new one
        randomInt = np.random.poisson(1/8)
        if randomInt == 1:
            other_agent = self.random.choice(self.model.schedule.agents)
            while other_agent.infected == 1:
                other_agent = self.random.choice(self.model.schedule.agents)
            other_agent.infected = 1

        #Subtract 1 from infection period. Reset infection period if == 0 and make agent not infected anymore
        # (not yet immun)
        self.infection_period -= 1
        if self.infection_period == 0:
            self.infected = 0
            self.infection_period = 9
        else: self.infected = 1



