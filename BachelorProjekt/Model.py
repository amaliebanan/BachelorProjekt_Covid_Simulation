import AgentClass as ac
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
from mesa import Agent, Model
import numpy as np
import matplotlib

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

            #Place agent randomly in empty cell on grid
            x,y = self.grid.find_empty()
            self.grid.place_agent(newAgent, (x,y))

        #Tilføj en positiv agenter (fjern fra oprindelig liste af agenter, for at ændre infected-status)
        for i in range(0,20):
            randomAgents = self.random.choice(self.schedule.agents)
            self.schedule.remove(randomAgents)
            postive_agent = randomAgents
            postive_agent.infected = 1
            self.schedule.add(postive_agent)

    def step(self):
        self.schedule.step()

all_agents = []
timesteps = []

# Create our model with N=agents, width and height on grid
myModel = covid_Model(200,15,20)
#How many timesteps?
for j in range(50):
    counter = 0
    myModel.step()
    for agent in myModel.schedule.agents:
        status = agent.infected
        if status == 1:
            counter += 1
    timesteps.append(counter)

agents_status = [agent.infected for agent in myModel.schedule.agents]
#print(timesteps)


#Final status , plot picture after last time step
final_status = np.zeros((myModel.grid.width, myModel.grid.height))
for cell in myModel.grid.coord_iter():
    cell_content, x, y = cell
    if len(cell_content)>0:
        status = cell_content[0].infected
    else:
        status = 2
    final_status[x][y] = status
#print(final_status)
colors = 'green red white'.split()
cmap = matplotlib.colors.ListedColormap(colors, name='colors', N=None)
plt.imshow(final_status, cmap=cmap)
plt.colorbar()
plt.show()
