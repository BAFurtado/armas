from mesa.agent import Agent

# TODO: step: update_work, run.


class Person(Agent):
    """
    A person who lives within a family, incurs in chance of suffering violence.

    """

    def __init__(self, unique_id, model, pos, gender='male', age=25, is_working=False, wage=.5):
        super().__init__(unique_id, model)
        self.pos = pos
        self.gender = gender
        self.age = age
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
        # Check and execute
        self.trigger_violence()

    def step_change(self):
        # How conditions that cause stress change?
        changes = self.random.random()
        if changes < self.model.chance_changing_working_status:
            self.is_working = not self.is_working
        if changes < self.model.pct_change_wage:
            self.wage *= self.model.random.uniform(-self.model.pct_change_wage, self.model.pct_change_wage)

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
        # TODO: Change age filter before goes through steps
        if self.age > 18:
            self.update_stress()
        else:
            return

        # First time offender get registered in the system and changes class as an Aggressor and a Victim
        if self.assaulted == 0:
            if self.stress > self.random.random():
                m = self.model
                # Transforming a person into an aggressor
                new_aggressor = Aggressor(self.unique_id, self.model, self.pos,
                                          spouse=self.spouse, family=self.family)
                m.grid._remove_agent(self.pos, self)
                m.schedule.remove(self)
                m.grid.place_agent(new_aggressor, new_aggressor.pos)
                m.schedule.add(new_aggressor)
                new_aggressor.assaulted += 1

                # Transforming a person into victim
                victim = self.spouse
                new_victim = Victim(victim.unique_id, victim.model, victim.pos,
                                    spouse=victim.spouse, family=victim.family)
                m.grid.place_agent(new_victim, new_victim.pos)
                m.schedule.add(new_victim)
                m.grid._remove_agent(victim.pos, victim)
                m.schedule.remove(victim)
                new_victim.got_attacked += 1

        # Second-time offender, checks to see if it is a recidivist.
        elif self.stress > self.random.random():
            self.assaulted += 1
            self.spouse.got_attacked += 1

    def trigger_call_help(self):
        pass


class Victim(Person):
    """
    A person from the family becomes first victimized
    """

    def __init__(self, unique_id, model, pos, spouse, family):
        super().__init__(unique_id, model, pos, spouse, family)


class Aggressor(Person):
    """
    A person from the family makes first aggression
    """

    def __init__(self, unique_id, model, pos, spouse, family):
        super().__init__(unique_id, model, pos, spouse, family)
        self.spouse = spouse
        self.family = family


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
    bob = m1.schedule.agents[0]
    maria = m1.schedule.agents[1]
    f1 = Family(m1.next_id(), m1, (1, 1))
    f1.add_agent(bob)
    f1.add_agent(maria)
    bob.assign_spouse(maria)
    bob.update_stress()
    bob.trigger_violence()
