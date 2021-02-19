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
        TA = ac.covid_Agent(1000,model)
        TA.mask = 1
        model.schedule.add(TA)
        x,y = random.choice([(7,5),(7,4)])
        model.grid.place_agent(TA,(x,y))

    elif setUpType == 3: #Rows
        listOfPositions = [(1,5),(1,6),(1,7),(1,8),(1,9),(2,0),(2,1),(2,2),(2,3),
                           (3,5),(3,6),(3,7),(3,8),(3,9),(4,0),(4,1),(4,2),(4,3),
                           (5,6),(5,7),(5,8),(5,9),(6,0),(6,1),(6,2),(6,3)]
        for i in range(N):
            newAgent = ac.covid_Agent(i, model)
            model.schedule.add(newAgent)
            x,y = listOfPositions.pop()
            model.grid.place_agent(newAgent,(x,y))

        TA = ac.covid_Agent(1000,model)
        model.schedule.add(TA)
        x,y = random.choice([(7,6),(7,5),(7,4)])
        model.grid.place_agent(TA,(x,y))
    elif setUpType == 4:
        listOfPositions = [(1,1),(1,2),(2,1),(2,2),
                           (1,4),(1,5),(2,4),(2,5),
                           (1,7),(1,8),(2,7),(2,8),
                           (4,1),(4,2),(5,1),(5,2),(6,1),(6,2),
                           (4,4),(4,5),(5,4),(5,5),
                           (4,7),(4,8),(5,7),(5,8)]
        for i in range(1,N):
            newAgent = ac.covid_Agent(i, model)
            model.schedule.add(newAgent)
            x,y = listOfPositions.pop()
            model.grid.place_agent(newAgent,(x,y))

        TA = ac.covid_Agent(1000,model)
        model.schedule.add(TA)
        x,y = random.choice([(7,6),(7,5),(7,4)])
        model.grid.place_agent(TA,(x,y))


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
        self.datacollector = DataCollector(model_reporters={"infected": lambda m:find_status(self)})
        #The scheduler is a special model component which controls the order in which agents are activated
        self.minute_count = 0
        self.day_count = 1

        #Classroom only
        self.timeToTeach = 5

        ' Tilføj agenter til vores setup '
        setUp(self.n_agents+1,self,setUpType)


        'Tilføj positive person-agenter'
        for i in range(init_positive_agents):
            randomAgent = self.random.choice(self.schedule.agents)
            self.schedule.remove(randomAgent)
            postive_agent = randomAgent
            postive_agent.infected = 1
            self.schedule.add(postive_agent)

        self.datacollector.collect(self)
        self.running = True

    def step(self):

        if not self.setUpType == 1 and (self.schedule.time+1)%10 == 0:   #Add asking student
          randomStudent = self.random.choice(self.schedule.agents)
          self.schedule.remove(randomStudent)
          student_with_Question = randomStudent
          student_with_Question.hasQuestion = 1
          self.schedule.add(student_with_Question)


        self.recovered = 0
        self.schedule.step()
        self.datacollector.collect(self)



        #Minute count
        self.minute_count += 1
        if self.minute_count % 120 == 0:
            self.day_count += 1

        #Terminate model when everyone is healthy
        if find_status(self) == 0:
           self.running = False
