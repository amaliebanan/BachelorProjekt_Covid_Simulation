import AgentClass as ac
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Agent, Model

class covid_Model(Model):
    def __init__(self,N):
        self.n_agents = N
        for i in range(0,N):
            newAgent = ac.Agent(i,False,self)
