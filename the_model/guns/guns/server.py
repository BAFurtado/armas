from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from guns.agents import Wolf, Victim, GrassPatch
from guns.model import Guns


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # aggressor "https://icons8.com/icons/set/bandit"
    # victim "https://icons8.com/icons/set/gender-neutral-user"
    # police "https://icons8.com/icons/set/policeman-male"

    if type(agent) is Victim:
        portrayal["Shape"] = "guns/resources/sheep.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Wolf:
        portrayal["Shape"] = "guns/resources/wolf.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = agent.has_gun
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Aggressor", "Color": "#AA0000"},
                             {"Label": "Victims", "Color": "#666666"}])

model_params = {"grass": UserSettableParameter('checkbox', 'Grass Enabled', True),
                "grass_regrowth_time": UserSettableParameter('slider', 'Grass Regrowth Time', 20, 1, 50),
                "initial_victims": UserSettableParameter('slider', 'Initial Victim Population', 100, 10, 300),
                "sheep_reproduce": UserSettableParameter('slider', 'Sheep Reproduction Rate', 0.04, 0.01, 1.0,
                                                         0.01),
                "initial_aggressors": UserSettableParameter('slider', 'Initial Wolf Population', 50, 10, 300),
                "wolf_reproduce": UserSettableParameter('slider', 'Wolf Reproduction Rate', 0.05, 0.01, 1.0,
                                                        0.01,
                                                        description="The rate at which wolf agents reproduce."),
                "wolf_gain_from_food": UserSettableParameter('slider', 'Wolf Gain From Food Rate', 20, 1, 50),
                "sheep_gain_from_food": UserSettableParameter('slider', 'Sheep Gain From Food', 4, 1, 10)}

server = ModularServer(Guns, [canvas_element, chart_element], "Wolf Victim Predation", model_params)
server.port = 8521
