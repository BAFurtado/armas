"""
A simple victim x aggressor encounter model
================================
Directly adapted from mesa example which is inspired by the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/GunsPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

try:
    from guns.agents import Victim, Aggressor, Police
    from guns.schedule import RandomActivationByBreed
except ModuleNotFoundError:
    from agents import Victim, Aggressor, Police
    from schedule import RandomActivationByBreed


class Guns(Model):
    """
    A Gun Possession Model
    """

    height = 20
    width = 20

    initial_victims = 100
    initial_aggressors = 5
    initial_policepersons = 5

    police_letality = 0.5

    prob_victims_have_gun = 0.2
    reaction_if_has_gun = 0.85
    chance_death_gun = 0.85

    verbose = False  # Print-monitoring

    description = 'A model for simulating the victim aggressor interaction mediated by presence of guns.'

    def __init__(self, height=20, width=20,
                 initial_victims=100,
                 initial_aggressors=5,
                 initial_policepersons=5,
                 police_letality=0.5,
                 prob_victims_have_gun=0.2,
                 reaction_if_has_gun=0.85,
                 chance_death_gun=0.85):
        """
        Create a new Guns model with the given parameters.

        Args:
            initial_victims: Number of potential victims to start with
            initial_aggressors: Number of aggressors to start with

        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_victims = initial_victims
        self.initial_aggressors = initial_aggressors
        self.initial_policepersons = initial_policepersons

        self.prob_victims_have_gun = prob_victims_have_gun
        self.reaction_if_has_gun = reaction_if_has_gun
        self.chance_death_gun = chance_death_gun

        self.police_letality = police_letality

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        # It is here that we provide data for the DataCollector. It will be then retrieved from key "Wolves" within
        # ChartModule at server.py and sent ver to as a canvas element
        self.datacollector = DataCollector(
            {"Aggressors": lambda m: m.schedule.get_breed_count(Aggressor),
             "Victims": lambda m: m.schedule.get_breed_count(Victim),
             "Policepersons": lambda m: m.schedule.get_breed_count(Police)})

        # Create victims:
        for i in range(self.initial_victims):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            has_gun = True if self.random.random() < self.prob_victims_have_gun else False
            victim = Victim(self.next_id(), (x, y), self, True, has_gun)
            self.grid.place_agent(victim, (x, y))
            self.schedule.add(victim)

        # Create police:
        for i in range(self.initial_policepersons):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            has_gun = True
            bobby = Police(self.next_id(), (x, y), self, True, has_gun)
            self.grid.place_agent(bobby, (x, y))
            self.schedule.add(bobby)

        # Create aggressors
        for i in range(self.initial_aggressors):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            has_gun = True
            aggressor = Aggressor(self.next_id(), (x, y), self, True, has_gun)
            self.grid.place_agent(aggressor, (x, y))
            self.schedule.add(aggressor)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Aggressor),
                   self.schedule.get_breed_count(Victim),
                   self.schedule.get_breed_count(Police)])

        # New condition to stop the model
        if self.schedule.get_breed_count(Victim) == 0 or self.schedule.get_breed_count(Aggressor) == 0:
            self.running = False

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number aggressors: ',
                  self.schedule.get_breed_count(Aggressor))
            print('Initial number victims: ',
                  self.schedule.get_breed_count(Victim))
            print('Initial number policepersons: ',
                  self.schedule.get_breed_count(Police))

        # Steps are not being set here, but on superclass. Changes should be made in the step function above!
        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number aggressors: ',
                  self.schedule.get_breed_count(Aggressor))
            print('Final number victims: ',
                  self.schedule.get_breed_count(Victim))
            print('Final number policepersons: ',
                  self.schedule.get_breed_count(Police))


if __name__ == '__main__':
    # Bernardo's debugging
    mymodel = Guns()
    mymodel.run_model()
