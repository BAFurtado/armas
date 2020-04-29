from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter


try:
    from home.agents import Aggressor, Victim, Person, Family
    from home.model import Home
except ModuleNotFoundError:
    from model import Home
    from agents import Aggressor, Victim, Person, Family


PERSON = "#0066CC"
VICTIM = "#CC0000"
AGGRESSOR = "#757575"


def home_violence_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "x": agent.pos[0], "y": agent.pos[1],
                 "Filled": "true"}

    if type(agent) is Person:
        portrayal["Color"] = PERSON
        portrayal["r"] = 0.3
        portrayal["Layer"] = 1

    elif type(agent) is Victim:
        portrayal["Color"] = VICTIM
        portrayal["r"] = 0.6
        portrayal["Layer"] = 2

    elif type(agent) is Aggressor:
        portrayal["Color"] = AGGRESSOR
        portrayal["r"] = 0.8
        portrayal["Layer"] = 3

    elif type(agent) is Family:
        portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


model_params = dict(height=40,
                    width=40)

canvas_element = CanvasGrid(home_violence_portrayal, 40, 40, 480, 480)
chart_element = ChartModule([{"Label": "Aggressors", "Color": AGGRESSOR},
                             {"Label": "Victims", "Color": VICTIM},
                             {"Label": "People", "Color": PERSON}])

model_params = {"initial_families": UserSettableParameter('slider', 'Initial Families', 100, 5, 300)}

server = ModularServer(Home, [canvas_element, chart_element], "Home Violence", model_params)
server.port = 8521
