from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
import AgentClass as ac
from Model import covid_Model,get_infected_count,is_off_campus,is_student, with_dir, dir, is_human
from PIL import Image
import numpy as np
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt

'''
Module responsible for visualizing the agents 

Initializes a Model object with correct number of agents per classand and with correct width and height 
of the grid
'''

agentsN = 24
width, height = 26,38


class infected_Element(TextElement):
    '''
    Display a text count of how many infected agents there are. FROM MESA-EXAMPLES
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Infected agents: " + str(get_infected_count(model))

class count_Days(TextElement):
    '''
    Display a text count of how many happy agents there are.   FROM MESA-EXAMPLES
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Day #: " + str(model.day_count)


class count_Minutes(TextElement):
    '''
    Display a text count of how many happy agents there are.   FROM MESA-EXAMPLES
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Minute #: " + str(model.minute_count)


def covid_draw(agent):
    '''
    Responsible for visualizing the agents correctly without arrows

    :param self: agent-object
    :return: None
    '''
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.8, "Filled": "true", "Layer": 0}

    if isinstance(agent, ac.class_Agent) or isinstance(agent, ac.canteen_Agent):
        if agent.recovered == 1:
            portrayal["Color"] = "purple"
        if agent.infected == 0:
            portrayal["Color"] = "green"
        if agent.infected == True and agent.non_contageous_period == 0:
                portrayal["Shape"] = "resources/corona.png"
                portrayal["scale"] = 0.9
        if agent.infected == True and agent.non_contageous_period > 0:
                portrayal["Shape"] = "resources/exposed.png"
                portrayal["scale"] = 0.9

        if isinstance(agent, ac.class_Agent) and agent.has_question == True:
            if agent.infected == True:
                portrayal["Color"] = "#000"
            if agent.infected == False:
                portrayal["Color"] = "Blue"
    if agent.id in [1001,1002,1003,1004,1005,1006]:
        if agent.infected == False:
            if agent.mask == True:
                portrayal["Shape"] = "resources/mundbind_TA.png"
                portrayal["scale"] = 0.9
            else:
                portrayal["Color"] = "Brown"
                portrayal["scale"] = 0.9
        elif agent.infected == True:
            portrayal["Color"] = "Pink"
            portrayal["scale"] = 0.9
    if isinstance(agent, ac.table):
        portrayal['Shape']="rect"
        portrayal["Color"] = "Black"
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["Layer"]=1
    if isinstance(agent,ac.door):
        portrayal["Shape"] = "resources/door.png"
        portrayal["scale"] = 0.9
    if isinstance(agent,ac.wall):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "Black"
        if agent.orientation == 'v':
            portrayal["w"] = 0.2
            portrayal["h"] = 1
        elif agent.orientation == 'h':
            portrayal["w"] = 1
            portrayal["h"] = 0.2
    if agent.id in range(0,agentsN):
        portrayal["Color"] = "Silver"
        portrayal["scale"] = 0.9
    if agent.id in range(agentsN,2*agentsN):
        portrayal["Color"] = "gold"
        portrayal["scale"] = 0.9
    if agent.id in range(2*agentsN,3*agentsN):
        portrayal["Color"] = "purple"
        portrayal["scale"] = 0.9
    if agent.id in range(3*agentsN,4*agentsN):
        portrayal["Color"] = "black"
        portrayal["scale"] = 0.9
    if agent.id in range(4*agentsN,5*agentsN):
        portrayal["Color"] = "grey"
        portrayal["scale"] = 0.9
    if agent.id in range(5*agentsN,6*agentsN):
        portrayal["Color"] = "green"
        portrayal["scale"] = 0.9
    if isinstance(agent, ac.employee_Agent):
        if agent.infected ==0:
            portrayal["Shape"] = "resources/burger.png"
            portrayal["scale"] =1.5
        else:
            portrayal["Shape"] = "resources/blueburger.png"
            portrayal["scale"] =1
    if isinstance(agent,ac.desk):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "Brown"
        portrayal["w"] = 0.2
        portrayal["h"] = 1
    if isinstance(agent, ac.canteen_Agent):
        if agent.queue==1 or agent.sitting_in_canteen > 45:
            portrayal["Shape"] = "resources/burger.png"
            portrayal["scale"] = 0.9
        elif (agent.queue ==1 or agent.sitting_in_canteen in range(45,75)) and agent.infected ==1:
            portrayal["Shape"] = "resources/blueburger.png"
            portrayal["scale"] = 0.9
    if isinstance(agent,ac.toilet):
        portrayal["Shape"] = "resources/toilet2.jpg"
        portrayal["scale"] = 0.9
    if ac.is_human(agent):
            if agent.is_home_sick == True:
                portrayal["Shape"] = "resources/white.jpg"
                portrayal["scale"] = 0.9
            if agent.recovered == 1:
                portrayal["Shape"] = "resources/healthy.png"
                portrayal["scale"] = 0.9
    if is_off_campus(agent):
            portrayal["Shape"] = "resources/white.jpg"
            portrayal["scale"] = 0.9
    if is_student(agent) and agent.day_off == True:
        portrayal["Shape"] = "resources/healthy.png"
        portrayal["scale"] = 0.9
    if is_human(agent) and agent.mask == True:
        portrayal["Shape"] = "resources/healthy.png"
        portrayal["scale"] = 0.9

    return portrayal

def covid_draw_arrow(agent):
    '''
    Responsible for visualizing the agents correctly with arrows

    :param self: agent-object
    :return: None
    '''
    portrayal = {"Shape": "circle", "r": 0.8, "Filled": "true", "Layer": 0}
    if agent is None:
        return
    if agent.pos in agent.model.entre:
        portrayal["Shape"] = "resources/white.jpg"
        portrayal["scale"] = 0.9
    elif isinstance(agent, ac.canteen_Agent):
        if agent.off_school ==1 or agent.is_home_sick == True:
            portrayal["Shape"] = "resources/white.jpg"
            portrayal["scale"] = 0.9

        elif agent.queue != 0:
            if agent.infected == True and agent.non_contageous_period > 0:
                if agent.coords == dir['N']:
                        portrayal["Shape"] = "resources/pizzaexposedN.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['S']:
                        portrayal["Shape"] = "resources/pizzaexposedS.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['E']:
                        portrayal["Shape"] = "resources/pizzaexposedE.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['W']:
                        portrayal["Shape"] = "resources/pizzaexposedW.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['NE']:
                        portrayal["Shape"] = "resources/pizzaexposedNE.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['NW']:
                        portrayal["Shape"] = "resources/pizzaexposedNW.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['SE']:
                        portrayal["Shape"] = "resources/pizzaexposedSE.png"
                        portrayal["scale"] = 0.9
                else:
                        portrayal["Shape"] = "resources/pizzaexposedSW.png"
                        portrayal["scale"] = 0.9
            elif agent.infected == True:
                if agent.coords == dir['N']:
                        portrayal["Shape"] = "resources/pizzainfectedN.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['S']:
                        portrayal["Shape"] = "resources/pizzainfectedS.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['E']:
                        portrayal["Shape"] = "resources/pizzainfectedE.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['W']:
                        portrayal["Shape"] = "resources/pizzainfectedW.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['NE']:
                        portrayal["Shape"] = "resources/pizzainfectedNE.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['NW']:
                        portrayal["Shape"] = "resources/pizzainfectedNW.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['SE']:
                        portrayal["Shape"] = "resources/pizzainfectedSE.png"
                        portrayal["scale"] = 0.9
                else:
                        portrayal["Shape"] = "resources/pizzainfectedSW.png"
                        portrayal["scale"] = 0.9
            elif agent.recovered == 1:
                if agent.coords == dir['N']:
                        portrayal["Shape"] = "resources/pizzarecoveredN.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['S']:
                        portrayal["Shape"] = "resources/pizzarecoveredS.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['E']:
                        portrayal["Shape"] = "resources/pizzarecoveredE.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['W']:
                        portrayal["Shape"] = "resources/pizzarecoveredW.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['NE']:
                        portrayal["Shape"] = "resources/pizzarecoveredNE.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['NW']:
                        portrayal["Shape"] = "resources/pizzarecoveredNW.png"
                        portrayal["scale"] = 0.9
                elif agent.coords == dir['SE']:
                        portrayal["Shape"] = "resources/pizzarecoveredSE.png"
                        portrayal["scale"] = 0.9
                else:
                        portrayal["Shape"] = "resources/pizzarecoveredSW.png"
                        portrayal["scale"] = 0.9
            else:
                if agent.coords == dir['N']:
                    portrayal["Shape"] = "resources/pizzaN.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['S']:
                    portrayal["Shape"] = "resources/pizzaS.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/pizzaE.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/pizzaW.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/pizzaNE.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/pizzaSE.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/pizzaNW.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['SW']:
                    portrayal["Shape"] = "resources/pizzaSW.png"
                    portrayal["scale"] = 1.1

        elif agent.sitting_in_canteen > 45:
            if agent.infected == True and agent.non_contageous_period > 0:
                if agent.coords == dir['E']:
                        portrayal["Shape"] = "resources/blackpizzaexposedE.png"
                        portrayal["scale"] = 0.9
                else:
                        portrayal["Shape"] = "resources/blackpizzaexposedW.png"
                        portrayal["scale"] = 0.9

            elif agent.infected == True:
                if agent.coords == dir['E']:
                        portrayal["Shape"] = "resources/blackpizzainfectedE.png"
                        portrayal["scale"] = 0.9
                else:
                        portrayal["Shape"] = "resources/blackpizzainfectedW.png"
                        portrayal["scale"] = 0.9
            elif agent.recovered == 1:
                if agent.coords == dir['E']:
                        portrayal["Shape"] = "resources/blackpizzarecoveredE.png"
                        portrayal["scale"] = 0.9
                else:
                        portrayal["Shape"] = "resources/blackpizzarecoveredW.png"
                        portrayal["scale"] = 0.9

            else:
                if agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/blackpizzaE.png"
                    portrayal["scale"] = 1
                else:
                    portrayal["Shape"] = "resources/blackpizzaW.png"
                    portrayal["scale"] = 1


        elif agent.infected == True and agent.non_contageous_period > 0:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/greenexposedN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/greenexposedS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/greenexposedE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/greenexposedW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/greenexposedNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/greenexposedSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/greenexposedNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/greenexposedSW.png"
                portrayal["scale"] = 0.9
        elif agent.infected == True:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/greeninfectedN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/greeninfectedS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/greeninfectedE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/greeninfectedW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/greeninfectedNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/greeninfectedSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/greeninfectedNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/greeninfectedSW.png"
                portrayal["scale"] = 0.9


        elif agent.recovered == 1:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/greenrecoveredN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/greenrecoveredS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/greenrecovereddE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/greenrecoveredW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/greenrecoveredNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/greenrecoveredSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/greenrecoveredNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/greenrecoveredSW.png"
                portrayal["scale"] = 0.9
        elif agent.vaccinated == True:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/greenvaccineN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/greenvaccineS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/greenvaccineE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/greenvaccineW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/greenvaccineNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/greenvaccineSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/greenvaccineNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/greenvaccineSW.png"
                portrayal["scale"] = 0.9


        else:
            if agent.coords in [dir['N'], dir['S'], dir['E'], dir['W']]:
                portrayal = {
                "Shape": "arrowHead",
                "Filled": "true",
                "Layer": 0,
                "Color": 'green',
                "heading_x": agent.coords[0],
                "heading_y": agent.coords[1],
                "scale": 0.8,
                }
            else:
                if agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/greenarrowNE.png"
                    portrayal["scale"] = 0.9
                elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/greenarrowSE.png"
                    portrayal["scale"] = 0.9
                elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/greenarrowNW.png"
                    portrayal["scale"] = 0.9
                elif agent.coords == dir['SW']:
                    portrayal["Shape"] = "resources/greenarrowSW.png"
                    portrayal["scale"] = 0.9

    elif isinstance(agent, ac.class_Agent):
        if agent.is_home_sick == True:
            portrayal["Shape"] = "resources/white.jpg"
            portrayal["scale"] = 0.9
        elif agent.infected == True and agent.non_contageous_period > 0:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/greenexposedN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/greenexposedS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/greenexposedE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/greenexposedW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/greenexposedNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/greenexposedSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/greenexposedNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/greenexposedSW.png"
                portrayal["scale"] = 0.9
        elif agent.infected == True:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/greeninfectedN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/greeninfectedS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/greeninfectedE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/greeninfectedW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/greeninfectedNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/greeninfectedSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/greeninfectedNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/greeninfectedSW.png"
                portrayal["scale"] = 0.9
        elif agent.recovered == 1:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/greenrecoveredN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/greenrecoveredS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/greenrecovereddE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/greenrecoveredW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/greenrecoveredNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/greenrecoveredSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/greenrecoveredNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/greenrecoveredSW.png"
                portrayal["scale"] = 0.9
        elif agent.vaccinated == True:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/greenvaccineN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/greenvaccineS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/greenvaccineE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/greenvaccineW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/greenvaccineNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/greenvaccineSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/greenvaccineNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/greenvaccineSW.png"
                portrayal["scale"] = 0.9
        else:
            if agent.coords in [dir['N'], dir['S'], dir['E'], dir['W']]:
                    portrayal = {
                    "Shape": "arrowHead",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": 'green',
                    "heading_x": agent.coords[0],
                    "heading_y": agent.coords[1],
                    "scale": 0.8,
                    }
            else:
                if agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/greenarrowNE.png"
                    portrayal["scale"] = 0.9
                elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/greenarrowSE.png"
                    portrayal["scale"] = 0.9
                elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/greenarrowNW.png"
                    portrayal["scale"] = 0.9
                elif agent.coords == dir['SW']:
                    portrayal["Shape"] = "resources/greenarrowSW.png"
                    portrayal["scale"] = 0.9
    elif isinstance(agent, ac.TA):
        if agent.is_home_sick == True:
            portrayal["Shape"] = "resources/white.jpg"
            portrayal["scale"] = 0.9
        elif agent.infected == True and agent.non_contageous_period > 0:
            if agent.coords == dir['N']:
                    portrayal["Shape"] = "resources/skyexposedN.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                    portrayal["Shape"] = "resources/skyexposedS.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/skyexposedE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/skyexposedW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/skyexposedNE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/skyexposedNW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/skyexposedSE.png"
                    portrayal["scale"] = 0.9
            else:
                    portrayal["Shape"] = "resources/skyexposedSW.png"
                    portrayal["scale"] = 0.9
        elif agent.infected == True:
            if agent.coords == dir['N']:
                    portrayal["Shape"] = "resources/skyinfectedN.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                    portrayal["Shape"] = "resources/skyinfectedS.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/skyinfectedE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/skyinfectedW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/skyinfectedNE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/skyinfectedNW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/skyinfectedSE.png"
                    portrayal["scale"] = 0.9
            else:
                    portrayal["Shape"] = "resources/skyinfectedSW.png"
                    portrayal["scale"] = 0.9
        elif agent.recovered == 1:
            if agent.coords == dir['N']:
                    portrayal["Shape"] = "resources/skyrecoveredN.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                    portrayal["Shape"] = "resources/skyrecoveredS.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/skyrecoveredE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/skyrecoveredW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/skyrecoveredNE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/skyrecoveredNW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/skyrecoveredSE.png"
                    portrayal["scale"] = 0.9
            else:
                    portrayal["Shape"] = "resources/skyrecoveredSW.png"
                    portrayal["scale"] = 0.9
        elif agent.vaccinated == True:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/skyvaccineN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/skyvaccineS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/skyvaccineE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/skyvaccineW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/skyvaccineNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/skyvaccineSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/skyvaccineNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/skyvaccineSW.png"
                portrayal["scale"] = 0.9
        else:
            if agent.coords in [dir['N'], dir['S'], dir['E'], dir['W']]:
                portrayal = {
                "Shape": "arrowHead",
                "Filled": "true",
                "Layer": 0,
                "Color": 'DeepSkyBlue',
                "heading_x": agent.coords[0],
                "heading_y": agent.coords[1],
                "scale": 0.9,
                }
            elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/skyNE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/skyNW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/skySE.png"
                    portrayal["scale"] = 0.9
            else:
                    portrayal["Shape"] = "resources/skySW.png"
                    portrayal["scale"] = 0.9
    elif isinstance(agent, ac.employee_Agent):
        if agent.infected == True and agent.non_contageous_period > 0:
            if agent.coords == dir['N']:
                    portrayal["Shape"] = "resources/pizzaexposedN.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                    portrayal["Shape"] = "resources/pizzaexposedS.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/pizzaexposedE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/pizzaexposedW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/pizzaexposedNE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/pizzaexposedNW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/pizzaexposedSE.png"
                    portrayal["scale"] = 0.9
            else:
                    portrayal["Shape"] = "resources/pizzaexposedSW.png"
                    portrayal["scale"] = 0.9
        elif agent.infected == True:
            if agent.coords == dir['N']:
                    portrayal["Shape"] = "resources/pizzainfectedN.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                    portrayal["Shape"] = "resources/pizzainfectedS.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/pizzainfectedE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/pizzainfectedW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/pizzainfectedNE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/pizzainfectedNW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/pizzainfectedSE.png"
                    portrayal["scale"] = 0.9
            else:
                    portrayal["Shape"] = "resources/pizzainfectedSW.png"
                    portrayal["scale"] = 0.9
        elif agent.recovered == 1:
            if agent.coords == dir['N']:
                    portrayal["Shape"] = "resources/pizzarecoveredN.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                    portrayal["Shape"] = "resources/pizzarecoveredS.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/pizzarecoveredE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/pizzarecoveredW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/pizzarecoveredNE.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/pizzarecoveredNW.png"
                    portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/pizzarecoveredSE.png"
                    portrayal["scale"] = 0.9
            else:
                    portrayal["Shape"] = "resources/pizzarecoveredSW.png"
                    portrayal["scale"] = 0.9
        else:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/pizzaN.png"
                portrayal["scale"] = 1.1
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/pizzaS.png"
                portrayal["scale"] = 1.1
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/pizzaE.png"
                portrayal["scale"] = 1.1
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/pizzaW.png"
                portrayal["scale"] = 1.1
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/pizzaNE.png"
                portrayal["scale"] = 1.1
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/pizzaSE.png"
                portrayal["scale"] = 1.1
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/pizzaNW.png"
                portrayal["scale"] = 1.1
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/pizzaSW.png"
                portrayal["scale"] = 1.1
    elif isinstance(agent, ac.table):
        portrayal['Shape']="rect"
        portrayal["Color"] = "Black"
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["Layer"]=1
    elif isinstance(agent,ac.door):
        portrayal["Shape"] = "resources/door.png"
        portrayal["scale"] = 0.9
    elif isinstance(agent,ac.wall):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "Black"
        if agent.orientation == 'v':
            portrayal["w"] = 0.2
            portrayal["h"] = 1
        elif agent.orientation == 'h':
            portrayal["w"] = 1
            portrayal["h"] = 0.2
    elif isinstance(agent,ac.desk):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "Brown"
        portrayal["w"] = 0.2
        portrayal["h"] = 1
    elif isinstance(agent,ac.toilet):
        portrayal["Shape"] = "resources/toilet2.jpg"
        portrayal["scale"] = 0.9



    return portrayal

days_chart = count_Days()
minute_chart = count_Minutes()
infected_element = infected_Element()

if with_dir == True:
    grid = CanvasGrid(covid_draw_arrow, width, height, 900, 1000)
else:
    grid = CanvasGrid(covid_draw, width, height, 900, 1000)

infected_chart = ChartModule([{"Label":"infected","Color":"Black"}], data_collector_name="datacollector")


server = ModularServer(covid_Model,
                       [grid,infected_element, days_chart, minute_chart,infected_chart],
                       "Covid Model",
                       {"N":agentsN, "width":width, "height":height, "setUpType":[4,4,4]})


server.port = 8521 # The default


