from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
import AgentClass as ac
from Model import covid_Model, find_status
import numpy as np
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt

ids = [i for i in range(0,78)]

class infected_Element(TextElement):
    '''
    Display a text count of how many happy agents there are. FROM MESA-EXAMPLES
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Infected agents: " + str(find_status(model, "infected", [ac.covid_Agent, ac.canteen_Agent, ac.TA]))

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

    if isinstance(agent,ac.covid_Agent) or isinstance(agent,ac.canteen_Agent):
        if agent.recovered == 1:
            portrayal["Color"] = "purple"
        if agent.infected == 0:
            portrayal["Color"] = "green"
        if agent.infected == 1 and agent.exposed == 0:
                portrayal["Shape"] = "resources/corona.png"
                portrayal["scale"] = 0.9
        if agent.infected == 1 and agent.exposed > 0:
                portrayal["Shape"] = "resources/exposed.png"
                portrayal["scale"] = 0.9

        if isinstance(agent,ac.covid_Agent) and agent.hasQuestion == 1:
            if agent.infected == 1:
                portrayal["Color"] = "black"
            if agent.infected == 0:
                portrayal["Color"] = "Blue"
    if agent.id in [1001,1002,1003]:
        if agent.infected == 0:
            portrayal["Color"] = "blue"
            portrayal["scale"] = 0.9
        elif agent.infected == 1:
            portrayal["Color"] = "Pink"
            portrayal["scale"] = 0.9
    if agent.id in [1004,1005,1006]:
        if agent.infected == 0:
            portrayal["Color"] = "brown"
            portrayal["scale"] = 0.9
        elif agent.infected == 1:
            portrayal["Color"] = "Pink"
            portrayal["scale"] = 0.9


    if (isinstance(agent,ac.TA) or isinstance(agent,ac.covid_Agent) or isinstance(agent,ac.canteen_Agent)):
            if agent.is_home_sick == 1:
                portrayal["Shape"] = "resources/white.jpg"
                portrayal["scale"] = 0.9
            if agent.recovered == 1:
                portrayal["Shape"] = "resources/healthy.png"
                portrayal["scale"] = 0.9
    if isinstance(agent,ac.canteen_Agent):
          if agent.off_school == 1:
                portrayal["Shape"] = "resources/white.jpg"
                portrayal["scale"] = 0.9
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
    if agent.id in range(0,26):
        portrayal["Color"] = "Silver"
        portrayal["scale"] = 0.9
    if agent.id in range(26,52):
        portrayal["Color"] = "gold"
        portrayal["scale"] = 0.9
    if agent.id in range(52,78):
        portrayal["Color"] = "purple"
        portrayal["scale"] = 0.9
    if agent.id in range(78,104):
        portrayal["Color"] = "black"
        portrayal["scale"] = 0.9
    if agent.id in range(104,130):
        portrayal["Color"] = "grey"
        portrayal["scale"] = 0.9
    if agent.id in range(130,156):
        portrayal["Color"] = "green"
        portrayal["scale"] = 0.9
    return portrayal

agentsN = 25
width, height = 25,33

infected_element = infected_Element()
days_chart = count_Days()
grid = CanvasGrid(covid_draw, width, height, 500, 500)

infected_chart = ChartModule([{"Label":"infected","Color":"Black"}], data_collector_name="datacollector")

server = ModularServer(covid_Model,
                       [grid,infected_element, infected_chart,days_chart],
                       "Covid Model",
                       {"N":agentsN, "width":width, "height":height, "setUpType":[4,4,4]})

server.port = 8521 # The default



