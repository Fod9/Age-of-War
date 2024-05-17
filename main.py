import pygame
import sys
from src.game.game import Game

# ? INITIALIZATION

pygame.init()

WIDTH: int = 1920
HEIGHT: int = 1080
GAME_NAME: str = "Age of War"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()

FPS = 60


# ? GAME LOOP

def main():
    game: Game = Game(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        pygame.display.update()
        clock.tick(FPS)

        screen.fill((0, 0, 0))
        game.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
