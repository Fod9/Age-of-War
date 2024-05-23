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
        self.units = self._initialize_units()
        self.last_money_update = pygame.time.get_ticks()

    def _initialize_units(self) -> List[Unit]:
        # Initialize units based on the team and age
        units = []
        if self.team == "R":
            units = [
                Infantry(age=self.age, team=self.team),
                Infantry(age=self.age, team=self.team),
                Infantry(age=self.age, team=self.team),
                AntiTank(age=self.age, team=self.team)
            ]
        elif self.team == "B":
            units = [
                Heavy(age=self.age, team=self.team),
                Support(age=self.age, team=self.team),
                Infantry(age=self.age, team=self.team),
                Infantry(age=self.age, team=self.team)
            ]
        return units

    def update(self, all_units: List[Unit]):
        for unit in self.units[:]:
            unit.update(all_units, self)

        # Update money every 5 seconds
        if pygame.time.get_ticks() - self.last_money_update > 2_000:
            self.money += 1
            self.last_money_update = pygame.time.get_ticks()

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def remove_unit(self, unit: Unit):
        self.units.remove(unit)
