from mesa import Agent, Model
import math
from mesa.space import MultiGrid
import numpy as np
import random
from operator import itemgetter
import sys
from Model import covid_Model,with_mask,is_student, is_off_campus, is_human, dir,students_who_has_question_count, infection_rate, infection_rate_1_to_2_meter, infection_rate_2plus_meter, infection_decrease_with_mask_pct, calculate_percentage, with_dir, go_home_in_breaks
from scipy.stats import truncnorm,bernoulli

day_length = 525
#other_courses = random.sample([4]*26+[5]*26+[6]*26,k=len([4]*26+[5]*26+[6]*26))
#ids = [i for i in range(0,78)]

##Helper functions
def calc_distance(pos1, pos2):
    '''
    Calculate the euclidean distance between two points in 2D space

    :param pos1: a tuple
    :param pos2: a tuple
    :return: the distance in float
    '''
    
    x1,y1 = pos1
    x2,y2 = pos2
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def update_direction(self, start_pos, end_pos):
    '''
    Update the direction based on how the agent moves

    :param self: agent-object
    :param start_pos: a tuple
    :param end_pos: a tuple
    :return: A tuple indicating the direction
    '''

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

def calc_angle(self_direction, other_agent_direction):
    '''
    Calculate the angle between two agents based on their direction

    :param self_direction: a tuple
    :param other_agent_direction: a tuple
    :return: An angle (float)
    '''

    ang1 = np.arctan2(*self_direction[::-1])
    ang2 = np.arctan2(*other_agent_direction[::-1])
    return ((ang1 - ang2) % (2 * np.pi))

def get_agent_at_cell(self,pos):
    '''
    Get the agent located at a specific position in the grid

    :param self: agent-object
    :param pos: a tuple
    :return: agent-object
    '''
    return self.model.grid.get_cell_list_contents(pos)[0]

def truncnorm_(a,b,mu,sigma):
    '''
    Generates a float number from a truncated normal distribution

    :param a: integer, lower bound
    :param b: integer, upper bound
    :param mu: integer, mean value
    :param sigma: integer, standard deviation
    :return: a float
    '''

    alpha, beta = (a-mu)/sigma, (b-mu)/sigma
    return math.floor(truncnorm.rvs(alpha,beta,loc=mu,scale=sigma))
def wander(self):
    '''
    Moves an agent randomly to a possible position in the grid

    :param self: agent-object
    :return: None
    '''
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

    if go_home_in_breaks is False and self.pos in [x for (x,y) in self.model.canteen_tables] and self.sitting_in_canteen == 0:
        set_parameters_sitting_in_canteen(self)
def set_parameters_sitting_in_canteen(self):
    '''
    Set direction and timer on agent who just sat down at table in canteen
    Depending on what time of the day the agent sits down and what table the agent sits with,
    these two parameters will change

    :param self: agent-object
    :return: None
    '''

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

def infect(self):
    '''
    Finds all susceptible neighbors within distance of 2 (meter) from infectious agent and calculates mu based on
    direction and distance from infectious agent. Then decides if neighbor is getting infected by random variable bernoulli(mu)

    :param self: agent-object
    :return: None
    '''

    "Agent doesn't infect yet"
    if self.non_contageous_period != 0:
        return
    "Agent is off campus, thus cannot infect"
    if (self.is_home_sick == True) or (isinstance(self,canteen_Agent) and self.off_school == True) or (go_home_in_breaks == True and self.pos in self.model.entre):
        return

    "Get the correct neighbors based on what type of agent 'self' is."
    if isinstance(self, TA):
        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=True,radius=2)
        all_neighbors_within_radius = [n for n in all_neighbors_within_radius if isinstance(n,class_Agent)]
    else:
        all_neighbors_within_radius = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False,radius=2)
    if isinstance(self,class_Agent):
        all_neighbors_within_radius = [n for n in all_neighbors_within_radius if (isinstance(n,class_Agent) and n.courses[0] == self.courses[0]) or (isinstance(n,TA) and n.door.id == self.door.id)]
    elif isinstance(self,canteen_Agent):
        all_neighbors_within_radius = [n for n in all_neighbors_within_radius if not isinstance(n,TA) and not isinstance(n,class_Agent)]



    "Only infect your own squad (A or B) when day is changing"
    if self.model.minute_count in list(range(0,60)):
        if self.id in list(range(0,(len(self.model.setUpType)*self.model.n_agents)))+[1001,1002,1003]:
            all_neighbors_within_radius = [n for n in all_neighbors_within_radius if n.id in list(range(0,(len(self.model.setUpType)*self.model.n_agents)))+[1001,1002,1003]]
        elif self.id in list(range((len(self.model.setUpType)*self.model.n_agents)+1,2*(len(self.model.setUpType)*self.model.n_agents)))+[1004,1005,1006]:
            all_neighbors_within_radius = [n for n in all_neighbors_within_radius if n.id in list(range((len(self.model.setUpType)*self.model.n_agents)+1,2*(len(self.model.setUpType)*self.model.n_agents)))+[1004,1005,1006]]


    "Extract all the humans within radius"
    all_humans_within_radius = []
    for neighbor in all_neighbors_within_radius:
        if is_human(neighbor):
            #Dont infect neighbors that are home sick / not on campus
            if neighbor.is_home_sick == True or (isinstance(neighbor,canteen_Agent) and neighbor.off_school == True) or (go_home_in_breaks == True and neighbor.pos in neighbor.model.entre):
                continue
            #Dont infect neighbors that are vaccinated, recorvered or infected
            if neighbor.vaccinated == True or neighbor.recovered == True or neighbor.infected == True: # kan ikke blive smittet, da den er immun eller allerede infected
                continue
            if not self.model.grid.is_cell_empty(neighbor.pos):
                    all_humans_within_radius.append(neighbor)

    "Define infection rates depending on agent's parameters (mask and asymptomatic)"
    if self.mask == True:
        if self.asymptomatic:
            ir = calculate_percentage(calculate_percentage(infection_rate, infection_decrease_with_mask_pct),25)
            ir1_2 = calculate_percentage(calculate_percentage(infection_rate_1_to_2_meter, infection_decrease_with_mask_pct),25)
            ir2_plus = calculate_percentage(calculate_percentage(infection_rate_2plus_meter, infection_decrease_with_mask_pct),25)
        else:
            ir = calculate_percentage(infection_rate, infection_decrease_with_mask_pct)
            ir1_2 = calculate_percentage(infection_rate_1_to_2_meter, infection_decrease_with_mask_pct)
            ir2_plus = calculate_percentage(infection_rate_2plus_meter, infection_decrease_with_mask_pct)
    else:
        if self.asymptomatic:
            ir = calculate_percentage(infection_rate, 25)
            ir1_2 = calculate_percentage(infection_rate_1_to_2_meter, 25)
            ir2_plus = calculate_percentage(infection_rate_2plus_meter, 25)
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
        if agent.mask == True:
            ir = calculate_percentage(ir,15)
        if bernoulli.rvs(ir*10) == 1:
            newly_infected.append(agent)
            self.model.infected_agents.append(agent)
    for agent in N_list:
        distance = calc_distance(self.pos, agent.pos)
        if calc_angle(self.coords, agent.coords) == math.pi: #10xir
            if 1 <= distance <= 2:
                if bernoulli.rvs(ir1_2*10) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
            else:
                if bernoulli.rvs(ir2_plus*10) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)

        elif calc_angle(self.coords, agent.coords) in [math.pi * 5 / 4, math.pi * 3 / 4]: #8x ir
            if 1 <= distance <= 2:
                if bernoulli.rvs(ir1_2*8) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
            else:
                if bernoulli.rvs(ir2_plus*8) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
        elif calc_angle(self.coords, agent.coords) in [math.pi * 3 / 2, math.pi / 2]: #6xir
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
            distance = calc_distance(self.pos, agent.pos)
            if calc_angle(self.coords, agent.coords) == math.pi*3/4: #7xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*7) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*7) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif calc_angle(self.coords, agent.coords) in [math.pi, math.pi / 2]: #5xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*5) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*5) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif calc_angle(self.coords, agent.coords) in [math.pi / 4, math.pi * 5 / 4]: #3xir
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
            distance = calc_distance(self.pos, agent.pos)
            if (isinstance(self, class_Agent) and self.pos in self.model.classroom_2+self.model.classroom_3+self.model.classroom_4) or self.pos in self.model.canteen_tables:# if nextdoor neighbor in class
                if distance <2:
                    if bernoulli.rvs(ir1_2*10) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                    continue

            if calc_angle(self.coords, agent.coords) == math.pi/2: #4xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*4) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*4) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif calc_angle(self.coords, agent.coords) in [math.pi / 4, math.pi * 3 / 4]: #3xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif calc_angle(self.coords, agent.coords) in [0, math.pi]: #2xir
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
    for agent in Behind_list:
        distance = calc_distance(self.pos, agent.pos)
        if 1 <= distance <= 2:
                if bernoulli.rvs(ir1_2) == 1:
                    newly_infected.append(agent)
                    self.model.infected_agents.append(agent)
        else:
                if bernoulli.rvs(ir2_plus) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
    for agent in W_list:
            distance = calc_distance(self.pos, agent.pos)
            if (isinstance(self, class_Agent) and self.pos in self.model.classroom_2+self.model.classroom_3+self.model.classroom_4) or self.pos in self.model.canteen_tables:
                if distance <2:
                    if bernoulli.rvs(ir1_2*10) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                continue
            if calc_angle(self.coords, agent.coords) == math.pi*3/2: #4xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*4) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*4) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif calc_angle(self.coords, agent.coords) in [math.pi * 7 / 4, math.pi * 5 / 4]: #3xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*3) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif calc_angle(self.coords, agent.coords) in [0, math.pi]: #2xir
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
            distance = calc_distance(self.pos, agent.pos)
            if calc_angle(self.coords, agent.coords) == math.pi*5/4: #7xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*7) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*7) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif calc_angle(self.coords, agent.coords) in [math.pi, math.pi * 3 / 2]: #5xir
                if 1 <= distance <= 2:
                    if bernoulli.rvs(ir1_2*5) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
                else:
                    if bernoulli.rvs(ir2_plus*5) == 1:
                        newly_infected.append(agent)
                        self.model.infected_agents.append(agent)
            elif calc_angle(self.coords, agent.coords) in [math.pi * 7 / 4, math.pi * 3 / 4]: #3xir
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
    if self.pos in self.model.canteen_tables:
        print(self.id,self.pos,self.model.day_count,self.model.minute_count,"Im sitting and chillin and Im sick!")

    for a in newly_infected:
        self.reproduction =+ 1
        if a.mask and bernoulli(0.15) == 1:
            continue
        a.infected = True
        if bernoulli.rvs(0.3) == 1:
            a.asymptomatic = True
            a.infection_period = truncnorm_(5 * day_length, 21*day_length, 10*day_length, 2*day_length) #How long are they sick?
            a.incubation_period = a.infection_period
            a.non_contageous_period = 2 * day_length
        else:
            a.incubation_period = truncnorm_(3 * day_length, 11.5*day_length, 5*day_length, 1*day_length) #Agents are asymptomatic for 5 days
            a.infection_period = a.incubation_period + 10*day_length
            a.non_contageous_period = a.incubation_period - 2 * day_length
        if a.pos in self.model.canteen_tables:
            print(a.pos,self.pos,"it happened")
            self.canteen_counter = self.canteen_counter+1

"CHANGING OBJECT-TYPE"
def change_obj_params(new,old):
    '''
    Function called when objects change from class-to-canteen, canteen-to-class, TA-to-class, canteen-to-TA
    Transfer essential parameters from old object type to new

    :param new: agent-object
    :param old: agent-object
    :return: None
    '''
    new.is_home_sick, new.vaccinated = old.is_home_sick,\
                                       old.vaccinated

    new.infection_period,new.non_contageous_period, new.incubation_period = old.infection_period, \
                                                              old.non_contageous_period, \
                                                              old.incubation_period

    new.infected, new.recovered,  new.mask = old.infected,\
                                             old.recovered,\
                                             old.mask
    new.reproduction = old.reproduction
    new.day_off = old.day_off
    new.pos = old.pos
    new.asymptomatic = old.asymptomatic

def canteen_to_class(self):
    '''
    Copy canteen object to class object

    :param self: canteen-object
    :return: None
    '''

    "Which classroom are agent entering, adjust the y-coordinate accordingly."
    i = self.door.id-501

    try:
        seat = self.model.seats[i].pop()

        c_agent = class_Agent(self.id, self.model)
        change_obj_params(c_agent,self)

        c_agent.courses = self.courses
        c_agent.leaving_class = False
        c_agent.door = self.door

        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)
        self.model.schedule.add(c_agent)

        return c_agent,seat
    except:
        seat = ()
        print(self.model.day_count, self.model.minute_count,self.day_off,self.next_to_attend_class,self.pos,self.id)
        agents = [a for a in self.model.schedule.agents if is_human(a)]
        newlist = sorted(agents, key=lambda a: a.id, reverse=True)
        return self, seat

def class_to_canteen(self):
    '''
    Copy class object to canteen object

    :param self: class-object
    :return: None
    '''

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
        next_door_id = self.door.id ##TA has the same door throughout (always go to same classroom)

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

def TA_to_class(self):
    '''
    Copy TA object to class object

    :param self: TA-object
    :return: None
    '''

    c_agent = class_Agent(self.id, self.model)
    change_obj_params(c_agent,self)

    c_agent.door, c_agent.leaving_class = self.door, True

    self.model.grid.remove_agent(self)
    self.model.schedule.remove(self)
    self.model.TAs.remove(self)

    self.model.schedule.add(c_agent)
    self.model.grid.place_agent(c_agent,c_agent.pos)
    c_agent.coords = dir['E']

def canteen_to_TA(self):
    '''
    Copy canteen object to TA object

    :param self: canteen-object
    :return: None
    '''

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

def move_to_entre(self):
    '''
    Move agent one step closer to a randomly chosen entré-position

    :param self: agent-object
    :return: None
    '''
    if self.entre_door == ():
        self.entre_door = self.model.entre[random.randint(0,len(self.model.entre)-1)]

    pos_ = self.entre_door
    possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    possible_empty_steps = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos) or pos == pos_]

    "Back up list if list of possible steps are empty"
    if len(possible_empty_steps) == 0:
          pos_other_agents = [cell for cell in self.model.grid.get_neighbors(self.pos,moore=True,include_center=False) if is_human(cell)]
          possible_empty_steps = [cell.pos for cell in pos_other_agents]

    distances = [(pos, calc_distance(pos_, pos)) for pos in possible_empty_steps]
    x_,y_ = min(distances,key=lambda x:x[1])[0]
    if min(calc_distance((x_, y_), pos_), calc_distance(self.pos, pos_)) == calc_distance(self.pos, pos_):
        return
    else:
        self.model.grid.move_agent(self,(x_,y_))
        if self.pos == pos_:
            self.off_school = True
            self.entre_door = ()

def move_for_class(self, position):
    '''
    Invoked when an agent is moving either towards, in or from classroom

    :param self: agent-object
    :param position: a tuple
    :return: None
    '''
    possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    possible_empty_steps = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos) or is_off_campus(get_agent_at_cell(self, pos))]

    #If no cell is empty, agent can go through others human-agents (to avoid bottleneck)
    #Back-up list contains cells with covid,TA and canteen agents in
    pos_other_agents = [cell for cell in self.model.grid.get_neighbors(self.pos,moore=True,include_center=False)
                        if is_human(cell)]
    back_up_empty_cells = [cell.pos for cell in pos_other_agents]

    if position in possible_steps:
        if position == self.door.pos:
            if isinstance(self, class_Agent):
                newAgent = class_to_canteen(self)
                x,y = position
                newY = random.randint(-1, 1)
                newAgent.pos = x+1,y+newY
                newAgent.coords = dir['E']
                self.model.grid.place_agent(newAgent, newAgent.pos)
                if go_home_in_breaks == True:
                    move_to_entre(newAgent)
                if newAgent.has_more_courses_today == False:
                    move_to_entre(newAgent)
                return
            elif isinstance(self,canteen_Agent) and self.id in [1001,1002,1003,1004,1005,1006]:
                    newAgent = canteen_to_TA(self)
                    x,y = position
                    newY = random.randint(-1, 1)
                    newAgent.pos = x-1,y+newY
                    newAgent.coords = dir['W']
                    newAgent.mask = with_mask  #From model
                    self.model.grid.place_agent(newAgent, newAgent.pos)
                    return
            elif isinstance(self,canteen_Agent):
                    newAgent,seat_ = canteen_to_class(self)
                    if seat_ == ():
                        print(self.model.day_count,self.model.minute_count,self, "JEG BLEV LAVET OM",self.id,self.pos,self.courses)
                        move_to_entre(self)
                    else:
                        x,y = position
                        newY = random.randint(-1, 1)
                        newAgent.pos = x-1,y+newY
                        newAgent.seat = seat_[0]
                        newAgent.seat_coords = seat_[1]
                        newAgent.coords = dir['W']
                        self.model.grid.place_agent(newAgent, newAgent.pos)
                    return

        #If goal-position is the seat, go there
        if isinstance(self, class_Agent) and position == self.seat:
            self.model.grid.move_agent(self, position)
            self.coords = self.seat_coords
            self.mask = False
            return

    #If you are already at your seat, stay there
    if position == self.pos:
        return


    "Agent is moving one step closer to goal-position"
    #If possible_empty_steps is empty, use back-up list (allowing agent to go through agents)
    if len(possible_empty_steps) == 0:
        cells_to_check = back_up_empty_cells
    else: cells_to_check = possible_empty_steps

    #Distances from all possible positions and goal-position
    distances = [(pos, calc_distance(position, pos)) for pos in cells_to_check]

    #Get x,y position of the cell with the smallest distance between goal-position and possible cells to go to
    x_,y_ = min(distances,key=lambda x:x[1])[0]

    #Force agent to goal_pos - avoid logic flaw when agent is flipping back and forth between two positions
    if self.model.minute_count in [40,160,340,470]:
        x,y = position
        force_agent_to_specific_pos(self,(x+1,y))
        return
    self.model.grid.move_agent(self,(x_,y_))

def force_agent_to_specific_pos(self,pos):
    '''
    Moves an agent from its current position to a new specified position

    :param self: agent-object
    :param pos: a tuple - the position the agent is to be moved to
    :return: None
    '''
    self.model.grid.move_agent(self,pos)

def send_agent_home(self):
    '''
    If an agent is showing symptoms, set an agents parameter is_home_sick to True, thus making the agent go home.
    If agent going home is an employee, create a back-up employee

    :param self: agent-object
    :return: None
    '''
    if self.asymptomatic == True:
        return
    self.is_home_sick = True
    self.model.agents_at_home.append(self)

    if isinstance(self, employee_Agent) and self.id not in [1252,1253]:
        newLunchlady = employee_Agent(self.id+2,self.model)
        newLunchlady.coords = dir['W']
        self.model.schedule.add(newLunchlady)
        self.model.grid.place_agent(newLunchlady, self.pos)
        if self in self.model.canteen_agents_at_work:
            self.model.canteen_agents_at_work.remove(self)

def send_agent_back_to_school(self):
    '''
    Agents who have been home sick are now ready to go back to school.
    Agent is now recovered.

    :param self: agent-object
    :return: None
    '''

   # newList_at_home = [a for a in self.model.agents_at_home if a.id != self.id]
    #self.model.agents_at_home = newList_at_home

    self.model.recovered_agents.append(self)
    self.is_home_sick = False
    self.infected = False
    self.recovered = True
    if isinstance(self, employee_Agent) and (self.id==1250 or self.id==1251):
        self.model.canteen_agents_at_work.append(self)

def update_infection_parameters(self):
    '''
    Update an infected agent's infection_period, incubation_period and non_contageous_period.

    :param self: agent-object
    :return: None
    '''

    if self.recovered == True:
        return              #Agent is recovered

    if self.is_home_sick == True: #Agent is already home. Just update infection period
        self.infection_period = max(0,self.infection_period-1)
        if self.infection_period == 0:
            send_agent_back_to_school(self)
        return

    if self.asymptomatic == True:       #Agent is asymptomatic
        self.infection_period = max(0,self.infection_period-1)
        if self.infection_period == 0: #Agent is not sick any more
            self.infected = False
            self.recovered = True
            self.model.recovered_agents.append(self)
            self.is_home_sick = False #should always be false
        return

    self.incubation_period = max(0, self.incubation_period - 1)
    if self.incubation_period == 0:
        send_agent_home(self)
    self.non_contageous_period = max(0, self.non_contageous_period - 1)
    self.infection_period = max(0,self.infection_period-1)

class class_Agent(Agent):
    '''
    A class to represent the agents attending class as students

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    infected: bool
        States if the agent is infected or not
    asymptomatic : bool
        States if the agent is going to show symptoms or not
    recovered : bool
        States if the agent is recovered from the disease or not
    vaccinated : bool
        States if the agent is vaccinated or not
    is_home_sick : bool
        States if the agent is home sick or not
    mask : bool
        States if the agent is wearing a mask or not
    infection_period : int
        The number of timesteps the agent is infected (only invoked if agent gets infected)
    incubation_period : int
        The number of timesteps the agent is asymptomatic and thus infect others without knowing it (only invoked if agent gets infected)
    non_contageous_period : int
        The number of timesteps the agent does not infect or show symptoms (only invoked if agent gets infected)
    reproduction : int
        The number of individuals the agent infects
    coords : tuple ()
        Direction of the agent
    day_off : bool
         States if the agent has the day off (from school)
    door : door-object
        The door to the classroom the agent is attending class in next
    courses : list []
        List of the two courses the agent is attending (specifies which classroom)
    leaving_class : bool
        States if the agent is going to class or not
    seat : tuple ()
        The position of the seat the agent will sit on
    seat_coords : tuple ()
        Direction of that agent's seat
    TA : TA-object
        The TA of the class the agent is attending
    has_question : bool
        States if the agent has a question or not
    '''
    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id
        self.model = model

        self.infected = False
        self.asymptomatic = False #Does the agent show symptoms during infection period?
        self.recovered = False
        self.vaccinated = False
        self.is_home_sick = False
        self.mask = False

        self.infection_period = 0
        self.incubation_period = math.pi
        self.non_contageous_period = math.pi
        self.reproduction = 0
        self.coords = ()

        self.day_off = False
        self.door = ()
        self.courses = [0,0]
        self.leaving_class = False

        self.seat = ()
        self.seat_coords = ()

        self.TA = ()
        self.has_question = False

    def move(self, move_in_class=False):
        '''
        Called every time step. Depending on agent's state and objective, move agent accordingly

        :param self: class-object
        :optional param leave_class: bool
        :return: None
        '''
        start_pos = self.pos
        if move_in_class:
            if self.leaving_class == True: #Agents go to door
                move_for_class(self, self.door.pos)
                if with_mask:
                    self.mask = True
            elif self.leaving_class == False: #Agents go to seat
                move_for_class(self, self.seat)
        else: wander(self)
        if with_dir:
            end_pos = self.pos
            if self.pos != self.seat:
                self.coords = update_direction(self, start_pos, end_pos)

    def step(self):
        ''''
        Invoked every time step and is multi-purposed.
        Update agent's parameters and handle if the agent is off_campus.
        Invoke infect-function if agent is infectious and present at campus.
        Keep track of and change direction of agent.
        Invoke move-function.

        :param self: class-object
        :return: None
        '''
        if self.infected == True:
            update_infection_parameters(self)

        if is_off_campus(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,len(self.model.entre)-1)])

        if is_off_campus(self) == False and self.is_home_sick == False:
            if self.infected == True:
                infect(self)

        "Move the agent"
        if self.model.day_count == 1:
            if self.model.minute_count in self.model.class_times and self.model.minute_count%2 == 1:
                self.leaving_class = True

        elif self.model.day_count > 1 and self.model.minute_count in self.model.class_times+[1] and self.model.minute_count%2 == 1:
            self.leaving_class = True

        self.move(True)
class TA(Agent):
    '''
    A class to represent the TA-agents

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    infected: bool
        States if the agent is infected or not
    asymptomatic : bool
        States if the agent is going to show symptoms or not
    recovered : bool
        States if the agent is recovered from the disease or not
    vaccinated : bool
        States if the agent is vaccinated or not
    is_home_sick : bool
        States if the agent is home sick or not
    mask : bool
        States if the agent is wearing a mask or not
    infection_period : int
        The number of timesteps the agent is infected (only invoked if agent gets infected)
    incubation_period : int
        The number of timesteps the agent is asymptomatic and thus infect others without knowing it (only invoked if agent gets infected)
    non_contageous_period : int
        The number of timesteps the agent does not infect or show symptoms (only invoked if agent gets infected)
    reproduction : int
        The number of individuals the agent infects
    day_off : bool
         States if the agent has the day off (from school)
    time_remaining : int

    time_to_teach : int
        The number of timesteps each student is given when asking a question
    door : door-object
      The door to the classroom the agent is attending class in next
    courses : List []
         List of the two courses the agent is attending (specifies which classroom)
    students : List []
         List of the students the agent is teaching at the moment
    coords : tuple ()
        Direction of the agent
    '''
    def __init__(self,id,model):
        super().__init__(id,model)
        self.id = id
        self.model = model

        self.infected = False
        self.asymptomatic = False
        self.recovered = False
        self.vaccinated = False
        self.is_home_sick = False

        self.mask = False

        self.infection_period = 0#How long are they sick?
        self.incubation_period = math.pi #Agents are asymptomatic for 5 days
        self.non_contageous_period = math.pi #Dummy
        self.reproduction = 0

        self.day_off = False

        self.time_remaining = 105
        self.time_to_teach = 5

        self.door = ()
        self.courses = []
        self.students = []
        self.coords = ()

    def move_to_student(self,student):
        '''
        Go to the student who asked a question

        :param self: TA-object
        :param student: class-object
        :return: None
        '''
        x,y = student.pos
        if self.time_to_teach == 0: #Student has recieved help for 5 minutes
            student.has_question = False            #Student does not have question anymore
            self.time_to_teach = 5          #Reset timer

        elif self.time_to_teach == 5:   #Go to that student and answer question
            newTA = self
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            self.model.schedule.add(newTA)
            self.model.grid.place_agent(newTA,(x,y))
            self.time_to_teach -= 1
        else:  #Student is still recieving help, subtract one minut and stay put
            self.time_to_teach -= 1

    def connect_TA_and_students(self):
        '''
        Every time a class starts, connect the TA with the correct students (allows for questions)

        :param self: TA-object
        :return: None
        '''
        students_in_class = [a for a in self.model.schedule.agents if isinstance(a, class_Agent) and a.door == self.door]

        #Get the correct students, because they can overlap when a class is ending and new one is starting
        if self.id in [1001,1002,1003]:
            self.students = [a for a in students_in_class if a.id in range(0,(self.model.n_agents+1)*3) and a.is_home_sick == False]
        elif self.id in [1004,1005,1006]:
            self.students = [a for a in students_in_class if a.id not in range(0,(self.model.n_agents+1)*3) and a.is_home_sick == False]

        #Apply TA to students
        for s in self.students:
            s.TA = self

    def move(self):
        '''
        Move the TA. Either the TA wanders around or else the TA answers a question from a student.

        :param self: TA-object
        :return: None
        '''
        question_count = students_who_has_question_count(self.model, self.students)

        if question_count > 0 and len(self.students) > 15:  #Class is started and somebody has a question
            for s in self.students:
                if s.has_question:
                    self.move_to_student(s)
                    self.coords = s.coords
        else:
            start_pos = self.pos
            wander(self)
            if with_dir:
                end_pos = self.pos
                self.coords = update_direction(self, start_pos, end_pos)

    def step(self):
        '''
        Invoked every timestep and is multi-purposed.
        Update parameters accordingly.
        If agent is infected, the infect-function is invoked.
        Connect TA and students.
        When class has ended and students have left the room, TA-duty is over, hence turn TA-object into class-object.

        :param self: TA-object
        :return: None
        '''

        if self.infected:
            update_infection_parameters(self)
        if is_off_campus(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,2)])

        self.connect_TA_and_students()

        if is_off_campus(self) == False and self.is_home_sick == False:
            if self.infected:
                infect(self)

        if self.time_remaining <= 0 and len(self.students)<5:
            TA_to_class(self)
            return
        self.move()
        self.time_remaining -=1
class canteen_Agent(Agent):
    '''
    A class to represent the students in the canteen-area

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    infected: bool
        States if the agent is infected or not
    asymptomatic : bool
        States if the agent is going to show symptoms or not
    recovered : bool
        States if the agent is recovered from the disease or not
    vaccinated : bool
        States if the agent is vaccinated or not
    is_home_sick : bool
        States if the agent is home sick or not
    mask : bool
        States if the agent is wearing a mask or not
    infection_period : int
        The number of timesteps the agent is infected (only invoked if agent gets infected)
    incubation_period : int
        The number of timesteps the agent is asymptomatic and thus infect others without knowing it (only invoked if agent gets infected)
    non_contageous_period : int
        The number of timesteps the agent does not infect or show symptoms (only invoked if agent gets infected)
    reproduction : int
        The number of individuals the agent infects
    coords : tuple ()
        Direction of the agent
    queue : bool
        States if the agent is queuing in canteen or not
    buying_lunch : int
        The number of timesteps it takes to make a purchase at the desk in the canteen (only invoked if agent is queuing in the canteen)
    sitting_in_canteen : int
        The number of timesteps the agent is sitting at one of the tables in the canteen (only invoked when agent sits down)
    going_to_toilet : bool
         States if the agent is going to the toilet or not
    in_toilet_queue : bool
         States if the agent is queuing for the toilet or not
    sitting_on_toilet : int
         The number of timesteps the agent is still in the toilet (only invoked when agent is at toilet)
    since_last_toilet : int
        The number of timesteps until the agent can feel the need to go to toilet again
    off_school : bool
         States if the agent is off campus or not
    next_to_attend_class : bool
         States if the agent is going to attend class next or not
    day_off : bool
         States if the agent has the day off (from school)
    has_more_courses_today : bool
         States if the agent has more courses that day or not

    entre_door : tuple ()
        The position (in the entre) the agent goes to when leaving campus
    door : door-object
        The door to the classroom the agent is attending class in next
    courses : list []
        List of the two courses the agent is attending (specifies which classroom)
    going_to_class : bool
        States if the agent is going to class or not
    TA : TA-object
        The TA which will be the TA of the class the agent is attending next
    '''
    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id
        self.model = model

        self.infected = False
        self.asymptomatic = False
        self.recovered = False
        self.vaccinated = False
        self.is_home_sick = False
        self.mask = False


        self.infection_period = 0
        self.incubation_period = math.pi
        self.non_contageous_period = math.pi
        self.reproduction = 0

        self.coords = ()
        self.queue = False
        self.buying_lunch = 0
        self.sitting_in_canteen = 0

        self.going_to_toilet = False
        self.in_toilet_queue = False


        self.sitting_on_toilet = 0
        self.since_last_toilet = 0

        #Class-schedule parameters
        self.off_school = False
        self.next_to_attend_class = False
        self.day_off = False
        self.has_more_courses_today = True

        self.entre_door = ()
        self.door = ()
        self.courses = []
        self.going_to_class = False
        self.TA = ()

    def check_if_agent_is_queuing(self):
        '''
        If an agent is in the pre-defined canteen area, set the agent to stand in line for buying food.
        Update an agent's queue parameters when the agent is queuing in the line in the canteen

        :param self: canteen-object
        :return: None
        '''

        if self.model.minute_count in range(225,301):
            if self.pos in self.model.enter_canteen_area12: #in beginning of queue area at lunchbreak
                if self.off_school ==False and self.is_home_sick ==False:
                    self.queue = True #stands in line for canteen
        else:
            if self.pos in self.model.enter_canteen_area10: #in beginning of queue area at 10break
                if self.off_school == False and self.is_home_sick == False:
                    self.queue = True #stands in line for canteen

        if self.pos in [(23,j) for j in range(4,20)]: #already in queue area
            self.queue= True
        elif self.pos == (23,20):
            self.queue = False #done in line

    def move_to_toilet(self):
        '''
        Go one step closer to the toilet queue

        :param self: canteen-object
        :return: None
        '''
        pos_ = self.model.toilet.queue[-1]
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        possible_empty_steps = [pos for pos in possible_steps if self.model.grid.is_cell_empty(pos) and pos not in self.model.toilet.queue[:-1]]
        if len(possible_empty_steps) == 0: #nowhere to go, stay
            return
        distances = [(pos, calc_distance(pos_, pos)) for pos in possible_empty_steps]
        x_,y_ = min(distances,key=lambda x:x[1])[0]
        if min(calc_distance((x_, y_), pos_), calc_distance(self.pos, pos_)) == calc_distance(self.pos, pos_): #Hvis du kun kan rykke længere væk
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

    def use_toilet(self):
        '''
        Use and possibly infect the toilet

        :param self: canteen-object
        :return: None
        '''
        if len(self.model.grid.get_cell_list_contents(self.model.toilet.pos))<4:
            self.model.grid.move_agent(self,self.model.toilet.pos)
            self.in_toilet_queue = False
            self.sitting_on_toilet = 3
            self.since_last_toilet = 120
            if self.model.toilet.has_been_infected == True and self.infected == False and self.vaccinated == False:
                if self.mask:
                    p = bernoulli.rvs(1/300)
                else:
                    p = bernoulli.rvs(5/100)
                if p == 1:
                    self.infected = True
                    self.model.toilet.counter = self.model.toilet.counter+1
                    if bernoulli.rvs(0.3) == 1:
                        self.asymptomatic = True
                        self.infection_period = truncnorm_(5 * day_length, 21*day_length, 10*day_length, 2*day_length) #How long are they sick?
                        self.incubation_period = self.infection_period
                        self.non_contageous_period = 2 * day_length
                    else:
                        self.incubation_period = truncnorm_(3 * day_length, 11.5*day_length, 5*day_length, 1*day_length) #Agents are asymptomatic for 5 days
                        self.infection_period = self.incubation_period+10*day_length
                        self.non_contageous_period = self.incubation_period - 2 * day_length
            if self.infected and self.non_contageous_period == 0 and self.model.toilet.has_been_infected == False:
                self.model.toilet.has_been_infected = True
        else:
            return

    def move_in_toilet_queue(self):
        '''
        Move one step in the toilet queue if possible. If agent is the first in the line, the agent uses the toilet.

        :param self: canteen-object
        :return: None
        '''
        if self.pos == self.model.toilet.queue[0]: #Forest i køen
            self.use_toilet()
        else:
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            next_queue_steps = [pos for pos in possible_steps if (self.model.grid.is_cell_empty(pos) or is_off_campus(get_agent_at_cell(self, pos))) and pos in self.model.toilet.queue]
            if len(next_queue_steps) == 0: #Nogle er foran dig og bag dig
                return
            else:
                pos_ = self.model.toilet.pos
                distances = [(pos, calc_distance(pos_, pos)) for pos in next_queue_steps]
                x_,y_ = min(distances,key=lambda x:x[1])[0]
                "There is someone in front of you, but not behind you"
                if min(calc_distance((x_, y_), pos_), calc_distance(self.pos, pos_)) == calc_distance(self.pos, pos_):
                    return
                self.model.grid.move_agent(self,(x_,y_))

    def move_in_canteen_queue(self, pos_):
        '''
        Move one step in canteen queue

        :param self: canteen-object
        :param pos_: a tuple
        :return: None
        '''
        if self.buying_lunch != 0:
            self.buying_lunch -= 1
            if self.buying_lunch == 0:
                self.coords = dir['N']
        else:
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            possible_empty_steps = [cell for cell in possible_steps if self.model.grid.is_cell_empty(cell)]
            if len(possible_empty_steps) == 0: #if someone in front of you - dont move
                return
            distances = [(pos, calc_distance(pos_, pos)) for pos in possible_empty_steps]
            x_,y_ = min(distances,key=lambda x:x[1])[0]
            if min(calc_distance((x_, y_), pos_), calc_distance(self.pos, pos_)) == calc_distance(self.pos, pos_):
                return
            else:
                self.model.grid.move_agent(self,(x_,y_))
                if self.pos == (23,17):
                    self.buying_lunch = 3
                    self.coords = dir['E']

    def move(self, go_to_class=False):
        '''
        Called every time step. Depending on agent's state and objective, move agent accordingly

        :param self: canteen-object
        :optional param go_to_class: bool
        :return: None
        '''

        if go_to_class is True: #Agent go to class
            if self.queue == False and self.sitting_in_canteen == 0:
                if with_mask:
                    self.mask = True
                move_for_class(self, self.door.pos)

            else:
                if self.in_toilet_queue:
                    force_agent_to_specific_pos(self,self.model.toilet.exit)
                self.queue, self.going_to_toilet,self.in_toilet_queue = False, False, False
                self.sitting_in_canteen = 0
                self.sitting_on_toilet = 0
                move_for_class(self, self.door.pos)

        else: #Agent dont go to class
            #Go home
            if (go_home_in_breaks == True or self.has_more_courses_today == False) and self.entre_door != ():
                move_to_entre(self)
            #Dont go home
            else:
                if self.going_to_toilet: #Go to toilet
                    self.move_to_toilet()
                elif self.in_toilet_queue:  #Queuing to toilet already
                    self.move_in_toilet_queue()
                elif self.sitting_on_toilet>0: #Sitting in toilet
                    self.sitting_on_toilet = max(0,self.sitting_on_toilet-1)
                    if self.sitting_on_toilet == 0:
                        self.model.grid.move_agent(self,self.model.toilet.exit)
                elif self.queue: #Queuing to canteen
                    if self.pos in [(23,j) for j in range(0,20)]:
                        self.move_in_canteen_queue((23,20)) # moves towards end of canteen
                    else:
                        self.move_in_canteen_queue((23,3))# move towards canteen-line-entrance
                elif self.sitting_in_canteen > 45: # sitting in canteen, stay there
                    self.sitting_in_canteen = max(0, self.sitting_in_canteen-1)
                elif self.sitting_in_canteen in range(0,46): # not sitting in canteen, wander around
                    self.sitting_in_canteen = max(0, self.sitting_in_canteen-1)
                    if with_mask:
                        self.mask = True
                    wander(self)
                else: wander(self)

    def step(self):
        ''''
        Invoked every time step and is multi-purposed.
        Update agent's parameters and handle if the agent is off_campus.
        Invoke infect-function if agent is infectious and present at campus.
        Keep track of and change direction of agent.
        Invoke move-function.

        :param self: canteen-object
        :return: None
        '''
        self.since_last_toilet = max(0,self.since_last_toilet-1)

        if self.infected:
            update_infection_parameters(self)

        if go_home_in_breaks == False:
            self.check_if_agent_is_queuing()

        if is_off_campus(self):
            if self.pos in self.model.entre:
                return
            else:
                self.model.grid.move_agent(self,self.model.entre[random.randint(0,len(self.model.entre)-1)])

        "For changing direction"
        start_pos = self.pos

        if is_off_campus(self) == False and self.is_home_sick == False:
            if self.infected:
                infect(self)

        "When should the agent go to class?"
        if self.model.day_count == 1:
            if self.model.minute_count in self.model.class_times and self.model.minute_count % 2 == 0 and self.next_to_attend_class == True:
                self.going_to_class = True
        elif (self.model.minute_count == 0 or (self.model.minute_count in self.model.class_times+[2] and self.model.minute_count%2 == 0))\
                and self.next_to_attend_class:
            self.going_to_class = True

        if self.going_to_class:
            self.move(True)
        else:
            self.move()

        "Avoid agents to go inside the toilet area (top left corner of grid)"
        try:
            if self.pos[0]<8 and self.pos[1]>32:
                force_agent_to_specific_pos(self,self.model.toilet.exit)
        except:
            pass

        "Change direction"
        if with_dir and self.sitting_in_canteen <= 45:
            end_pos = self.pos
            self.coords = update_direction(self, start_pos, end_pos)
class employee_Agent(Agent):
    '''
    A class to represent the employees in the canteen

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    infected: bool
        States if the agent is infected or not
    asymptomatic : bool
        States if the agent is going to show symptoms or not
    recovered : bool
        States if the agent is recovered from the disease or not
    vaccinated : bool
        States if the agent is vaccinated or not
    is_home_sick : bool
        States if the agent is home sick or not

    mask : bool
        States if the agent is wearing a mask or not

    infection_period : int
        The number of timesteps the agent is infected (only invoked if agent gets infected)
    incubation_period : int
        The number of timesteps the agent is asymptomatic and thus infect others without knowing it (only invoked if agent gets infected)
    non_contageous_period : int
        The number of timesteps the agent does not infect or show symptoms (only invoked if agent gets infected)
    reproduction : int
        The number of individuals the agent infects

    coords : tuple ()
        Direction of the agent
    '''
    def __init__(self,id,model):
        super().__init__(id,model)
        self.id = id
        self.model = model

        self.infected = False
        self.asymptomatic = False
        self.recovered = False
        self.vaccinated = False
        self.is_home_sick = False

        if with_mask ==  True:
            self.mask = True
        else:
            self.mask = False


        self.infection_period = 0
        self.incubation_period = math.pi
        self.non_contageous_period = math.pi
        self.reproduction = 0

        self.coords = ()

    def step(self):
        if is_off_campus(self):
            return
        if self.infected:
            infect(self)
            update_infection_parameters(self)


        if self.id %2 == 0:
            self.move()
        if self.id in [1252,1253] and len(self.model.canteen_agents_at_work)==2: #if both other employees is at work
            self.model.canteen_backups_to_go_home.append(self)


    def move(self):
        start_pos = self.pos
        wander(self)
        if with_dir:
            end_pos = self.pos
            self.coords = update_direction(self, start_pos, end_pos)
class wall(Agent):
    '''
    A class to represent the walls

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    '''
    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id
        self.orientation = ()
class door(Agent):
    '''
    A class to represent the doors to enter and exit the classrooms

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    '''
    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id
        self.model = model
class desk(Agent):
    '''
    A class to represent the desk at the canteen.

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    '''

    def __init__(self, id, model):
        super().__init__(id, model)
        self.id = id
        self.model = model
class table(Agent):
    '''
    A class to represent a table.

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    counter : int
        Counter of how many people get infected at the tables
    '''
    def __init__(self,id, model):
        super().__init__(id,model)
        self.id = id
        self.model = model
        self.counter = 0
class toilet(Agent):
    '''
    A class to represent a toilet.

    Attributes
    ----------
    id : int
        States which agent we are looking at
    model : Model
        Model the agent belongs to
    has_been_infected: bool
        Indicating wether or not the toilet has been infected
    queue : list []
        List of positions indicating the queue of toilet
    exit : tuple ()
        The position of the exit of the toilet
    counter : int
        Counter of how many people have been infected at the toilet
    '''
    def __init__(self,id, model):
        super().__init__(id,model)
        self.id = id
        self.model = model
        self.has_been_infected = False
        self.queue = [(i,37) for i in range(9,15)]
        self.exit = (9,34)
        self.counter = 0
