import random

from src.ai.base_ai import AIBot
from src.game.units import Infantry, Support, Heavy, AntiTank


class EasyBot(AIBot):
    def __init__(self, player):
        super().__init__(player)

    def perform_actions(self):
        if random.random() < 0.1:  # 10% chance to spawn a unit
            self.spawn_unit()

    def spawn_unit(self):
        available_units = [Infantry, Support, Heavy, AntiTank]
        chosen_unit = random.choice(available_units)
        new_unit = chosen_unit(age=self.player.age, team=self.player.team)
        self.player.add_unit(new_unit)