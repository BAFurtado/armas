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
        self.hours_home = 0
        self.family = None
        self.num_members_family = 1
        self.stress = 0

    def step(self):
        """
        A model step.
        """
        self.trigger_violence()

    def assign_spouse(self, agent):
        self.spouse = agent
        agent.spouse = self

    def update_stress(self):
        self.update_hours()
        # Update num_members_family
        self.num_members_family = 1 if self.family is None else len(self.family.members)

        # Update stress based on gender, wage level, hours at home, family size and history of violence
        tmp = self.model.gender_stress if self.gender == 'male' else 1 - self.model.gender_stress
        tmp *= (1 - self.wage)
        tmp *= self.hours_home
        tmp **= 1/self.num_members_family
        tmp **= 1/(1 + self.assaulted)
        self.stress = tmp

    def update_hours(self):
        self.hours_home = .34 if self.is_working else .67

    def update_work(self, working, wage):
        self.is_working = working
        self.wage = wage
        self.update_hours()

    def trigger_violence(self):
        """
        Uses self stress and family context to incur in probability of becoming violent
        """
        self.update_stress()
        if self.assaulted == 0:
            if self.stress > self.model.violence_threshold:
                # Transforming a person into an aggressor
                new_aggressor = Aggressor(self.unique_id, self.model, self.pos)
                self.model.grid.place_agent(new_aggressor, self.pos)
                self.model.schedule.add(new_aggressor)
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                new_aggressor.assaulted += 1

                # Transforming a person into victim
                victim = self.spouse
                new_victim = Victim(victim.unique_id, victim.model, victim.pos)
                self.model.grid.place_agent(new_victim, self.pos)
                self.model.schedule.add(new_victim)
                self.model.grid._remove_agent(victim.pos, victim)
                self.model.schedule.remove(victim)
                new_victim.got_attacked += 1

        else:
            self.assaulted += 1
            self.spouse.got_attacked += 1

    def trigger_call_help(self):
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
        self.context_stress = 0
        self.members = dict()

    def add_agent(self, agent):
        self.members[agent.unique_id] = agent
        agent.family = self

    def step(self):
        """
        A model step.
        """
        # It will include family stress indicator update
        # Likelihood of triggering aggression
        # New values
        pass


if __name__ == '__main__':
    # Bernardo's debugging model
    from home_violence.home.model import Home
    m1 = Home()
    bob = Person(0, m1, (1, 1))
    maria = Person(1, m1, (1, 1), gender='female', wage=.7, is_working=True)
    f1 = Family(0, m1, (1, 1))
    f1.add_agent(bob)
    f1.add_agent(maria)
    bob.assign_spouse(maria)
    bob.update_stress()
