from mesa import Agent, Model
import math
from mesa.space import MultiGrid
import numpy as np

#From sugerscape_cg
'Afstandskrav: 2 meter'
def getDistance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2

    dx = abs(x1-x2)
    dy = abs(y1-y2)

    return math.sqrt(dx**2+dy**2)

class covid_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.infected = 0 #0 for False, 1 for True
        self.recovered = 0 #0 for False, 1 for True
        self.mask = 0 #0 for False, 1 for True
        self.infection_period = 9
        self.id = id

        #Relevant for classroom only
        self.hasQuestion = 0


    #Go through neighbors and find one to infect.
    def infectNewAgent(self):

        all_neighbors_within_radius = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False,radius=2)

        closest_neighbors = []
        for position in all_neighbors_within_radius:
            if not self.model.grid.is_cell_empty(position):
                closest_neighbors.append(position)

        r68 = np.random.poisson(68/100)
        r30 = np.random.poisson(30/100)
        r10 = np.random.poisson(10/100)
        r2 = np.random.poisson(2/100)
        for position in closest_neighbors:
            distance = getDistance(self.pos,position)
            agent = self.model.grid[position[0]][position[1]]
            agent_status = agent[0].infected
            agent_recovered_status = agent[0].recovered

            'Agent kan ikke blive smittet'
            if agent_recovered_status == 1 or agent_status == 1:
                continue
            elif distance <= 1.0:
                if r68 == 1:
                    agent[0].infected = 1
            elif distance > 1.0 and distance <= 1.7:
                if r30 == 1:
                    agent[0].infected = 1
            elif distance > 1.7 and distance <= 2.0:
                if r10 == 1:
                    agent[0].infected = 1
            elif r2 == 1:
                agent[0].infected = 1

    def move(self,student=None):
        print("TIDEN ER NU",self.model.timeToTeach)
        if student is not None:
            x,y = student.pos
            if self.model.timeToTeach == 0:           #Student has recieved help for 5 minutes
                student.hasQuestion = 0             #Student does not have question anymore
                self.model.timeToTeach = 5          #Reset timer

            elif self.model.timeToTeach == 4:   #Student has not recieved help yet, go to that student
                TA = self

                self.model.schedule.remove(TA)
                self.model.grid.remove_agent(TA)
                newTA = covid_Agent(1000,self.model)
                self.model.schedule.add(newTA)
                self.model.grid.place_agent(newTA,(x,y))
                self.model.timeToTeach -= 1
            else:                               #Student is still recieving help, subtract one minut and stay put
                self.model.timeToTeach -= 1


        elif self.model.timeToTeach == 5:           #No one is recieving help or asking for help
            possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
            possible_empty_steps = []
            for position in possible_steps:
                if self.model.grid.is_cell_empty(position):
                    possible_empty_steps.append(position)

            if len(possible_empty_steps) != 0:
                next_move = self.random.choice(possible_empty_steps)
                self.model.grid.move_agent(self, next_move)




    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):

          #Infect another agent random
        if self.infected == 0:
            pass
        else:
            #Generate random int and infect a new agent if int = 1.
            randomInt = np.random.poisson(1/2)
            if randomInt == 1:
                self.infectNewAgent()

            #Subtract 1 from infection period. Reset infection period if == 0 and make agent not infected anymore
            # (not yet immun)
            self.infection_period -= 1
            if self.infection_period == 0:
                self.infected = 0
                if np.random.poisson(1/100) == 0:
                    self.recovered = 0
                    self.infection_period = 9
                else:
                    self.recovered = 1
            else: self.infected = 1

          ##MOVE###
        if self.model.setUpType == 1:
            self.move()
        elif not self.model.setUpType == 1 and self.id == 1000: #Move only TA
            listOfStudents = self.model.schedule.agents
            for student in listOfStudents:
                if student.hasQuestion == 1:
                    self.move(student)

            else: self.move()









class Table(Agent):
    def __init__(self,id,model):
        super().__init__(id, model)
        self.id = id
        self.model = model
        self.occupied = 0 #Der sidder ikke nogen fra start

    def step(self):
        print("hej")
        #TBI

