from mesa import Agent, Model
import numpy as np


class covid_Agent(Agent):
    def __init__(self,id, model):
        super().__init__(id, model)
        self.infected = 0 #0 for False, 1 for True
        self.id = id

    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):
        #to be implemented
        #whatever the agent does when activated
        print("Hi, my ID is",self.id,"Do I have covid?:", self.infected)

        #Infect another agent random
        if self.infected == 0:
            return
        other_agent = self.random.choice(self.model.schedule.agents)
        other_agent.infected = 1
        self.infected = 1



