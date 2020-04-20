from guns.random_walk import RandomWalker


class Victim(RandomWalker):
    """
    A victim that walks around, incurs in chance of getting mugged.

    The init is the same as the RandomWalker.
    """

    has_gun = False

    def __init__(self, unique_id, pos, model, moore, has_gun=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.has_gun = has_gun

    def step(self):
        """
        A model step. Move, awaits confront. If has gun, more likely to react and die.
        """
        self.random_move()


class Aggressor(RandomWalker):
    """
    An aggressor that walks around, looking for victims.
    """

    has_gun = True

    def __init__(self, unique_id, pos, model, moore, has_gun=True):
        super().__init__(unique_id, pos, model, moore=moore)
        self.has_gun = has_gun

    def step(self):
        self.random_move()

        # If there are victims present, confront one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        victim = [obj for obj in this_cell if isinstance(obj, Victim)]
        if len(victim) > 0:
            victim_to_attack = self.random.choice(victim)

            # Confront
            if victim_to_attack.has_gun:
                print('victim has hun')
                if self.random.random() < self.model.reaction_if_has_gun / 100:
                    if self.random.random() < self.model.chance_death_gun / 100:
                        self.model.grid._remove_agent(self.pos, victim_to_attack)
                        self.model.schedule.remove(victim_to_attack)
