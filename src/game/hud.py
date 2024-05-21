import pygame


class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        text = self.font.render("Health: %d" % self.player.base.health, 1, (255, 255, 255))
        screen.blit(text, (10, 10))