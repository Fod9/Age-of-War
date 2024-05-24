import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)

        self.title = self.font.render("Choose Game Mode", True, (255, 255, 255))
        self.easy_button = self.small_font.render("Easy", True, (0, 255, 0))
        self.intermediate_button = self.small_font.render("Intermediate", True, (255, 255, 0))
        self.hard_button = self.small_font.render("Hard", True, (255, 0, 0))
        self.multiplayer_button = self.small_font.render("Multiplayer", True, (0, 0, 255))

        self.selected_mode = None
        self.running = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title, (100, 50))

        self.screen.blit(self.easy_button, (100, 200))
        self.screen.blit(self.intermediate_button, (100, 300))
        self.screen.blit(self.hard_button, (100, 400))
        self.screen.blit(self.multiplayer_button, (100, 500))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.easy_button.get_rect(topleft=(100, 200)).collidepoint(x, y):
                self.selected_mode = "easy"
                self.running = False
            elif self.intermediate_button.get_rect(topleft=(100, 300)).collidepoint(x, y):
                self.selected_mode = "intermediate"
                self.running = False
            elif self.hard_button.get_rect(topleft=(100, 400)).collidepoint(x, y):
                self.selected_mode = "hard"
                self.running = False
            elif self.multiplayer_button.get_rect(topleft=(100, 500)).collidepoint(x, y):
                self.selected_mode = "multiplayer"
                self.running = False


    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            self.clock.tick(60)
        return self.selected_mode
