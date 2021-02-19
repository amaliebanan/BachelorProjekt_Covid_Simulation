from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer

from Model import covid_Model, find_status


class infected_Element(TextElement):
    '''
    Display a text count of how many happy agents there are.
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Infected agents: " + str(find_status(model))

class count_Days(TextElement):
    '''
    Display a text count of how many happy agents there are.
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
    if agent.infected == 0:
        #portrayal["Shape"] = "resources/healthy.png"
        #portrayal["scale"] = 0.9
        portrayal["Color"] = "green"
    else:
        portrayal["Shape"] = "resources/corona.png"
        portrayal["scale"] = 0.9
    if agent.id == 1000:
        portrayal["Color"] = "Orange"
        portrayal["scale"] = 0.9
    return portrayal

agentsN = 25
width, height = 8,10

infected_element = infected_Element()
grid = CanvasGrid(covid_draw, width, height, 500, 500)

infected_chart = ChartModule([{"Label":"infected","Color":"Black"}],data_collector_name="datacollector")
days_chart = count_Days()
server = ModularServer(covid_Model,
                       [grid,infected_element, infected_chart, days_chart],
                       "Covid Model",
                       {"N":agentsN, "width":width, "height":height, "setUpType":2})
server.port = 8521 # The default
