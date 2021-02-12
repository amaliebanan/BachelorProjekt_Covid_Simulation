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
        for i in range(0,7):
            randomAgents = self.random.choice(self.schedule.agents)
            self.schedule.remove(randomAgents)
            postive_agent = randomAgents
            postive_agent.infected = 1
            self.schedule.add(postive_agent)

    def step(self):
        self.schedule.step()



all_agents = []
tidskridt = []
#for i in range(1):


myModel = covid_Model(100)
for j in range(40):
    counter = 0
    myModel.step()
    for agent in myModel.schedule.agents:
        status = agent.infected
        if status == 1:
            counter += 1
    tidskridt.append(counter)

agents_status = [agent.infected for agent in myModel.schedule.agents]
print(tidskridt)

#plt.hist(all_agents)
#plt.show()
