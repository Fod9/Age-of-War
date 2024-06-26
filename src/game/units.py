from typing import Tuple, Union
import pygame

from src.game.base import Base


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
    position: Tuple[float, float]
    weak_against: list
    screen: pygame.Surface
    age: int
    team: str
    build_start_time: Union[int, None]

    def __init__(self, nom: str, HP: int, price: float, damage: float, attack_speed: float, range: float,
                 gold_value: float, walk_speed: float, build_time: float, image: pygame.Surface,
                 weak_against: list = [], age: int = 1, team: str = "B"):
        self.id = id(self)
        self.nom = nom
        multiplier = 1 + 0.2 * (age - 1)
        # Age affects the unit's stats
        self.HP = HP * multiplier
        self.price = price
        self.damage = damage * multiplier
        self.attack_speed = attack_speed * multiplier
        self.range = range
        self.gold_value = gold_value
        self.walk_speed = walk_speed * multiplier
        self.max_health = HP * multiplier
        self.build_time = build_time
        self.base_image = image
        self.image = pygame.transform.scale(image, (int(image.get_width() * .5), int(image.get_height() * .5)))
        self.screen = pygame.display.get_surface()
        self.build_start_time = None

        # Calculer la position pour que les pieds soient alignés à 20% au-dessus du bas de l'écran
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()
        y_position = self.define_y_position(age)

        if team == "B":
            x_position = int(screen_width * 0.05)  # Unités bleues à gauche
        else:
            x_position = screen_width - int(screen_width * 0.05) - self.image.get_width()  # Unités rouges à droite

        self.position = (x_position, y_position)
        self.weak_against = weak_against
        self.collide_rect = self.image.get_rect(topleft=self.position)
        self.last_attack_time = 0
        self.age = age
        self.team = team
        self.sound = pygame.mixer.Sound("assets/sounds/punch.mp3")
        self.sound.set_volume(0.05)

    def __str__(self):
        return f"{self.nom} (HP: {self.HP}, Price: {self.price}, Damage: {self.damage}, Attack Speed: {self.attack_speed}, Range: {self.range}, Gold Value: {self.gold_value}, Walk Speed: {self.walk_speed}, Build Time: {self.build_time})"

    def handle_resize(self, screen):
        self.screen = screen
        self.position = (self.position[0], screen.get_height() - 300)
        self.collide_rect = self.image.get_rect(topleft=self.position)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.position)

        # Draw health bar
        health_bar_width = 50  # Width of the health bar
        health_bar_height = 5  # Height of the health bar
        health_bar_x = self.position[0] + (self.image.get_width() - health_bar_width) / 2
        health_bar_y = self.position[1] - 10  # Position the health bar above the unit

        # Calculate health percentage
        health_percentage = self.HP / self.max_health

        # Draw the health bar background
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Draw the health bar foreground
        pygame.draw.rect(screen, (0, 255, 0),
                         (health_bar_x, health_bar_y, health_bar_width * health_percentage, health_bar_height))

    def move(self, x: int, y: int, units: list):
        # Calculate new position based on team direction
        if self.team == "B":
            new_position = (self.position[0] + x, self.position[1] + y)
            move_direction = "right"
        else:
            new_position = (self.position[0] - x, self.position[1] + y)
            move_direction = "left"

        # Check if the new position is within the screen bounds
        if 0 <= new_position[0] <= self.screen.get_width() - self.image.get_width() and 0 <= new_position[
            1] <= self.screen.get_height() - self.image.get_height():
            # Create a new rectangle for the new position
            new_rect = pygame.Rect(new_position, self.image.get_size())

            # Check for collision with enemy units only
            collision_detected = False
            for unit in units:
                if unit is not self:
                    if move_direction == "right" and unit.position[0] > self.position[0]:
                        if unit.collide_rect.colliderect(new_rect):
                            collision_detected = True
                            break
                    elif move_direction == "left" and unit.position[0] < self.position[0]:
                        if unit.collide_rect.colliderect(new_rect):
                            collision_detected = True
                            break  # If collision is detected, stop checking further

            if not collision_detected:
                # Update position and rectangle
                self.position = new_position
                self.collide_rect.topleft = self.position

    def attack(self, target: "Unit"):
        target.take_damage(self.damage, self)
        self.sound.play()
        self.last_attack_time = pygame.time.get_ticks()  # Update last attack time

    def attack_base(self, base: "Base"):
        base.take_damage(self.damage)
        self.sound.play()
        self.last_attack_time = pygame.time.get_ticks()

    def take_damage(self, damage: float, attacker: Union["Unit", None]):
        # Check if the attacker is weak against this unit
        if attacker.nom in self.weak_against:
            damage *= 2

        self.HP -= damage

    def die(self, player, other_player):
        if self in player.units:
            player.units.remove(self)
            other_player.money += self.gold_value
            if other_player.xp < other_player.next_age_xp:
                other_player.xp += 10

    def update(self, units: list, player, other_player):
        if self.HP <= 0:
            self.die(player, other_player)
            return

        self.position = (self.position[0], self.define_y_position(self.age, other_player, player))

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

        # Check if the unit can attack the enemy base
        if not can_attack and self.can_attack_base(other_player.base):
            can_attack = True
            if time - self.last_attack_time >= self.attack_speed * 1000:
                self.attack_base(other_player.base)
                self.last_attack_time = time

        # If the unit cannot attack, it should move
        if not can_attack:
            self.move(self.walk_speed, 0, units)

    def can_attack(self, target: "Unit"):
        # Check if the target is within the attack range
        distance = abs(self.position[0] - target.position[0])
        return distance <= self.range

    def can_attack_base(self, base: "Base"):
        distance = abs(self.position[0] - base.position[0])
        return distance <= self.range

    def define_y_position(self, age: int, other_player: "Player" = None, player: "Player" = None):
        game_age = age
        if player is not None:
            game_age = player.age
            if other_player.age > player.age:
                game_age = other_player.age

        if game_age == 1:
            return int(self.screen.get_height() - 300)
        elif game_age == 2:
            return int(self.screen.get_height() * 0.75)
        elif game_age == 3:
            return int(self.screen.get_height() - 300)
        elif game_age == 4:
            return int(self.screen.get_height() * 0.80)


class Infantry(Unit):
    build_time = 1
    price = 10
    weak_against = ["Heavy"]

    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/units/{age}/{team}_Infantry.png")
        super().__init__(
            "Infantry",
            100,
            self.price,
            10,
            0.5,
            200,
            5,
            1,
            Infantry.build_time,
            image,
            weak_against=["Heavy"],
            age=age,
            team=team
        )


class Support(Unit):
    price = 10
    build_time = 1
    weak_against = ["Infantry"]

    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/units/{age}/{team}_Support.png")
        super().__init__(
            "Support",
            100,
            self.price,
            5,
            0.5,
            300,
            2.5,
            2,
            Support.build_time,
            image,
            weak_against=["Infantry"],
            age=age,
            team=team
        )


class Heavy(Unit):
    build_time = 3
    price = 18
    weak_against = ["AntiTank"]

    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/units/{age}/{team}_Heavy.png")
        super().__init__(
            "Heavy",
            300,
            self.price,
            5,
            0.7,
            150,
            10,
            1,
            Heavy.build_time,
            image,
            weak_against=["AntiTank"],
            age=age,
            team=team
        )


class AntiTank(Unit):
    build_time = 3
    price = 18
    weak_against = ["Heavy"]

    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/units/{age}/{team}_AntiTank.png")
        super().__init__(
            "AntiTank",
            200,
            18,
            self.price,
            0.7,
            150,
            7.5,
            1,
            AntiTank.build_time,
            image,
            weak_against=["Heavy"],
            age=age,
            team=team
        )
