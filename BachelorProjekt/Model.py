import AgentClass as ac
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
from mesa import Agent, Model
import numpy as np

class covid_Model(Model):
    def __init__(self,N,height, width):
        self.n_agents = N
        self.grid = MultiGrid(width,height,True)
        self.schedule = RandomActivation(self)

        #The scheduler is a special model component which controls the order in which agents are activated
        for i in range(1,self.n_agents+1):
            newAgent = ac.covid_Agent(i,self)
            #Add agent to scheduler
            self.schedule.add(newAgent)

            #Place agent randomly on grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(newAgent, (x, y))

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
timesteps = []

myModel = covid_Model(60,10,10)
for j in range(50):
    counter = 0
    myModel.step()
    for agent in myModel.schedule.agents:
        status = agent.infected
        if status == 1:
            counter += 1
    timesteps.append(counter)

agents_status = [agent.infected for agent in myModel.schedule.agents]
print(timesteps)

#plt.hist(all_agents)
#plt.show()

agents_status = np.zeros((myModel.grid.width, myModel.grid.height))
for cell in myModel.grid.coord_iter():
    cell_content, x, y = cell
    if type(cell_content) == ac.covid_Agent:
        status = cell_content[0].infected
    else: status = 2
    agents_status[x][y] = status

plt.imshow(agents_status)
plt.colorbar()
#plt.show()
