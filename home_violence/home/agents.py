from mesa.agent import Agent


class Victim(Agent):
    """
    A victim that walks around, incurs in chance of getting mugged.

    The init is the same as the RandomWalker.
    """

    has_gun = False

    def __init__(self, unique_id, pos, has_gun=False):
        super().__init__(unique_id, pos)
        self.has_gun = has_gun

    def step(self):
        """
        A model step. Move, awaits confront. If has gun, more likely to react and die.
        """
        pass


class Police(Agent):
    """
    A policeperson that walks around, intervenes in incidents when happening around a moore buffer of one cell.

    The init is the same as the RandomWalker.
    """

    has_gun = True

    def __init__(self, unique_id, pos, has_gun=False):
        super().__init__(unique_id, pos)
        self.has_gun = has_gun

    def step(self):
        """
        A model step. Move, awaits confront. If has gun, more likely to react and die.
        """
        pass


class Aggressor(Agent):
    """
    An aggressor that walks around, looking for victims.
    """

    has_gun = True

    def __init__(self, unique_id, pos, has_gun=True):
        super().__init__(unique_id, pos)
        self.has_gun = has_gun

    def step(self):
        pass

        # If there are victims present, confront one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        victim = [obj for obj in this_cell if isinstance(obj, Victim)]
        neighbors = self.model.grid.get_neighbors(self.pos, True)
        police = [obj for obj in neighbors if isinstance(obj, Police)]
        if len(victim) > 0:
            victim_to_attack = self.random.choice(victim)

            # Confront
            if len(police) > 0:
                if self.random.random() < self.model.police_letality:
                    # Aggressor dies
                    self.model.grid._remove_agent(self.pos, self)
                    self.model.schedule.remove(self)
                else:
                    # Police dies
                    bobby = self.random.choice(police)
                    self.model.grid._remove_agent(bobby.pos, bobby)
                    self.model.schedule.remove(bobby)

            elif victim_to_attack.has_gun:
                # Victim decides to react
                if self.random.random() < self.model.reaction_if_has_gun:
                    # Who gets hurt
                    if self.random.random() < self.model.chance_death_gun:
                        # Victim dies
                        self.model.grid._remove_agent(self.pos, victim_to_attack)
                        self.model.schedule.remove(victim_to_attack)
                    else:
                        # Aggressor dies
                        self.model.grid._remove_agent(self.pos, self)
                        self.model.schedule.remove(self)
