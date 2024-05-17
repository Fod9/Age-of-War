# src/game/game.py

import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.units = []
        self.turrets = []

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        b = 20

        pygame.draw.rect(screen, (255, 0, 0), (a, b, 100, 100))

        for unit in self.units:
            unit.draw(screen)
        for turret in self.turrets:
            turret.draw(screen)
