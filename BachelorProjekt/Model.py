import AgentClass as ac
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
from mesa import Agent, Model

class covid_Model(Model):
    def __init__(self,N):
        self.n_agents = N
        self.schedule = RandomActivation(self)

        #The scheduler is a special model component which controls the order in which agents are activated
        for i in range(1,self.n_agents+1):
            newAgent = ac.covid_Agent(i,self)
            #Add agent to scheduler
            self.schedule.add(newAgent)

        #Tilføj en positiv agenter (fjern fra oprindelig liste af agenter, for at ændre infected-status)
        randomAgent = self.random.choice(self.schedule.agents)
        self.schedule.remove(randomAgent)

        postive_agent = randomAgent
        postive_agent.infected = 1
        self.schedule.add(postive_agent)

    def step(self):
        self.schedule.step()

myModel = covid_Model(10)
myModel.step()
