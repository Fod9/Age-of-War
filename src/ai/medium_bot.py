import random

from src.ai.base_ai import AIBot
from src.game.players import Player
from src.game.units import Infantry, Support, Heavy, AntiTank


class MediumBot(AIBot):
    def __init__(self, player: Player):
        super().__init__(player)
        self.unit_memory = {
            "Infantry": 0,
            "Support": 0,
            "Heavy": 0,
            "AntiTank": 0
        }

    def perform_actions(self, all_units: list["Unit"], other_player: "Player"):
        evaluation = self.evaluate_unit(all_units, other_player)
        print(evaluation)

        if evaluation > 0:
            self.play_aggressively()
        elif evaluation == 0:
            self.play_balanced()
        else:
            self.play_defensively()

    def evaluate_unit(self, all_unit: list["Unit"], other_player: "Player"):
        enemie_units_on_board = other_player.units
        self_units_on_board = self.player.units

        enemie_base_position = other_player.base.position
        self_base_position = self.player.base.position

        if len(enemie_units_on_board) != 0:
            enemie_distance = abs(enemie_units_on_board[0].position[0] - enemie_base_position[0])
        else:
            enemie_distance = abs(enemie_base_position[0] - self_base_position[0])

        if len(self_units_on_board) != 0:
            self_distance = abs(self_units_on_board[0].position[0] - self_base_position[0])
        else:
            self_distance = abs(self_base_position[0] - enemie_base_position[0])

        # Who is closer to the base?
        if enemie_distance < self_distance:
            # enemie is closer
            pos_score = 1
        elif enemie_distance == self_distance:
            # both are at the same distance
            pos_score = 0
        else:
            # self is closer
            pos_score = -1

        # Who has more units?
        if len(enemie_units_on_board) > len(self_units_on_board):
            # enemie has more units
            unit_score = 1
        elif len(enemie_units_on_board) == len(self_units_on_board):
            # both have the same amount of units
            unit_score = 0
        else:
            # self has more units
            unit_score = -1

        # Who has more money?
        if other_player.money > self.player.money:
            # enemie has more money
            money_score = 1
        elif other_player.money == self.player.money:
            # both have the same amount of money
            money_score = 0
        else:
            # self has more money
            money_score = -1

        # Who counters the largest amount of units?
        self_unit_counter = 0
        enemie_unit_counter = 0
        for unit in self_units_on_board:
            for enemie_unit in enemie_units_on_board:
                if unit.weak_against == enemie_unit.nom:
                    self_unit_counter += 1

        for enemie_unit in enemie_units_on_board:
            for unit in self_units_on_board:
                if enemie_unit.weak_against == unit.nom:
                    enemie_unit_counter += 1

        if self_unit_counter > enemie_unit_counter:
            counter_score = 1
        elif self_unit_counter == enemie_unit_counter:
            counter_score = 0
        else:
            counter_score = -1

        return pos_score + unit_score + money_score + counter_score

    def play_aggressively(self):
        self.spawn_unit()  # Prioritize spawning more units

    def play_balanced(self):
        if random.random() < 0.5:
            self.spawn_unit()
        else:
            self.attempt_upgrade()

    def play_defensively(self):
        self.spawn_defensive_units()
        self.attempt_upgrade()  # Prioritize upgrading

    def spawn_unit(self):
        available_units = [Infantry, Support, Heavy, AntiTank]
        chosen_unit = random.choice(available_units)
        if self.can_afford(chosen_unit):
            self.player.add_unit(chosen_unit(age=self.player.age, team=self.player.team))
            self.unit_memory[chosen_unit.__name__] += 1
            print(f"Spawned unit: {chosen_unit.__name__}")

    def spawn_defensive_units(self):
        # Prioritize spawning more defensive or support units
        defensive_units = [Heavy, Support]
        chosen_unit = random.choice(defensive_units)
        if self.can_afford(chosen_unit):
            self.player.add_unit(chosen_unit(age=self.player.age, team=self.player.team))
            self.unit_memory[chosen_unit.__name__] += 1
            print(f"Spawned defensive unit: {chosen_unit.__name__}")

    def attempt_upgrade(self):
        available_upgrades = ["damage", "hp", "range", "gold"]
        chosen_upgrade = random.choice(available_upgrades)
        if chosen_upgrade == "gold":
            if self.can_afford_upgrade("gold", "gold"):
                self.player.upgrade_gold_per_kill()
                print(f"Upgraded Gold per Kill")
        else:
            most_used_unit = max(self.unit_memory, key=self.unit_memory.get)
            print(f"Chosen upgrade: {chosen_upgrade}")
            print(f"Most used unit: {most_used_unit}")
            if self.can_afford_upgrade(chosen_upgrade,most_used_unit):
                if chosen_upgrade == "damage":
                    self.player.upgrade_damage(most_used_unit)
                elif chosen_upgrade == "hp":
                    self.player.upgrade_hp(most_used_unit)
                elif chosen_upgrade == "range":
                    self.player.upgrade_range(most_used_unit)
                print(f"Upgraded {chosen_upgrade} for {most_used_unit}")

    def can_afford(self, unit):
        if self.player.money >= unit.price:
            return True
        return False

    def can_afford_upgrade(self, unit, upgrade):
        if self.player.money >= self.player.get_upgrade_cost(unit, upgrade):
            return True
        return False


