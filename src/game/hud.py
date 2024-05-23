from typing import Tuple, Callable

import pygame

from src.game.units import Infantry, Support, Heavy, AntiTank


class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)
        self.buttons = []
        self.initialize_buttons()

    def initialize_buttons(self):
        baseline = pygame.display.get_surface().get_height() - 20
        button_size = pygame.display.get_surface().get_width() // 20
        size = (button_size, button_size)
        spacing = 20

        # Chargement des images des boutons
        buttons_data = [
            ("assets/hud/Infantry.png", "Infantry"),
            ("assets/hud/Support.png", "Support"),
            ("assets/hud/Heavy.png", "Heavy"),
            ("assets/hud/AntiTank.png", "AntiTank")
        ]

        # Initialisation des boutons
        for i, (image_path, name) in enumerate(buttons_data):
            x_position = 100 + i * (button_size + spacing)
            y_position = baseline - button_size
            if name == "Infantry":
                button = Button(pygame.image.load(image_path), (x_position, y_position), size, action=lambda: self.player.add_unit(
                    Infantry(age=self.player.age, team=self.player.team)
                ))
            elif name == "Support":
                button = Button(pygame.image.load(image_path), (x_position, y_position), size, action=lambda: self.player.add_unit(
                    Support(age=self.player.age, team=self.player.team)
                ))
            elif name == "Heavy":
                button = Button(pygame.image.load(image_path), (x_position, y_position), size, action=lambda: self.player.add_unit(
                    Heavy(age=self.player.age, team=self.player.team)
                ))
            elif name == "AntiTank":
                button = Button(pygame.image.load(image_path), (x_position, y_position), size, action=lambda: self.player.add_unit(
                    AntiTank(age=self.player.age, team=self.player.team)
                ))

            self.buttons.append(button)

    def draw(self, screen):
        # Draw money
        money_text = self.font.render(f"Money: {self.player.money}", True, (0, 0, 0))
        screen.blit(money_text, (20, 20))
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


class Button:
    def __init__(self, image: pygame.Surface, position: Tuple[int, int], size: Tuple[int, int], action: Callable = None):
        self.image = pygame.transform.scale(image, size)
        self.position = position
        self.size = size
        self.action = action
        self.rect = pygame.Rect(position, size)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.position)

    def is_hovered(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.action:
            self.action()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_hovered(event.pos):
                    self.click()


