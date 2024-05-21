# src/game/castle.py

import pygame


class Base:
    def __init__(self, name, owner, age):
        self.name = name
        self.owner = owner
        self.units = []
        self.turrets = []
        self.age = age
        self.h_percent = 0.8
        self.v_percent = 0.8
        self.heigth_offset = 1
        self.health = 100
        self.base_image = pygame.image.load(f'assets/base/{self.age}/{self.owner}_Base.png').convert_alpha()

    def handle_resize(self, screen):
        self.base_image = pygame.image.load(f'assets/base/{self.age}/{self.owner}_Base.png').convert_alpha()
        self.draw(screen)

    def define_render_params(self):
        if self.age == 1:
            self.h_percent = 1
            self.v_percent = 1
        elif self.age == 2:
            pass
        elif self.age == 3:
            self.heigth_offset = 0.8

    def draw(self, screen):

        # ? define the percentage of the screen the base will take
        self.define_render_params()

        # ? get the screen size
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # ? define positions for the base
        if self.owner == "red":
            castle_x = screen_width - self.base_image.get_width()
            castle_y = (screen_height - self.base_image.get_height()) * self.heigth_offset
        else:
            castle_x = 0
            castle_y = (screen_height - self.base_image.get_height()) * self.heigth_offset

        castle_width = screen_width * self.h_percent
        castle_height = screen_height * self.h_percent

        # ? resize the base
        self.base_image = pygame.transform.scale(self.base_image, (int(castle_width), int(castle_height)))

        # ? Draw the base
        screen.blit(self.base_image, (castle_x, castle_y))
