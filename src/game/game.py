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

    def __init__(self, screen, mode="single"):
        self.age = 1
        self.background = pygame.image.load(f"assets/backgrounds/{self.age}/background.png").convert_alpha()
        self.screen = screen
        self.running = True
        self.mode = mode

        # Initialisation des joueurs
        self.red_player = Player(name="Player 1", team="R", age=self.age)
        self.blue_player = Player(name="Player 2", team="B", age=self.age)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            reload_image = pygame.image.load(f"assets/backgrounds/{self.age}/background.png").convert_alpha()
            self.background = pygame.transform.scale(reload_image,
                                                     (self.screen.get_width(), self.screen.get_height()))
            self.red_player.base.handle_resize(self.screen)
            self.blue_player.base.handle_resize(self.screen)

    def update(self):
        all_units = self.red_player.units + self.blue_player.units
        self.red_player.update(all_units)
        self.blue_player.update(all_units)

    def draw(self, screen):
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        screen.blit(self.background, (0, 0))

        # Dessiner les bases ensuite
        self.red_player.base.draw(screen)
        self.blue_player.base.draw(screen)

        # Dessiner les unités en premier
        for unit in self.red_player.units + self.blue_player.units:
            unit.draw(screen)

        # Dessiner les joueurs
        self.red_player.draw(screen)
        self.blue_player.draw(screen)

        # Dessiner l'interface
        hud = HUD(self.red_player)
        hud.draw(screen)


