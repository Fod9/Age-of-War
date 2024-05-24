import pygame
from src.game.base import Base
from src.game.units import Infantry, Support, Heavy, AntiTank
from src.game.players import Player
from src.game.hud import HUD

class Game:
    age: int
    background: pygame.Surface
    screen: pygame.Surface
    running: bool
    red_player: Player
    blue_player: Player
    mode: str

    def __init__(self, screen):
        self.age = 1
        self.background = pygame.image.load(f"assets/backgrounds/{self.age}/background.png").convert_alpha()
        self.screen = screen
        self.running = True
        self.game_mode = None
        # Initialisation des joueurs
        self.red_player = Player(name="Player 1", team="R", age=self.age)
        self.blue_player = Player(name="Player 2", team="B", age=self.age)
        self.hud = HUD(self.blue_player)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            reload_image = pygame.image.load(f"assets/backgrounds/{self.age}/background.png").convert_alpha()
            self.background = pygame.transform.scale(reload_image,
                                                     (self.screen.get_width(), self.screen.get_height()))
            self.red_player.base.handle_resize(self.screen)
            self.blue_player.base.handle_resize(self.screen)

            units = self.red_player.units + self.blue_player.units
            screen = self.screen

            for unit in units:
                unit.handle_resize(screen)

        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.hud.handle_event(event)

    def update(self):
        all_units = self.red_player.units + self.blue_player.units
        self.red_player.update(all_units)
        self.blue_player.update(all_units)

    def handle_game_config(self):
        if self.game_mode == "easy":
            # Configure the bot to be easy
            pass


    def draw(self, screen):
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        screen.blit(self.background, (0, 0))

        # Dessiner les bases ensuite
        self.red_player.base.draw(screen)
        self.blue_player.base.draw(screen)

        # Dessiner les unités en premier
        for unit in self.red_player.units + self.blue_player.units:
            unit.draw(screen)

        # Dessiner l'interface utilisateur
        self.hud.draw(screen)

    def set_game_mode(self, game_mode):
        self.game_mode = game_mode


