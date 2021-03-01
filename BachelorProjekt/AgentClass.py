from mesa import Agent, Model
import math
from mesa.space import MultiGrid
import numpy as np
import sys
from Model import find_status

infection_period = abs(round(np.random.normal(9,4)))*120 #How long are they sick?
asymptomatic = 600 #Agents are asymptomatic for 5 days
#From sugerscape_cg
##Helper functions
'Afstandskrav: 2 meter'
def getDistance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2

    dx = abs(x1-x2)
    dy = abs(y1-y2)

    return math.sqrt(dx**2+dy**2)
def dotproduct(v1, v2):
  return v1[0]*v2[0]+v1[1]*v2[1]
def length(v):
  return math.sqrt(v[0]**2+v[1]**2)
def angle(v1, v2):
  angle_in_radians = math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
  angle_in_degrees = (angle_in_radians*180)/math.pi
  return angle_in_degrees


#Moving function
def wonder(self):
    possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
    possible_empty_steps = []
    for position in possible_steps:
        if self.model.grid.is_cell_empty(position):
            possible_empty_steps.append(position)

    if len(possible_empty_steps) != 0:
        next_move = self.random.choice(possible_empty_steps)
        self.model.grid.move_agent(self, next_move)

#check direction between two agents
def checkDirection(agent,neighbor):
    dirA,dirN = agent.coords, neighbor.coords
    angle_ = angle((1,0),(-1,1))
    if -1 <= angle_ <= 1: #The look in the same direction
        return 0
    elif 179 <= angle_ <= 181: #They look in opposite direction
        return 180
    elif 89 <= angle_ <= 91: #De kigger vinkelret på hianden
        return 90
    elif 44 <= angle_ <= 46: #De kigger næsten i samme retning
        return 45
    elif 134 <= angle_ <= 136: #Næsten i modsat retning
        return 135
    elif 224 <= angle_ <= 226: #næsten i modsat retning
        return 225
    elif 314 <= angle_ <= 316: #næsten i samme retning
        return 315
    else: return angle_

#Infect a person
def infect(self):
        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False,radius=2)
        closest_neighbors = []

        for neighbor in all_neighbors_within_radius:
            if not self.model.grid.is_cell_empty(neighbor.pos):
                if isinstance(neighbor,covid_Agent) or isinstance(neighbor,TA):
                    closest_neighbors.append(neighbor)

        pTA = np.random.poisson(2.5/100) #TA står meget tæt og snakker højt
        p_1 = np.random.poisson(0.25/100) #Indenfor 1 meters afstand
        p_1_til_2 = np.random.poisson(0.22450/100) #Mellem 1 og 2 meters afstand
        p_over_2 = np.random.poisson(0.2199651/100) #Over 2 meters afstand
        for agent in closest_neighbors:
            distance = getDistance(self.pos,agent.pos)
            agent_status = agent.infected
            agent_recovered_status = agent.recovered

            if agent_recovered_status == 1 or agent_status == 1: # kan ikke blive smittet, da den er immun eller allerede infected
                continue
            elif distance <= 0.1:
                if pTA == 1:
                    agent.infected = 1
            elif distance > 0.5 and distance <= 1.0:
                if p_1 == 1:
                    agent.infected = 1
            elif distance > 1.0 and distance <= 2.0:
                if p_1_til_2 == 1:
                    agent.infected = 1
            elif p_over_2 == 1:
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
def updateInfectionStatus(self):
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
        self.coords = ()
        self.moving_to_door = 0
        self.TA = 0

        #Relevant for classroom only
        self.hasQuestion = 0
        self.hasEnteredDoor = []

    def move_to_door(self):
        """" Takes one step closer to door"""
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        possible_empty_steps = []
        door_pos = self.door.pos

        for position in possible_steps:
            if position == door_pos:
                self.model.grid.move_agent(self, door_pos)
                self.hasEnteredDoor.append(self)
                return
            elif self.model.grid.is_cell_empty(position):
                 possible_empty_steps.append(position)
        distances = []
        if len(possible_empty_steps) != 0:
            for pos in possible_empty_steps:
                distances.append((pos,getDistance(pos, door_pos)))
            min_dist = min(distances,key=lambda x:x[1])
            if getDistance(self.pos,door_pos) <= min_dist[1]:
               return
            else: self.model.grid.move_agent(self, min_dist[0])

    def move(self,timestep=False):
        if timestep is True:                    #Agents go to door
            self.move_to_door()
        else: wonder(self)

    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):
        if self.infected == 1:
            #Infect if agent should go home
            if hasSymptoms(self):
                return
            #Try to infect
            infect(self)
            #Update infection status
            updateInfectionStatus(self)

        ##MOVE###
        if self.model.minute_count > 2 and (self.model.minute_count)%120==0:
            self.moving_to_door = 1
        if self.moving_to_door == 1 and self.model.setUpType is not 1:
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

class wall(Agent):
    """" Door for people to enter by and to exit by end of class"""
    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id

class TA(Agent):
    def __init__(self,id,model):
        super().__init__(id,model)
        self.infected = 0 #0 for False, 1 for True
        self.recovered = 0 #0 for False, 1 for True
        self.mask = 1 #0 for False, 1 for True
        self.infection_period = infection_period
        self.asymptomatic = asymptomatic # Agents are asymptomatic for 5 days
        self.id = id

        self.timeToTeach = 5
        self.door = self.model.door
        self.students = []
        self.coords = ()

    def move_to_student(self,student):
        x,y = student.pos
        print("VI I LOOP",self.timeToTeach)
        if self.timeToTeach == 0:           #Student has recieved help for 5 minutes
            student.hasQuestion = 1             #Student does not have question anymore
            self.timeToTeach = 5          #Reset timer

        elif self.timeToTeach == 4:   #Student has not recieved help yet, go to that student
            id = self.id
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            newTA = TA(id,self.model)
            newTA.mask = 1
            newTA.coords = self.coords
            newTA.infected = self.infected
            self.model.schedule.add(newTA)
            self.model.grid.place_agent(newTA,(x,y))
            self.timeToTeach -= 1
        else:                               #Student is still recieving help, subtract one minut and stay put
            self.timeToTeach -= 1
        print("STATUS Q",student.hasQuestion)

    def move(self):
        questionStatus = find_status(self.model,"hasQuestion",covid_Agent,self.students)
        print(self.id,self.pos,questionStatus,self.timeToTeach)

        if questionStatus > 0 and self.model.day_count == 1:  #Someone has a question
            for s in self.students:
                if s.hasQuestion == 1:
                    self.move_to_student(s)
        else:
            wonder(self)
            wonder(self)

    def step(self):
        #Check if TA should go home
          if self.infected == 1:
            #Infect if agent should go home
            if hasSymptoms(self):
                return

            infect(self)

            #Update infection status
            updateInfectionStatus(self)

          self.move()

class Cantine_Agent(Agent):
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
