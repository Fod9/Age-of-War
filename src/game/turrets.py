from typing import Tuple, Union
import pygame

from src.game.units import Unit


class Turret:
    id: int
    nom: str
    price: float
    damage: float
    attack_speed: float
    range: float
    screen: pygame.Surface
    age: int
    team: str

    def __init__(self, nom: str, price: float, damage: float, attack_speed: float, range: float,
                 image: pygame.Surface, age: int = 1, team: str = "B", position: Tuple[float, float] = (0, 0)):
        self.id = id(self)
        self.nom = nom
        self.price = price
        self.damage = damage
        self.attack_speed = attack_speed
        self.range = range
        self.base_image = image
        self.image = pygame.transform.scale(image, (int(image.get_width() * .5), int(image.get_height() * .5)))
        self.screen = pygame.display.get_surface()
        self.position = position
        self.collide_rect = self.image.get_rect(topleft=self.position)
        self.last_attack_time = 0
        self.age = age
        self.team = team

    def __str__(self):
        return f"{self.nom} (Price: {self.price}, Damage: {self.damage}, Attack Speed: {self.attack_speed}, Range: {self.range})"

    def handle_resize(self, screen):
        self.screen = screen
        self.position = (self.position[0], screen.get_height() - 300)
        self.collide_rect = self.image.get_rect(topleft=self.position)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.position)

    def attack(self, target: "Unit"):
        target.take_damage(self.damage, None)
        self.last_attack_time = pygame.time.get_ticks()

    def update(self, units: list, player, other_player):
        time = pygame.time.get_ticks()
        can_attack = False

        # Check if the unit can attack any enemy unit
        for unit in units:
            if unit.team != self.team and self.can_attack(unit):
                can_attack = True
                if time - self.last_attack_time >= self.attack_speed * 1000:
                    self.attack(unit)
                    self.last_attack_time = time
                    break  # Exit the loop after attacking

    def can_attack(self, target: "Unit"):
        # Check if the target is within the attack range
        distance = abs(self.position[0] - target.position[0])
        return distance <= self.range


class Cannon(Turret):
    price = 1

    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/turrets/{age}/{team}_Cannon.png")
        super().__init__(
            "Cannon",
            1,
            20,
            2,
            200,
            image,
            age,
            team
        )


class Laser(Turret):
    price = 2

    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/turrets/{age}/{team}_Laser.png")
        super().__init__(
            "Laser",
            2,
            10,
            0.5,
            300,
            image,
            age,
            team
        )


class Minigun(Turret):
    price = 3

    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/turrets/{age}/{team}_Minigun.png")
        super().__init__(
            "Missile",
            3,
            30,
            3,
            250,
            image,
            age,
            team
        )
