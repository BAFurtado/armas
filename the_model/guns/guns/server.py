from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from guns.agents import Aggressor, Victim
from guns.model import Guns


def guns_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # aggressor "https://icons8.com/icons/set/bandit"
    # victim "https://icons8.com/icons/set/gender-neutral-user"
    # police "https://icons8.com/icons/set/policeman-male"

    if type(agent) is Victim:
        portrayal["Shape"] = "guns/resources/person.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Aggressor:
        portrayal["Shape"] = "guns/resources/bandit.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = agent.has_gun
        portrayal["text_color"] = "White"

    return portrayal


canvas_element = CanvasGrid(guns_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Aggressors", "Color": "#AA0000"},
                             {"Label": "Victims", "Color": "#666666"}])

model_params = {"initial_victims": UserSettableParameter('slider', 'Initial Victim Population', 100, 10, 300),
                "initial_aggressors": UserSettableParameter('slider', 'Initial Aggressor Population', 5, 1, 20),
                "reaction_if_has_gun": UserSettableParameter('slider', 'Reaction if Victim has gun', 85, 1, 100),
                "prob_victims_have_gun": UserSettableParameter('slider', 'Prob. Victims have guns', 20, 1, 100),
                "chance_death_gun": UserSettableParameter('slider',
                                                          'Chance Victim dies if Victim has gun', 85, 1, 100)}

server = ModularServer(Guns, [canvas_element, chart_element], "Aggressor Victim Confront", model_params)
server.port = 8521
