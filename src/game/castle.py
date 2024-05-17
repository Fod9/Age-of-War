# src/game/castle.py

import pygame


class Castle:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.units = []
        self.turrets = []
        self.castle_image = pygame.image.load(f'assets/castle/{owner}_castle.png').convert_alpha()

    def handle_resize(self, screen):
        self.castle_image = pygame.image.load(f'assets/castle/{self.owner}_castle.png').convert_alpha()
        self.castle_image = pygame.image.load(f'assets/castle/{self.owner}_castle.png').convert_alpha()
        self.draw(screen)

    def draw(self, screen):
        # ? get the screen size
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # ? define positions for the castles
        if self.owner == "red":
            castle_x = screen_width - self.castle_image.get_width()
            castle_y = screen_height - self.castle_image.get_height()
        else:
            castle_x = 0
            castle_y = screen_height - self.castle_image.get_height()

        castle_width = screen_width * 0.8
        castle_height = screen_height * 0.8

        # ? resize the castles
        self.castle_image = pygame.transform.scale(self.castle_image, (int(castle_width), int(castle_height)))

        # ? Draw the castles
        screen.blit(self.castle_image, (castle_x, castle_y))
