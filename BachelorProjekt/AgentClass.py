from mesa import Agent, Model
import math
from mesa.space import MultiGrid
import numpy as np
import random
import sys
from Model import covid_Model,with_mask,is_same_object, is_invisible, is_human, dir,count_students_who_has_question, infection_rate, infection_rate_1_to_2_meter, infection_rate_2plus_meter, infection_decrease_with_mask_pct, calculate_percentage
from scipy.stats import truncnorm

day_length = 525
other_courses = random.sample([4]*26+[5]*26+[6]*26,k=len([4]*26+[5]*26+[6]*26))
ids = [i for i in range(0,78)]

##Helper functions

def getDistance(pos1,pos2):
    return math.sqrt((pos2[0]-pos1[0])**2+(pos2[1]-pos1[1])**2)
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
def change_direction(self, start_pos, end_pos):
    if end_pos == None:
        return dir['E']
    change_of_pos = np.subtract(start_pos, end_pos)
    if (np.array(change_of_pos)==np.array([1,1])).all(): #if agent moves SW
        return dir['SW']
    elif (np.array(change_of_pos)==np.array([1,0])).all(): #if agent moves W
        return dir['W']
    elif (np.array(change_of_pos)==np.array([1,-1])).all(): #if agent moves NW
        return dir['NW']
    elif (np.array(change_of_pos)==np.array([0,-1])).all(): #if agent moves N
        return dir['N']
    elif (np.array(change_of_pos)==np.array([-1,-1])).all(): #if agent moves NE
        return dir['NE']
    elif (np.array(change_of_pos)==np.array([-1,0])).all(): #if agent moves E
        return dir['E']
    elif (np.array(change_of_pos)==np.array([-1,1])).all(): #if agent moves SE
        return dir['SE']
    elif (np.array(change_of_pos)==np.array([0,1])).all(): #if agent moves S
        return dir['S']
    elif start_pos == end_pos: #if agent doesn't move
        return self.coords
    else:
        return self.coords

def get_agent_at_cell(self,pos):
    return self.model.grid.get_cell_list_contents(pos)[0]

def truncnorm_(lower,upper,mu,sigma):
    return int(truncnorm((lower - mu) /sigma, (upper - mu) /sigma, loc = mu, scale=sigma))

#Wander around function
def wander(self):
    possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
    possible_empty_steps = []
    for position in possible_steps:
        if isinstance(self, canteen_Agent):
            if position not in [(23,18), (23,19)]:#cant walk wrong way through canteen
                if self.model.grid.is_cell_empty(position) or is_invisible(get_agent_at_cell(self,position)) or\
                        isinstance(get_agent_at_cell(self,position),table):
                    possible_empty_steps.append(position)

        elif position not in [(23,18), (23,19)]:#cant walk wrong way through canteen
            if self.model.grid.is_cell_empty(position):
                possible_empty_steps.append(position)
            elif isinstance(get_agent_at_cell(self,position),table):
                possible_empty_steps.append(position)

    if len(possible_empty_steps) != 0:
        next_move = self.random.choice(possible_empty_steps)
        self.model.grid.move_agent(self, next_move)

    if self.pos in [x for (x,y) in self.model.canteen_table_1]+[x for (x,y) in self.model.canteen_table_2]:
        self.sitting_in_canteen = 15

#check direction between two agents
def checkDirection(agent,neighbor):
    dirA,dirN = agent.coords, neighbor.coords
    angle_ = angle(dirA,dirN)
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

        if isinstance(self, TA):
            all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=True,radius=2)
        else:
            all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False,radius=2)
        closest_neighbors = []

        for neighbor in all_neighbors_within_radius:
            if not self.model.grid.is_cell_empty(neighbor.pos):
                if is_human(neighbor):
                    closest_neighbors.append(neighbor)

        for agent in closest_neighbors:

            #Dont infect neighbors that are home sick / not on campus
            if is_invisible(agent):
                return
            #Dont infect neighbors that are vaccinated, recorvered or
            if agent.vaccinated == True or agent.recovered == True or agent.infected == True: # kan ikke blive smittet, da den er immun eller allerede infected
                continue

            distance = getDistance(self.pos,agent.pos)
            if distance <= 0.1:
                if is_same_object(self,agent) == False: #Its a TA
                    if self.mask == True:
                        pTA = np.random.poisson(calculate_percentage(100*infection_rate,infection_decrease_with_mask_pct))
                    elif self.mask == False:
                        pTA = np.random.poisson(100*infection_rate) #TA står meget tæt og snakker højt
                    if pTA == 1:
                        agent.infected = True
                        self.model.infected_agents.append(agent)
                else: ##De er i indgangen, smit mindre
                    if self.mask == True:
                        pTA = np.random.poisson(calculate_percentage(10*infection_rate,infection_decrease_with_mask_pct))
                    elif self.mask == False:
                        pTA = np.random.poisson(10*infection_rate)
                    if pTA == 1:
                        agent.infected = True
                        self.model.infected_agents.append(agent)
                 #Indenfor 1 meters afstand
            elif distance > 0.5 and distance <= 1.0:
                 if self.mask == True:
                    p_1 = np.random.poisson(calculate_percentage(infection_rate, infection_decrease_with_mask_pct)) #70 percent decrease if masks
                 elif self.mask == False:
                     p_1 = np.random.poisson(infection_rate)
                 if p_1 == 1:
                    agent.infected = True
                    self.model.infected_agents.append(agent)

                 #Mellem 1 og 2 meters afstand
            elif distance > 1.0 and distance <= 2.0:
                if self.mask == True:
                    p_1_til_2 = np.random.poisson(calculate_percentage(infection_rate_1_to_2_meter,infection_decrease_with_mask_pct))
                elif self.mask == False:
                     p_1_til_2 = np.random.poisson(infection_rate_1_to_2_meter)
                if p_1_til_2 == 1:
                    agent.infected = True
                    self.model.infected_agents.append(agent)

                #Over 2 meters afstand
            elif distance>2.0:
                if self.mask == True:
                    p_over_2 = np.random.poisson(calculate_percentage(infection_rate_2plus_meter,infection_decrease_with_mask_pct))
                elif self.mask == False:
                     p_over_2 = np.random.poisson(infection_rate_2plus_meter)
                if p_over_2 == 1:
                    agent.infected = True
                    self.model.infected_agents.append(agent)

def new_infect(self):
    if self.exposed != 0:   #Agent smitter ikke endnu.
        return
    if (self.is_home_sick == 1) or (isinstance(self,canteen_Agent) and self.off_school == 1): #Agenten er derhjemme og kan ikke smitte
        return

    if isinstance(self, TA):
        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=True,radius=2)
    else:
        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False,radius=2)

    all_humans_within_radius = []
    for neighbor in all_neighbors_within_radius:
            #Dont infect neighbors that are home sick / not on campus
        if neighbor.is_home_sick == True or (isinstance(neighbor,canteen_Agent) and neighbor.off_school == True):
            continue
            #Dont infect neighbors that are vaccinated, recorvered or infected
        if neighbor.vaccinated == True or neighbor.recovered == True or neighbor.infected == True: # kan ikke blive smittet, da den er immun eller allerede infected
            continue
        if not self.model.grid.is_cell_empty(neighbor.pos):
            if is_human(neighbor):
                all_humans_within_radius.append(neighbor)
            """"HVIS UNDER EN METER VÆK, GÅ IKKE VIDERE"""
    neighbor_in_front = []
    neighbor_behind = []
    neighbor_aligned = []
    if self.coords == dir['N']:
        for agent in all_humans_within_radius:
            if agent.pos[1] > self.pos[1]:
                neighbor_in_front.append(agent)
            elif agent.pos[1] == self.pos[1]:
                neighbor_aligned.append(agent)
            else:
                neighbor_behind.append(agent)
    if self.coords == dir['NE']:
        for agent in all_humans_within_radius:
            if agent.pos in [(self.pos[0]+i,self.pos[1]-i) for i in range(-2,3)]:
                neighbor_aligned.append(agent)
            elif (agent.pos[0] >= self.pos[0] and agent.pos[1] >= self.pos[1]) or agent.pos in [(self.pos[0]+2, self.pos[1]-1), (self.pos[0]-1, self.pos[1]+2)]:
                neighbor_in_front.append(agent)
            else:
                neighbor_behind.append(agent)

    if self.coords == dir['E']:
        for agent in all_humans_within_radius:
            if agent.pos[0] > self.pos[0]:
                neighbor_in_front.append(agent)
            elif agent.pos[0] == self.pos[0]:
                neighbor_aligned.append(agent)
            else:
                neighbor_behind.append(agent)
    if self.coords == dir['SE']:
        for agent in all_humans_within_radius:
            if agent.pos in [(self.pos[0]+i,self.pos[1]+i) for i in range(-2,3)]:
                neighbor_aligned.append(agent)
            elif (agent.pos[0]>= self.pos[0] and agent.pos[1]<=self.pos[1]) or agent.pos in [(self.pos[0]-1,self.pos[1]-2), (self.pos[0]+2, self.pos[1]+1)]:
                neighbor_in_front.append(agent)
            else:
                neighbor_behind.append(agent)
    if self.coords == dir['S']:
        for agent in all_humans_within_radius:
            if agent.pos[1] < self.pos[1]:
                neighbor_in_front.append(agent)
            elif agent.pos[1] == self.pos[1]:
                neighbor_aligned.append(agent)
            else:
                neighbor_behind.append(agent)
    if self.coords == dir['SW']:
        for agent in all_humans_within_radius:
            if agent.pos in [(self.pos[0]+i,self.pos[1]-i) for i in range(-2,3)]:
                neighbor_aligned.append(agent)
            elif (agent.pos[0] >= self.pos[0] and agent.pos[1] >= self.pos[1]) or agent.pos in [(self.pos[0]+2, self.pos[1]-1), (self.pos[0]-1, self.pos[1]+2)]:
                neighbor_behind.append(agent)
            else:
                neighbor_in_front.append(agent)
    if self.coords == dir['W']:
        for agent in all_humans_within_radius:
            if agent.pos[0] < self.pos[0]:
                neighbor_in_front.append(agent)
            elif agent.pos[0] == self.pos[0]:
                neighbor_aligned.append(agent)
            else:
                neighbor_behind.append(agent)
    if self.coords == dir['NW']:
        for agent in all_humans_within_radius:
            if agent.pos in [(self.pos[0]+i,self.pos[1]+i) for i in range(-2,3)]:
                neighbor_aligned.append(agent)
            elif (agent.pos[0]>= self.pos[0] and agent.pos[1]<=self.pos[1]) or agent.pos in [(self.pos[0]-1,self.pos[1]-2), (self.pos[0]+2, self.pos[1]+1)]:
                neighbor_behind.append(agent)
            else:
                neighbor_in_front.append(agent)

###CHANGING OBJECT-TYPE###
#Get all essential parameters transfered
def change_obj_params(new,old):

    new.is_home_sick, new.vaccinated = old.is_home_sick,\
                                       old.vaccinated

    new.infection_period,new.exposed, new.asymptomatic = old.infection_period,\
                                                         old.exposed,\
                                                         old.asymptomatic

    new.infected, new.recovered,  new.mask = old.infected,\
                                             old.recovered,\
                                             old.mask
    new.day_off = old.day_off
    new.pos = old.pos

###CHANGING OBJECT-TYPE###

#Turn canteen-object to class-object
def canteen_to_class(self):
    c_agent = class_Agent(self.id, self.model)
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
        if self in students and self.is_home_sick == False:
            students.remove(self)
        self.TA.students = students

    self.model.schedule.remove(self)
    self.model.grid.remove_agent(self)
    self.model.schedule.add(c_agent)

    return c_agent

#Turn TA-object to class-object
def TA_to_class(self):
    c_agent = class_Agent(self.id, self.model)
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
    c_agent.coords = dir['E']

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

def move_in_queue(self, pos_):
    if self.buying_lunch != 0:
        self.buying_lunch -= 1
        if self.buying_lunch == 0:
            self.coords = dir['N']
    else:
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        possible_empty_steps = [cell for cell in possible_steps if self.model.grid.is_cell_empty(cell)]
        if possible_empty_steps == []: #if someone in front of you - dont move
            return
        distances = [(pos,getDistance(pos_,pos)) for pos in possible_empty_steps]
        x_,y_ = min(distances,key=lambda x:x[1])[0]
        if min(getDistance((x_,y_), pos_), getDistance(self.pos, pos_)) == getDistance(self.pos, pos_):
            return
        else:
            self.model.grid.move_agent(self,(x_,y_))
            if self.pos == (23,17):
                self.buying_lunch = 3
                self.coords = dir['E']

def move_to_specific_pos(self,pos_):
    if self.id in [1001,1002,1003,1004,1005,1006]:
        if isinstance(self,canteen_Agent):
            newAgent = canteen_to_TA(self)
            #"push" agent through door
            x,y = pos_                      #Door position
            newY = random.randint(-1, 1)
            newAgent.pos = x-1,y+newY
            newAgent.coords = dir['W']
            newAgent.mask = with_mask  #From Model
            self.model.grid.place_agent(newAgent, newAgent.pos)
            return


    possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    possible_empty_steps = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos) or is_invisible(get_agent_at_cell(self,pos))]

    #If no cell is empty, agent can go through others "person"-agents (to avoid bottleneck)
    #Back-up list contains cells with covid,TA and canteen agents in
    pos_other_agents = [cell for cell in self.model.grid.get_neighbors(self.pos,moore=True,include_center=False)
                        if is_human(cell)]
    back_up_empty_cells = [cell.pos for cell in pos_other_agents]

    #If goal-position is in possible steps, go there
    if pos_ in possible_steps:
        #If goal-position is a door change object accordingly
        if pos_ == self.door.pos:
            if isinstance(self, class_Agent):
                newAgent = class_to_canteen(self)
                #"push" agent through door
                x,y = pos_                         #Door position
                newY = random.randint(-1, 1)
                newAgent.pos = x+1,y+newY
                newAgent.coords = dir['E']
                self.model.grid.place_agent(newAgent, newAgent.pos)
                return
            elif isinstance(self,canteen_Agent):
                    newAgent,seat_ = canteen_to_class(self)
                    #"push" agent through door
                    x,y = pos_                      #Door position
                    newY = random.randint(-1, 1)
                    newAgent.pos = x-1,y+newY
                    newAgent.seat = seat_
                    newAgent.coords = dir['W']
                    self.model.grid.place_agent(newAgent, newAgent.pos)
                    return
        #If goal-position is the seat, go there
        if isinstance(self, class_Agent) and pos_ == self.seat:
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

    #to prevent logic-flaw when student cannot get to seat
    #???? if student isnt making it to class in time ???
    if self.model.minute_count in [40,160,340,470]:
        x,y = pos_
        force_agent_to_specific_pos(self,(x+1,y))
        return
    self.model.grid.move_agent(self,(x_,y_))

def force_agent_to_specific_pos(self,pos):
    self.model.grid.move_agent(self,pos)

def send_agent_home(self):
    self.is_home_sick = True
    self.model.agents_at_home.append(self)
    if isinstance(self, employee_Agent):
        call_backup_employee(self)
        if self in self.model.canteen_agents_at_work:
            self.model.canteen_agents_at_work.remove(self)

def send_agent_back_to_school(self):
    newList_at_home = [a for a in self.model.agents_at_home if a.id != self.id]
    self.model.agents_at_home = newList_at_home

    self.model.recovered_agents.append(self)
    self.is_home_sick = False
    self.infected = False
    self.recovered = True
    if isinstance(self, employee_Agent) and (self.id==1250 or self.id==1251):
        self.model.canteen_agents_at_work.append(self)

def update_infection_parameters(self):
    if self.is_home_sick == True: #Agent is already home. Just update infection period
        self.infection_period = max(0,self.infection_period-1)
        if self.infection_period == 0:
            send_agent_back_to_school(self)
        return
    if self.recovered == True:
        return              #Agent is recovered

    self.asymptomatic = max(0,self.asymptomatic-1)
    if self.asymptomatic == 0:
        send_agent_home(self)
    self.exposed = max(0,self.exposed-1)    #If already 0 stay there, if larger than 0 subtract one
    self.infection_period = max(0,self.infection_period-1)

def call_backup_employee(self):
    newLunchlady = employee_Agent(self.id+2,self.model)
    newLunchlady.coords = dir['W']
    self.model.schedule.add(newLunchlady)
    self.model.grid.place_agent(newLunchlady, self.pos)

class class_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id
        self.model = model
        self.coords = ()

        self.infected = False
        self.recovered = False
        self.mask = False
        self.is_home_sick = False
        self.vaccinated = False

          #Infection parameters
        self.infection_period = max(5*day_length,abs(round(np.random.normal(9*day_length,1*day_length))))#How long are they sick?
        self.asymptomatic = min(max(3*day_length,abs(round(np.random.normal(5*day_length,1*day_length)))),self.infection_period) #Agents are asymptomatic for 5 days
        self.exposed = self.asymptomatic-2*day_length

        self.day_off = False
        self.moving_to_door = 0
        self.door = ()
        self.courses = [0,0]


        self.TA = ()
        self.seat = ()

        #Relevant for classroom only
        self.hasQuestion = False
        self.hasEnteredDoor = []

    def move(self,timestep=False):
        start_pos = self.pos
        if timestep is True:
            if self.moving_to_door == 1: #Agents go to door
                move_to_specific_pos(self,self.door.pos)
         #       move_to_specific_pos(self,self.door.pos)
            elif self.moving_to_door == 0: #Agents go to seat
                move_to_specific_pos(self,self.seat)
               # move_to_specific_pos(self,self.seat)
        else: wander(self)
        end_pos = self.pos
        self.coords = change_direction(self, start_pos, end_pos)

    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):
        if is_invisible(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,2)])
        if self.infected == True:
            #Try to infect
            infect(self)
            update_infection_parameters(self)
        #if self.is_home_sick == 1:
         #   update_infection_parameters(self)

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
        self.infected = False
        self.recovered = False
        self.mask = False
        self.is_home_sick = False
        self.vaccinated = False

        self.time_remaining = 105

          #Infection parameters
        self.infection_period = max(5*day_length,abs(round(np.random.normal(9*day_length,1*day_length))))#How long are they sick?
        self.asymptomatic = min(max(3*day_length,abs(round(np.random.normal(5*day_length,1*day_length)))),self.infection_period) #Agents are asymptomatic for 5 days
        self.exposed = self.asymptomatic-2*day_length

        self.day_off = False
        self.timeToTeach = 5
        self.courses = ()
        self.door = ()
        self.students = []
        self.coords = ()


    def move_to_student(self,student):

        x,y = student.pos
        if self.timeToTeach == 0:           #Student has recieved help for 5 minutes
            student.hasQuestion = False            #Student does not have question anymore
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
        ss = [a for a in self.model.schedule.agents if isinstance(a, class_Agent) and a.door == self.door]

        #Get the correct students, because they can overlap when a class is ending and new one is starting
        if self.id in [1001,1002,1003]:
            self.students = [a for a in ss if a.id in range(0,(self.model.n_agents+1)*3) and a.is_home_sick == False]
        elif self.id in [1004,1005,1006]:
            self.students = [a for a in ss if a.id not in range(0,(self.model.n_agents+1)*3) and a.is_home_sick == False]

        #Apply TA to students
        for s in self.students:
            s.TA = self

    def move(self):
        question_count = count_students_who_has_question(self.model, self.students)

        if question_count > 0 and len(self.students) > 15:  #Class is started and somebody a question
            for s in self.students:
                if s.hasQuestion == True:
                    self.move_to_student(s)
                    self.coords = s.coords
        else:
            wander(self)
            start_pos = self.pos
            wander(self)
            end_pos = self.pos
            self.coords = change_direction(self, start_pos, end_pos)

    def step(self):
        if is_invisible(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,2)])
        self.time_remaining -=1
        self.connect_TA_and_students()

        if self.infected == True:
            infect(self)
            update_infection_parameters(self)
        if self.time_remaining <= 0 and len(self.students)<5:
            TA_to_class(self)
            return

        self.move()

class canteen_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        #Person parameters
        self.id = id
        self.infected = False
        self.recovered = False
        self.mask = False
        self.is_home_sick = False
        self.vaccinated = False
        self.queue = 0
        self.buying_lunch = 0
        self.sitting_in_canteen = 0

        self.off_school = 0
        self.coords = ()

        #Infection parameters
        self.infection_period = max(5*day_length,abs(round(np.random.normal(9*day_length,1*day_length))))#How long are they sick?
        self.asymptomatic = min(max(3*day_length,abs(round(np.random.normal(5*day_length,1*day_length)))),self.infection_period) #Agents are asymptomatic for 5 days
        self.exposed = self.asymptomatic-2*day_length

        #Class-schedule parameters
        self.next_to_attend_class = False
        self.day_off = False
        self.door = ()
        self.courses = ()
        self.moving_to_door = 0
        self.TA = ()


    def move(self,timestep=False):
        if timestep is True: #Agents go to door
            if self.queue == 0 and self.sitting_in_canteen == 0:
                move_to_specific_pos(self,self.door.pos)
            else:
                self.queue = 0
                self.sitting_in_canteen = 0
                force_agent_to_specific_pos(self, (23,21))
                move_to_specific_pos(self,self.door.pos)

        elif self.queue == 1:
            move_in_queue(self, (23,20)) # moves towards end of canteen
        elif self.sitting_in_canteen != 0:
            self.sitting_in_canteen = max(0, self.sitting_in_canteen -1)
        else: wander(self)


    def step(self):
        if is_invisible(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,2)])

        start_pos = self.pos #for changing direction
        if self.infected == True:
            infect(self)
            update_infection_parameters(self)
        if self.pos in [(22,3),(23,3),(24,3)]: #in beginning of queue area
            if self.off_school ==0 and self.is_home_sick ==0:
                self.queue =1 #stands in line for canteen
        if self.pos in [(23,j) for j in range(4,19)]:
            self.queue=1
        if self.pos == (23,20):
            self.queue = 0 #done in line
            #When should canteen agent go to door?
        if self.model.day_count == 1:
            if self.model.minute_count in self.model.class_times and self.model.minute_count % 2 == 0 and self.next_to_attend_class is True:
                self.moving_to_door = 1
        elif (self.model.minute_count == 0 or (self.model.minute_count in self.model.class_times+[2] and self.model.minute_count%2 == 0))\
                and self.next_to_attend_class is True:
            self.moving_to_door = 1
        if self.moving_to_door == 1:
            self.move(True)
        else:
            self.move()
        end_pos = self.pos
        self.coords = change_direction(self, start_pos, end_pos)

class employee_Agent(Agent):
    def __init__(self,id,model):
        super().__init__(id,model)
        self.id = id
        self.infected = False
        self.recovered = False
        self.mask = True
        self.is_home_sick = False
        self.vaccinated = False

        self.infection_period = max(5*day_length,abs(round(np.random.normal(9*day_length,1*day_length))))#How long are they sick?
        self.asymptomatic = min(max(3*day_length,abs(round(np.random.normal(5*day_length,1*day_length)))),self.infection_period) #Agents are asymptomatic for 5 days
        self.exposed = self.asymptomatic-2*day_length

        self.coords = ()

    def step(self):
        if is_invisible(self):
            return
        if self.infected == True:
            infect(self)
            update_infection_parameters(self)


        if self.id %2 == 0:
            self.move()
        if self.id > 1251 and len(self.model.canteen_agents_at_work)==2: #if both other employees is at work
            self.model.canteen_backups_to_go_home.append(self)



    def move(self):
        start_pos = self.pos
        wander(self)
        end_pos = self.pos
        self.coords = change_direction(self, start_pos, end_pos)

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

class desk(Agent):
    """" Desk is for the canteen. Get's ID"""
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        self.id = id
        self.pos=pos

class table(Agent):
    def __init__(self,id, model):
        super().__init__(id,model)
        self.id = id
        self.model = model

