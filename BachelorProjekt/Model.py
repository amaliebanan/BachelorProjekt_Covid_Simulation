import AgentClass as ac
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
import random
from enum import Enum
import matplotlib.pyplot as plt
from mesa import Agent, Model
import numpy as np
from mesa.datacollection import DataCollector
import matplotlib

init_positive_agents = 2

def find_status(model):
    agents_status = [agent.infected for agent in model.schedule.agents]
    return sum(agents_status)

def setUp(N,model,setUpType):
    'random set-up'
    if setUpType == 1:
        for i in range(1,N):
            newAgent = ac.covid_Agent(i, model)
            model.schedule.add(newAgent) #Add agent to scheduler
            x, y = model.grid.find_empty()#Place agent randomly in empty cell on grid
            model.grid.place_agent(newAgent, (x,y))
    elif setUpType == 2:
        listOfPositions = [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(1,2),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),
                                          (1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(1,7),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8)]
        for i in range(N):
            newAgent = ac.covid_Agent(i, model)
            model.schedule.add(newAgent) #Add agent to scheduler
            x,y = listOfPositions.pop()
            model.grid.place_agent(newAgent,(x,y))
        instruktor_agent = ac.covid_Agent(1000,model)
        model.schedule.add(instruktor_agent)
        x,y = random.choice([(7,5),(7,4)])
        model.grid.place_agent(instruktor_agent,(x,y))

class SetUpType():
    random = 1
    horseshoe = 2
    rows = 3
    groups = 4


class covid_Model(Model):
    def __init__(self, N, height, width,setUpType):
        self.n_agents = N
        self.grid = MultiGrid(width, height, torus=False) #torus wraps edges
        self.schedule = SimultaneousActivation(self)
        self.setUpType = setUpType
        self.status = find_status(self)
        self.datacollector = DataCollector(model_reporters={"infected":lambda m:m.status})
        #The scheduler is a special model component which controls the order in which agents are activated


        ' Tilføj person-agenter '
        setUp(self.n_agents+1,self,setUpType)


        'Tilføj positive person-agenter'
        for i in range(init_positive_agents):
            randomAgents = self.random.choice(self.schedule.agents)
            self.schedule.remove(randomAgents)
            postive_agent = randomAgents
            postive_agent.infected = 1
            self.schedule.add(postive_agent)



        self.running = True

    def step(self):
        self.recovered = 0
        self.datacollector.collect(self)
        self.schedule.step()

        if find_status(self) == 0:
           self.running = False
