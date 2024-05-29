from src.game.players import Player
from src.game.units import Unit


class AIBot:
    def __init__(self, player):
        self.player = player

    def perform_actions(self, all_units: list["Unit"], other_player: "Player"):
        raise NotImplementedError("This method should be overridden by subclasses")

    def spawn_unit(self, unit_type=None):
        raise NotImplementedError("This method should be overridden by subclasses")

    def can_afford(self, unit):
        return self.player.money >= unit.price

    def update(self):
        # check if player can upgrade Age
        if self.player.xp >= self.player.next_age_xp:
            self.player.upgrade_age()

    def get_spawn_position(self):
        return self.player.base.get_spawn_position()
