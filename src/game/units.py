from typing import Tuple

import pygame


class Unit:
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

    def __init__(self, nom: str, HP: int, price: float, damage: float, attack_speed: float, range: float,
                 gold_value: float, walk_speed: float, build_time: float, image: pygame.Surface,
                 position: Tuple[int, int], weak_against: list = []):
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

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)
        # move the unit to the new position
        pass

    def attack(self, target):
        # attack the target
        pass

    def take_damage(self, damage):
        self.HP -= damage
        if self.HP <= 0:
            self.die()

    def die(self):
        # remove the unit from the game
        pass

    def update(self):
        # update the unit's state
        pass


class Infantry(Unit):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            "Infantry",
            100,
            10,
            10,
            1,
            1,
            5,
            1,
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
            20,
            1,
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
