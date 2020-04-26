from mesa.agent import Agent


class Person(Agent):
    """
    A victim that lives within a family, incurs in chance of suffering violence.

    """

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

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
    """
    A person from the family becomes first victimized
    """

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    pass


class Aggressor(Person):
    """
    A person from the family makes first aggression
    """

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
    pass
