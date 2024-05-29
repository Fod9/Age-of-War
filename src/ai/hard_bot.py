import random
from src.ai.base_ai import AIBot
from src.game.players import Player
from src.game.units import Infantry, Support, Heavy, AntiTank
import pygame


class HardBot(AIBot):
    def __init__(self, player: Player, other_player: Player):
        super().__init__(player)
        self.unit_memory = {
            "Infantry": 0,
            "Support": 0,
            "Heavy": 0,
            "AntiTank": 0
        }
        self.enemy_memory = {
            "Infantry": 0,
            "Support": 0,
            "Heavy": 0,
            "AntiTank": 0
        }
        self.other_player = other_player
        self.savings_threshold = 25
        self.last_evaluation = pygame.time.get_ticks()

    def perform_actions(self, all_units: list["Unit"], other_player: "Player"):
        self.update_memory()
        evaluation = self.evaluate_unit(all_units)

        if evaluation >= 0:
            self.play_aggressively()
        else:
            self.play_defensively()

    def update_memory(self):
        self.unit_memory = {unit_type: 0 for unit_type in self.unit_memory}
        self.enemy_memory = {unit_type: 0 for unit_type in self.enemy_memory}

        for unit in self.player.units:
            self.unit_memory[type(unit).__name__] += 1

        for unit in self.other_player.units:
            self.enemy_memory[type(unit).__name__] += 1

    def evaluate_unit(self, all_unit: list["Unit"]):
        enemie_units_on_board = self.other_player.units
        self_units_on_board = self.player.units

        enemie_base_position = self.other_player.base.position
        self_base_position = self.player.base.position

        # Dynamic distance evaluation
        if enemie_units_on_board:
            enemie_distance = sum(
                [abs(unit.position[0] - enemie_base_position[0]) for unit in enemie_units_on_board]) / len(
                enemie_units_on_board)
        else:
            enemie_distance = abs(enemie_base_position[0] - self_base_position[0])

        if self_units_on_board:
            self_distance = sum([abs(unit.position[0] - self_base_position[0]) for unit in self_units_on_board]) / len(
                self_units_on_board)
        else:
            self_distance = abs(self_base_position[0] - enemie_base_position[0])

        pos_score = -1 if enemie_distance < self_distance else 1 if enemie_distance > self_distance else 0

        # Number of units
        unit_score = 2 if len(enemie_units_on_board) < len(self_units_on_board) else 0 if len(
            enemie_units_on_board) == len(self_units_on_board) else -1

        # Money comparison
        money_score = 2 if self.other_player.money < self.player.money else 0 if self.other_player.money == self.player.money else -1

        # Unit counter
        self_unit_counter = sum(1 for unit in self_units_on_board for enemie_unit in enemie_units_on_board if
                                unit.weak_against == enemie_unit.nom)
        enemie_unit_counter = sum(1 for enemie_unit in enemie_units_on_board for unit in self_units_on_board if
                                  enemie_unit.weak_against == unit.nom)
        counter_score = 2 if self_unit_counter > enemie_unit_counter else 0 if self_unit_counter == enemie_unit_counter else -1

        # Base health comparison
        base_health_score = 2 if self.player.base.HP > self.other_player.base.HP else 0 if self.player.base.HP == self.other_player.base.HP else -1

        # Diversity of units
        diversity_score = 1 if len(set(type(unit).__name__ for unit in self_units_on_board)) > len(
            set(type(unit).__name__ for unit in enemie_units_on_board)) else 0

        return pos_score + unit_score + money_score + counter_score + base_health_score + diversity_score

    def play_aggressively(self):
        print("JE JOUE AGRESSIF FDP")
        if self.player.money > self.savings_threshold:
            self.spawn_combo_units()
        else:
            self.spawn_units()
            self.attempt_upgrade()

    def play_defensively(self):
        print("JE JOUE DEFENSIF FDP")
        self.spawn_defensive_units()

    def spawn_units(self):
        available_units = [Infantry, Heavy, AntiTank]
        chosen_unit = random.choice(available_units)

        if self.can_afford(chosen_unit):
            self.player.add_unit(chosen_unit(age=self.player.age, team=self.player.team))
            self.unit_memory[chosen_unit.__name__] += 1
            print(f"Spawned unit: {chosen_unit.__name__}")

    def spawn_combo_units(self):
        combo_units = [
            (Heavy, Support),
            (Infantry, Support)
        ]
        chosen_combo = random.choice(combo_units)
        for unit in chosen_combo:
            if self.can_afford(unit):
                self.player.add_unit(unit(age=self.player.age, team=self.player.team))
                self.unit_memory[unit.__name__] += 1
                print(f"Spawned unit: {unit.__name__}")

    def spawn_defensive_units(self):
        defensive_units = [Heavy, Infantry]
        most_common_enemy_unit = max(self.enemy_memory, key=self.enemy_memory.get)
        print(f"J'ai : {self.player.money} et l'ennemi a : {self.other_player.money}")
        if most_common_enemy_unit == "Infantry":
            chosen_unit = Heavy
        elif most_common_enemy_unit == "Heavy":
            chosen_unit = Infantry
        else:
            chosen_unit = random.choice(defensive_units)

        if self.can_afford(chosen_unit):
            self.player.add_unit(chosen_unit(age=self.player.age, team=self.player.team))
            self.unit_memory[chosen_unit.__name__] += 1
            print(f"Spawned unit: {chosen_unit.__name__}")

    def attempt_upgrade(self):
        available_upgrades = ["damage", "hp", "range", "gold"]
        chosen_upgrade = random.choice(available_upgrades)
        if chosen_upgrade == "gold":
            if self.can_afford_upgrade("gold", "gold"):
                self.player.upgrade_gold_per_kill()
        else:
            most_used_unit = max(self.unit_memory, key=self.unit_memory.get)
            if self.can_afford_upgrade(chosen_upgrade, most_used_unit):
                if chosen_upgrade == "damage":
                    self.player.upgrade_damage(most_used_unit)
                elif chosen_upgrade == "hp":
                    self.player.upgrade_hp(most_used_unit)
                elif chosen_upgrade == "range":
                    self.player.upgrade_range(most_used_unit)
                print(f"Upgraded {chosen_upgrade} for {most_used_unit}")

            # Upgrade units that counter enemy's most used units
            most_used_enemy_unit = max(self.enemy_memory, key=self.enemy_memory.get)
            weak_against = {"Infantry": "Heavy", "Support": "Infantry", "Heavy": "AntiTank", "AntiTank": "Support"}
            counter_unit = weak_against.get(most_used_enemy_unit)
            if self.can_afford_upgrade(chosen_upgrade, counter_unit):
                if chosen_upgrade == "damage":
                    self.player.upgrade_damage(counter_unit)
                elif chosen_upgrade == "hp":
                    self.player.upgrade_hp(counter_unit)
                elif chosen_upgrade == "range":
                    self.player.upgrade_range(counter_unit)
                print(f"Upgraded {chosen_upgrade} for {counter_unit} to counter {most_used_enemy_unit}")

    def can_afford(self, unit):
        return self.player.money >= unit.price

    def can_afford_soon(self, unit):
        # check in how many seconds the player will be able to afford the unit ( 2 gold per 2 seconds)
        seconds = (unit.price - self.player.money) / 2
        return seconds

    def can_afford_upgrade(self, unit, upgrade):
        return self.player.money >= self.player.get_upgrade_cost(unit, upgrade)
