import AgentClass as ac
from mesa.time import SimultaneousActivation,RandomActivation
from mesa.space import MultiGrid
import random
from mesa import Agent, Model

import numpy as np
from mesa.datacollection import DataCollector

init_positive_agents = 2
init_canteen_agents = 85
dir = {'N':(0,1), 'S':(0,-1), 'E':(1,0), 'W':(-1,0),'NE': (1,1), 'NW': (-1,1), 'SE':(1,-1), 'SW':(-1,-1)}
listOfSetup = []

#Get the status of a given parameter at any time in model (infected, hasQuestion, recovered, etc).
def find_status(model,parameter,agent_type=None,list=None):
    agents_status = []
    if agent_type is not None:
        if list is not None:
            for agent in list:
                for i in range(len(agent_type)):
                    if isinstance(agent, agent_type[i]):
                        agents_status.append(getattr(agent,parameter))
        else:
            for agent in model.schedule.agents:
                for i in range(len(agent_type)):
                    if isinstance(agent, agent_type[i]):
                        agents_status.append(getattr(agent,parameter))
    else:
        for agent in model.schedule.agents:
            if not isinstance(agent, ac.door) and not isinstance(agent,ac.wall):
                agents_status.append(getattr(agent,parameter))
    return sum(agents_status)

def count_agents(model):
    Agents = []
    for agent in model.schedule.agents:
        if not isinstance(agent, ac.door) and not isinstance(agent,ac.wall):
            Agents.append(agent)
    return len(Agents)

def add_init_infected_to_grid(self,n):
    i = 0
    positives = []
    while i<n:
        randomAgent = self.random.choice(self.schedule.agents)
        if randomAgent.pos in positives: #Dont pick the same agent as before
            pass
        elif isinstance(randomAgent,ac.covid_Agent) or isinstance(randomAgent,ac.TA) or isinstance(randomAgent,ac.canteen_Agent):
            self.schedule.remove(randomAgent)
            positive_agent = randomAgent
            positive_agent.infected = 1
            positive_agent.exposed = 0
            positive_agent.asymptomatic = 1040
            self.schedule.add(positive_agent)
            positives.append(randomAgent.pos) # To keep track of initial positives
            self.infected_agents.append(positive_agent)
            i+=1
        else: pass

def add_init_cantine_agents_to_grid(self,N,n):
    id_ = N
    limit = N #We start by initializing N many canteen-agents. These are the agents that will be attending courses.
    counter = 0
    while limit > counter:
            newAgent = ac.canteen_Agent(id_,self)
            self.schedule.add(newAgent) #Add agent to scheduler
            x, y = self.grid.find_empty()#Place agent randomly in empty cell on grid
            newAgent.coords = random.choice(list(dir.values()))   #Give agent random direction to look at

            newAgent.courses = [self.range13.pop(),self.range46.pop()]
            next_door_id = 500+newAgent.courses[0]  #Which door should agent go to when class starts - depending on course
            next_door = [a for a in self.schedule.agents if isinstance(a,ac.door) and a.id == next_door_id]
            newAgent.door = next_door[0]
            newAgent.next_to_attend_class = True
            newAgent.off_school = 1
            self.grid.place_agent(newAgent, (max(x,9),y))
            id_+=1
            counter+=1
    #m >= 3 since we want to create 3 TAs that start in the canteen
    #Thus, these 3 are soon-to-be TAs. Dont have courses, only have door attached.
    j=4
    for i in range(0,3):
        newAgent = ac.canteen_Agent(1000+j+i,self)
        self.schedule.add(newAgent) #Add agent to scheduler
        x, y = self.grid.find_empty()#Place agent randomly in empty cell on grid
        newAgent.coords = random.choice(list(dir.values()))   #Give agent random direction to look at
        next_door_id = newAgent.id-503 #Which door should agent go to when class starts - depending on course
        next_door = [a for a in self.schedule.agents if isinstance(a,ac.door) and a.id == next_door_id]
        newAgent.next_to_attend_class = True
        newAgent.door = next_door[0]
        newAgent.off_school = 1
        self.grid.place_agent(newAgent, (max(x,9),y))


    m = n-limit-3
    if n-3>limit: #We still need to initialize more canteen-agents, but these will not attend classes (fx students writing their master thesis)
        #They are initialized without door, courses, etc. They are "dummy" agents which can only contribute
        #to infecting others.
        for i in range(0,m):
            newAgent = ac.canteen_Agent(id_,self)
            self.schedule.add(newAgent) #Add agent to scheduler
            x, y = self.grid.find_empty()#Place agent randomly in empty cell on grid
            newAgent.coords = random.choice(list(dir.values()))   #Give agent random direction to look at
            self.grid.place_agent(newAgent, (max(x,9),y))
            id_+=1

def set_canteen_agents_next_to_attend_class(self):
     canteens_agents = [a for a in self.schedule.agents if isinstance(a,ac.canteen_Agent)
                        and a.id not in [1001,1002,1003,1004,1005,1006]
                        and a.door is not ()] #Only get students who are attending class
     get_correct_TAs = list(set([a.TA.id for a in canteens_agents if a.TA is not ()])) #Get unique id of TAs-to-be. These will also get True in nexT_to_attend_class
     soon_to_be_TAs = [a for a in self.schedule.agents if a.id in get_correct_TAs]
     for agent in soon_to_be_TAs:
         canteens_agents.append(agent)

     going_to_class_next_agents = canteens_agents

     not_TAs = [a for a in going_to_class_next_agents if isinstance(a,ac.canteen_Agent)]


     for agent in going_to_class_next_agents:
         if isinstance(agent,ac.TA):
             print(self.minute_count,self.setUpType,agent.id,agent.pos)
         if isinstance(agent,ac.canteen_Agent):
                agent.next_to_attend_class = not agent.next_to_attend_class

#Set up the grid accordingly
#Add walls, doors, TAs and classrooms
def setUp(N,model,setUpType,i):
    listOfPositions = []
    'random set-up'
    if setUpType == 1:
        for i in range(N*i,(1+i)*N):
            newAgent = ac.covid_Agent(i, model)
            model.schedule.add(newAgent) #Add agent to scheduler
            x, y = model.grid.find_empty()#Place agent randomly in empty cell on grid
            newAgent.coords = random.choice(list(dir.values()))   #Give agent random direction to look at
            model.grid.place_agent(newAgent, (x,y))
    elif setUpType == 2: #Horseshoe
        listOfPositions = [((x,y+i*11),z) for ((x,y),(z)) in model.classroom_2]
    elif setUpType == 3: #Rows
        listOfPositions = [((x,y+i*11),z) for ((x,y),(z)) in model.classroom_3]
    elif setUpType == 4: #4-people table with correct direction added
        listOfPositions = [((x,y+i*11),z) for ((x,y),(z)) in model.classroom_4]
    elif setUpType == 5:
         listOfPositions = [((x,y+i*11),z) for ((x,y),(z)) in model.classroom_5]
    if setUpType is not 1:

        #Add door(s) to model and grid
        door_location = (8,5+i*11)
        door = ac.door(501+i, door_location, model)
        door.classroom = i+1
        model.door = door
        model.schedule.add(door)
        model.grid.place_agent(door,door_location)


        students = []
        # Add TA
        x,y = random.choice([(7,5+i*11),(7,4+i*11)])
        TA = ac.TA(1001+i,model)
        TA.coords = dir['W']
        TA.door = door
        model.schedule.add(TA)
        model.grid.place_agent(TA,(x,y))
        model.TAs.append(TA)




        for j in range(N*i,(i+1)*N):
            newAgent = ac.covid_Agent(j, model)
            model.schedule.add(newAgent)
            posAndDirection = listOfPositions.pop()
            x,y = posAndDirection[0]
            newAgent.coords = posAndDirection[1]
            other_course = model.other_courses.pop()
            newAgent.courses = [i+1,other_course]
            newAgent.door = door
            model.grid.place_agent(newAgent,(x,y))
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
            newBrick = ac.wall(wall_placements_v_id[j], model)
            newBrick.orientation = 'v'
            model.schedule.add(newBrick)
            model.grid.place_agent(newBrick, wall_placements_vertical[j])
        for j in range(len(wall_placements_horizontal)):
            newWall = ac.wall(wall_placements_h_id[j],model)
            newWall.orientation = 'h'
            model.schedule.add(newWall)
            model.grid.place_agent(newWall,wall_placements_horizontal[j])

#Returns list of lists of seats I can assign to agents
def make_classrooms_fit_to_grid(list_of_setuptypes,model):
    seats = []

    for j in range(len(list_of_setuptypes)):
        number = str("classroom_") + str(list_of_setuptypes[j])    #Which type of class room are we constructing?
        class_room = [(x,y+j*11) for ((x,y),z) in getattr(model,number)]
        seats.append(class_room)
    return seats

def weekend(self):
    infected_agents = [a for a in self.schedule.agents if (isinstance(a, ac.TA) or isinstance(a,ac.covid_Agent) or isinstance(a,ac.canteen_Agent)) and a.infected == 1]
    print("før",len(infected_agents))
    ids_to_remove = []
    for a in infected_agents:
        a.asymptomatic = max(0,a.asymptomatic-2*540)  #Træk 2 dage fra asymtom
        a.infection_period = max(0,a.infection_period-2*540) #Træk 2 dage fra infektionsperiode
        a.exposed = max(0,a.exposed-2*540) #Træk 2 dage fra exposed
       # print("JEG ER , AIE",a.id, a.asymptomatic,a.infection_period,a.exposed)
        if a.is_home_sick == 1: #Agenten er hjemme, skal den tilbage nu?
            print("JEG ER HJEMME",a.id, a.asymptomatic,a.infection_period,a.exposed)
            if a.infection_period == 0:
                print("MEN JEG MÅ KOMME TILBAGE",a.id)
                ac.send_agent_back_to_school(a) #Agenten er rask og skal tilbage i skole
                ids_to_remove.append(a.id)
                continue
        elif a.asymptomatic == 0: #Agenten har symptomer nu og skal blive hjemme
            print("Jeg skal hjem nu!",a.id, a.asymptomatic,a.infection_period,a.exposed)
            ac.send_agent_home(a)
            ids_to_remove.append(a.id)
            continue
    infected_agents = [a for a in self.infected_agents if a.id not in ids_to_remove]
    print("efter",len(infected_agents))

class covid_Model(Model):
    def __init__(self, N, height, width,setUpType):
        self.n_agents = N
        self.TAs = []
        self.grid = MultiGrid(width, height, torus=False) #torus wraps edges
        self.schedule = RandomActivation(self)
        self.setUpType = setUpType
        self.status = find_status(self,"infected",[ac.covid_Agent])
        self.datacollector = DataCollector(model_reporters={"infected": lambda m: find_status(self, "infected", [ac.covid_Agent, ac.canteen_Agent, ac.TA]),
                                                            "Agent_count": lambda m: count_agents(self),
                                                            "recovered": lambda m: find_status(self, "recovered", [ac.covid_Agent, ac.canteen_Agent, ac.TA]),
                                                            "Home":lambda m: find_status(self, "is_home_sick", [ac.covid_Agent, ac.canteen_Agent, ac.TA])})

        self.agents_at_home = []
        self.recovered_agents = []
        self.infected_agents = []

        #Counting minutes and days
        self.minute_count = 0
        self.hour_count = 0
        self.day_count = 0
        self.door = ()

        self.class_times = [120,135,240,315,420,435,540]

        self.other_courses = random.sample([4]*26+[5]*26+[6]*26,k=len([4]*26+[5]*26+[6]*26))

        self.range46 = random.sample([4]*26+[5]*26+[6]*26,k=len([4]*26+[5]*26+[6]*26))
        self.range13 = random.sample([1]*26+[2]*26+[3]*26,k=len([1]*26+[2]*26+[3]*26))

        #Classrooms +  directions
        self.classroom_2 = [((1,1),dir['E']),((2,1),dir['N']),((3,1),dir['N']),((4,1),dir['N']),((5,1),dir['N']),
                           ((6,1),dir['N']),((1,2),dir['E']),((1,3),dir['E']),((2,3),dir['S']),((3,3),dir['S']),
                           ((4,3),dir['S']),((5,3),dir['S']),((6,3),dir['S']),
                           ((1,6),dir['E']),((2,6),dir['N']),((3,6),dir['N']),((4,6),dir['N']),((5,6),dir['N']),
                           ((6,6),dir['N']),((1,7),dir['E']),((1,8),dir['E']),((2,8),dir['S']),((3,8),dir['S']),
                           ((4,8),dir['S']),((5,8),dir['S']),((6,8),dir['S'])]
        self.classroom_3 = [((1,5),dir['E']),((1,6),dir['E']),((1,7),dir['E']),((1,8),dir['E']),((1,9),dir['E']),
                           ((2,0),dir['E']),((2,1),dir['E']),((2,2),dir['E']),((2,3),dir['E']),
                           ((3,5),dir['E']),((3,6),dir['E']),((3,7),dir['E']),((3,8),dir['E']),((3,9),dir['E']),
                           ((4,0),dir['E']),((4,1),dir['E']),((4,2),dir['E']),((4,3),dir['E']),
                           ((5,6),dir['E']),((5,7),dir['E']),((5,8),dir['E']),((5,9),dir['E']),((6,0),dir['E']),
                           ((6,1),dir['E']),((6,2),dir['E']),((6,3),dir['E'])]
        self.classroom_4 = [((1,1),dir['N']),((1,2),dir['S']),((2,1),dir['N']),((2,2),dir['S']),
                           ((1,4),dir['N']),((1,5),dir['S']),((2,4),dir['N']),((2,5),dir['S']),
                           ((1,7),dir['N']),((1,8),dir['S']),((2,7),dir['N']),((2,8),dir['S']),
                           ((4,1),dir['E']),((4,2),dir['E']),((5,1),dir['N']),((5,2),dir['S']),((6,1),dir['N']),((6,2),dir['S']),
                           ((4,4),dir['N']),((4,5),dir['S']),((5,4),dir['N']),((5,5),dir['S']),
                           ((4,7),dir['N']),((4,8),dir['S']),((5,7),dir['N']),((5,8),dir['S'])]
        self.classroom_5 = [((0,0),dir['N']),((0,1),dir['S']),((0,3),dir['N']),((0,4),dir['S']),
                           ((0,6),dir['N']),((0,7),dir['S']),((0,9),dir['N']),((2,0),dir['S']),
                           ((2,2),dir['N']),((2,3),dir['S']),((2,5),dir['N']),((2,6),dir['S']),
                           ((2,8),dir['E']),((2,9),dir['E']),((4,0),dir['N']),((4,1),dir['S']),((4,3),dir['N']),((4,4),dir['S']),
                           ((4,6),dir['N']),((4,7),dir['S']),((4,9),dir['N']),((6,0),dir['S']),
                           ((6,2),dir['N']),((6,4),dir['S']),((6,6),dir['N']),((6,8),dir['S'])]
        self.classroom_56 = [((1,0),dir['N']),((1,1),dir['S']),((1,3),dir['N']),((1,4),dir['S']),
                           ((1,6),dir['N']),((1,7),dir['S']),((1,9),dir['N']),((3,0),dir['S']),
                           ((3,2),dir['N']),((3,3),dir['S']),((3,5),dir['N']),((3,6),dir['S']),
                           ((3,8),dir['E']),((3,9),dir['E']),((5,0),dir['N']),((5,1),dir['S']),((5,3),dir['N']),((5,4),dir['S']),
                           ((5,6),dir['N']),((5,7),dir['S']),((5,9),dir['N']),((0,5),dir['S']),
                           ((0,2),dir['N']),((6,8),dir['S']),((6,2),dir['N']),((0,8),dir['S'])]
        self.seats = []
        self.seat = ()


        #Add agents to model and grid
        i = 0
        for s in setUpType:
            setUp(self.n_agents+1,self,s,i)
            i+=1

        add_init_cantine_agents_to_grid(self,(self.n_agents+1)*i,init_canteen_agents)
        add_init_infected_to_grid(self,init_positive_agents)

        self.seat = make_classrooms_fit_to_grid(setUpType,self)
        for list in self.seat:
            self.seats.append(random.sample(list,k=len(list)))
        self.datacollector.collect(self)
        self.running = True

    def step(self):
        #Every 10th timestep add asking student
        if not self.setUpType == 1 and self.schedule.time > 2 and (self.schedule.time) % 10 == 0:
            for ta in self.TAs:
                if len(ta.students) == 0:
                    continue
                if len(ta.students)>1:
                    TAs_students = ta.students
                    randomStudent = self.random.choice(TAs_students)
                    randomStudent.hasQuestion = 1

        self.schedule.step()
        self.datacollector.collect(self)



        if self.day_count>0 and self.minute_count in [110,220,390,539]:
            set_canteen_agents_next_to_attend_class(self)
        elif self.minute_count in [220,390,539]:
            set_canteen_agents_next_to_attend_class(self)

        first_third_class = [a for a in self.schedule.agents if a.id in range(0,(self.n_agents+1)*len(self.setUpType))]
        first_third_TAs = [a for a in self.schedule.agents if a.id in [1001,1002,1003]]
        second_fourth_class = [a for a in self.schedule.agents if a.id in range((self.n_agents+1)*len(self.setUpType),2*(self.n_agents+1)*len(self.setUpType))]
        second_fourth_TAs = [a for a in self.schedule.agents if a.id in [1004,1005,1006]]

        minutes = [x for x in range(0,45)]
        if self.minute_count in minutes:
            for a in second_fourth_class+second_fourth_TAs:
                a.off_school = 1
            for a in first_third_class:
                a.off_school = 0

        if self.minute_count == 120:
             for a in second_fourth_class+second_fourth_TAs:
                a.off_school = 0

        if self.minute_count == 435:
            for a in first_third_class+first_third_TAs:
                a.off_school = 1



        #Terminate model when everyone is healthy
        #if find_status(self,"infected") == 0:
         #  self.running = False

        #Time count
        self.minute_count += 1
        if self.minute_count % 60 == 0:
            self.hour_count += 1
            #Reset list of seats so new agents can pop from original list of seats in classrooms
            self.seats = []
            for list in self.seat:
                self.seats.append(random.sample(list,k=len(list)))

        if self.minute_count % 540 == 0:
            self.day_count += 1
            self.minute_count = 0
            self.hour_count = 0

            if self.day_count%5 == 0: ##WEEKEND
                print(self.day_count)
                weekend(self)

        infected_agents = [a for a in self.schedule.agents if (isinstance(a, ac.TA) or isinstance(a,ac.covid_Agent) or isinstance(a,ac.canteen_Agent)) and a.infected == 1]
     #   print("så mange er infeected",len(infected_agents))


        #update_status_infected_agents(self)
