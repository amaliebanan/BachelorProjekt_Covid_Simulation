import AgentClass as ac
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
from mesa import Agent, Model
import numpy as np
from mesa.datacollection import DataCollector
import matplotlib

def find_status(model):
    agents_status = [agent.infected for agent in model.schedule.agents]
    return agents_status

class covid_Model(Model):
    def __init__(self, N, height, width):
        self.n_agents = N
        self.grid = MultiGrid(width, height, torus=False) #torus wraps edges
        self.schedule = SimultaneousActivation(self)
        #The scheduler is a special model component which controls the order in which agents are activated


        'Tilføj table-agents'
        for i in range(1,13,2):
            newTableA = ac.Table(i,self)
            newTableB = ac.Table(i+1,self)
       #     table = (newTableA,newTableB)
        #    self.schedule.add(table)
         #   x,y = self.grid.find_empty()
          #  self.grid.place_agent(table,(x,y))


        ' Tilføj person-agenter '
        for i in range(1, self.n_agents+1): #adds agents
            newAgent = ac.covid_Agent(i, self)
            self.schedule.add(newAgent) #Add agent to scheduler
            x, y = self.grid.find_empty()#Place agent randomly in empty cell on grid
            self.grid.place_agent(newAgent, (x,y))

        'Tilføj positive person-agenter'
        for i in range(0,2):
            randomAgents = self.random.choice(self.schedule.agents)
            self.schedule.remove(randomAgents)
            postive_agent = randomAgents
            postive_agent.infected = 1
            self.schedule.add(postive_agent)







        self.running = True

    def step(self):
        self.recovered = 0
        #self.datacollector.collect(self)
        self.schedule.step()

        agents_status = sum([agent.infected for agent in self.schedule.agents])
        if agents_status == 0:
           self.running = False


all_agents = []
timesteps = []

# Create our model with N=agents, width and height on grid
myModel = covid_Model(30,10,10)
#How many timesteps?
for j in range(50):
    counter = 0
    myModel.step()
    for agent in myModel.schedule.agents:
        status = agent.infected
        if status == 1:
            counter += 1
    timesteps.append(counter)
print(timesteps)
agents_status = [agent.infected for agent in myModel.schedule.agents]
#print(timesteps)

