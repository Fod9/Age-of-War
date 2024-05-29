from typing import Tuple, Callable, Union
import pygame
from src.game.players import Player
from src.game.units import Infantry, Support, Heavy, AntiTank
from src.game.turrets import Cannon, Minigun, Laser


class HUD:
    def __init__(self, player: Player):
        self.player = player
        self.font = pygame.font.Font(None, 36)
        self.buttons = []
        self.upgrade_buttons = []
        self.slot_buttons = []
        self.turret_buttons = []
        self.upgrade_dialog = None
        self.sell_turret_dialog = None
        self.buy_turret_dialog = None
        self.initialize_buttons()

    def initialize_buttons(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_width(), screen.get_height()
        units_button_size = screen_width // 20
        upgrade_button_size = units_button_size
        units_size = (units_button_size, units_button_size)
        upgrade_size = (upgrade_button_size, upgrade_button_size)
        spacing = 20

        # Initialisation des boutons d'unité
        buttons_data = [
            ("assets/hud/Infantry.png", Infantry, Infantry.build_time, Infantry.price),
            ("assets/hud/Support.png", Support, Support.build_time, Support.price),
            ("assets/hud/Heavy.png", Heavy, Heavy.build_time, Heavy.price),
            ("assets/hud/AntiTank.png", AntiTank, AntiTank.build_time, AntiTank.price)
        ]

        for i, (image_path, unit_class, build_time, price) in enumerate(buttons_data):
            x_position = 100 + i * (units_button_size + spacing)
            y_position = screen_height - units_button_size - 20
            button = Button(
                pygame.image.load(image_path),
                (x_position, y_position),
                units_size,
                action=lambda unit_class=unit_class: self.player.add_unit(
                    unit_class(age=self.player.age, team=self.player.team)
                ),
                build_time=build_time,
                player=self.player,
                price=price
            )
            self.buttons.append(button)

        # Initialisation des boutons d'amélioration
        upgrade_buttons_data = [
            (self.upgrade_selected_unit, "HP"),
            (self.upgrade_selected_unit, "Damage"),
            (self.upgrade_selected_unit, "Range"),
            (self.upgrade_gold_per_kill, "Gold")
        ]

        for i, (action, upgrade_type) in enumerate(upgrade_buttons_data):
            x_position = 20
            y_position = 100 + i * (upgrade_button_size + spacing)
            button = Button(
                pygame.image.load(f"assets/hud/{upgrade_type}.png"),
                (x_position, y_position),
                upgrade_size,
                action=lambda upgrade_type=upgrade_type: action(upgrade_type),
                player=self.player
            )
            self.upgrade_buttons.append(button)

        # Initialisation des boutons de slot
        slot_buttons_data = [
            (self.add_slot),
            (self.sell_turret),
            (self.buy_turret)
        ]

        for i, (action) in enumerate(slot_buttons_data):
            x_position = 100
            y_position = 100 + i * (upgrade_button_size + spacing)
            button = Button(
                pygame.image.load(f"assets/hud/Heavy.png"),
                (x_position, y_position),
                upgrade_size,
                action=lambda action=action: action(),
                player=self.player
            )
            self.slot_buttons.append(button)

    def draw(self, screen):
        # Draw money
        money_text = self.font.render(f"Money: {self.player.money}", True, (0, 0, 0))
        screen.blit(money_text, (20, 20))
        # Draw buttons
        for button in self.buttons + self.upgrade_buttons + self.slot_buttons:
            button.draw(screen)
        # Draw upgrade dialog if it's active
        if self.upgrade_dialog:
            self.upgrade_dialog.draw(screen)

        # if self.sell_turret_dialog:
        # self.sell_turret_dialog.draw(screen)

        if self.buy_turret_dialog:
            self.buy_turret_dialog.draw(screen)

    def update(self):
        for button in self.buttons + self.upgrade_buttons + self.slot_buttons:
            button.update()
        if self.upgrade_dialog:
            self.upgrade_dialog.update()

        # if self.sell_turret_dialog:
        # self.sell_turret_dialog.update()

        if self.buy_turret_dialog:
            self.buy_turret_dialog.update()

    def handle_event(self, event):
        for button in self.buttons + self.upgrade_buttons + self.slot_buttons:
            button.handle_event(event)
        if self.upgrade_dialog:
            self.upgrade_dialog.handle_event(event)
        if self.sell_turret_dialog:
            self.sell_turret_dialog.handle_event(event)
        if self.buy_turret_dialog:
            self.buy_turret_dialog.handle_event(event)

    def upgrade_selected_unit(self, upgrade_type: str):
        # Show the upgrade dialog
        self.upgrade_dialog = UpgradeDialog(self.player, upgrade_type, self)

    def add_slot(self):
        self.player.add_slot(team=self.player.team)

    def sell_turret(self):
        self.sell_turret_dialog = SellTurretDialog(self.player, self)

    def buy_turret(self):
        self.buy_turret_dialog = BuyTurretDialog(self.player, self)

    def upgrade_gold_per_kill(self, upgrade_type: str):
        self.player.upgrade_gold_per_kill()

    def apply_upgrade(self, upgrade_type: str, unit_type: str):
        print(f"Applying upgrade {upgrade_type} to {unit_type}")
        if upgrade_type == "HP":
            self.player.upgrade_hp(unit_type)
        elif upgrade_type == "Damage":
            self.player.upgrade_damage(unit_type)
        elif upgrade_type == "Range":
            self.player.upgrade_range(unit_type)
        self.upgrade_dialog = None  # Close the dialog after applying the upgrade

    def apply_buy_turret(self, turret_type):
        self.player.add_turret(turret_type)
        self.buy_turret_dialog = None

    def apply_sell_turret(self, turret_type):
        self.player.sell_turret(turret_type)
        self.sell_turret_dialog = None


class UpgradeDialog:
    def __init__(self, player: Player, upgrade_type: str, hud: HUD):
        self.player = player
        self.upgrade_type = upgrade_type
        self.hud = hud
        self.font = pygame.font.Font(None, 36)
        self.buttons = []
        self.initialize_buttons()

    def initialize_buttons(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_width(), screen.get_height()
        button_size = screen_width // 20
        size = (button_size, button_size)
        spacing = 20

        # Boutons pour sélectionner le type d'unité à améliorer
        buttons_data = [
            ("Infantry", Infantry),
            ("Support", Support),
            ("Heavy", Heavy),
            ("AntiTank", AntiTank),
            ("Gold", "")
        ]

        for i, (unit_name, unit_class) in enumerate(buttons_data):
            x_position = screen_width // 2 - (
                    button_size * len(buttons_data) + spacing * (len(buttons_data) - 1)) // 2 + i * (
                                 button_size + spacing)

            y_position = screen_height // 2 - button_size // 2
            button = Button(
                pygame.image.load(f"assets/hud/{unit_name}.png"),
                (x_position, y_position),
                size,
                action=lambda unit_class=unit_name: self.hud.apply_upgrade(self.upgrade_type, unit_class)
            )
            self.buttons.append(button)

    def draw(self, screen):
        # Draw dialog background
        # calcul button length
        button_length = len(self.buttons)
        size = (button_length * 100, 100)
        dialog_rect = pygame.Rect(0, 0, size[0], size[1])
        dialog_rect.center = screen.get_rect().center
        pygame.draw.rect(screen, (255, 255, 255),
                         dialog_rect)
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

    def update(self):
        for button in self.buttons:
            button.update()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


class BuyTurretDialog:
    def __init__(self, player: Player, hud: HUD):
        self.player = player
        self.hud = hud
        self.font = pygame.font.Font(None, 36)
        self.buttons = []
        self.initialize_buttons()

    def initialize_buttons(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_width(), screen.get_height()
        button_size = screen_width // 20
        size = (button_size, button_size)
        spacing = 20

        # Boutons pour sélectionner le type de tourelle à acheter
        buttons_data = [
            (Cannon),
            (Minigun),
            (Laser),
        ]

        for i, (turret_type) in enumerate(buttons_data):
            x_position = screen_width // 2 - (
                    button_size * len(buttons_data) + spacing * (len(buttons_data) - 1)) // 2 + i * (
                                 button_size + spacing)

            y_position = screen_height // 2 - button_size // 2
            button = Button(
                pygame.image.load(f"assets/hud/Heavy.png"),
                (x_position, y_position),
                size,
                action=lambda turret_type=turret_type: self.hud.apply_buy_turret(turret_type(team=self.player.team))
            )
            self.buttons.append(button)

    def draw(self, screen):
        # Draw dialog background
        # calcul button length
        button_length = len(self.buttons)
        size = (button_length * 100, 100)
        dialog_rect = pygame.Rect(0, 0, size[0], size[1])
        dialog_rect.center = screen.get_rect().center
        pygame.draw.rect(screen, (255, 255, 255),
                         dialog_rect)
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

    def update(self):
        for button in self.buttons:
            button.update()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


class SellTurretDialog:
    def __init__(self, player: Player, hud: HUD):
        self.player = player
        self.hud = hud
        self.font = pygame.font.Font(None, 36)
        self.buttons = []
        self.initialize_buttons()

    def initialize_buttons(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_width(), screen.get_height()
        button_size = screen_width // 20
        size = (button_size, button_size)
        spacing = 20

        # Boutons pour sélectionner le type d'unité à améliorer
        buttons_data = [
            ("Infantry", Infantry),
            ("Support", Support),
            ("Heavy", Heavy),
            ("AntiTank", AntiTank)
        ]

        for i, (unit_name, unit_class) in enumerate(buttons_data):
            x_position = screen_width // 2 - (
                    button_size * len(buttons_data) + spacing * (len(buttons_data) - 1)) // 2 + i * (
                                 button_size + spacing)

            y_position = screen_height // 2 - button_size // 2
            button = Button(
                pygame.image.load(f"assets/hud/{unit_name}.png"),
                (x_position, y_position),
                size,
                action=lambda unit_class=unit_class: self.hud.apply_sell_turret(unit_name)
            )
            self.buttons.append(button)

    def draw(self, screen):
        # Draw dialog background
        # calcul button length
        button_length = len(self.buttons)
        size = (button_length * 100, 100)
        dialog_rect = pygame.Rect(0, 0, size[0], size[1])
        dialog_rect.center = screen.get_rect().center
        pygame.draw.rect(screen, (255, 255, 255),
                         dialog_rect)
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
    player: Union[Player, None]

    def __init__(self, image: pygame.Surface, position: Tuple[int, int], size: Tuple[int, int], action: Callable = None,
                 build_time: int = 0, player=None, price=0):
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
        elif self.price and self.player.money < self.price:

            overlay = pygame.Surface(self.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, self.position)

    def is_hovered(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.action and self.cooldown == 0 and (not self.price or self.player.money >= self.price):
            self.cooldown = self.build_time
            self.last_click_time = pygame.time.get_ticks()
            self.action()

    def update(self):
        # Update cooldown
        if self.cooldown > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_click_time > self.cooldown * 1000:
                self.cooldown = 0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_hovered(event.pos):
                    self.click()


class TextButton:
    def __init__(self, text: str, position: Tuple[int, int], size: Tuple[int, int], action: Callable = None):
        self.text = text
        self.position = position
        self.size = size
        self.action = action
        self.rect = pygame.Rect(position, size)
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 128, 0), self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.position[0] + (self.size[0] - text_surface.get_width()) // 2,
                                   self.position[1] + (self.size[1] - text_surface.get_height()) // 2))

    def is_hovered(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.action:
            self.action()

    def update(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_hovered(event.pos):
                    self.click()
