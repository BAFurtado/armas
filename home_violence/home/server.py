from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter


try:
    from home.agents import Aggressor, Victim, Person
    from home.model import Home
except ModuleNotFoundError:
    from model import Home
    from agents import Aggressor, Victim, Person


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
        color = PERSON
        portrayal["Color"] = color
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0

    elif type(agent) is Victim:
        portrayal["Color"] = VICTIM
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

    elif type(agent) is Aggressor:
        portrayal["Color"] = AGGRESSOR
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

    return portrayal


model_params = dict(height=40,
                    width=40)

canvas_element = CanvasGrid(home_violence_portrayal, 40, 40, 480, 480)
chart_element = ChartModule([{"Label": "Aggressors", "Color": AGGRESSOR},
                             {"Label": "Victims", "Color": VICTIM},
                             {"Label": "People", "Color": PERSON}])

model_params = {"initial_victims": UserSettableParameter('slider', 'Initial Population', 100, 5, 300)}

server = ModularServer(Home, [canvas_element, chart_element], "Home Violence", model_params)
server.port = 8521
