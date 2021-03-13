from mesa import Agent, Model
import math
from mesa.space import MultiGrid
import numpy as np
import random
import sys
from Model import find_status, make_classrooms_fit_to_grid, covid_Model


day_length = 525
other_courses = random.sample([4]*26+[5]*26+[6]*26,k=len([4]*26+[5]*26+[6]*26))
ids = [i for i in range(0,78)]

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
def intersect(list1,list2):
    list3 = [v for v in list1 if v in list2]
    if list3 == []:
        return False        #Intersection is the empty set
    else: return True       #Intersection is not the empty set

#Wander around function
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
        if self.exposed != 0:   #Agent smitter ikke endnu.
            return
        if (self.is_home_sick == 1) or (isinstance(self,canteen_Agent) and self.off_school == 1): #Agenten er derhjemme og kan ikke smitte
            return

        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False,radius=2)
        closest_neighbors = []

        for neighbor in all_neighbors_within_radius:
            if not self.model.grid.is_cell_empty(neighbor.pos):
                if isinstance(neighbor,covid_Agent) or isinstance(neighbor,TA) or isinstance(neighbor,canteen_Agent):
                    closest_neighbors.append(neighbor)

        for agent in closest_neighbors:

            #Dont infect neighbors that are home sick / not on campus
            if agent.is_home_sick == 1 or (isinstance(self,canteen_Agent) and self.off_school == 1):
                continue
            #Dont infect neighbors that are vaccinated
            if agent.vaccinated == 1:
                continue
            distance = getDistance(self.pos,agent.pos)
            agent_status = agent.infected
            agent_recovered_status = agent.recovered

            if agent_recovered_status == 1 or agent_status == 1: # kan ikke blive smittet, da den er immun eller allerede infected
                continue
            elif distance <= 0.1:
                if self.mask == 1:
                    pTA = np.random(0.25/100)
                elif self.mask == 0:
                    pTA = np.random.poisson(2.5/100) #TA står meget tæt og snakker højt
                if pTA == 1:
                    agent.infected = 1
                    self.model.infected_agents.append(agent)
                 #Indenfor 1 meters afstand
            elif distance > 0.5 and distance <= 1.0:
                 if self.mask == 1:
                    p_1 = np.random.poisson(0.025/100)
                 elif self.mask == 0:
                     p_1 = np.random.poisson(0.25/100)
                 if p_1 == 1:
                    agent.infected = 1
                    self.model.infected_agents.append(agent)

                 #Mellem 1 og 2 meters afstand
            elif distance > 1.0 and distance <= 2.0:
                if self.mask == 1:
                    p_1_til_2 = np.random.poisson(0.022450/100)
                elif self.mask == 0:
                     p_1_til_2 = np.random.poisson(0.22450/100)
                if p_1_til_2 == 1:
                    agent.infected = 1
                    self.model.infected_agents.append(agent)

                #Over 2 meters afstand
            elif distance>2.0:
                if self.mask == 1:
                    p_over_2 = np.random.poisson(0.02199651/100)
                elif self.mask == 0:
                     p_over_2 = np.random.poisson(0.2199651/100)
                if p_over_2 == 1:
                    agent.infected = 1
                    self.model.infected_agents.append(agent)

###CHANGING OBJECT-TYPE###
#Get all essential parameters transfered
def change_obj_params(new,old):

    new.is_home_sick, new.vaccinated = old.is_home_sick,\
                                       old.vaccinated

    new.infection_period,new.exposed, new.asymptomatic = old.infection_period,\
                                                         old.exposed,\
                                                         old.asymptomatic,
    #Set up TA agent to have same paramters as prior canteen-agent
    new.infected, new.recovered,  new.mask = old.infected,\
                                             old.recovered,\
                                             old.mask
    new.pos = old.pos
###CHANGING OBJECT-TYPE###

#Turn canteen-object to class-object
def canteen_to_class(self):
    c_agent = covid_Agent(self.id,self.model)
    change_obj_params(c_agent,self)

    c_agent.courses = self.courses
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

#Turn class-object to canteen-object
def class_to_canteen(self):
    c_agent = canteen_Agent(self.id,self.model)
    change_obj_params(c_agent,self)

    c_agent.TA = self.TA

    #Get the correct door (based on the next course the agent will attend)
    x,y = self.courses
    c_agent.courses = [y,x]

    if y in [4,5,6]:
        next_door_id = 500+(y%4)+1
    elif y in [1,2,3]:
        next_door_id = 500+y
    else:
        next_door_id = self.door.id ##TO BE FIXED !! TAS DOOR

    next_door = [a for a in self.model.schedule.agents if isinstance(a,door) and a.id == next_door_id]
    c_agent.door = next_door[0]


    #If it is a TA->Class->Canteen, we cannot remove TA from its own list of students.
    if self.TA is not ():
        students = self.TA.students
        #If student is present
        if self in students and self.is_home_sick == 0:
            students.remove(self)
        self.TA.students = students

    self.model.schedule.remove(self)
    self.model.grid.remove_agent(self)
    self.model.schedule.add(c_agent)

    return c_agent

#Turn TA-object to class-object
def TA_to_class(self):
    c_agent = covid_Agent(self.id,self.model)
    change_obj_params(c_agent,self)

    c_agent.door, c_agent.moving_to_door = self.door, 1
    if self.courses == (): #First time, we need to initialize TA's courses
        c_agent.courses = [0,0]
    else: c_agent.courses = self.courses

    self.model.grid.remove_agent(self)
    self.model.schedule.remove(self)
    self.model.TAs.remove(self)

    self.model.schedule.add(c_agent)
    self.model.grid.place_agent(c_agent,c_agent.pos)

#Turn canteen-object to TA-object
def canteen_to_TA(self):
    c_agent = TA(self.id,self.model)
    change_obj_params(c_agent,self)

    c_agent.door = self.door
    c_agent.students = [0] ##Dummy list, when all students are in class we update the TA's list of students
    c_agent.enrolled_students = [0] ##Dummy list

    self.model.TAs.append(c_agent)

    self.model.schedule.remove(self)
    self.model.grid.remove_agent(self)
    self.model.schedule.add(c_agent)

    return c_agent

def move_to_specific_pos(self,pos_):
    if self.id in [1001,1002,1003,1004,1005,1006]:
        if isinstance(self,canteen_Agent):
            newAgent = canteen_to_TA(self)
            #"push" agent through door
            x,y = pos_                      #Door position
            newY = random.randint(-1, 1)
            newAgent.pos = x-1,y+newY
            self.model.grid.place_agent(newAgent, newAgent.pos)
            return

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

    if self.model.minute_count in [50,170,350,480]:
        force_agent_to_specific_pos(self,pos_)
        return
    self.model.grid.move_agent(self,(x_,y_))

def force_agent_to_specific_pos(self,pos):
    self.model.grid.move_agent(self,pos)

def send_agent_home(self):
    self.is_home_sick = 1
    self.model.agents_at_home.append(self)

def send_agent_back_to_school(self):
    newList_at_home = [a for a in self.model.agents_at_home if a.id != self.id]
    self.model.agents_at_home = newList_at_home

    self.model.recovered_agents.append(self)
    self.is_home_sick = 0
    self.infected = 0
    self.recovered = 1

def update_infection_parameters(self):
    if self.is_home_sick == 1: #Agent is already home. Just update infection period
        self.infection_period = max(0,self.infection_period-1)
        if self.infection_period == 0:
            send_agent_back_to_school(self)
        return
    if self.recovered == 1:
        return              #Agent is recovered

    self.asymptomatic = max(0,self.asymptomatic-1)
    if self.asymptomatic == 0:
        send_agent_home(self)
    self.exposed = max(0,self.exposed-1)    #If already 0 stay there, if larger than 0 subtract one
    self.infection_period = max(0,self.infection_period-1)

class covid_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id
        self.model = model
        self.coords = ()

        self.infected = 0
        self.recovered = 0
        self.mask = 0
        self.is_home_sick = 0
        self.vaccinated = 0

          #Infection parameters
        self.infection_period = max(5*day_length,abs(round(np.random.normal(9*day_length,1*day_length))))#How long are they sick?
        self.asymptomatic = min(max(3*day_length,abs(round(np.random.normal(5*day_length,1*day_length)))),self.infection_period) #Agents are asymptomatic for 5 days
        self.exposed = self.asymptomatic-2*day_length



        self.moving_to_door = 0
        self.door = ()
        self.courses = [0,0]


        self.TA = ()
        self.seat = ()

        #Relevant for classroom only
        self.hasQuestion = 0
        self.hasEnteredDoor = []

    def move(self,timestep=False):
        if timestep is True:
            if self.moving_to_door == 1: #Agents go to door
                move_to_specific_pos(self,self.door.pos)
         #       move_to_specific_pos(self,self.door.pos)
            elif self.moving_to_door == 0: #Agents go to seat
                move_to_specific_pos(self,self.seat)
               # move_to_specific_pos(self,self.seat)
        else: wonder(self)


    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):
        if self.infected == 1:
            #Try to infect
            infect(self)
            update_infection_parameters(self)
        if self.is_home_sick == 1:
            update_infection_parameters(self)

        ##MOVE###
        if self.model.day_count == 1:
            if self.model.minute_count in self.model.class_times and self.model.minute_count%2 == 1:
                self.moving_to_door = 1

        elif self.model.day_count > 1 and self.model.minute_count in self.model.class_times+[1] and self.model.minute_count%2 == 1:
            self.moving_to_door = 1

        self.move(True)

class TA(Agent):
    def __init__(self,id,model):
        super().__init__(id,model)
        self.id = id
        self.infected = 0
        self.recovered = 0
        self.mask = 1
        self.is_home_sick = 0
        self.vaccinated = 0

        self.time_remaining = 105

          #Infection parameters
        self.infection_period = max(5*day_length,abs(round(np.random.normal(9*day_length,1*day_length))))#How long are they sick?
        self.asymptomatic = min(max(3*day_length,abs(round(np.random.normal(5*day_length,1*day_length)))),self.infection_period) #Agents are asymptomatic for 5 days
        self.exposed = self.asymptomatic-2*day_length

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

    def connect_TA_and_students(self):
        ss = [a for a in self.model.schedule.agents if isinstance(a,covid_Agent) and a.door == self.door]

        #Get the correct students, because they can overlap when a class is ending and new one is starting
        if self.id in [1001,1002,1003]:
            self.students = [a for a in ss if a.id in range(0,(self.model.n_agents+1)*3) and a.is_home_sick != 1]
        elif self.id in [1004,1005,1006]:
            self.students = [a for a in ss if a.id not in range(0,(self.model.n_agents+1)*3) and a.is_home_sick != 1]

        #Apply TA to students
        for s in self.students:
            s.TA = self

    def move(self):
        questionStatus = find_status(self.model,"hasQuestion",[covid_Agent],self.students)

        if questionStatus > 0 and len(self.students) > 15:  #Class is started and somebody a question
            for s in self.students:
                if s.hasQuestion == 1:
                    self.move_to_student(s)
        else:
            wonder(self)
            wonder(self)

    def step(self):
      self.time_remaining -=1
      self.connect_TA_and_students()

      if self.time_remaining <= 0 and len(self.students)<5:
          TA_to_class(self)
          return

      if self.infected == 1:
         infect(self)
         update_infection_parameters(self)
    #  if self.is_home_sick == 1:
   #         update_infection_parameters(self)
      self.move()

class canteen_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        #Person parameters
        self.id = id
        self.infected = 0
        self.recovered = 0
        self.mask = 0
        self.is_home_sick = 0
        self.vaccinated = 0

        self.off_school = 0
        self.coords = ()

        #Infection parameters
        self.infection_period = max(5*day_length,abs(round(np.random.normal(9*day_length,1*day_length))))#How long are they sick?
        self.asymptomatic = min(max(3*day_length,abs(round(np.random.normal(5*day_length,1*day_length)))),self.infection_period) #Agents are asymptomatic for 5 days
        self.exposed = self.asymptomatic-2*day_length

        #Class-schedule parameters
        self.next_to_attend_class = False
        self.door = ()
        self.courses = ()
        self.moving_to_door = 0
        self.TA = ()


    def move(self,timestep=False):
        if timestep is True: #Agents go to door
            move_to_specific_pos(self,self.door.pos)
        else: wonder(self)

    def step(self):
        if self.infected == 1:
            if self.off_school == 0:
                infect(self)
                update_infection_parameters(self)

        if self.is_home_sick == 1:
            update_infection_parameters(self)

        #When should canteen agent go to door?
        if self.model.day_count == 1:
            if self.model.minute_count in self.model.class_times and self.model.minute_count % 2 == 0 and self.next_to_attend_class is True:
                self.moving_to_door = 1
        elif (self.model.minute_count == 0 or (self.model.minute_count in self.model.class_times+[2] and self.model.minute_count%2 == 0))\
                and self.next_to_attend_class is True:
            self.moving_to_door = 1

        if self.moving_to_door == 1:
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
