from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
import AgentClass as ac
from Model import covid_Model,get_infected,is_off_campus,is_student, with_dir, dir, is_human
from PIL import Image
import numpy as np
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt

agentsN = 26
width, height = 26,38


class infected_Element(TextElement):
    '''
    Display a text count of how many infected agents there are. FROM MESA-EXAMPLES
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Infected agents: " + str(get_infected(model))

class count_Days(TextElement):
    '''
    Display a text count of how many happy agents there are.   FROM MESA-EXAMPLES
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Day #: " + str(model.day_count)

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal

def covid_draw(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.8, "Filled": "true", "Layer": 0}
    #if is_invisible(agent):
    #    portrayal["text"]=agent.id

    if isinstance(agent, ac.class_Agent) or isinstance(agent, ac.canteen_Agent):
        if agent.recovered == 1:
            portrayal["Color"] = "purple"
        if agent.infected == 0:
            portrayal["Color"] = "green"
        if agent.infected == True and agent.exposed == 0:
                portrayal["Shape"] = "resources/corona.png"
                portrayal["scale"] = 0.9
        if agent.infected == True and agent.exposed > 0:
                portrayal["Shape"] = "resources/exposed.png"
                portrayal["scale"] = 0.9

        if isinstance(agent, ac.class_Agent) and agent.hasQuestion == True:
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
    return portrayal

def covid_draw_arrow(agent):

    portrayal = {"Shape": "circle", "r": 0.8, "Filled": "true", "Layer": 0}
    if agent is None:
        return

    if isinstance(agent, ac.canteen_Agent):
        if agent.off_school ==1 or agent.is_home_sick == True:
            portrayal["Shape"] = "resources/white.jpg"
            portrayal["scale"] = 0.9
        elif agent.queue != 0:
            if agent.infected == True:
                if agent.coords == dir['N']:
                    portrayal["Shape"] = "resources/pinkpizzaN.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['S']:
                    portrayal["Shape"] = "resources/pinkpizzaS.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/pinkpizzaE.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/pinkpizzaW.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['NE']:
                    portrayal["Shape"] = "resources/pinkpizzaNE.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['SE']:
                    portrayal["Shape"] = "resources/pinkpizzaSE.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['NW']:
                    portrayal["Shape"] = "resources/pinkpizzaNW.png"
                    portrayal["scale"] = 1.1
                elif agent.coords == dir['SW']:
                    portrayal["Shape"] = "resources/pinkpizzaSW.png"
                    portrayal["scale"] = 1.1
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
            if agent.infected == True:
                if agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/pinkblackE.png"
                    portrayal["scale"] = 1
                elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/pinkblackW.png"
                    portrayal["scale"] = 1
            else:
                if agent.coords == dir['E']:
                    portrayal["Shape"] = "resources/blackpizzaE.png"
                    portrayal["scale"] = 1
                elif agent.coords == dir['W']:
                    portrayal["Shape"] = "resources/blackpizzaW.png"
                    portrayal["scale"] = 1

        elif agent.infected == True and agent.exposed > 0:
            portrayal["Shape"] = "resources/exposed.png"
            portrayal["scale"] = 0.9
        elif agent.infected == True:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/coronaarrowN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/coronaarrowS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/coronaarrowE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/coronaarrowW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/coronaarrowNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/coronaarrowSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/coronaarrowNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/coronaarrowSW.png"
                portrayal["scale"] = 0.9
        elif agent.recovered == 1:
            portrayal["Shape"] = "resources/healthy.png"
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
        elif agent.infected == True and agent.exposed > 0:
            portrayal["Shape"] = "resources/exposed.png"
            portrayal["scale"] = 0.9
        elif agent.infected == True:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/coronaarrowN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/coronaarrowS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/coronaarrowE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/coronaarrowW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/coronaarrowNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/coronaarrowSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/coronaarrowNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/coronaarrowSW.png"
                portrayal["scale"] = 0.9
        elif agent.recovered == 1:
            portrayal["Shape"] = "resources/healthy.png"
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
        elif agent.exposed == 1:
            portrayal["Color"] = "pink"
            portrayal["scale"] = 0.9
        elif agent.infected == True:
            if agent.coords == dir['N']:
                portrayal["Shape"] = "resources/coronaarrowN.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['S']:
                portrayal["Shape"] = "resources/coronaarrowS.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['E']:
                portrayal["Shape"] = "resources/coronaarrowE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['W']:
                portrayal["Shape"] = "resources/coronaarrowW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NE']:
                portrayal["Shape"] = "resources/coronaarrowNE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SE']:
                portrayal["Shape"] = "resources/coronaarrowSE.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['NW']:
                portrayal["Shape"] = "resources/coronaarrowNW.png"
                portrayal["scale"] = 0.9
            elif agent.coords == dir['SW']:
                portrayal["Shape"] = "resources/coronaarrowSW.png"
                portrayal["scale"] = 0.9
        elif agent.recovered == 1:
            portrayal["Shape"] = "resources/healthy.png"
            portrayal["scale"] = 0.9
        else:
            if agent.coords in [dir['N'], dir['S'], dir['E'], dir['W']]:
                portrayal = {
                "Shape": "arrowHead",
                "Filled": "true",
                "Layer": 0,
                "Color": 'brown',
                "heading_x": agent.coords[0],
                "heading_y": agent.coords[1],
                "scale": 0.8,
                }
            else:
                portrayal["Color"] = "brown"
                portrayal["scale"] = 0.9
    elif isinstance(agent, ac.employee_Agent):
        if agent.infected ==0:
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
        else:
            portrayal["Shape"] = "resources/blueburger.png"
            portrayal["scale"] =1
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

infected_element = infected_Element()
days_chart = count_Days()
if with_dir == True:
    grid = CanvasGrid(covid_draw_arrow, width, height, 1000, 900)
else:
    grid = CanvasGrid(covid_draw, width, height, 900, 1000)

infected_chart = ChartModule([{"Label":"infected","Color":"Black"}], data_collector_name="datacollector")


server = ModularServer(covid_Model,
                       [grid,infected_element, infected_chart,days_chart],
                       "Covid Model",
                       {"N":agentsN, "width":width, "height":height, "setUpType":[2,3,4]})



server.port = 8521 # The default


