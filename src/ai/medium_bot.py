from random import choice
from random import random

from src.ai.base_ai import AIBot
from src.game.players import Player
from src.game.units import Unit, Infantry, Support, Heavy, AntiTank


class Medium_bot(AIBot):
    # This bot will have a decision tree to decide what to do
    def __init__(self, player: "Player"):
        super().__init__(player)

    def perform_actions(self, all_units: list["Unit"], other_player: "Player"):

        all_units_type = {
            "Infantry": {"unit": Infantry, "count": 0},
            "Support": {"unit": Support, "count": 0},
            "Heavy": {"unit": Heavy, "count": 0},
            "AntiTank": {"unit": AntiTank, "count": 0}
        }

        # 10% chance to upgrade a unit
        if random() < 0.05:
            self.upgrade_unit()
            return
        elif random() < 0.5:
            for unit in other_player.units:
                all_units_type[unit.__class__.__name__]["count"] += 1

            most_common_unit = max(all_units_type, key=lambda x: all_units_type[x]["count"])

            weak_against = all_units_type[most_common_unit]["unit"].weak_against

            # If the player has more of the most common unit, spawn a unit that is strong against it
            if all_units_type[most_common_unit]["count"] > len(other_player.units) / 2:
                for unit in all_units_type:
                    if unit in weak_against:
                        self.spawn_unit(all_units_type[unit]["unit"])
                        break
            else:
                self.spawn_unit(all_units_type[most_common_unit]["unit"])

    def upgrade_unit(self):

        # Choose a random unit
        available_units = ["Infantry", "Support", "Heavy", "AntiTank"]
        chosen_unit = choice(available_units)

        available_upgrade = [self.player.upgrade_damage, self.player.upgrade_hp,
                             self.player.upgrade_range]
        upgrade = choice(available_upgrade)
        upgrade(chosen_unit)

    def spawn_unit(self, unit_type=None):
        if unit_type is None:
            # Choose a random unit
            available_units = [Infantry, Support, Heavy, AntiTank]
            chosen_unit = choice(available_units)
        else:
            chosen_unit = unit_type

        unit_instance = chosen_unit(age=self.player.age, team=self.player.team)
        if self.can_afford(unit_instance):
            self.player.add_unit(chosen_unit(age=self.player.age, team=self.player.team))
