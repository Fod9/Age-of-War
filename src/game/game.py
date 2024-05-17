# src/game/game.py

import pygame
from src.game.castle import Castle
class Game:

    def __init__(self, screen):

        self.red_castle = Castle("red", "red")
        self.blue_castle = Castle("blue", "blue")
        self.screen = screen
        self.running = True
        self.units = []
        self.turrets = []

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.red_castle.handle_resize(self.screen)
            self.blue_castle.handle_resize(self.screen)

    def update(self):
        pass

    def draw(self, screen):
        # Draw a line between the castles
        pygame.draw.line(screen, (235, 195, 136), (0, screen.get_height() / 1.13), (screen.get_width(),
                                                                                   screen.get_height() / 1.13), 70)
        # ? draw castles
        self.red_castle.draw(screen)
        self.blue_castle.draw(screen)

        for unit in self.units:
            unit.draw(screen)
        for turret in self.turrets:
            turret.draw(screen)
