from mesa import Agent, Model
import math
from mesa.space import MultiGrid
import numpy as np
import random
import sys
from Model import find_status, make_classrooms_fit_to_grid, covid_Model

infection_period = abs(round(np.random.normal(9,4)))*120 #How long are they sick?
asymptomatic = 600 #Agents are asymptomatic for 5 days
courses_first = [1,2,3]
courses_second = [4,5,6]
i=1
ids_first = [i for i in range(0,78)]
ids_second = [i for i in range(78,160)]+[1000]+[1001]+[1002]

other_courses = random.sample([4]*26+[5]*26+[6]*26,k=len([4]*26+[5]*26+[6]*26))
#From sugerscape_cg
##Helper functions
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

#Turn class-object to canteen-object
def class_to_canteen(self):
    c_agent = canteen_Agent(self.id,self.model)

    #Set up canteen agent to have same paramters as prior class-agent
    c_agent.infected, c_agent.recovered, c_agent.mask = self.infected, self.recovered,self.mask
    c_agent.pos = self.pos

    #Get the correct door (based on the next course the agent will attend)
    x,y = self.courses
    c_agent.courses = [y,x]

    if y in [4,5,6]:
        next_door_id = 500+(y%4)+1
    elif y in [1,2,3]:
        next_door_id = 500+y
    else:
        next_door_id = 500+1 ##TO BE FIXED !! TAS DOOR

    next_door = [a for a in self.model.schedule.agents if isinstance(a,door) and a.id == next_door_id]
    c_agent.door = next_door[0]

    self.model.schedule.remove(self)
    self.model.grid.remove_agent(self)
    self.model.schedule.add(c_agent)


    #If it is a TA->Class->Canteen, we cannot remove TA from its own list of students.
    if self.TA is not ():
        self.TA.students.remove(self)

    return c_agent

#Turn TA-object to class-object
def TA_to_class(self):
    self.model.grid.move_agent(self, self.pos)
    c_agent = covid_Agent(self.id,self.model)
    c_agent.infected, c_agent.recovered, c_agent.mask = self.infected, self.recovered,self.mask
    c_agent.door, c_agent.moving_to_door = self.door, 1

    if self.courses == (): #First time, we need to initialize TA's courses
        c_agent.courses = [0,0]
    else: c_agent.courses = self.courses

    self.model.schedule.remove(self)
    x,y = self.pos

    self.model.schedule.add(c_agent)
    self.model.grid.place_agent(c_agent,(x,y))

    self.model.grid.remove_agent(self)

def move_to_specific_pos(self,pos_):
    possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    possible_empty_steps = [cell for cell in possible_steps if self.model.grid.is_cell_empty(cell)]

    #If no cell is empty, agent can go through others "person"-agents (to avoid bottleneck)
    #Back-up list contains cells with covid,TA and canteen agents in
    pos_other_agents = [cell for cell in self.model.grid.get_neighbors(self.pos,moore=True,include_center=False)
                         if isinstance(cell,covid_Agent) or isinstance(cell,TA) or isinstance(cell,canteen_Agent)]
    back_up_empty_cells = [cell.pos for cell in pos_other_agents]

    #If goal-position is in possible steps, go there
    if pos_ in possible_steps:
        #If goal-position is a door change object accordingly
        if pos_ == self.door.pos:
            if isinstance(self,covid_Agent):
                newAgent = class_to_canteen(self)
                #"push" agent through door
                x,y = pos_                         #Door position
                newY = random.randint(-1, 1)
                newAgent.pos = x+1,y+newY
                self.model.grid.place_agent(newAgent, newAgent.pos)
                return

            elif isinstance(self,canteen_Agent):
                newAgent,seat_ = canteen_to_class(self)
                #"push" agent through door
                x,y = pos_                      #Door position
                newY = random.randint(-1, 1)
                newAgent.pos = x-1,y+newY
                newAgent.seat = seat_
                self.model.grid.place_agent(newAgent, newAgent.pos)
                return
        #If goal-position is the seat, go there
        if isinstance(self,covid_Agent) and pos_ == self.seat:
            self.model.grid.move_agent(self,pos_)
            return

    #If you are already at your seat, stay there
    if pos_ == self.pos:
        return

   #### Agent is moving one step closer to goal-position ####

    #Which list to use? If possible_empty_steps is empty, use back-up list (allowing agent to go through agents)
    if possible_empty_steps == []:
        cells_to_check = back_up_empty_cells
    else: cells_to_check = possible_empty_steps

    #Distances from all possible positions and goal-position
    distances = [(pos,getDistance(pos_,pos)) for pos in cells_to_check]

    #Get x,y position of the cell with the smallest distance between goal-position and possible cells to go to
    x_,y_ = min(distances,key=lambda x:x[1])[0]


    dist_from_desired_cell_to_pos_ = min(distances,key=lambda x:x[1])[1]
    dist_self_to_pos_ = getDistance(self.pos,pos_)

    #Only move if the cell is closer to desired cell than your own cell
    #if dist_self_to_pos_ > dist_from_desired_cell_to_pos_:
    self.model.grid.move_agent(self,(x_,y_))

def canteen_to_class(self):
    c_agent = covid_Agent(self.id,self.model)

    #Set up canteen agent to have same paramters as prior class-agent
    c_agent.infected, c_agent.recovered, c_agent.mask = self.infected, self.recovered,self.mask
    c_agent.courses, c_agent.classrooms = self.courses, self.classrooms
    c_agent.pos = self.pos
    c_agent.moving_to_door = 0

    c_agent.door = self.door

    #Which classroom are agent entering, adjust the y-coordinate accordingly.
    i = self.door.id-501

    #Get a seat
    seat = self.model.seats[i].pop()


    self.model.schedule.remove(self)
    self.model.grid.remove_agent(self)
    self.model.schedule.add(c_agent)

    return c_agent,seat

#Turn canteen-object to TA-object
def canteen_to_TA(self):
    print("To be implemented")

class covid_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.infected = 0 #0 for False, 1 for True
        self.recovered = 0 #0 for False, 1 for True
        self.mask = 0 #0 for False, 1 for True

        self.infection_period = infection_period
        self.asymptomatic = asymptomatic
        self.id = id
        self.coords = ()
        self.moving_to_door = 0
        self.TA = ()
        self.door = ()
        self.courses = [0,0]
        self.classrooms = [0,0]
        self.seat = ()

        #Relevant for classroom only
        self.hasQuestion = 0
        self.hasEnteredDoor = []

    def move(self,timestep=False):
        if timestep is True:
            if self.moving_to_door == 1: #Agents go to door
                move_to_specific_pos(self,self.door.pos)
            elif self.moving_to_door == 0: #Agents go to seat
                move_to_specific_pos(self,self.seat)
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
        if self.model.minute_count > 2 and self.model.minute_count in self.model.class_times and self.model.minute_count%2 == 0:
            self.moving_to_door = 1
        self.move(True)

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
        self.courses = ()
        self.door = ()
        self.students = []
        self.coords = ()

    def move_to_student(self,student):

        x,y = student.pos
        if self.timeToTeach == 0:           #Student has recieved help for 5 minutes
            student.hasQuestion = 0            #Student does not have question anymore
            self.timeToTeach = 5          #Reset timer

        elif self.timeToTeach == 4:   #Student has not recieved help yet, go to that student
            newTA = self
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            self.model.schedule.add(newTA)
            self.model.grid.place_agent(newTA,(x,y))
            self.timeToTeach -= 1
        else:                               #Student is still recieving help, subtract one minut and stay put
            self.timeToTeach -= 1


    def move(self):
        questionStatus = find_status(self.model,"hasQuestion",[covid_Agent],self.students)

        if questionStatus > 0 and self.model.day_count == 1:  #Someone has a question
            for s in self.students:
                if s.hasQuestion == 1:
                    self.move_to_student(s)
        else:
            wonder(self)
            wonder(self)

    def step(self):
      if len(self.students) == 0:
          TA_to_class(self)
          return

      if self.infected == 1:
        #Infect if agent should go home
        if hasSymptoms(self):
            return

        infect(self)

        #Update infection status
        updateInfectionStatus(self)

      self.move()

class canteen_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.infected = 0 #0 for False, 1 for True
        self.recovered = 0 #0 for False, 1 for True
        self.mask = 0 #0 for False, 1 for True
        self.infection_period = infection_period
        self.asymptomatic = asymptomatic
        self.id = id
        self.door = ()
        self.just_finished_class = 1
        self.courses = ()
        self.classrooms = ()
        self.moving_to_door = 0
        self.just_created = 0
        self.next_to_attend_class = False

        #Relevant for classroom only
        self.hasQuestion = 0

    def move(self,timestep=False):
        if timestep is True: #Agents go to door
            move_to_specific_pos(self,self.door.pos)
        else: wonder(self)

    def step(self):
        if self.model.minute_count in self.model.class_times and self.model.minute_count % 2 == 1 and \
                self.next_to_attend_class is True and self.courses is not ():
            self.moving_to_door = 1
        if self.moving_to_door == 1 and self.model.setUpType is not 1:
            self.move(True)
        else: self.move()

class wall(Agent):
    """" Door for people to enter by and to exit by end of class"""
    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id
        self.orientation = ()

class door(Agent):
    """" Door for people to enter by and to exit by end of class"""
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        self.pos = pos
        self.id = id
        self.model = model
        self.classroom = 0

#Places in canteen to attract people
#Toilets, canteen, tables in hall, etc.
class hotspot(Agent):
    def __init__(self,id,model):
        super().__init__(id,model)
        self.id = id
        self.model = id
        self.students_to_attrach = []
