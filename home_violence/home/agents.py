from mesa.agent import Agent


# TODO: Define agents attributes and update stress_indicator
# TODO: Function probability to trigger violent action
# TODO: As a result of violence, we have new inherited agents: aggressors and victims
# TODO: Stress_indicator is at the level of the family or the agent, or both?


class Person(Agent):
    """
    A person who lives within a family, incurs in chance of suffering violence.

    """

    def __init__(self, unique_id, model, pos, gender='male', is_working=False, wage=.5):
        super().__init__(unique_id, model)
        self.pos = pos
        self.gender = gender
        self.is_working = is_working
        self.wage = wage
        self.spouse = None
        self.got_attacked = 0
        self.assaulted = 0
        self.hours_home = (24 - 16) if is_working else (24 - 8)
        self.num_members_family = 1
        self.stress = 0

    def step(self):
        """
        A model step.
        """
        pass

    def update_stress(self):
        pass

    def trigger_violence(self, family):
        """
        Uses self stress and family context to incur in probability of becoming violent
        """
        pass


class Victim(Person):
    """
    A person from the family becomes first victimized
    """

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)


class Aggressor(Person):
    """
    A person from the family makes first aggression
    """

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)


class Family(Agent):
    """
    A family that provides the environment and contain agents who might become victims or aggressors
    """

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

    def update_family_data(self):
        pass

    def step(self):
        """
        A model step.
        """
        # It will include family stress indicator update
        # Likelihood of triggering aggression
        # New values


if __name__ == '__main__':
    # Bernardo's debugging model
    from home_violence.home.model import Home
    m1 = Home()
    bob = Person(0, m1, (1, 1))
