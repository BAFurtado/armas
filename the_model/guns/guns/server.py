from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from guns.agents import Aggressor, Victim, Police
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

    elif type(agent) is Police:
        portrayal["Shape"] = "guns/resources/police.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3

    return portrayal


canvas_element = CanvasGrid(guns_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Aggressors", "Color": "#AA0000"},
                             {"Label": "Victims", "Color": "#666666"},
                             {"Label": "Policepersons", "Color": "#CCCC00"}])

model_params = {"initial_victims": UserSettableParameter('slider', 'Initial Victim Population', 100, 5, 300),
                "initial_aggressors": UserSettableParameter('slider',
                                                            'Initial Aggressor Population', 5, 1, 50),
                "initial_policepersons": UserSettableParameter('slider',
                                                            'Initial Policer Population', 5, 1, 50),
                "police_letality": UserSettableParameter('slider',
                                                         'Police Letality', 0.5, 0.01, 1.0, 0.01),
                "reaction_if_has_gun": UserSettableParameter('slider',
                                                             'Reaction if Victim has gun', 0.85, 0.01, 1.0, 0.01),
                "prob_victims_have_gun": UserSettableParameter('slider',
                                                               'Prob. Victims have guns', 0.85, 0.01, 1.0, 0.01),
                "chance_death_gun": UserSettableParameter('slider',
                                                          'Chance Victim dies if Victim has gun',
                                                          0.85, 0.01, 1.0, 0.01)}

server = ModularServer(Guns, [canvas_element, chart_element], "Aggressor Victim Confront", model_params)
server.port = 8521
