import pygame
from src.game.units import Infantry, Support, Heavy, AntiTank, Unit
from src.game.base import Base
from typing import List


import pygame
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

    def update(self, all_units: List[Unit], other_player: "Player"):
        for unit in self.units[:]:
            unit.update(all_units, self, other_player)

        # Update money every 5 seconds
        if pygame.time.get_ticks() - self.last_money_update > 2000:
            self.money += 1
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
        if self.money >= unit.price:
            # Check if the unit is already in the queue
            if not any(isinstance(q_unit, unit.__class__) for q_unit in self.queue):
                unit.build_start_time = pygame.time.get_ticks()
                self.queue.append(unit)
                self.money -= unit.price
            else:
                print(f"Cannot add {unit.nom}: Another {unit.nom} is already being built.")

    def remove_unit(self, unit: Unit):
        self.units.remove(unit)
