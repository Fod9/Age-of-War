from typing import Tuple, Union
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
        self.HP = HP
        self.price = price
        self.damage = damage
        self.attack_speed = attack_speed
        self.range = range
        self.gold_value = gold_value
        self.walk_speed = walk_speed
        self.build_time = build_time
        self.base_image = image
        self.image = pygame.transform.scale(image, (int(image.get_width() * .5), int(image.get_height() * .5)))
        self.screen = pygame.display.get_surface()
        self.build_start_time = None

        # Calculer la position pour que les pieds soient alignés à 20% au-dessus du bas de l'écran
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()
        y_position = screen_height - 300

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
        self.max_health = HP

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
        else:
            new_position = (self.position[0] - x, self.position[1] + y)

        # Check if the new position is within the screen bounds
        if 0 <= new_position[0] <= self.screen.get_width() - self.image.get_width() and 0 <= new_position[
            1] <= self.screen.get_height() - self.image.get_height():
            # Create a new rectangle for the new position
            new_rect = pygame.Rect(new_position, self.image.get_size())

            # Check for collision with enemy units only
            collision_detected = False
            for unit in units:
                if unit is not self:
                    # Skip collision detection for allied units
                    if unit.team != self.team:
                        if unit.collide_rect.colliderect(new_rect):
                            collision_detected = True
                            break  # If collision is detected, stop checking further

            if not collision_detected:
                # Update position and rectangle
                self.position = new_position
                self.collide_rect.topleft = self.position

    def attack(self, target: "Unit"):
        target.take_damage(self.damage, self)
        self.last_attack_time = pygame.time.get_ticks()  # Update last attack time

    def take_damage(self, damage: float, attacker: "Unit"):
        # Check if the attacker is weak against this unit
        if attacker.nom in self.weak_against:
            damage *= 2

        self.HP -= damage

    def die(self, player):
        if self in player.units:
            player.units.remove(self)
            player.money += self.gold_value

    def update(self, units: list, player):
        if self.HP <= 0:
            self.die(player)
            return

        time = pygame.time.get_ticks()
        can_attack = False

        # Check if the unit can attack any enemy unit
        for unit in units:
            if unit.team != self.team and self.can_attack(unit):
                can_attack = True
                if time - self.last_attack_time >= self.attack_speed * 1000:
                    self.attack(unit)
                    self.last_attack_time = time  # Reset the last attack time after attacking
                    break

        # If the unit cannot attack, it should move
        if not can_attack:
            self.move(self.walk_speed, 0, units)

    def can_attack(self, target: "Unit"):
        # Check if the target is within the attack range
        distance = abs(self.position[0] - target.position[0])
        return distance <= self.range


class Infantry(Unit):
    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/units/{age}/{team}_Infantry.png")
        super().__init__(
            "Infantry",
            100,
            10,
            10,
            0.5,
            200,
            5,
            1,
            2,
            image,
            weak_against=["Heavy"],
            age=age,
            team=team
        )


class Support(Unit):
    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/units/{age}/{team}_Support.png")
        super().__init__(
            "Support",
            50,
            5,
            5,
            0.5,
            300,
            2.5,
            1,
            1,
            image,
            weak_against=["Infantry"],
            age=age,
            team=team
        )


class Heavy(Unit):
    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/units/{age}/{team}_Heavy.png")
        super().__init__(
            "Heavy",
            400,
            20,
            2,
            1,
            150,
            10,
            1,
            5,
            image,
            weak_against=["AntiTank"],
            age=age,
            team=team
        )


class AntiTank(Unit):
    def __init__(self, age: int = 1, team: str = "B"):
        image = pygame.image.load(f"assets/units/{age}/{team}_AntiTank.png")
        super().__init__(
            "AntiTank",
            150,
            15,
            10,
            0.7,
            150,
            7.5,
            1,
            6,
            image,
            weak_against=["Heavy"],
            age=age,
            team=team
        )
