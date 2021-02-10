import AgentClass as ac
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Agent, Model

class covid_Model(Model):
    def __init__(self,N):
        self.n_agents = N
        self.schedule = RandomActivation(self)
        #The scheduler is a special model component which controls the order in which agents are activated
        for i in range(self.n_agents):
            newAgent = ac.covid_Agent(i,self)
            #add agent to scheduler
            self.schedule.add(newAgent)

    def step(self):
        self.schedule.step()

myModel = covid_Model(10)
myModel.step()
