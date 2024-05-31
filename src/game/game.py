from typing import Union

import pygame
from src.game.base import Base
from src.game.units import Infantry, Support, Heavy, AntiTank
from src.game.players import Player
from src.game.hud import HUD
from src.ai.easy_bot import EasyBot
from src.ai.medium_bot import MediumBot
from src.ai.hard_bot import HardBot
from src.ai.base_ai import AIBot


class Game:
    age: int
    background: pygame.Surface
    screen: pygame.Surface
    running: bool
    red_player: Union[Player, None]
    blue_player: Player
    bot: Union[AIBot, None]
    mode: str
    config_done: bool

    def __init__(self, screen):
        self.age = 1
        self.background = pygame.image.load(f"assets/backgrounds/{self.age}/background.png").convert_alpha()
        self.screen = screen
        self.running = True
        self.game_mode = None
        # Initialisation des joueurs
        self.blue_player = Player(name="Player 1", team="B", age=self.age)
        self.red_player = Player(name="Player 2", team="R", age=self.age)
        self.bot = None
        self.hud = HUD(self.blue_player)
        self.config_done = False
        self.background_music = pygame.mixer.Sound(f"assets/sounds/{self.age}.mp3")
        self.background_music.play()

    def handle_event(self, event):
        #self.background_music.play()
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

        if event.type == pygame.KEYDOWN:
            #if k pressed, change the game speed
            if event.key == pygame.K_k:
                self.hud.change_speed()

        if event.type == pygame.USEREVENT:
            new_age = max(self.red_player.age, self.blue_player.age)
            self.age = new_age
            self.background = pygame.image.load(f"assets/backgrounds/{self.age}/background.png").convert_alpha()
            self.background_music.stop()
            self.background_music = pygame.mixer.Sound(f"assets/sounds/{self.age}.mp3")
            if self.age != 4:
                self.background_music.set_volume(0.1)
            else :
                self.background_music.set_volume(0.5)
            self.background_music.play()

    def update(self):
        if not self.config_done and self.game_mode:
            self.handle_game_config()
            self.config_done = True
        all_units = self.red_player.units + self.blue_player.units
        if self.bot:
            self.bot.perform_actions(all_units, self.blue_player)
        self.red_player.update(all_units, self.blue_player)
        self.blue_player.update(all_units, self.red_player)
        self.hud.update()
        self.bot.update()

    def age_has_changed(self):
        return self.age != self.red_player.age or self.age != self.blue_player.age

    def handle_game_config(self):
        if self.game_mode == "easy":
            self.bot = EasyBot(self.red_player)
        elif self.game_mode == "intermediate":
            self.bot = MediumBot(self.red_player)
        elif self.game_mode == "hard":
            self.bot = HardBot(self.red_player, self.blue_player)

    def draw(self, screen):
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        screen.blit(self.background, (0, 0))

        # Dessiner les bases ensuite
        self.red_player.base.draw(screen)
        self.blue_player.base.draw(screen)


        # Dessiner les unités en premier
        for unit in self.red_player.units + self.blue_player.units:
            unit.draw(screen)

        for turret_slots in self.red_player.base.slots + self.blue_player.base.slots:
            if turret_slots["slot"]:
                turret_slots["slot"].draw(screen)

        for turret in self.red_player.base.turrets + self.blue_player.base.turrets:
            turret.draw(screen)

        # Dessiner l'interface utilisateur
        self.hud.draw(screen)

    def set_game_mode(self, game_mode):
        self.game_mode = game_mode
