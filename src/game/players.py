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
        if pygame.time.get_ticks() - self.last_money_update > 500:
            self.money += 1
            self.last_money_update = pygame.time.get_ticks()

            # Check if the build time has passed for the first unit in the queue
            if self.queue:
                unit = self.queue[0]
                if pygame.time.get_ticks() - unit.build_start_time > unit.build_time * 1_000:
                    self.units.append(unit)
                    self.queue.pop(0)
                    print(f"Unit {unit.nom} built")

    def add_unit(self, unit: Unit):
        if self.money >= unit.price:
            unit.build_start_time = pygame.time.get_ticks()
            self.queue.append(unit)
            self.money -= unit.price

    def remove_unit(self, unit: Unit):
        self.units.remove(unit)
