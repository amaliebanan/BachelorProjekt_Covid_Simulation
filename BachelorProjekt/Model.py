import AgentClass as ac
from mesa.time import SimultaneousActivation,RandomActivation
from mesa.space import MultiGrid
import random
from itertools import chain
import copy
from operator import itemgetter
import math
import numpy
from mesa import Agent, Model

import numpy as np
from mesa.datacollection import DataCollector
from scipy.stats import truncnorm,bernoulli

def truncnorm_(lower,upper,mu,sigma):
    return int(truncnorm.rvs((lower - mu) /sigma, (upper - mu) /sigma, loc = mu, scale=sigma))

def calculate_percentage(original_number, percent_to_subtract):
    return original_number-(percent_to_subtract*original_number/100)
def intersect(list1,list2):
    list3 = [v for v in list1 if v in list2]
    return list3

day_length = 525
init_positive_agents = 1
new_positives_after_weekends = 2
init_canteen_agents = 80
infection_rate = (0.035/100)
infection_rate_1_to_2_meter = calculate_percentage(infection_rate, 10.2)
infection_rate_2plus_meter = calculate_percentage(infection_rate_1_to_2_meter,2.02)
infection_decrease_with_mask_pct = 60


go_home_in_breaks = False
family_groups = False
with_mask = False
with_dir = True
percentages_of_vaccinated = 0 #Number 0<=x<1
number_of_vaccinated = math.floor(percentages_of_vaccinated*(init_canteen_agents+3*25+2))

dir = {'N':(0,1), 'S':(0,-1), 'E':(1,0), 'W':(-1,0),'NE': (1,1), 'NW': (-1,1), 'SE':(1,-1), 'SW':(-1,-1)}
listOfSetup = []

def get_toilet_inf_count(self):
    agents = [a.counter for a in self.schedule.agents if isinstance(a,ac.toilet)]
    return sum(agents)

def get_canteen_table_inf_count(self):
    return self.canteen_counter

def get_infected_count(self):
    '''
    Retrieves the number of infectied agents

    :param self: model-object
    :return: int
    '''
    agents = [a for a in self.schedule.agents if is_human(a) and a.infected == True]
    return len(agents)

def get_asymptom_count(self):
    '''
    Retrieves the number of asymptomatic agents

    :param self: model-object
    :return: int
    '''
    agents = [a for a in self.schedule.agents if is_human(a) and a.asymptomatic == True]
    return len(agents)

def get_vaccinated_count(self):
    '''
    Retrieves the number of vaccinated agents

    :param self: model-object
    :return: int
    '''
    agents = [a for a in self.schedule.agents if is_human(a) and a.vaccinated == True]
    return len(agents)

def get_susceptible_count(self):
    '''
    Retrieves the number of susceptible agents

    :param self: model-object
    :return: int
    '''
    susceptibles = [a for a in self.schedule.agents if is_human(a) and a.infected == False and a.recovered == False and a.vaccinated == False]
    return susceptibles

def get_recovered_count(self):
    '''
    Retrieves the number of recovered agents

    :param self: model-object
    :return: int
    '''
    agents = [a for a in self.schedule.agents if is_human(a) and a.recovered == True]
    return len(agents)

def get_home_sick_count(self):
    '''
    Retrieves the number of agents who are home sick because of symptoms

    :param self: model-object
    :return: int
    '''
    agents = [a for a in self.schedule.agents if is_human(a) and a.is_home_sick == True]
    return len(agents)

"KAN EVT SLETTES?"
def get_list_of_reproduction(self):
    '''
    Retrieves the number of asymptomatic agents

    :param self: model-object
    :return: int
    '''
    list_of_reproduction = []
    agents = [a for a in self.schedule.agents if is_human(a)]
    for a in agents:
        if (a.infected == True or a.recovered == True) and a.non_contageous_period == 0:
            list_of_reproduction.append(a.reproduction)
    return list_of_reproduction

def students_who_has_question_count(self, list_of_students):
    '''
    Retrieves the number of students who has question in a specific list

    :param self: model-object
    :param list_of_students: list [] of agent-objects
    :return: int
    '''
    agents = [a for a in self.schedule.agents if a in list_of_students and a.has_question == True]
    return len(agents)

def is_human(agent_to_check):
    '''
    Decides if input agent is a human (class, canteen, TA, employee) or not (wall, door, desk)

    :param self: agent-object
    :return: bool
    '''
    if isinstance(agent_to_check, ac.class_Agent) or isinstance(agent_to_check, ac.TA) or isinstance(agent_to_check, ac.canteen_Agent) or isinstance(agent_to_check, ac.employee_Agent):
        return True
    else:
        return False

def is_student(agent_to_check):
     '''
     Decides if input agent is a student (class, canteen, TA) or not (employee, wall, door, desk)

     :param self: agent-object
     :return: bool
     '''
     if isinstance(agent_to_check, ac.class_Agent) or isinstance(agent_to_check, ac.TA) or isinstance(agent_to_check, ac.canteen_Agent):
        return True
     else:
        return False

def is_off_campus(agent_to_check):
    '''
    Decides if input agent is off campus

    :param self: agent-object
    :return: bool
    '''
    if is_student(agent_to_check) and agent_to_check.day_off == True:
        return True
    elif isinstance(agent_to_check, ac.canteen_Agent) and agent_to_check.off_school == True:
        return True
    else:
        return False

def set_off_school(self):
    '''
    Change agents' off_school parameter (depeding on the time of day)

    :param self: model-object
    :return: None
    '''
    if go_home_in_breaks == True:
        if self.minute_count in [295,524]:
            off_school_students = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and (a.id < len(self.setUpType)*self.n_agents or a.id in [1001,1002,1003]) and a.off_school == True and a.is_home_sick == False and a.day_off == False]
            for a in off_school_students:
                a.off_school = False
        if self.minute_count in [110,415]:
            off_school_students = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and (len(self.setUpType)*2*self.n_agents > a.id >= len(self.setUpType)*self.n_agents or a.id in [1004,1005,1006]) and a.off_school == True and a.is_home_sick == False and a.day_off == False]
            for a in off_school_students:
                a.off_school = False

    elif go_home_in_breaks == False:
        if self.minute_count in [1]:
            off_school_students = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and (a.id < 3*self.n_agents or a.id in [1001,1002,1003]) and a.off_school == True and a.is_home_sick == False and a.day_off == False]
            for a in off_school_students:
                a.has_more_courses_today = True
                a.off_school = False
        if self.minute_count in [110]:
            off_school_students = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and (6*self.n_agents > a.id >= 3*self.n_agents or a.id in [1004,1005,1006]) and a.off_school == True and a.is_home_sick == False and a.day_off == False]
            for a in off_school_students:
                a.has_more_courses_today = True
                a.off_school = False

def set_day_off(self):
    '''
    Change agents' day_off parameter (depeding on the day of the week)

    :param self: model-object
    :return: None
    '''

    if self.day_count%7==2: #Squad A has day off
        off_school_students = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and (a.id < 3*self.n_agents or a.id in [1001,1002,1003]) and a.day_off == False]
        for a in off_school_students:
                a.day_off = True
    elif self.day_count%7==3: #Squad A has day off
        off_school_students = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and (a.id < 3*self.n_agents or a.id in [1001,1002,1003]) and a.day_off == True]
        for a in off_school_students:
                a.day_off = False
    elif self.day_count%7 == 4: #Squad B has day off
        off_school_students = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and (6*self.n_agents > a.id >= 3*self.n_agents or a.id in [1004,1005,1006]) and a.day_off == False]
        for a in off_school_students:
            a.day_off = True
    elif self.day_count%7 == 5: #Squad B returning to campus
        off_school_students = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and (6*self.n_agents > a.id >= 3*self.n_agents or a.id in [1004,1005,1006]) and a.day_off == True]
        for a in off_school_students:
            a.day_off = False

def all_agents_count(self):
    '''
    Retrieves the total number of agents

    :param self: model-object
    :return: int
    '''
    agents = [a for a in self.schedule.agents if is_human(a)]
    return len(agents)

def add_init_infected(self, n):
    '''
    Add initial infected

    :param self: model-object
    :param n: int - number of initial infected agents
    :return: None
    '''
    i = 0
    positives = []
    while i<n:
        all_agents = [a for a in self.schedule.agents if is_human(a) and a.id in [x for x in range(3*24,3*24*3-1)] or a.id in [1004,1005,1006]]
     #   students = [a for a in self.schedule.agents if isinstance(a,ac.class_Agent)]
      #  TA = [a for a in self.schedule.agents if isinstance(a,ac.TA)]
        #canteen = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and a.off_school == False]
        employee = [a for a in self.schedule.agents if isinstance(a,ac.employee_Agent)]
        randomAgent = self.random.choice(all_agents)
        if randomAgent.pos in positives: #Dont pick the same agent as before
            pass
        elif is_human(randomAgent):
            self.schedule.remove(randomAgent)
            positive_agent = randomAgent
            positive_agent.infected = True
            print(positive_agent.id)

           # positive_agent.asymptomatic = True
           # positive_agent.infection_period = truncnorm_(5 * day_length, 21*day_length, 10*day_length, 2*day_length) - 2* day_length #How long are they sick?
           # positive_agent.incubation_period = positive_agent.infection_period
           # positive_agent.non_contageous_period = 0
            positive_agent.non_contageous_period = 0
            positive_agent.incubation_period = 2*day_length
            positive_agent.infection_period = positive_agent.incubation_period+10*day_length

            self.schedule.add(positive_agent)
            positives.append(randomAgent.pos) # To keep track of initial positives
            self.infected_agents.append(positive_agent)
            i+=1
        else: pass

"ÆNDRE NAVN PÅ DENNE FUNK"
def add_init_canteen_agents(self, N, n):
    '''
    Add agents to both (visual) grid og (logical) schedule

    :param self: model-object
    :param N: int - number of agents to initialise that will attend classes
    :param n: int - number of agents to initialise in total
    :return: None
    '''
    id_ = N #The next ID in line
    limit = N #We start by initializing N many canteen-agents. These are the agents that will be attending courses.
    counter = 0
    while limit > counter:
            newAgent = ac.canteen_Agent(id_,self)
            self.schedule.add(newAgent) #Add agent to scheduler
            newAgent.coords = random.choice(list(dir.values()))   #Give agent random direction to look at
            newAgent.courses = [self.range13.pop(),self.range46.pop()] #Add agent to two courses
            next_door_id = 500+newAgent.courses[0]  #Which door should agent go to when class starts - depending on course
            next_door = [a for a in self.schedule.agents if isinstance(a,ac.door) and a.id == next_door_id]
            newAgent.door = next_door[0]
            newAgent.off_school = True
            newAgent.next_to_attend_class = True
            pos = self.entre[random.randint(0,len(self.entre)-1)]
            self.grid.place_agent(newAgent, pos)

            if with_mask == True:
                newAgent.mask = True

            id_+=1
            counter+=1
    #We want to create 3 TAs that start in the canteen
    j=4
    for i in range(0,3):
        newAgent = ac.canteen_Agent(1000+j+i,self)
        self.schedule.add(newAgent) #Add agent to scheduler
        newAgent.off_school = True
        newAgent.coords = random.choice(list(dir.values()))   #Give agent random direction to look at
        next_door_id = newAgent.id-503 #Which door should agent go to when class starts - depending on course
        next_door = [a for a in self.schedule.agents if isinstance(a,ac.door) and a.id == next_door_id]
        newAgent.next_to_attend_class = True
        newAgent.door = next_door[0]
        pos = self.entre[random.randint(0,len(self.entre)-1)]
        self.grid.place_agent(newAgent, pos)

        if with_mask == True:
            newAgent.mask = True


    #We still need to initialize more canteen-agents, but these will not attend classes (fx students writing their master thesis)
    #They are initialized without door, courses, etc. They are "dummy" agents
    m = n-limit-3
    if n-3>limit:
        if go_home_in_breaks:
            return
        for i in range(0,m):
            newAgent = ac.canteen_Agent(id_,self)
            self.schedule.add(newAgent) #Add agent to scheduler
            newAgent.coords = random.choice(list(dir.values()))
            if with_mask == True:
                newAgent.mask = True
            x, y = self.grid.find_empty()#Place agent randomly in empty cell on grid
            while (x,y) in (self.classroom_area+self.canteen_queue_area+self.canteen_tables+self.toilet_queue_area):
                 x, y = self.grid.find_empty()

            self.grid.place_agent(newAgent, (x,y))
            id_+=1

def add_init_employee(self):
    '''
    Add employees in the canteen

    :param self: model-object
    :return: None
    '''
    cashier = ac.employee_Agent(1251, self)
    lunchlady = ac.employee_Agent(1250, self)
    self.schedule.add(lunchlady) #Add agent to scheduler
    self.schedule.add(cashier)
    lunchlady.coords = dir['W'] #looks west
    cashier.coords = dir['W']
    if with_mask == True:
        cashier.mask = True
        lunchlady.mask = True
    x1, y1 = (25,17)
    x2, y2 = random.choice([(25,j) for j in range(5,17)])
    self.grid.place_agent(cashier, (x1,y1))
    self.grid.place_agent(lunchlady,(x2,y2))
    self.canteen_agents_at_work.append(cashier)
    self.canteen_agents_at_work.append(lunchlady)

def set_up_classroom(self, N, setUpType, i):
    '''
    Set up a classroom with table setting specified in setUpType with N many agents and one TA.

    :param self: model-object
    :param N: int - number of agents to initialise in the classroom
    :param setUpType: int - the table setting (2,3 or 4 indicating horseshoe, rows or groups)
    :param i: int - the number this specific classroom in the grid (0,1 or 2) - indicating the position on the grid
    :return: None
    '''
    listOfPositions = []
    if setUpType == 2: #Horseshoe
        if self.n_agents<24:
            list = [((x,y+i*11),z) for ((x,y),(z)) in self.classroom_2]
            list_ = random.sample(list,k=len(list))
        else:
            list_ = [((x,y+i*11),z) for ((x,y),(z)) in self.classroom_2]
        listOfPositions = list_
    elif setUpType == 3: #Rows
        if self.n_agents<24:
            list = [((x,y+i*11),z) for ((x,y),(z)) in self.classroom_3]
            list_ = random.sample(list,k=len(list))
        else:
            list_ = [((x,y+i*11),z) for ((x,y),(z)) in self.classroom_3]

        listOfPositions = list_
    elif setUpType == 4: #Group (4-people) tables with correct direction added
        if self.n_agents<24:
            list = [((x,y+i*11),z) for ((x,y),(z)) in self.classroom_4]
            list_ = random.sample(list,k=len(list))
        else:
            list_ = [((x,y+i*11),z) for ((x,y),(z)) in self.classroom_4]

        listOfPositions = list_

    #Add door(s) to model and grid
    door = ac.door(501 + i, self)
    self.door = door
    self.schedule.add(door)
    self.grid.place_agent(door, (8, 5 + i * 11))


    students = []
    # Add TA
    x,y = random.choice([(7,5+i*11),(7,4+i*11)])
    TA = ac.TA(1001 + i, self)
    TA.coords = dir['W']
    TA.door = door
    if with_mask == True:
        TA.mask = True
    self.schedule.add(TA)
    self.grid.place_agent(TA, (x, y))
    self.TAs.append(TA)



    for j in range(N*i,(i+1)*N):
        newAgent = ac.class_Agent(j, self)
        self.schedule.add(newAgent)
        posAndDirection = listOfPositions.pop()
        x,y = posAndDirection[0]
        newAgent.coords = posAndDirection[1]
        other_course = self.other_courses.pop()
        newAgent.courses = [i+1,other_course]
        newAgent.door = door
        self.grid.place_agent(newAgent, (x, y))
        newAgent.TA = TA
        newAgent.seat = (x,y)
        students.append(newAgent)
    TA.students = students

    #Place walls
    wall_placements_vertical = [(8,j+i*11) for j in range(0,11)]
    wall_placements_horizontal = [(j,10+i*11) for j in range(0,8)]
    wall_placements_v_id = [k for k in range(7000+len(wall_placements_vertical)*i,7000+(i+1)*len(wall_placements_vertical))]
    wall_placements_h_id = [k for k in range(6000+len(wall_placements_horizontal)*i,6000+(i+1)*len(wall_placements_horizontal))]
    for j in range(len(wall_placements_vertical)):
        newBrick = ac.wall(wall_placements_v_id[j], self)
        newBrick.orientation = 'v'
        self.schedule.add(newBrick)
        self.grid.place_agent(newBrick, wall_placements_vertical[j])
    for j in range(len(wall_placements_horizontal)):
        newWall = ac.wall(wall_placements_h_id[j], self)
        newWall.orientation = 'h'
        self.schedule.add(newWall)
        self.grid.place_agent(newWall, wall_placements_horizontal[j])

def set_up_canteen(self):
    '''
    Set up walls, door and desk in canteen area

    :param self: model-object
    :return: None
    '''

    wall_placements_canteen_v = [(22,j) for j in range(4,20)]+[(24,j) for j in range(4,17)]+[(24,18), (24,19)]
    wall_placements_canteen_h = [(25,4), (25,19)]
    ids_h = [i for i in range(10000,10002)]
    ids_v = [i for i in range(10002,10002+len(wall_placements_canteen_v))]
    for pos_ in wall_placements_canteen_v:
        newBrick = ac.wall(ids_v.pop(), self)
        newBrick.orientation = 'v'
        self.schedule.add(newBrick)
        self.grid.place_agent(newBrick, pos_)
    for pos_ in wall_placements_canteen_h:
        newWall = ac.wall(ids_h.pop(),self)
        newWall.orientation = 'h'
        self.schedule.add(newWall)
        self.grid.place_agent(newWall,pos_)

    #Place desk
    desk = ac.desk(1234, self)
    self.schedule.add(desk)
    self.grid.place_agent(desk,(24,17))

    add_init_employee(self)

    table_pos = [x for (x,y) in self.canteen_table_1]+[x for (x,y) in self.canteen_table_2]
    counter = 0
    for pos in table_pos:
        newTable = ac.table(8000+counter,self)
        self.schedule.add(newTable)
        self.grid.place_agent(newTable, pos)
        counter += 1

def set_up_toilet(self):
     '''
     Set up toilet in canteen-area

     :param self: model-object
     :return: None
     '''
     id_max = max([w.id for w in self.schedule.agents if isinstance(w,ac.wall)])
     ids_ = [i for i in range(id_max+1,id_max+1+self.height-33)]
     positions = [(8,i) for i in range(33,self.height)]

     for i in range(len(ids_)):
        pos =  positions.pop()
        if pos == (8,37):
            newToilet = ac.toilet(ids_[i], self)
            self.schedule.add(newToilet)
            self.grid.place_agent(newToilet, pos)
        else:
            newBrick = ac.wall(ids_[i], self)
            newBrick.orientation = 'v'
            self.schedule.add(newBrick)
            self.grid.place_agent(newBrick, pos)
     self.toilet = newToilet
     for x in range(9,14):
        id_max = max([w.id for w in self.schedule.agents if isinstance(w,ac.wall)])
        newBrick = ac.wall(id_max+1, self)
        newBrick.orientation = 'h'
        pos = (x,36)
        self.schedule.add(newBrick)
        self.grid.place_agent(newBrick, pos)

def set_canteen_agents_next_to_attend_class(self):
     '''
     Set agent's next_to_attend_class if they are in the canteen and are the next to go to class.
     :param self: model-object
     :return: None
     '''
     canteens_agents = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent)
                        and a.id not in [1001,1002,1003,1004,1005,1006]
                        and a.door is not ()] #Only get students who are attending class
     get_correct_TAs = list(set([a.TA.id for a in canteens_agents if a.TA is not ()])) #Get unique id of TAs-to-be. These will also get True in nexT_to_attend_class
     soon_to_be_TAs = [a for a in self.schedule.agents if a.id in get_correct_TAs]
     for agent in soon_to_be_TAs:
         canteens_agents.append(agent)

     going_to_class_next_agents = canteens_agents

     for agent in going_to_class_next_agents:
         if isinstance(agent,ac.canteen_Agent):
                agent.next_to_attend_class = not agent.next_to_attend_class

def make_classroom_seating(list_of_setuptypes, self):
    '''
    Make lists of seat-positions in corrected format depending on table-setting (horseshoe, row, or group)

    :param self: model-object
    :param list_of_setuptypes: list of int indicating table setting (horseshoe, row, or group)
    :return: List of lists
    '''
    seats = []

    for j in range(len(list_of_setuptypes)):
        number = str("classroom_") + str(list_of_setuptypes[j])    #Which type of class room are we constructing?
        classroom_ = [((x,y+j*11),z) for ((x,y),z) in getattr(self, number)]
        list_ = random.sample(classroom_,k=len(classroom_))
        seats.append(list_)
    return seats

def weekend(self):
    '''
    Handle weekends logically by subtracting 1050 (2 days) from incubation, infection and non_contageous periods. Send
    agents home, if they develop symptoms, and send agents back to school if they recover during the 2 days.

    Introduce #new_positives_after_weekends new infected if no one is vaccinated. Otherwise,
    take #new_positives_after_weekends randomly selected agents not infected right now and if not vaccinated, set infect=True

    :param self: model-object
    :return: None
    '''

    newly_infected = [a for a in self.schedule.agents if is_human(a) and a.infected == True]
    ids_to_remove = []
    for a in newly_infected:
        a.incubation_period = max(0, a.incubation_period - 2 * day_length)  #Træk 2 dage fra asymtom
        a.infection_period = max(0,a.infection_period-2*day_length) #Træk 2 dage fra infektionsperiode
        a.non_contageous_period = max(0, a.non_contageous_period - 2 * day_length) #Træk 2 dage fra non_contageous_period
        if a.is_home_sick == True: #Agenten er hjemme, skal den tilbage nu?
            if a.infection_period == 0:
                ac.send_agent_back_to_school(a) #Agenten er rask og skal tilbage i skole
                ids_to_remove.append(a.id)
                continue
        elif a.incubation_period == 0: #Agenten har symptomer nu og skal blive hjemme
            ac.send_agent_home(a)
            ids_to_remove.append(a.id)
            continue

    n = new_positives_after_weekends

    if self.day_count%2 == 1:
        return
    else:
        while n>0:
             if percentages_of_vaccinated == 0: #Get all susceptibles (not sick, not recovered)
                 agents_to_infect = get_susceptible_count(self)
             else: #Get all susceptibles (not sick, not recovered, not vaccinated)
                 agents_to_infect = [a for a in self.schedule.agents if is_human(a) and a.infected == False and a.recovered == False]
             if len(agents_to_infect)>0:
                a = self.random.choice(agents_to_infect)
                if a.vaccinated:
                    n-=1
                else:
                    a.infected = True
                    n-=1
                    if bernoulli.rvs(0.3)==1:
                        a.asymptomatic = True
                        a.infection_period = truncnorm_(5 * day_length, 21*day_length, 10*day_length, 2*day_length)#How long are they sick?
                        a.incubation_period = a.infection_period #Agents are asymptomatic for 5 days
                        a.non_contageous_period =  2 * day_length
                    else:
                        a.incubation_period = truncnorm_(3 * day_length, 11.5*day_length, 5*day_length, 1*day_length) #Agents are asymptomatic for 5 days
                        a.infection_period = a.incubation_period+10*day_length#How long are they sick?
                        a.non_contageous_period = a.incubation_period - 2 * day_length
             else:
                n-=1

def choose_agents_to_go_to_toilet(self):
    '''
    Depending on what time of the day it is, let poisson distribution determine how many randomly chosen agents have
    the need to use the toilet

    :param self: model-object
    :return: None
    '''
    if self.minute_count in intersect(self.breaks_for_ft,self.breaks_for_sf): #Everyone is on break
        poisson_ = np.random.poisson(1/4)
    else:
        poisson_ = np.random.poisson(1/8)
    counter=0
    while poisson_ > counter:
        agents = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) and a.going_to_toilet == False and a.in_toilet_queue == False and a.sitting_on_toilet == 0 and is_off_campus(a)==False and a.is_home_sick == False and a.sitting_in_canteen < 45 and a.queue == False and a.since_last_toilet == 0]
        try:
            randomStudent = self.random.choice(agents)
            randomStudent.going_to_toilet = 1
            counter+=1
        except: #No one in list
            break

def students_with_questions(self):
    '''
    If no one is recieving help, let a bernoulli distribution with mu = 1/5 decide if a new student has a question
    Set that student's has_question attribute to True

    :param self: model-object
    :return: None
    '''
    for ta in self.TAs:
        p = bernoulli.rvs(1/5)
        if len(ta.students) == 0 or p == 0:
            continue
        if len(ta.students)>10 and p == 1:
            questions_ = [a for a in ta.students if a.has_question == True]
            if len(questions_) == 0: #Only answer question if no one is recieving help at the moment
                TAs_students = [a for a in ta.students if a.is_home_sick == False]
                randomStudent = self.random.choice(TAs_students)
                randomStudent.has_question = True

def set_canteen_employees(self):
    '''
    When employee is recovered, send the back-up employee home

    :param self: model-object
    :return: None
    '''
    for agent in self.canteen_backups_to_go_home: #sending home spare employees
        if not agent.pos is None:
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
            self.canteen_backups_to_go_home.remove(agent)
        else:
            self.canteen_backups_to_go_home.remove(agent)

def vaccinate_agents(self):
    '''
    Vaccinate the % of the population specified in the model parameters.
    Setting the agent's attribute vaccinated = True.
    Can not happen to initial infected(s) agent(s).

    :param self: model-object
    :return: None
    '''
    n_agents_has_been_vaccinated = math.floor(all_agents_count(self) * percentages_of_vaccinated)
    n = 0
    agents = [a for a in self.schedule.agents if is_human(a)]
    while n_agents_has_been_vaccinated>n:
        vaccinate_agent = self.random.choice(agents)
        if vaccinate_agent.vaccinated == True or vaccinate_agent.infected == True:
            continue
        else:
            vaccinate_agent.vaccinated = True
            n+=1

def set_students_go_to_class_next(self):
    '''
    Calls the set_canteen_agents_next_to_attend_class-function in correct time steps if go_home_in_breaks is False.
    Sets the attribute directly if go_home_in_breaks is True.

    The timing depends on wether go_home_in_breaks is True or False.
    :param self: model-object
    :return: None
    '''
    if go_home_in_breaks == False:
        if self.day_count>1 and self.minute_count in [100,220,400,520]:
            set_canteen_agents_next_to_attend_class(self)
        elif self.minute_count in [220,400,520]:
            set_canteen_agents_next_to_attend_class(self)
    else:
        if self.minute_count in [100,400]:
            self.seats = make_classroom_seating(self.setUpType, self)
            for a in agents:
                a.next_to_attend_class = True
        if self.minute_count in [220,520]:
            self.seats = make_classroom_seating(self.setUpType, self)
            agents = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent) if (a.id < 3*24 or a.id in [1001,1002,1003]) and a.day_off == False and a.pos in self.entre]
            for a in agents:
                a.next_to_attend_class = True

def set_up_initial_attributes(self):
    '''
    Calls other functions.
    If go_home_in_breaks is False, set up canteen and toilet.
    Always set up classrooms.
    Add initial canteen agents and initial infected

    :param self: model-object
    :return: None
    '''
    if go_home_in_breaks == False:
            set_up_canteen(self)
    #Add agents to model and grid
    i = 0
    for s in self.setUpType:
        set_up_classroom(self, self.n_agents, s, i)
        i+=1
    if go_home_in_breaks == False:
        set_up_toilet(self)
    if len(self.setUpType)>1:
        add_init_canteen_agents(self, (self.n_agents) * i, init_canteen_agents)
    add_init_infected(self, init_positive_agents)

def create_courses(self):
    '''
    Depending on wether or not family_groups is True or False,
    set up courses. Family_groups dictacted that everyone has both courses with the same people.
    Otherwise, the courses are randomly distributed amongst the students.

    :param self: model-object
    :return: None
    '''
    if family_groups == False: #Shuffle courses
        self.other_courses = random.sample([4]*self.n_agents+[5]*self.n_agents+[6]*self.n_agents,
                                           k=len([4]*self.n_agents+[5]*self.n_agents+[6]*self.n_agents))

        self.range46 = random.sample([4]*self.n_agents+[5]*self.n_agents+[6]*self.n_agents,
                                 k=len([4]*self.n_agents+[5]*self.n_agents+[6]*self.n_agents))

        self.range13 = random.sample([1]*self.n_agents+[2]*self.n_agents+[3]*self.n_agents,
                                 k=len([1]*self.n_agents+[2]*self.n_agents+[3]*self.n_agents))
    elif family_groups == True: #Wihtout shuffle
        self.other_courses = [4]*self.n_agents+[5]*self.n_agents+[6]*self.n_agents
        self.range46 = [4]*self.n_agents+[5]*self.n_agents+[6]*self.n_agents
        self.range13 = [1]*self.n_agents+[2]*self.n_agents+[3]*self.n_agents

class covid_Model(Model):
    """
    Class representing Model. The Model is responsible for the logical structure of the ABM.
    Here, the model is set up both visually to the grid and logical to the algorithm

    The most important attributes are listed below.
    The rest is commented in the class below.
    ---------
    N : int
        Number of agents in grid in current timestep
    height : int
        height of grid
    width : int
        width of grid
    setUpType : List
        List of classroom types/construction (2,3,4/H,R,G)
    grid : grid
        Visual grid
    schedule : module
        Logical grid
    datacollector : module
        collects data that we want to analyze
    time_step : int
        Indicates current time step
    minute_count : int
        Counting minutes
    hour_count : int
        Counting hours
    day_count : int
        Counting days
    TAs : List
        List of TAs at the current time_step
    classroom_2 : List
        List of seat-positions with corrosponding direction in the H set up
    classroom_3 : List
        List of seat-positions with corrosponding direction in the R set up
    classroom_4 : List
        List of seat-positions with corrosponding direction in the G set up

    """
    def __init__(self, N, height, width,setUpType):
        self.n_agents = N
        self.height = height

        self.grid = MultiGrid(width, height, torus=False) #torus wraps edges
        self.schedule = SimultaneousActivation(self)
        self.setUpType = setUpType
        self.datacollector = DataCollector(model_reporters={"infected": lambda m: get_infected_count(self),
                                                            "Agent_count": lambda m: all_agents_count(self),
                                                            "recovered": lambda m: get_recovered_count(self),
                                                            "Home":lambda m: get_home_sick_count(self),
                                                            "Toilet":lambda m: get_toilet_inf_count(self),
                                                            "CanTables":lambda  m: get_canteen_table_inf_count(self)
                                                            #,"Reproduction": lambda m: get_list_of_reproduction(self)
                                                             })

        #Lists to hold agent-objects with with different states
        self.TAs = []
        self.agents_at_home = []
        self.recovered_agents = []
        self.infected_agents = []
        self.canteen_agents_at_work = []
        self.canteen_backups_to_go_home = []

        #Counting minutes and days
        self.minute_count = 1
        self.hour_count = 1
        self.day_count = 1
      #  self.door = ()

        self.entre = [(15,0),(16,0),(17,0),(25,34),(25,33),(25,32)]

        #Define time schedule + when breaks are
        self.class_times = [105,120,225,300,405,420,525]
        self.breaks_for_all = [i for i in range(105, 120)] + [i for i in range(225, 300)] + [i for i in range(405, 420)]
        self.breaks_for_ft = [i for i in range(105,300)]
        self.breaks_for_sf = [i for i in range(225,420)]


        self.other_courses, self.range46, self.range13 = [], [], []

        create_courses(self)


        #Define classrooms +  directions
        self.classroom_2 = [((0,0),dir['E']),((1,0),dir['N']),((2,0),dir['N']),((3,0),dir['N']),((4,0),dir['N']),
                           ((5,0),dir['N']),((6,0),dir['N']),((7,0),dir['N']),((0,1),dir['E']),((0,2),dir['E']),
                           ((0,3),dir['E']),((0,4),dir['E']),((0,5),dir['E']),((0,6),dir['E']),
                           ((0,7),dir['E']),((0,8),dir['E']),((0,9),dir['E']),((1,9),dir['S']),((2,9),dir['S']),
                           ((3,9),dir['S']),((4,9),dir['S']),((5,9),dir['S']),((6,9),dir['S']),((7,9),dir['S'])]
        self.classroom_3 = [((1,6),dir['E']),((1,7),dir['E']),((1,8),dir['E']),((1,9),dir['E']),
                           ((2,0),dir['E']),((2,1),dir['E']),((2,2),dir['E']),((2,3),dir['E']),
                           ((3,6),dir['E']),((3,7),dir['E']),((3,8),dir['E']),((3,9),dir['E']),
                           ((4,0),dir['E']),((4,1),dir['E']),((4,2),dir['E']),((4,3),dir['E']),
                           ((5,6),dir['E']),((5,7),dir['E']),((5,8),dir['E']),((5,9),dir['E']),((6,0),dir['E']),
                           ((6,1),dir['E']),((6,2),dir['E']),((6,3),dir['E'])]
        self.classroom_4 = [((1,1),dir['N']),((1,2),dir['S']),((2,1),dir['N']),((2,2),dir['S']),
                           ((1,4),dir['N']),((1,5),dir['S']),((2,4),dir['N']),((2,5),dir['S']),
                           ((1,7),dir['N']),((1,8),dir['S']),((2,7),dir['N']),((2,8),dir['S']),
                           ((4,1),dir['N']),((4,2),dir['S']),((5,1),dir['N']),((5,2),dir['S']),
                           ((4,4),dir['N']),((4,5),dir['S']),((5,4),dir['N']),((5,5),dir['S']),
                           ((4,7),dir['N']),((4,8),dir['S']),((5,7),dir['N']),((5,8),dir['S'])]

        #Set up seats, canteen tables, queuing area
        self.seats, self.seat,self.toilet = [], (), ()
        self.canteen_table_1 = [((22,y), dir['E']) for y in range(25,33)]+[((18,y), dir['E']) for y in range(25,33)]+[((14,y), dir['E']) for y in range(25,33)]
        self.canteen_table_2 = [((23,y), dir['W']) for y in range(25,33)]+[((19,y), dir['W']) for y in range(25,33)]+[((15,y), dir['W']) for y in range(25,33)]
        self.canteen_tables = self.canteen_table_1+self.canteen_table_2
        self.canteen_counter = 0
        self.enter_canteen_area12 = [(x,y) for y in range(0,4) for x in range(17,26)]
        self.enter_canteen_area10 = [(x,y) for y in range(0,4) for x in range(21,26)]
        self.canteen_queue_area = [(22,3), (24,3)]+[(23, y) for y in range(3,21)]+[(25, y) for y in range(5,19)]
        self.classroom_area = [(x,y) for y in range(0,height+1) for x in range(0,9)]
        self.toilet_queue_area = [(x,y) for x in range(8,15) for y in [height-1, height-2]]


        set_up_initial_attributes(self)

        #Make seats (if family group restriction is on, dont shuffle)
        self.seat = make_classroom_seating(setUpType, self)
        for list in self.seat:
            if family_groups == False: #Shuffle
                self.seats.append(random.sample(list,k=len(list)))
            elif family_groups == True: #Dont shuffle
                self.seats.append(list)

        self.copy_of_seats = self.seats
        self.datacollector.collect(self)
        self.running = True


        if 0 < percentages_of_vaccinated < 1:
            vaccinate_agents(self)


    def step(self):
        ''''
        Invoked every time step and is multi-purposed.
        Collect data in the data-collector and invokes all agents' step() function

        Tracks and manage time and time count, including weekends, day off and off school parameters at students.
        Initiate several different functions; chosing agents to go toilet, set students with questions in class,
        make classroom seating, set canteen employees,

        :param self: class-object
        :return: None
        '''
        #Only let people go to toilet, if toilet is open (closed when everyone go home in breaks)
        if go_home_in_breaks == False:
            choose_agents_to_go_to_toilet(self)

        #Go home if you dont have any more courses today
        set_off_school(self)

        #Day off
        if self.day_count%7==2 or self.day_count%7==3 or self.day_count%7==4 or self.day_count%7==5:
            set_day_off(self)

        #Update classroom seatings
        if go_home_in_breaks == False:
            if self.minute_count in [1,119,299,419]:
                self.seats = make_classroom_seating(self.setUpType, self)

        #Handle employees
        set_canteen_employees(self)
        #Answer questions
        students_with_questions(self)

        #Tell the students that are attending class next, that they need to go to class. Timing this depends on
        #wether or not everyone go home in breaks or not
        set_students_go_to_class_next(self)

        #Step every agent and collect data
        self.schedule.step()
        self.datacollector.collect(self)

        #Time count, manage weekends and toilet cleaning
        self.minute_count += 1
        if self.minute_count % 60 == 0:
            self.hour_count += 1

        if self.minute_count % 526 == 0:
            self.day_count += 1
            if self.day_count in [6,13,20,27,34,41,48,55,62]:
               self.day_count+=2
               weekend(self)
            self.minute_count = 1
            self.hour_count = 1
            try:
                self.toilet.has_been_infected = False #Clean toilet everyday
            except:
                return



