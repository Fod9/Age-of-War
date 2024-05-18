# src/game/game.py

import pygame
from src.game.base import Base
from src.game.units import Infantry, Support, Heavy, AntiTank


class Game:
    age: int
    background: pygame.Surface
    red_castle: Base
    blue_castle: Base
    screen: pygame.Surface
    running: bool
    units: list
    turrets: list

    def __init__(self, screen):
        self.age = 1
        self.background = pygame.image.load(f"assets/backgrounds/{self.age}/background.png").convert_alpha()
        self.red_castle = Base(name="red", owner="red", age=self.age)
        self.blue_castle = Base(name="blue", owner="blue", age=self.age)
        self.screen = screen
        self.running = True
        self.units = [
            Infantry((100, 100), age=self.age),
            Support((100, 200), age=self.age),
            Heavy((100, 300), age=self.age),
            AntiTank((100, 400), age=self.age),
        ]
        self.turrets = []

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            reload_image = pygame.image.load(f"assets/backgrounds/{self.age}/background.png").convert_alpha()
            self.background = pygame.transform.scale(reload_image,
                                                     (self.screen.get_width(), self.screen.get_height()))
            self.red_castle.handle_resize(self.screen)
            self.blue_castle.handle_resize(self.screen)

    def update(self):
        pass

    def draw(self, screen):
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        screen.blit(self.background, (0, 0))
        # ? draw castles
        self.red_castle.draw(screen)
        self.blue_castle.draw(screen)

        for unit in self.units:
            unit.update(self.units)
            unit.draw(screen)
        for turret in self.turrets:
            turret.draw(screen)
