import pygame
from src.game.units import Infantry, Support, Heavy, AntiTank, Unit
from src.game.base import Base
from typing import List

class Player:
    def __init__(self, name: str, team: str, age: int = 1):
        self.name = name
        self.team = team
        self.age = age
        self.base = Base(name=f"{team}_base", owner=team, age=self.age)
        self.units = self._initialize_units()

    def _initialize_units(self) -> List[Unit]:
        # Initialize units based on the team and age
        units = []
        if self.team == "R":
            units = [
                Infantry((800, 550), age=self.age, team=self.team),
                Infantry((750, 550), age=self.age, team=self.team),
                Infantry((700, 550), age=self.age, team=self.team),
                AntiTank((600, 550), age=self.age, team=self.team)
            ]
        elif self.team == "B":
            units = [
                Heavy((300, 550), age=self.age, team=self.team),
                Support((200, 550), age=self.age, team=self.team),
                Infantry((100, 550), age=self.age, team=self.team),
                Infantry((50, 550), age=self.age, team=self.team)
            ]
        return units

    def draw(self, screen: pygame.Surface):
        self.base.draw(screen)
        for unit in self.units:
            unit.draw(screen)

    def update(self, units: List[Unit]):
        for unit in self.units:
            unit.update(units)

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def remove_unit(self, unit: Unit):
        self.units.remove(unit)
