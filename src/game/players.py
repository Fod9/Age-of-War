import pygame
from src.game.units import Infantry, Support, Heavy, AntiTank, Unit
from src.game.base import Base
from typing import List

from src.game.units import Infantry, Support, Heavy, AntiTank, Unit
from src.game.base import Base
from typing import List


class Player:
    def __init__(self, name: str, team: str, age: int = 1):
        self.name = name
        self.team = team
        self.age = age
        self.money = 30
        self.base = Base(name=f"{team}_base", owner=team, age=self.age)
        self.units = []
        self.queue = []
        self.last_money_update = pygame.time.get_ticks()
        self.xp = 0
        self.next_age_xp = 100

        self.gold_multiplier = 1
        self.gold_upgrade_cost = 10

        self.damage_multiplier = {
            "Infantry": 1,
            "Support": 1,
            "Heavy": 1,
            "AntiTank": 1
        }

        self.hp_multiplier = {
            "Infantry": 1,
            "Support": 1,
            "Heavy": 1,
            "AntiTank": 1
        }

        self.range_multiplier = {
            "Infantry": 1,
            "Support": 1,
            "Heavy": 1,
            "AntiTank": 1
        }

        self.damage_upgrade_cost = {
            "Infantry": 10,
            "Support": 10,
            "Heavy": 10,
            "AntiTank": 10
        }

        self.hp_upgrade_cost = {
            "Infantry": 10,
            "Support": 10,
            "Heavy": 10,
            "AntiTank": 10
        }

        self.range_upgrade_cost = {
            "Infantry": 10,
            "Support": 10,
            "Heavy": 10,
            "AntiTank": 10
        }

    def update(self, all_units: List[Unit], other_player: "Player"):
        for unit in self.units[:]:
            unit.update(all_units, self, other_player)

        # Update money every 2 seconds
        if pygame.time.get_ticks() - self.last_money_update > 2000:
            self.money += 2
            self.last_money_update = pygame.time.get_ticks()

        # Check if the build time has passed for the first unit in the queue
        if self.queue:
            unit = self.queue[0]
            if pygame.time.get_ticks() - unit.build_start_time > unit.build_time * 1000:
                self.units.append(unit)
                self.queue.pop(0)

        # Update the base
        self.base.update()

    def add_unit(self, unit: Unit):

        # Check if another unit is placed at the same position
        for u in self.units:
            if u.position[0] == unit.position[0] or u.position[0] - 50 <= unit.position[0] <= u.position[0] + 50:
                return

        if self.money >= unit.price:
            # Apply multipliers
            unit.damage *= self.damage_multiplier[unit.nom]
            unit.HP *= self.hp_multiplier[unit.nom]
            unit.max_health *= self.hp_multiplier[unit.nom]
            unit.range *= self.range_multiplier[unit.nom]

            # Check if the unit is already in the queue
            if not any(isinstance(q_unit, unit.__class__) for q_unit in self.queue):
                unit.build_start_time = pygame.time.get_ticks()
                self.queue.append(unit)
                self.money -= unit.price
            else:
                print(f"Cannot add {unit.nom}: Another {unit.nom} is already being built.")

    def remove_unit(self, unit: Unit):
        self.units.remove(unit)

    def upgrade_damage(self, unit_type: str):
        if self.money >= self.damage_upgrade_cost[unit_type]:
            print(f"Upgrading damage for {unit_type}")
            self.damage_multiplier[unit_type] += 0.2
            print(self.money)
            print(self.damage_upgrade_cost[unit_type])
            self.money -= self.damage_upgrade_cost[unit_type]
            self.damage_upgrade_cost[unit_type] *= 1.5

    def upgrade_hp(self, unit_type: str):
        if self.money >= self.hp_upgrade_cost[unit_type]:
            print(f"Upgrading HP for {unit_type}")
            self.hp_multiplier[unit_type] += 0.2
            print(self.hp_upgrade_cost[unit_type])
            self.money -= self.hp_upgrade_cost[unit_type]
            self.hp_upgrade_cost[unit_type] *= 1.5

    def upgrade_range(self, unit_type: str):
        if self.money >= self.range_upgrade_cost[unit_type]:
            print(f"Upgrading Range for {unit_type}")
            self.range_multiplier[unit_type] += 0.2
            print(self.range_upgrade_cost[unit_type])
            self.money -= self.range_upgrade_cost[unit_type]
            self.range_upgrade_cost[unit_type] *= 1.5

    def upgrade_gold_per_kill(self):
        print(f"Upgrading GOLD")
        if self.money >= self.gold_upgrade_cost:
            self.gold_multiplier += 0.2
            self.money -= self.gold_upgrade_cost
            self.gold_upgrade_cost *= 2

    def upgrade_age(self):
        if self.xp >= self.next_age_xp and self.age < 4:
            self.age += 1
            self.next_age_xp *= 2
            self.base.upgrade_age()
            self.xp = 0
            #send to the game that the age has changed
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"age": self.age}))

    def get_upgrade_cost(self, upgrade_type, unit_type=None) -> int:
        if upgrade_type == "gold":
            return self.gold_upgrade_cost
        if upgrade_type == "damage":
            return self.damage_upgrade_cost[unit_type]
        elif upgrade_type == "hp":
            return self.hp_upgrade_cost[unit_type]
        elif upgrade_type == "range":
            return self.range_upgrade_cost[unit_type]
        else:
            raise ValueError(f"Unknown upgrade type: {upgrade_type}")

