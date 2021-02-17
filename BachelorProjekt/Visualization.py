from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from Model import covid_Model


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

grid = CanvasGrid(covid_draw, width, height, 500, 500)

infected_chart = ChartModule([{"Label":"infected","Color":"Black"}],data_collector_name="datacollector")

server = ModularServer(covid_Model,
                       [grid,infected_chart],
                       "Covid Model",
                       {"N":agentsN, "width":width, "height":height, "setUpType":2})
server.port = 8521 # The default
