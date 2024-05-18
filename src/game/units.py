from typing import Tuple

import pygame


class Unit:
    id: int
    nom: str
    HP: int
    price: float
    damage: float
    attack_speed: float
    range: float
    gold_value: float
    walk_speed: float
    build_time: float
    image: pygame.Surface
    position: Tuple[int, int]
    weak_against: list
    screen: pygame.Surface

    def __init__(self, nom: str, HP: int, price: float, damage: float, attack_speed: float, range: float,
                 gold_value: float, walk_speed: float, build_time: float, image: pygame.Surface,
                 position: Tuple[int, int], weak_against: list = []):
        self.id = id(self)
        self.nom = nom
        self.HP = HP
        self.price = price
        self.damage = damage
        self.attack_speed = attack_speed
        self.range = range
        self.gold_value = gold_value
        self.walk_speed = walk_speed
        self.build_time = build_time
        self.image = image
        self.position = position
        self.weak_against = weak_against
        self.collide_rect = self.image.get_rect(topleft=self.position)
        self.screen = pygame.display.get_surface()
        self.last_attack_time = 0

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def can_attack(self, target):
        if target.position[0] - self.position[0] <= self.range:
            return True
        return False

    def move(self, x, y, units: list):
        # Calculate new position
        new_position = (self.position[0] + x, self.position[1] + y)
        # Check if the new position is within the screen bounds
        if 0 <= new_position[0] <= self.screen.get_width() and 0 <= new_position[1] <= self.screen.get_height():
            # Check for collision with other units
            for unit in units:
                if unit is not self and unit.collide_rect.colliderect(pygame.Rect(new_position, self.image.get_size())):
                    return  # If collision is detected, stop moving
            # Update position and rectangle
            self.position = new_position
            self.collide_rect.topleft = self.position

    def attack(self, target):
        target.take_damage(self.damage, self)
        self.last_attack_time = pygame.time.get_ticks() # Update last attack time

    def take_damage(self, damage, attacker):

        if attacker.nom in self.weak_against:
            damage *= 2

        self.HP -= damage

    def die(self, units):
        units.remove(self)

    def update(self, units: list):
        # check if the unit is alive
        if self.HP <= 0:
            self.die([])
            return

        time = pygame.time.get_ticks()

        # check if the unit can attack
        if time - self.last_attack_time >= self.attack_speed * 1000:
            for unit in units:
                if unit is not self and self.can_attack(unit):
                    self.attack(unit)
                    break
        else:
            self.move(self.walk_speed, 0, units)


class Infantry(Unit):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            "Infantry",
            100,
            10,
            10,
            1.5,
            1,
            5,
            2,
            1,
            pygame.image.load("assets/infantry.png"),
            position,
            weak_against=["Heavy"]
        )


class Support(Unit):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            "Support",
            50,
            5,
            5,
            1,
            1,
            2.5,
            1,
            1,
            pygame.image.load("assets/support.png"),
            position,
            weak_against=["Infantry"]
        )


class Heavy(Unit):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            "Heavy",
            400,
            20,
            10,
            0.5,
            1,
            10,
            1,
            3,
            pygame.image.load("assets/heavy.png"),
            position,
            weak_against=["AntiTank"]
        )


class AntiTank(Unit):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            "AntiTank",
            200,
            15,
            15,
            1,
            1,
            7.5,
            1,
            2,
            pygame.image.load("assets/antitank.png"),
            position,
            weak_against=["Heavy"]
        )
