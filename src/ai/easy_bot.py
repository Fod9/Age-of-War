import random

from src.ai.base_ai import AIBot
from src.game.players import Player
from src.game.units import Infantry, Support, Heavy, AntiTank


class EasyBot(AIBot):
    def __init__(self, player: Player):
        super().__init__(player)

    def perform_actions(self):
        if random.random() < 0.3:
            self.spawn_unit()

    def spawn_unit(self):
        available_units = [Infantry, Support, Heavy, AntiTank]
        chosen_unit = random.choice(available_units)
        unit_instance = chosen_unit(age=self.player.age, team=self.player.team)
        if self.can_afford(unit_instance):
            self.player.add_unit(chosen_unit(age=self.player.age, team=self.player.team))

