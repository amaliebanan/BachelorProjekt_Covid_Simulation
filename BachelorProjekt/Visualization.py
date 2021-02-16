from mesa.visualization.modules import CanvasGrid
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
        portrayal["Color"] = "Green"
    else:
        portrayal["Color"] = "Red"
    return portrayal

grid = CanvasGrid(covid_draw, 30, 30, 500, 500)
server = ModularServer(covid_Model,
                       [grid],
                       "Covid Model",
                       {"N":120, "width":30, "height":30})
server.port = 8521 # The default
