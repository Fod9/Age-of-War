from random import choice, random
from src.ai.base_ai import AIBot
from src.game.players import Player
from src.game.units import Unit, Infantry, Support, Heavy, AntiTank

class HardBot(AIBot):
    def __init__(self, player: "Player"):
        super().__init__(player)
        self.unit_memory = {
            "Infantry": 0,
            "Support": 0,
            "Heavy": 0,
            "AntiTank": 0
        }
        self.enemy_unit_counts = {
            "Infantry": 0,
            "Support": 0,
            "Heavy": 0,
            "AntiTank": 0
        }
        self.savings_threshold = 50  # Amount of money to save before considering upgrades

    def perform_actions(self, all_units: list["Unit"], other_player: "Player"):
        self.evaluate_enemy_units(other_player)
        self.make_strategic_decisions(other_player)
        self.manage_resources()

    def evaluate_enemy_units(self, other_player: "Player"):
        for unit in self.enemy_unit_counts:
            self.enemy_unit_counts[unit] = 0
        for unit in other_player.units:
            self.enemy_unit_counts[unit.__class__.__name__] += 1

    def manage_resources(self):
        # Balance between saving money, upgrading units, and spawning units
        if self.player.money >= self.savings_threshold:
            if random() < 0.3:
                self.attempt_upgrade()
            else:
                self.spawn_unit()
        elif random() < 0.9:
            self.spawn_unit()
        else:
            self.attempt_upgrade()

    def make_strategic_decisions(self, other_player: "Player"):
        common_unit = max(self.enemy_unit_counts, key=self.enemy_unit_counts.get)
        strong_against = {
            "Infantry": "AntiTank",
            "Support": "Infantry",
            "Heavy": "Support",
            "AntiTank": "Heavy"
        }
        if self.enemy_unit_counts[common_unit] > len(other_player.units) / 2:
            unit_to_spawn = strong_against[common_unit]
            self.spawn_unit(globals()[unit_to_spawn])
        else:
            self.spawn_unit()

    def attempt_upgrade(self):
        upgrades = ["Damage", "HP", "Range", "Gold"]
        if random() < 0.2:  # 20% chance to prioritize Gold per Kill upgrade
            upgrades.append("Gold")

        chosen_upgrade = choice(upgrades)
        if chosen_upgrade == "Gold":
            if self.player.can_afford_upgrade("Gold", "Gold"):
                self.player.upgrade_gold_per_kill()
        else:
            most_used_unit = max(self.unit_memory, key=self.unit_memory.get)
            if self.player.can_afford_upgrade(most_used_unit, chosen_upgrade):
                self.upgrade_unit(most_used_unit, chosen_upgrade)

    def upgrade_unit(self, unit_type: str, upgrade_type: str):
        if upgrade_type == "Damage":
            self.player.upgrade_damage(unit_type)
        elif upgrade_type == "HP":
            self.player.upgrade_hp(unit_type)
        elif upgrade_type == "Range":
            self.player.upgrade_range(unit_type)

    def spawn_unit(self, unit_type=None):
        if unit_type is None:
            available_units = [Infantry, Support, Heavy, AntiTank]
            chosen_unit = choice(available_units)
        else:
            chosen_unit = unit_type

        unit_instance = chosen_unit(age=self.player.age, team=self.player.team)
        if self.can_afford(unit_instance):
            self.player.add_unit(unit_instance)
            self.unit_memory[chosen_unit.__name__] += 1

    def can_afford(self, unit_instance):
        return self.player.money >= unit_instance.price
