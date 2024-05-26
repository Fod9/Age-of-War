from typing import Tuple, Union
import pygame


class Slot:
    id: int
    screen: pygame.Surface
    turret: bool

    def __init__(self, image: pygame.Surface, team: str = "B"):
        self.id = id(self)
        self.image = pygame.transform.scale(image, (int(image.get_width() * .5), int(image.get_height() * .5)))
        self.screen = pygame.display.get_surface()
        self.turret = False

        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()
        y_position = screen_height - 300

        if team == "B":
            x_position = int(screen_width * 0.05)
        else:
            x_position = screen_width - int(screen_width * 0.05) - self.image.get_width()

        self.position = (x_position, y_position)
        self.collide_rect = self.image.get_rect(topleft=self.position)
        self.team = team

    def __str__(self):
        return f"Turret: {self.turret}"

    def update(self):
        pass

    def add_turret(self):
        self.turret = True

    def remove_turret(self):
        self.turret = False
