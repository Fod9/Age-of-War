import pygame
import sys

# Initialize Pygame
pygame.init()

# Window settings
SCREEN_WIDTH: int = 1920
SCREEN_HEIGHT: int = 1080
SCREEN_TITLE: str = "Age of War"

# Colors
WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)

# Create game window
screen: pygame.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

clock: pygame.time.Clock = pygame.time.Clock()
FPS: int = 60


def main():
    from src.game.game import Game

    game: Game = Game(screen)

    # Main game loop
    running: bool = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        # Update game state
        game.update()

        # Draw everything
        screen.fill(BLACK)
        game.draw(screen)
        pygame.display.flip()

        # Maintain frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
