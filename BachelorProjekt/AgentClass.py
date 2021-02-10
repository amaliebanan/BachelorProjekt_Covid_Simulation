from mesa import Agent, Model
import numpy as np


class covid_Agent(Agent):
    def __init__(self,id, model):
        super().__init__(id, model)
        self.infected = False
        self.id = id

    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):
        #to be implemented
        #whatever the agent does when activated
        print("Hi, my ID is",str(self.id))


