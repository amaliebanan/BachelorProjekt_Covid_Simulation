from mesa import Agent, Model
import math
from mesa.space import MultiGrid
import numpy as np
from Model import find_status


infection_period = 9 #How long are they sick?
asymptomatic = 100 #Agents are asymptomatic for 5 days
#From sugerscape_cg
'Afstandskrav: 2 meter'
def getDistance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2

    dx = abs(x1-x2)
    dy = abs(y1-y2)

    return math.sqrt(dx**2+dy**2)

#Moving functions

def wonder(self):
    possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
    possible_empty_steps = []
    for position in possible_steps:
        if self.model.grid.is_cell_empty(position):
            possible_empty_steps.append(position)

    if len(possible_empty_steps) != 0:
        next_move = self.random.choice(possible_empty_steps)
        self.model.grid.move_agent(self, next_move)

#Infect a person
def infect(self):
        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=True,radius=2)
        closest_neighbors = []

        for neigbor in all_neighbors_within_radius:
            if not self.model.grid.is_cell_empty(neigbor.pos):
                if isinstance(neigbor,covid_Agent) or isinstance(neigbor,TA):
                    closest_neighbors.append(neigbor)

        r90 = np.random.poisson(90/100)
        r68 = np.random.poisson(68/100)
        r30 = np.random.poisson(30/100)
        r10 = np.random.poisson(10/100)
        r2 = np.random.poisson(2/100)

        for agent in closest_neighbors:
            distance = getDistance(self.pos,agent.pos)
            agent_status = agent.infected
            agent_recovered_status = agent.recovered

            if agent_recovered_status == 1 or agent_status == 1: # kan ikke blive smittet, da den er immun eller allerede infected
                continue
            elif distance <= 0.1:
                if r90 == 1:
                    agent.infected = 1
            elif distance > 0.5 and distance <= 1.0:
                if r68 == 1:
                    agent.infected = 1
            elif distance > 1.0 and distance <= 1.7:
                if r30 == 1:
                    agent.infected = 1
            elif distance > 1.7 and distance <= 2.0:
                if r10 == 1:
                    agent.infected = 1
            elif r2 == 1:
                agent.infected = 1

#Check if a person has symptoms
def hasSymptoms(self):
    self.asymptomatic -= 1
    if self.asymptomatic == 0:
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)
        return True
    else: return False

#Update infection status
def setInfectionStatus(self):
    self.infection_period -= 1
    if self.infection_period == 0:
        self.infected = 0
        if np.random.poisson(1/100) == 1:
            self.recovered = 0
            self.infection_period = 9
        else:
            self.recovered = 1

class covid_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.infected = 0 #0 for False, 1 for True
        self.recovered = 0 #0 for False, 1 for True
        self.mask = 0 #0 for False, 1 for True
        self.infection_period = infection_period
        self.asymptomatic = asymptomatic
        self.id = id
        self.door = self.model.door

        #Relevant for classroom only
        self.hasQuestion = 0

    #Go through neighbors and find one to infect.


    def move_to_door(self):
        """" Takes one step closer to door"""
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        possible_empty_steps = []
        for position in possible_steps:
            if self.model.grid.is_cell_empty(position):
                possible_empty_steps.append(position)
        distances = []
        if len(possible_empty_steps) != 0:
            for pos in possible_empty_steps:
                distances.append((pos,getDistance(pos, self.door.pos)))
            min_dist = min(distances,key=lambda x:x[1])
            ##TJEK OM MAN SELV ER TÆTTERE PÅ DØREN, SÅ IK RYK!#
            self.model.grid.move_agent(self, min_dist[0])

    def move(self,timestep=False):
        if timestep is True:                    #Agents go to door
            self.move_to_door()

        else: wonder()

    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):

        if self.infected == 1:
            #Infect if agent should go home
            if hasSymptoms(self):
                return
            #If not, roll a dice
            randomInt = np.random.poisson(1/2)
            if randomInt == 1:
                infect(self)

            #Update infection status
            setInfectionStatus(self)

        ##MOVE###
        if self.model.minute_count > 2 and (self.model.minute_count)%120==0:
            self.move(True)                                           #Students go to door
        elif self.model.setUpType == 1:
            self.move()

class door(Agent):
    """" Door for people to enter by and to exit by end of class"""
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        self.pos = pos
        self.id = id
        self.model = model

class TA(Agent):
    def __init__(self,id,model):
        super().__init__(id,model)
        self.infected = 0 #0 for False, 1 for True
        self.recovered = 0 #0 for False, 1 for True
        self.mask = 1 #0 for False, 1 for True
        self.infection_period = infection_period
        self.asymptomatic = asymptomatic # Agents are asymptomatic for 5 days
        self.id = id
        self.door = self.model.door

    def move_to_student(self,student):
        x,y = student.pos
        if self.model.timeToTeach == 0:           #Student has recieved help for 5 minutes
            student.hasQuestion = 0             #Student does not have question anymore
            self.model.timeToTeach = 5          #Reset timer

        elif self.model.timeToTeach == 4:   #Student has not recieved help yet, go to that student

            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            newTA = TA(1000,self.model)
            newTA.mask = 1
            newTA.infected = self.infected
            self.model.schedule.add(newTA)
            self.model.grid.place_agent(newTA,(x,y))
            self.model.timeToTeach -= 1
        else:                               #Student is still recieving help, subtract one minut and stay put
            self.model.timeToTeach -= 1

    def move(self):
        students = [s for s in self.model.schedule.agents if isinstance(s,covid_Agent)]
        questionStatus = find_status(self.model,"hasQuestion",covid_Agent)

        if questionStatus > 0:  #Someone has a question
            for s in students:
                if s.hasQuestion == 1:
                    self.move_to_student(s)
        else: wonder(self)

    def step(self):
        #Check if TA should go home
          if self.infected == 1:
            #Infect if agent should go home
            if hasSymptoms(self):
                return
            #If not, roll a dice
            randomInt = np.random.poisson(1/2)
            if randomInt == 1:
                infect(self)

            #Update infection status
            setInfectionStatus(self)

          self.move()
