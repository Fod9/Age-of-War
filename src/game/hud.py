import pygame


class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)

    def draw_button(self, screen):
        # draw the buttons for the units

        baseline = screen.get_height() - 20
        button_size = screen.get_width() // 20
        size = (button_size, button_size)
        spacing = 20

        # Chargement des images des boutons
        buttons_data = [
            ("assets/hud/Infantry.png", "Infantry"),
            ("assets/hud/Support.png", "Support"),
            ("assets/hud/Heavy.png", "Heavy"),
            ("assets/hud/AntiTank.png", "AntiTank")
        ]

        buttons = []

        # Initialisation des boutons
        for i, (image_path, name) in enumerate(buttons_data):
            x_position = 100 + i * (button_size + spacing)
            y_position = baseline - button_size
            button = Button(pygame.image.load(image_path), (x_position, y_position), size)
            buttons.append(button)

        # Dessin des boutons
        for button in buttons:
            button.draw(screen)

    def draw(self, screen):
        text = self.font.render("Health: %d" % self.player.base.health, 1, (0, 0, 0))
        screen.blit(text, (10, 10))

        # draw money
        text = self.font.render("Money: %d" % self.player.money, 1, (0, 0, 0))
        screen.blit(text, (10, 50))

        self.draw_button(screen)


class Button:
    def __init__(self, image, position, size, action=None):
        self.image = pygame.transform.scale(image, size)
        self.position = position
        self.size = size
        self.action = None

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def is_clicked(self, position):
        pass
