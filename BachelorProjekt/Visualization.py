from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
import AgentClass as ac
from Model import covid_Model, find_status


class infected_Element(TextElement):
    '''
    Display a text count of how many happy agents there are. FROM MESA-EXAMPLES
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Infected agents: " + str(find_status(model,"infected",ac.covid_Agent))


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
    if isinstance(agent,ac.covid_Agent):
        if agent.infected == 0:
            portrayal["Color"] = "green"
        if agent.infected == 1:
                portrayal["Shape"] = "resources/corona.png"
                portrayal["scale"] = 0.9
        if agent.hasQuestion == 1 and agent.infected == 1:
            portrayal["Color"] = "black"
        if agent.hasQuestion == 1 and agent.infected == 0:
            portrayal["Color"] = "Blue"
    if isinstance(agent,ac.TA):
        if agent.infected == 0:
            portrayal["Color"] = "Orange"
            portrayal["scale"] = 0.9
        elif agent.infected == 1:
            portrayal["Color"] = "Pink"
            portrayal["scale"] = 0.9
    if isinstance(agent,ac.door):
        portrayal["Shape"] = "resources/door.png"
        portrayal["scale"] = 0.9

    return portrayal

agentsN = 25
width, height = 9, 10

infected_element = infected_Element()
days_chart = count_Days()
grid = CanvasGrid(covid_draw, width, height, 500, 500)

infected_chart = ChartModule([{"Label":"infected","Color":"Black"}], data_collector_name="datacollector")

server = ModularServer(covid_Model,
                       [grid,infected_element, infected_chart,days_chart],
                       "Covid Model",
                       {"N":agentsN, "width":width, "height":height, "setUpType":1})
server.port = 8521 # The default
