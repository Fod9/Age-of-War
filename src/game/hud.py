from typing import Tuple, Callable, Union

import pygame

from src.game.players import Player
from src.game.units import Infantry, Support, Heavy, AntiTank

from src.game.units import Infantry, Support, Heavy, AntiTank
import pygame

from src.game.units import Infantry, Support, Heavy, AntiTank
import pygame


class HUD:
    def __init__(self, player: Player):
        self.player = player
        self.font = pygame.font.Font(None, 36)
        self.buttons = []
        self.initialize_buttons()

    def initialize_buttons(self):
        baseline = pygame.display.get_surface().get_height() - 20
        button_size = pygame.display.get_surface().get_width() // 20
        size = (button_size, button_size)
        spacing = 20

        # Chargement des images des boutons et des classes associées à chaque bouton
        buttons_data = [
            ("assets/hud/Infantry.png", Infantry, Infantry.build_time, Infantry.price),
            ("assets/hud/Support.png", Support, Support.build_time, Support.price),
            ("assets/hud/Heavy.png", Heavy, Heavy.build_time, Heavy.price),
            ("assets/hud/AntiTank.png", AntiTank, AntiTank.build_time, AntiTank.price)
        ]

        # Initialisation des boutons
        for i, (image_path, unit_class, build_time, price) in enumerate(buttons_data):
            x_position = 100 + i * (button_size + spacing)
            y_position = baseline - button_size
            button = Button(pygame.image.load(image_path), (x_position, y_position), size,
                            action=lambda :
                            self.player.add_unit(
                                unit_class(age=self.player.age, team=self.player.team)
                            ), build_time=build_time, player=self.player, price=price)
            self.buttons.append(button)

    def draw(self, screen):
        # Draw money
        money_text = self.font.render(f"Money: {self.player.money}", True, (0, 0, 0))
        screen.blit(money_text, (20, 20))
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

    def update(self):
        for button in self.buttons:
            button.update()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


class Button:

    player: Union[Player,None]

    def __init__(self, image: pygame.Surface, position: Tuple[int, int], size: Tuple[int, int], action: Callable =
    None, build_time: int = 0, player=None, price=0):
        self.image = pygame.transform.scale(image, size)
        self.position = position
        self.size = size
        self.action = action
        self.rect = pygame.Rect(position, size)
        self.build_time = build_time
        self.cooldown = 0
        self.last_click_time = 0
        self.price = price
        self.player = player

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.position)
        if self.cooldown > 0:
            overlay = pygame.Surface(self.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, self.position)
            cooldown_text = pygame.font.Font(None, 36).render(str(self.cooldown), True, (255, 255, 255))
            screen.blit(cooldown_text, (self.position[0] + self.size[0] // 2 - cooldown_text.get_width() // 2,
                                        self.position[1] + self.size[1] // 2 - cooldown_text.get_height() // 2))

    def is_hovered(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        # Check if the button is hovered and the player has enough money to buy the unit
        if self.action and self.cooldown == 0 and self.player.money >= self.price:
            self.action()
            self.cooldown = self.build_time
            self.last_click_time = pygame.time.get_ticks()

    def update(self):
        if self.cooldown > 0:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.last_click_time) / 1000
            self.cooldown = max(0, self.build_time - int(elapsed_time))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_hovered(event.pos):
                    self.click()
