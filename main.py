import pygame
import sys
import threading
import importlib

from src.game.menu import Menu
from watcher import start_watcher  # Importer le watcher

# Initialize Pygame
pygame.init()

# Window settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Age of War"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Set up the clock for managing frame rate
clock = pygame.time.Clock()
FPS = 60

# Ensure the reload_event is global for accessibility
reload_event = threading.Event()


def run_game():
    while True:
        try:
            if reload_event.is_set():
                reload_event.clear()
                print("Reloading game module...")
                for module in sys.modules.copy():
                    if module.startswith("src.game"):
                        importlib.reload(sys.modules[module])

            print("Starting new game instance...")
            from src.game.game import Game

            menu = Menu(screen)
            game_mode = menu.run()

            game = Game(screen)

            if game_mode:
                game.set_game_mode(game_mode)
                # Main game loop
                running = True
                while running:
                    try:
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

                        # Check if reload is needed
                        if reload_event.is_set():
                            break

                    except Exception as e:
                        print(f"Error in game loop iteration: {e}")
                        running = False

                if not running:
                    break

        except Exception as e:
            print(f"Error starting new game instance: {e}")

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Start the watcher in a separate thread to avoid blocking
    watcher_thread = threading.Thread(target=start_watcher, args=(reload_event,))
    watcher_thread.daemon = True
    watcher_thread.start()

    run_game()
