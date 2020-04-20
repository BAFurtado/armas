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

from guns.agents import Victim, Wolf, GrassPatch
from guns.schedule import RandomActivationByBreed


class Guns(Model):
    """
    A Gun Possession Model
    """

    height = 20
    width = 20

    initial_victims = 100
    initial_aggressors = 5

    # sheep_reproduce = 0.04
    # wolf_reproduce = 0.05

    # wolf_gain_from_food = 20

    # grass = False
    # grass_regrowth_time = 30
    # sheep_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = 'A model for simulating the victim aggressor interaction mediated by presence of guns.'

    def __init__(self, height=20, width=20,
                 initial_victims=100,
                 initial_aggressors=5,
                 reaction_if_has_gun=.85,
                 chance_death_gun=.85):
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

        self.reaction_if_has_gun = reaction_if_has_gun
        self.chance_death_gun = chance_death_gun
        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        # It is here that we provide data for the DataCollector. It will be then retrieved from key "Wolves" within
        # ChartModule at server.py and sent ver to as a canvas element
        self.datacollector = DataCollector(
            {"Aggressors": lambda m: m.schedule.get_breed_count(Wolf),
             "Victims": lambda m: m.schedule.get_breed_count(Victim)})

        # Create sheep:
        for i in range(self.initial_victims):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sheep = Victim(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for i in range(self.initial_aggressors):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self,
                                   fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Wolf),
                   self.schedule.get_breed_count(Victim)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number wolves: ',
                  self.schedule.get_breed_count(Wolf))
            print('Initial number sheep: ',
                  self.schedule.get_breed_count(Victim))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number wolves: ',
                  self.schedule.get_breed_count(Wolf))
            print('Final number sheep: ',
                  self.schedule.get_breed_count(Victim))
