import AgentClass as ac
from mesa.time import SimultaneousActivation,RandomActivation
from mesa.space import MultiGrid
import random
from mesa import Agent, Model
import numpy as np
from mesa.datacollection import DataCollector


init_positive_agents = 2
dir = {'N':(1,0), 'S':(-1,0), 'E':(0,1), 'W':(0,-1),'NE': (1,1), 'NW': (-1,1), 'SE':(1,-1), 'SW':(-1,-1)}

#Get the status of a given parameter at any time in model (infected, hasQuestion, recovered, etc).
def find_status(model,parameter,agent_type=None):
    agents_status = []
    all_agents = model.schedule.agents

    if agent_type is not None:
        for agent in model.schedule.agents:
            if isinstance(agent, agent_type):
                agents_status.append(getattr(agent,parameter))
    else:
        for agent in model.schedule.agents:
            if not isinstance(agent, ac.door):
                agents_status.append(getattr(agent,parameter))
    return sum(agents_status)

#Set up the grid accordingly - also adding positive agents.
def setUp(N,model,setUpType):
    'random set-up'
    if setUpType == 1:
        for i in range(1,N):
            newAgent = ac.covid_Agent(i, model)
            model.schedule.add(newAgent) #Add agent to scheduler
            x, y = model.grid.find_empty()#Place agent randomly in empty cell on grid
            newAgent.coords = random.choice(list(dir.values()))   #Give agent random direction to look at
            model.grid.place_agent(newAgent, (x,y))
    elif setUpType == 2: #Horseshoe
        listOfPositions = [((1,1),dir['E']),((2,1),dir['N']),((3,1),dir['N']),((4,1),dir['N']),((5,1),dir['N']),
                           ((6,1),dir['N']),((1,2),dir['E']),((1,3),dir['E']),((2,3),dir['S']),((3,3),dir['S']),
                           ((4,3),dir['S']),((5,3),dir['S']),((6,3),dir['S']),
                           ((1,6),dir['E']),((2,6),dir['N']),((3,6),dir['N']),((4,6),dir['N']),((5,6),dir['N']),
                           ((6,6),dir['N']),((1,7),dir['E']),((1,8),dir['E']),((2,8),dir['S']),((3,8),dir['S']),
                           ((4,8),dir['S']),((5,8),dir['S']),((6,8),dir['S'])]

    elif setUpType == 3: #Rows
        listOfPositions = [((1,5),dir['E']),((1,6),dir['E']),((1,7),dir['E']),((1,8),dir['E']),((1,9),dir['E']),
                           ((2,0),dir['E']),((2,1),dir['E']),((2,2),dir['E']),((2,3),dir['E']),
                           ((3,5),dir['E']),((3,6),dir['E']),((3,7),dir['E']),((3,8),dir['E']),((3,9),dir['E']),
                           ((4,0),dir['E']),((4,1),dir['E']),((4,2),dir['E']),((4,3),dir['E']),
                           ((5,6),dir['E']),((5,7),dir['E']),((5,8),dir['E']),((5,9),dir['E']),((6,0),dir['E']),
                           ((6,1),dir['E']),((6,2),dir['E']),((6,3),dir['E'])]
    elif setUpType == 4: #4-people table with correct direction added
        listOfPositions = [((1,1),dir['N']),((1,2),dir['S']),((2,1),dir['N']),((2,2),dir['S']),
                           ((1,4),dir['N']),((1,5),dir['S']),((2,4),dir['N']),((2,5),dir['S']),
                           ((1,7),dir['N']),((1,8),dir['S']),((2,7),dir['N']),((2,8),dir['S']),
                           ((4,1),dir['E']),((4,2),dir['E']),((5,1),dir['N']),((5,2),dir['S']),((6,1),dir['N']),((6,2),dir['S']),
                           ((4,4),dir['N']),((4,5),dir['S']),((5,4),dir['N']),((5,5),dir['S']),
                           ((4,7),dir['N']),((4,8),dir['S']),((5,7),dir['N']),((5,8),dir['S'])]
    if setUpType is not 1:
        for i in range(N):
            newAgent = ac.covid_Agent(i, model)
            model.schedule.add(newAgent) #Add agent to scheduler
            posAndDirection = listOfPositions.pop()
            x,y = posAndDirection[0]
            newAgent.coords = posAndDirection[1]
            model.grid.place_agent(newAgent,(x,y))
        x,y = random.choice([(7,5),(7,4)])
        TA = ac.TA(1000,model)
        model.schedule.add(TA)
        model.grid.place_agent(TA,(x,y))

    #Add positive agents
    for i in range(init_positive_agents):
        randomAgent = model.random.choice(model.schedule.agents)
        model.schedule.remove(randomAgent)
        postive_agent = randomAgent
        postive_agent.infected = 1
        model.schedule.add(postive_agent)

class covid_Model(Model):
    def __init__(self, N, height, width,setUpType):
        self.n_agents = N
        self.grid = MultiGrid(width, height, torus=False) #torus wraps edges
        self.schedule = RandomActivation(self)
        self.setUpType = setUpType
        self.status = find_status(self,"infected",ac.covid_Agent)
        self.datacollector = DataCollector(model_reporters={"infected": lambda m:find_status(self,"infected",ac.covid_Agent)})

        #Counting minutes and days
        self.minute_count = 0
        self.day_count = 1

        #Classroom only
        self.timeToTeach = 5

        #Add door(s) to model and grid
        door_location = (8,5)
        self.door = ac.door(500, door_location, self)
        self.schedule.add(self.door)
        self.grid.place_agent(self.door,door_location)

        #Add agents to model and grid
        setUp(self.n_agents+1,self,setUpType)

        self.datacollector.collect(self)
        self.running = True

    def step(self):
        #Every 10th timestep add asking student
        if not self.setUpType == 1 and self.schedule.time>2 and (self.schedule.time) % 10 == 0:
          randomStudent = self.random.choice(self.schedule.agents)
          self.schedule.remove(randomStudent)
          student_with_Question = randomStudent
          student_with_Question.hasQuestion = 1
          self.schedule.add(student_with_Question)

        self.schedule.step()
        self.datacollector.collect(self)

        #Minute count
        self.minute_count += 1
        if self.minute_count % 120 == 0:
            self.day_count += 1

        #Terminate model when everyone is healthy
        if find_status(self,"infected") == 0:
           self.running = False
