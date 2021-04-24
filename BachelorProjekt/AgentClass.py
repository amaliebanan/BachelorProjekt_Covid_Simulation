from mesa import Agent, Model
import math
from mesa.space import MultiGrid
import numpy as np
import random
from operator import itemgetter
import sys
from Model import covid_Model,with_mask,is_student, is_off_campus, is_human, dir,count_students_who_has_question, infection_rate, infection_rate_1_to_2_meter, infection_rate_2plus_meter, infection_decrease_with_mask_pct, calculate_percentage, with_dir, go_home_in_breaks
from scipy.stats import truncnorm,bernoulli

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
def angle_between(selfdirection, agentdirection): #virker
    """
    arctan takes in (y,x) which is why we invert the input vector.
    ang1 and ang2 is two angels. each is the angle we get from creating  threesome with their (x,y) coordinates.
    :return returns the difference between the two angels:
    """
    ang1 = np.arctan2(*agentdirection[::-1])
    ang2 = np.arctan2(*selfdirection[::-1])
    return ((ang1 - ang2) % (2 * np.pi))

def get_agent_at_cell(self,pos):
    return self.model.grid.get_cell_list_contents(pos)[0]

def truncnorm_(a,b,mu,sigma):
        alpha, beta = (a-mu)/sigma, (b-mu)/sigma
        return math.floor(truncnorm.rvs(alpha,beta,loc=mu,scale=sigma))

#Wander around function
def wander(self):
    possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=True)
    possible_empty_steps = []
    for position in possible_steps:
        if isinstance(self, canteen_Agent) and self.sitting_in_canteen == 0:
            if position not in [(23,18), (23,19)] :#cant walk wrong way through canteen or toiletqueue
                if self.model.grid.is_cell_empty(position) or is_off_campus(get_agent_at_cell(self, position)) or\
                        isinstance(get_agent_at_cell(self,position),table):
                    possible_empty_steps.append(position)
        elif isinstance(self, canteen_Agent) and self.sitting_in_canteen != 0:
            if self.model.grid.is_cell_empty(position) or is_off_campus(get_agent_at_cell(self, position)):
                possible_empty_steps.append(position)

        elif position not in [(23,18), (23,19)]:#cant walk wrong way through canteen
            if self.model.grid.is_cell_empty(position):
                possible_empty_steps.append(position)
            elif isinstance(get_agent_at_cell(self,position),table):
                possible_empty_steps.append(position)
    try:
        pos_to_go_to = [pos for pos in possible_empty_steps if pos not in self.model.toilet.queue]
    except:
        pos_to_go_to = possible_empty_steps
    if len(pos_to_go_to) != 0:
        next_move = self.random.choice(pos_to_go_to)
        self.model.grid.move_agent(self, next_move)

    if go_home_in_breaks is False:
        if self.pos in [x for (x,y) in self.model.canteen_tables]:
                if self.sitting_in_canteen == 0:
                    if self.model.minute_count in range(225,301):
                        if self.pos in [x for (x,y) in self.model.canteen_table_1]:
                            self.coords = dir['E']
                        else:
                            self.coords = dir['W']
                        self.sitting_in_canteen = 70
                        self.mask = False
                    else:
                        if self.pos in [x for (x,y) in self.model.canteen_table_1]:
                            self.coords = dir['E']
                        else:
                            self.coords = dir['W']
                        self.sitting_in_canteen = 60
                        self.mask = False



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

def infect_(self):
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

        newly_infected = []
        for agent in closest_neighbors:
            #Dont infect neighbors that are home sick / not on campus
            if is_off_campus(agent) or (is_human(agent) and agent.is_home_sick == True):
                continue
            #Dont infect neighbors that are vaccinated, recovered or already infected
            if agent.vaccinated == True or agent.recovered == True or agent.infected == True: # kan ikke blive smittet, da den er immun eller allerede infected
                continue

            distance = getDistance(self.pos,agent.pos)
            if distance <= 0.1:
                if isinstance(self,TA) or isinstance(agent,TA): #Vi er i en TA-situation
                 ##De er i indgangen, smit mindre
                    if self.mask == True:
                        pTA = bernoulli.rvs(calculate_percentage(100*infection_rate,infection_decrease_with_mask_pct))
                    elif self.mask == False:
                        pTA = bernoulli.rvs(100*infection_rate)
                    if pTA == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if self.mask == True:
                        pTA = bernoulli.rvs(calculate_percentage(10*infection_rate,infection_decrease_with_mask_pct))
                    elif self.mask == False:
                        pTA = bernoulli.rvs(10*infection_rate)
                    if pTA == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                 #Indenfor 1 meters afstand
            elif distance > 0.5 and distance <= 1.0:
                 if self.mask == True:
                    p_1 = bernoulli.rvs(calculate_percentage(infection_rate, infection_decrease_with_mask_pct)) #70 percent decrease if masks
                 elif self.mask == False:
                     p_1 = bernoulli.rvs(infection_rate)
                 if p_1 == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)

                 #Mellem 1 og 2 meters afstand
            elif distance > 1.0 and distance <= 2.0:
                if self.mask == True:
                    p_1_til_2 = bernoulli.rvs(calculate_percentage(infection_rate_1_to_2_meter,infection_decrease_with_mask_pct))
                elif self.mask == False:
                     p_1_til_2 = bernoulli.rvs(infection_rate_1_to_2_meter)
                if p_1_til_2 == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)

                #Over 2 meters afstand
            elif distance>2.0:
                if self.mask == True:
                    p_over_2 = bernoulli.rvs(calculate_percentage(infection_rate_2plus_meter,infection_decrease_with_mask_pct))
                elif self.mask == False:
                     p_over_2 = bernoulli.rvs(infection_rate_2plus_meter)
                if p_over_2 == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)

        for a in newly_infected:
            a.infected = True
            a.infection_period = truncnorm_(5*day_length,67*day_length,9*day_length,1*day_length)#How long are they sick?
            a.asymptomatic = truncnorm_(3*day_length,a.infection_period,5*day_length,1*day_length) #Agents are asymptomatic for 5 days
            a.exposed = a.asymptomatic-2*day_length

def infect_p(self):
        if self.exposed != 0:   #Agent smitter ikke endnu.
            return

        if isinstance(self, TA):
            all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=True,radius=2)
        else:
            all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False,radius=2)
        closest_neighbors = []

        for n in all_neighbors_within_radius:
            if not self.model.grid.is_cell_empty(n.pos):
                if is_human(n):
                    if (not is_off_campus(n) or not n.is_home_sick)\
                            and not n.vaccinated and not n.recovered and not n.infected:
                        closest_neighbors.append(n)

        for agent in closest_neighbors:
             if is_off_campus(agent) or (is_human(agent) and agent.is_home_sick == True):
                closest_neighbors.remove(agent)
             if agent.vaccinated == True or agent.recovered == True or agent.infected == True: # kan ikke blive smittet, da den er immun eller allerede infected
                closest_neighbors.remove(agent)

        poission_ = np.random.poisson(1/525)
        if poission_ > 0:
            distances = [(a,getDistance(self.pos,a.pos)) for a in closest_neighbors]
            sorted_distances = sorted(distances,key=itemgetter(1))

            l,l1,l2,l3,l4=[],[],[],[],[]
            for t in sorted_distances:
                if t[1]<=0.1:
                    l1.append(t)
                elif 0.5<t[1]<=1.0:
                    l2.append(t)
                elif 1.0<t[1]<=2.0:
                    l3.append(t)
                elif 2.0<t[1]:
                    l4.append(t)
            l.append(l1)
            l.append(l2)
            l.append(l3)
            l.append(l4)

            temp = l
            counter=0
            #print(poission_)
            while counter<poission_:
                if not any(temp): #If all the lists are empty
                    return
                item =random.choices(temp, weights=(60,25,10,5), k=3)
                if item[0] == []:
                    continue
                get_a = random.choices(item[0])[0]
                temp = [[ele for ele in sub if ele != get_a] for sub in temp]
                counter+=1
                print("Iteration:", counter, "Weighted Random a is", item[0],"and it got",get_a[0],poission_)
                get_a[0].infected = True

def infect(self):
    if self.exposed != 0:   #Agent smitter ikke endnu.
        return
    if (self.is_home_sick == True) or (isinstance(self,canteen_Agent) and self.off_school == True): #Agenten er derhjemme og kan ikke smitte
        return

    if isinstance(self, TA):
        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=True,radius=2)
        all_neighbors_within_radius = [n for n in all_neighbors_within_radius if isinstance(n,class_Agent)]
    else:
        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False,radius=2)
    #Ikke smit igennem vægge hvis du er til time
    if isinstance(self,class_Agent):
        all_neighbors_within_radius = [n for n in all_neighbors_within_radius if (isinstance(n,class_Agent) and n.courses[0] == self.courses[0]) or (isinstance(n,TA) and n.door.id == self.door.id)]

    #Canteen-agents kan ikke smitte class eller TA-agents (fordi det er igennem væggen)
    if isinstance(self,canteen_Agent):
        all_neighbors_within_radius = [n for n in all_neighbors_within_radius if not isinstance(n,TA) and not isinstance(n,class_Agent)]


    #Smit kun dit eget hold (A eller B) hvis dagen skifter
    if self.model.minute_count in list(range(0,60)):
        if self.id in list(range(0,(len(self.model.setUpType)*self.model.n_agents)))+[1001,1002,1003]:
            all_neighbors_within_radius = [n for n in all_neighbors_within_radius if n.id in list(range(0,(len(self.model.setUpType)*self.model.n_agents)))+[1001,1002,1003]]
        elif self.id in list(range((len(self.model.setUpType)*self.model.n_agents)+1,2*(len(self.model.setUpType)*self.model.n_agents)))+[1004,1005,1006]:
            all_neighbors_within_radius = [n for n in all_neighbors_within_radius if n.id in list(range((len(self.model.setUpType)*self.model.n_agents)+1,2*(len(self.model.setUpType)*self.model.n_agents)))+[1004,1005,1006]]


    all_humans_within_radius = []
    for neighbor in all_neighbors_within_radius:
        if is_human(neighbor):
            #Dont infect neighbors that are home sick / not on campus
            if neighbor.is_home_sick == True or (isinstance(neighbor,canteen_Agent) and neighbor.off_school == True):
                continue
            #Dont infect neighbors that are vaccinated, recorvered or infected
            if neighbor.vaccinated == True or neighbor.recovered == True or neighbor.infected == True: # kan ikke blive smittet, da den er immun eller allerede infected
                continue
            if not self.model.grid.is_cell_empty(neighbor.pos):
                    all_humans_within_radius.append(neighbor)

            "Define infection rates"
    if self.mask == True:
        ir = calculate_percentage(infection_rate, 70)
        ir1_2 = calculate_percentage(infection_rate_1_to_2_meter, 70)
        ir2_plus = calculate_percentage(infection_rate_2plus_meter, 70)
    else:
        ir = infection_rate
        ir1_2 = infection_rate_1_to_2_meter
        ir2_plus = infection_rate_2plus_meter


    "Splits neighbors into lists"
    N_list = []
    NE_list = []
    E_list = []
    W_list = []
    NW_list = []
    Behind_list = []
    Same_pos = []
    newly_infected = []
    for agent in all_humans_within_radius:
        if agent.pos == self.pos:
            Same_pos.append(agent)
        elif agent.pos[1] > self.pos[1] and agent.pos[0] == self.pos[0]:
                if self.coords == dir['N']:
                    N_list.append(agent)
                elif self.coords == dir['E']:
                    W_list.append(agent)
                elif self.coords == dir['S']:
                    Behind_list.append(agent)
                elif self.coords == dir['W']:
                    E_list.append(agent)
                elif self.coords == dir['NE']:
                    NW_list.append(agent)
                elif self.coords == dir['SE']:
                    Behind_list.append(agent)
                elif self.coords == dir['NW']:
                    NE_list.append(agent)
                else:
                    Behind_list.append(agent)
        elif agent.pos[1] < self.pos[1] and agent.pos[0] == self.pos[0]:
                if self.coords == dir['N']:
                    Behind_list.append(agent)
                elif self.coords == dir['E']:
                    E_list.append(agent)
                elif self.coords == dir['S']:
                    N_list.append(agent)
                elif self.coords == dir['W']:
                    W_list.append(agent)
                elif self.coords == dir['NE']:
                    Behind_list.append(agent)
                elif self.coords == dir['SE']:
                    NE_list.append(agent)
                elif self.coords == dir['NW']:
                    Behind_list.append(agent)
                else:
                    NW_list.append(agent)
        elif agent.pos[1] == self.pos[1] and agent.pos[0] > self.pos[0]:
                if self.coords == dir['N']:
                    E_list.append(agent)
                elif self.coords == dir['E']:
                    N_list.append(agent)
                elif self.coords == dir['S']:
                    W_list.append(agent)
                elif self.coords == dir['W']:
                    Behind_list.append(agent)
                elif self.coords == dir['NE']:
                    NE_list.append(agent)
                elif self.coords == dir['SE']:
                    NW_list.append(agent)
                elif self.coords == dir['NW']:
                    Behind_list.append(agent)
                else:
                    Behind_list.append(agent)
        elif agent.pos[1] == self.pos[1] and agent.pos[0] < self.pos[0]:
                if self.coords == dir['N']:
                    W_list.append(agent)
                elif self.coords == dir['E']:
                    Behind_list.append(agent)
                elif self.coords == dir['S']:
                    E_list.append(agent)
                elif self.coords == dir['W']:
                    N_list.append(agent)
                elif self.coords == dir['NE']:
                    Behind_list.append(agent)
                elif self.coords == dir['SE']:
                    Behind_list.append(agent)
                elif self.coords == dir['NW']:
                    NW_list.append(agent)
                else:
                    NE_list.append(agent)
        elif agent.pos[1] > self.pos[1] and agent.pos[0] > self.pos[0]:
                if self.coords == dir['N']:
                    NE_list.append(agent)
                elif self.coords == dir['E']:
                    NW_list.append(agent)
                elif self.coords == dir['S']:
                    Behind_list.append(agent)
                elif self.coords == dir['W']:
                    Behind_list.append(agent)
                elif self.coords == dir['NE']:
                    N_list.append(agent)
                elif self.coords == dir['SE']:
                    W_list.append(agent)
                elif self.coords == dir['NW']:
                    E_list.append(agent)
                else:
                    Behind_list.append(agent)
        elif agent.pos[1] > self.pos[1] and agent.pos[0] < self.pos[0]:
                if self.coords == dir['N']:
                    NW_list.append(agent)
                elif self.coords == dir['E']:
                    Behind_list.append(agent)
                elif self.coords == dir['S']:
                    Behind_list.append(agent)
                elif self.coords == dir['W']:
                    NE_list.append(agent)
                elif self.coords == dir['NE']:
                    W_list.append(agent)
                elif self.coords == dir['SE']:
                    Behind_list.append(agent)
                elif self.coords == dir['NW']:
                    N_list.append(agent)
                else:
                    E_list.append(agent)
        elif agent.pos[1] < self.pos[1] and agent.pos[0] > self.pos[0]:
                if self.coords == dir['N']:
                    Behind_list.append(agent)
                elif self.coords == dir['E']:
                    NE_list.append(agent)
                elif self.coords == dir['S']:
                    NW_list.append(agent)
                elif self.coords == dir['W']:
                    Behind_list.append(agent)
                elif self.coords == dir['NE']:
                    E_list.append(agent)
                elif self.coords == dir['SE']:
                    N_list.append(agent)
                elif self.coords == dir['NW']:
                    Behind_list.append(agent)
                else:
                    W_list.append(agent)
        else:
                if self.coords == dir['N']:
                    Behind_list.append(agent)
                elif self.coords == dir['E']:
                    Behind_list.append(agent)
                elif self.coords == dir['S']:
                    NE_list.append(agent)
                elif self.coords == dir['W']:
                    NW_list.append(agent)
                elif self.coords == dir['NE']:
                    Behind_list.append(agent)
                elif self.coords == dir['SE']:
                    E_list.append(agent)
                elif self.coords == dir['NW']:
                    W_list.append(agent)
                else:
                    N_list.append(agent)

    "Now we'll infect"
    for agent in Same_pos:
        if bernoulli.rvs(ir*10) == 1:
            newly_infected.append(agent)
            self.model.infected_agents.append(agent)

    for agent in N_list:
        distance = getDistance(self.pos,agent.pos)
        if angle_between(self.coords, agent.coords) == math.pi: #10xir
            if 1 <= distance <= 2:
                if bernoulli.rvs(ir1_2*10) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
            else:
                if bernoulli.rvs(ir2_plus*10) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)

        elif angle_between(self.coords, agent.coords) in [math.pi*5/4, math.pi*3/4]: #8x ir
            if 1 <= distance <= 2:
                if bernoulli.rvs(ir1_2*8) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
            else:
                if bernoulli.rvs(ir2_plus*8) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
        elif angle_between(self.coords, agent.coords) in [math.pi*3/2, math.pi/2]: #6xir
            if 1 <= distance <= 2:
                if bernoulli.rvs(ir1_2*6) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
            else:
                if bernoulli.rvs(ir2_plus*6) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
        else: #4xir
            if 1 <= distance <= 2:
                if bernoulli.rvs(ir1_2*4) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
            else:
                if bernoulli.rvs(ir2_plus*4) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)

    for agent in NE_list:
            distance = getDistance(self.pos,agent.pos)
            if angle_between(self.coords, agent.coords) == math.pi*3/4: #7xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*7) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*7) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif angle_between(self.coords, agent.coords) in [math.pi, math.pi/2]: #5xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*5) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*5) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif angle_between(self.coords, agent.coords) in [math.pi/4, math.pi*5/4]: #3xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            else: #2xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)

    for agent in E_list:
            distance = getDistance(self.pos,agent.pos)
            if (isinstance(self, class_Agent) and self.pos in self.model.classroom_2+self.model.classroom_3+self.model.classroom_4) or self.pos in self.model.canteen_tables:# if nextdoor neighbor in class
                if distance <2:
                    if bernoulli.rvs(ir1_2*10) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                    continue

            if angle_between(self.coords, agent.coords) == math.pi/2: #4xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*4) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*4) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif angle_between(self.coords, agent.coords) in [math.pi/4, math.pi*3/4]: #3xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif angle_between(self.coords, agent.coords) in [0, math.pi]: #2xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            else: #1xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)

    for agent in Behind_list: #1xir
        distance = getDistance(self.pos,agent.pos)
        if 1 <= distance <= 2:
                if bernoulli.rvs(ir1_2) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
        else:
                if bernoulli.rvs(ir2_plus) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)

    for agent in W_list:
            distance = getDistance(self.pos,agent.pos)
            if (isinstance(self, class_Agent) and self.pos in self.model.classroom_2+self.model.classroom_3+self.model.classroom_4) or self.pos in self.model.canteen_tables:
                if distance <2:
                    if bernoulli.rvs(ir1_2*10) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                continue
            if angle_between(self.coords, agent.coords) == math.pi*3/2: #4xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*4) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*4) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif angle_between(self.coords, agent.coords) in [math.pi*7/4, math.pi*5/4]: #3xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif angle_between(self.coords, agent.coords) in [0, math.pi]: #2xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            else: #1xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)

    for agent in NW_list:
            distance = getDistance(self.pos,agent.pos)
            if angle_between(self.coords, agent.coords) == math.pi*5/4: #7xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*7) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*7) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif angle_between(self.coords, agent.coords) in [math.pi, math.pi*3/2]: #5xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*5) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*5) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif angle_between(self.coords, agent.coords) in [math.pi*7/4, math.pi*3/4]: #3xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            else: #2xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*2) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
    self.reproduction += len(newly_infected)
    for a in newly_infected:
        if bernoulli.rvs(0.3) == 1: #hvis agenten ikke udvikler symptomer
            print('agent med id ',a.id, 'udvikler ikke symptomer')
            a.infected = True
            a.infection_period = truncnorm_(5*day_length,67*day_length,9*day_length,1*day_length)#How long are they sick?
            a.asymptomatic = a.infection_period
            a.exposed = 2*day_length
        else:
            a.infected = True
            a.infection_period = truncnorm_(5*day_length,67*day_length,9*day_length,1*day_length)#How long are they sick?
            a.asymptomatic = truncnorm_(3*day_length,a.infection_period,5*day_length,1*day_length) #Agents are asymptomatic for 5 days
            a.exposed = a.asymptomatic-2*day_length
            print('agent med id ',a.id, 'får symptomer om', a.asymptomatic, 'tidsskridt')

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
    new.reproduction = old.reproduction
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

    #Go home for the day
    if self.model.minute_count > 400 or self.model.minute_count < 50:
        c_agent.has_more_courses_today = False

    return c_agent

#Turn TA-object to class-object
def TA_to_class(self):
    c_agent = class_Agent(self.id, self.model)
    change_obj_params(c_agent,self)

    c_agent.door, c_agent.moving_to_door = self.door, 1

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
        if len(possible_empty_steps) == 0: #if someone in front of you - dont move
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

def go_to_entre(self):
    if self.entre_door == ():
        self.entre_door = self.model.entre[random.randint(0,len(self.model.entre)-1)]

    pos_ = self.entre_door
    possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    possible_empty_steps = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos) or pos == pos_]
    if len(possible_empty_steps) == 0:
        return
    distances = [(pos,getDistance(pos_,pos)) for pos in possible_empty_steps]
    x_,y_ = min(distances,key=lambda x:x[1])[0]
    if min(getDistance((x_,y_), pos_), getDistance(self.pos, pos_)) == getDistance(self.pos, pos_):
        return
    else:
        self.model.grid.move_agent(self,(x_,y_))
        if self.pos == pos_:
            self.off_school = True
            self.entre_door = ()

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
    possible_empty_steps = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos) or is_off_campus(get_agent_at_cell(self, pos))]

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
                if go_home_in_breaks == True:
                    go_to_entre(newAgent)
                if newAgent.has_more_courses_today == False:
                    go_to_entre(newAgent)
                return
            elif isinstance(self,canteen_Agent):
                    newAgent,seat_ = canteen_to_class(self)
                    #"push" agent through door
                    x,y = pos_                      #Door position
                    newY = random.randint(-1, 1)
                    newAgent.pos = x-1,y+newY
                    newAgent.seat = seat_[0]
                    newAgent.seat_coords = seat_[1]
                    newAgent.coords = dir['W']
                    self.model.grid.place_agent(newAgent, newAgent.pos)
                    return
        #If goal-position is the seat, go there
        if isinstance(self, class_Agent) and pos_ == self.seat:
            self.model.grid.move_agent(self,pos_)
            self.coords = self.seat_coords
            self.mask = False
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
    if isinstance(self, employee_Agent) and self.id not in [1252,1253]:
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

        self.infection_period = 0#How long are they sick?
        self.asymptomatic = 0 #Agents are asymptomatic for 5 days
        self.exposed = math.pi

        self.day_off = False
        self.moving_to_door = 0
        self.door = ()
        self.courses = [0,0]


        self.TA = ()
        self.seat = ()
        self.seat_coords = ()

        #Relevant for classroom only
        self.hasQuestion = False
        self.hasEnteredDoor = []
        self.reproduction = 0

    def move(self,timestep=False):

        start_pos = self.pos
        if timestep is True:
            if self.moving_to_door == 1: #Agents go to door
                move_to_specific_pos(self,self.door.pos)
                if with_mask == True:
                    self.mask = True
            elif self.moving_to_door == 0: #Agents go to seat
                move_to_specific_pos(self,self.seat)
        else: wander(self)
        if with_dir == True:
            end_pos = self.pos
            if self.pos != self.seat:
                self.coords = change_direction(self, start_pos, end_pos)


    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):
        if self.infected == True:
            update_infection_parameters(self)

        if is_off_campus(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,len(self.model.entre)-1)])

        if is_off_campus(self) == False and self.is_home_sick == False:
            if self.infected == True:
                if with_dir == True:
                    infect(self)
                else:
                    infect_(self)

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
        self.infection_period = 0#How long are they sick?
        self.asymptomatic = 0 #Agents are asymptomatic for 5 days
        self.exposed = math.pi #Dummy

        self.day_off = False
        self.timeToTeach = 5
        self.door = ()
        self.students = []
        self.coords = ()
        self.reproduction = 0

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
            if with_dir == True:
                end_pos = self.pos
                self.coords = change_direction(self, start_pos, end_pos)

    def step(self):
        if self.infected == True:
            update_infection_parameters(self)
        if is_off_campus(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,2)])
        self.time_remaining -=1
        self.connect_TA_and_students()

        if is_off_campus(self) == False and self.is_home_sick == False:
            if self.infected == True:
                if with_dir == True:
                    infect(self)
                else:
                    infect_(self)
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

        self.going_to_toilet = False
        self.in_toilet_queue = False
        self.sitting_on_toilet = 0
        self.since_last_toilet = 0

        self.off_school = 0
        self.coords = ()
        self.reproduction = 0

        #Infection parameters
        self.infection_period = 0#How long are they sick?
        self.asymptomatic = 0 #Agents are asymptomatic for 5 days
        self.exposed = math.pi

        #Class-schedule parameters
        self.next_to_attend_class = False
        self.day_off = False
        self.has_more_courses_today = True

        self.entre_door = ()
        self.door = ()
        self.courses = ()
        self.moving_to_door = 0
        self.TA = ()

    def update_queue_parameters(self):
        if self.model.minute_count in range(225,301):
            if self.pos in self.model.enter_canteen_area12: #in beginning of queue area at lunchbreak
                if self.off_school ==0 and self.is_home_sick ==0:
                    self.queue =1 #stands in line for canteen
        else:
            if self.pos in self.model.enter_canteen_area10: #in beginning of queue area at 10break
                if self.off_school ==0 and self.is_home_sick ==0:
                    self.queue =1 #stands in line for canteen
        if self.pos in [(23,j) for j in range(4,20)]: #already in queue area
            self.queue=1
        elif self.pos == (23,20):
            self.queue = 0 #done in line

    def go_to_toilet_queue(self):
        pos_ = self.model.toilet.queue[-1]
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        possible_empty_steps = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos) and pos not in self.model.toilet.queue[:-1]]
        if len(possible_empty_steps) == 0: #nowhere to go, stay
            return
        distances = [(pos,getDistance(pos_,pos)) for pos in possible_empty_steps]
        x_,y_ = min(distances,key=lambda x:x[1])[0]
        if min(getDistance((x_,y_), pos_), getDistance(self.pos, pos_)) == getDistance(self.pos, pos_): #Hvis du kun kan rykke længere væk
            return
        else:
            if (x_,y_) == pos_:
                if self.model.grid.is_cell_empty(pos_):
                    self.model.grid.move_agent(self,(x_,y_))
                    self.going_to_toilet = False
                    self.in_toilet_queue = True
                else:
                    return
            else:
                self.model.grid.move_agent(self,(x_,y_))

    def move_in_toilet_queue(self):
        if self.pos == self.model.toilet.queue[0]: #Forest i køen
            if len(self.model.grid.get_cell_list_contents(self.model.toilet.pos))<4:
                self.model.grid.move_agent(self,self.model.toilet.pos)
                self.in_toilet_queue = False
                self.sitting_on_toilet = 3
                self.since_last_toilet = 120
                if self.model.toilet.has_been_infected == True and self.infected == False:
                    if self.mask == True:
                        p = bernoulli.rvs(1/300)
                    else:
                        p = bernoulli.rvs(5/100)
                    if p == 1:
                        #print(self.model.day_count,self.model.minute_count,self.id,self.pos,"I got infected at the toilet")
                        self.infected == True
                if self.infected == True and self.exposed == 0 and self.model.toilet.has_been_infected == False:
                    #print(self.model.day_count,self.model.minute_count,self.id,self.pos,"I just infected the toilet")
                    self.model.toilet.has_been_infected = True

            else:
                return
        else:
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            next_queue_steps = [pos for pos in possible_steps if (self.model.grid.is_cell_empty(pos) or is_off_campus(get_agent_at_cell(self, pos))) and pos in self.model.toilet.queue]
            if len(next_queue_steps) == 0: #Nogle er foran dig og bag dig
                return
            else:
                pos_ = self.model.toilet.pos
                distances = [(pos,getDistance(pos_,pos)) for pos in next_queue_steps]
                x_,y_ = min(distances,key=lambda x:x[1])[0]
                if min(getDistance((x_,y_), pos_), getDistance(self.pos, pos_)) == getDistance(self.pos, pos_):
                    return #Der er nogen foran dig, men ikke nogen bagved dig
                self.model.grid.move_agent(self,(x_,y_))

    def move(self,timestep=False):
        if timestep is True: #Agents go to door
            if self.queue == 0 and self.sitting_in_canteen == 0:
                if with_mask == True:
                    self.mask = True
                move_to_specific_pos(self,self.door.pos)

            else:
                if self.in_toilet_queue == True:
                    force_agent_to_specific_pos(self,self.model.toilet.exit)
                self.queue = 0
                self.sitting_in_canteen = 0
                self.in_toilet_queue = False
                self.going_to_toilet = False
                self.sitting_on_toilet = 0
                move_to_specific_pos(self,self.door.pos)
        else:
            if (go_home_in_breaks == True or self.has_more_courses_today == False) and self.entre_door != ():
                go_to_entre(self)
            else:
                if self.going_to_toilet == True: #På vej til toiletkø
                    self.go_to_toilet_queue()
                elif self.in_toilet_queue == True:  #I kø til toilettet
                    self.move_in_toilet_queue()
                elif self.sitting_on_toilet>0: #Sidder på toa
                    self.sitting_on_toilet = max(0,self.sitting_on_toilet-1)
                    if self.sitting_on_toilet == 0:
                        self.model.grid.move_agent(self,self.model.toilet.exit)
                elif self.queue == 1:
                    if self.pos in [(23,j) for j in range(0,20)]:
                        move_in_queue(self, (23,20)) # moves towards end of canteen
                    else:
                        move_in_queue(self, (23,3))
                elif self.sitting_in_canteen > 45:
                    self.sitting_in_canteen = max(0, self.sitting_in_canteen-1)
                elif self.sitting_in_canteen in range(0,46):
                    self.sitting_in_canteen = max(0, self.sitting_in_canteen-1)
                    if with_mask == True:
                        self.mask = True
                    wander(self)


                else: wander(self)

    def step(self):
        self.since_last_toilet = max(0,self.since_last_toilet-1)
        if self.infected == True:
            update_infection_parameters(self)
        if go_home_in_breaks is False:
            self.update_queue_parameters()

        if is_off_campus(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,len(self.model.entre)-1)])

        start_pos = self.pos #for changing direction

        if is_off_campus(self) == False and self.is_home_sick == False:
            if self.infected == True:
                if with_dir == True:
                    infect(self)
                else:
                    infect_(self)


            #When should canteen agent go to class?
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
        try:
            if self.pos[0]<8 and self.pos[1]>32:
                force_agent_to_specific_pos(self,self.model.toilet.exit)
        except:
            pass
        if with_dir == True and self.sitting_in_canteen <= 45:
            end_pos = self.pos
            self.coords = change_direction(self, start_pos, end_pos)

class employee_Agent(Agent):
    def __init__(self,id,model):
        super().__init__(id,model)
        self.id = id
        self.infected = False
        self.recovered = False
        self.mask = False
        self.is_home_sick = False
        self.vaccinated = False

        self.infection_period = 0#How long are they sick?
        self.asymptomatic = 0 #Agents are asymptomatic for 5 days
        self.exposed = math.pi
        self.reproduction = 0

        self.coords = ()

    def step(self):
        if is_off_campus(self):
            return
        if self.infected == True:
            if with_dir == True:
                infect(self)
            else:
                infect_(self)
            update_infection_parameters(self)


        if self.id %2 == 0:
            self.move()
        if self.id in [1252,1253] and len(self.model.canteen_agents_at_work)==2: #if both other employees is at work
            self.model.canteen_backups_to_go_home.append(self)


    def move(self):
        start_pos = self.pos
        wander(self)
        if with_dir == True:
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

class toilet(Agent):
    def __init__(self,id, model):
        super().__init__(id,model)
        self.id = id
        self.model = model
        self.queue = []
        self.has_been_infected = False
        self.exit = ()
