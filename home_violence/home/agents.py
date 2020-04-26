from mesa.agent import Agent


class Person(Agent):
    """
    A victim that lives within a family, incurs in chance of suffering violence.

    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """
        A model step.
        """
        pass


class Family:
    """
    A family that provides the environment and contain agents who might become victims or aggressors
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """
        A model step.
        """
        pass


class Victim(Person):
    pass


class Aggressor(Person):
    pass
