# src/game/base.py
from typing import Union, Tuple

import pygame

from src.game.turrets_slots import Slot


class Base:
    def __init__(self, name, owner, age):
        self.name = name
        self.owner = owner
        self.units = []
        self.slots = [{"slot": None, "position": (i*100, 100)} for i in range(4)]
        self.turrets = []
        self.next_slot_price = 15
        self.next_slot_pos = 300
        self.age = age
        self.h_percent = 0.8
        self.v_percent = 0.8
        self.heigth_offset = 1
        self.HP = 4000
        self.max_health = 4000
        self.base_image = pygame.image.load(f'assets/base/{self.age}/{self.owner}_Base.png').convert_alpha()
        self.position = self.init_position()
        self.last_repair = pygame.time.get_ticks()
        self.last_damage = pygame.time.get_ticks()

    def handle_resize(self, screen):
        self.base_image = pygame.image.load(f'assets/base/{self.age}/{self.owner}_Base.png').convert_alpha()
        self.draw(screen)

    def init_position(self):
        screen = pygame.display.get_surface()
        if self.owner == "R":
            return screen.get_width() - 50, screen.get_height() - screen.get_height() * self.v_percent
        elif self.owner == "B":
            return 0, screen.get_height() - screen.get_height() * self.v_percent

    def define_render_params(self):
        if self.age == 1:
            self.h_percent = 1
            self.v_percent = 1
        elif self.age == 2:
            pass
        elif self.age == 3:
            self.heigth_offset = 0.8

    def take_damage(self, damage):
        self.HP -= damage
        self.last_damage = pygame.time.get_ticks()
        if self.HP <= 0:
            self.destroy()

    def destroy(self):
        self.HP = 0
        # Message on screen
        message = f"{self.owner} base has been destroyed"
        # Show the victory or defeat message
        screen = pygame.display.get_surface()
        font = pygame.font.Font(None, 72)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds to show the message

        # Optionally, you can stop the game or reset it
        pygame.quit()
        exit()

    def update(self):
        current_time = pygame.time.get_ticks()
        # Repair the base every 2 seconds if it has not been damaged in the last 10 seconds
        if current_time - self.last_repair > 2000 and current_time - self.last_damage > 10000:
            self.HP += 2
            if self.HP > self.max_health:
                self.HP = self.max_health
            self.last_repair = current_time

    def draw(self, screen):
        # Define the percentage of the screen the base will take
        self.define_render_params()

        # Get the screen size
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Define positions for the base
        if self.owner == "R":
            castle_x = screen_width - screen_width * self.h_percent
            castle_y = (screen_height - screen_height * self.h_percent) * self.heigth_offset
        else:
            castle_x = 0
            castle_y = (screen_height - screen_height * self.h_percent) * self.heigth_offset

        castle_width = screen_width * self.h_percent
        castle_height = screen_height * self.h_percent

        # Resize the base
        scaled_base_image = pygame.transform.scale(self.base_image, (int(castle_width), int(castle_height)))

        # Draw the base
        screen.blit(scaled_base_image, (castle_x, castle_y))

        health_bar_width = 150
        health_bar_height = 10
        # Calculate health percentage
        health_percentage = self.HP / self.max_health

        health_bar_x = self.position[0] + 50

        if self.owner == "R":
            health_bar_x = self.position[0] - 250

        health_bar_y = self.position[1] + castle_height / 4

        #Show HP / Max HP
        font = pygame.font.Font(None, 30)
        text = font.render(f"{self.HP}/{self.max_health}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(health_bar_x + health_bar_width / 2, health_bar_y - 20))
        screen.blit(text, text_rect)

        # Draw the health bar background
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Draw the health bar foreground
        pygame.draw.rect(screen, (0, 255, 0),
                         (health_bar_x, health_bar_y, health_bar_width * health_percentage, health_bar_height))

    def add_slot(self, team: str):
        for slot in self.slots:
            if slot["slot"] is None:
                print(team)
                slot["slot"] = Slot(team=team, y_position=self.next_slot_pos)
                print("Slot added!")
                print(slot["slot"].turret)
                self.next_slot_price *= 2
                self.next_slot_pos += 100
                return True
        return False

    def add_turret(self, turret):
        for s in self.slots:
            # Check if the slot is not empty
            if s["slot"] is not None:
                # Check if the slot does not have a turret
                if s["slot"].turret is False:
                    # Add the turret to the slot
                    s["slot"].add_turret()
                    turret.position = s["slot"].position
                    self.turrets.append(turret)
                    print("Turret added!")
                    print(turret)
                    return True
        return False

    def remove_turret(self, turret):
        for s in self.slots:
            if s["slot"] is not None:
                if s["slot"].turret:
                    s["slot"].remove_turret(turret)
                    self.turrets.remove(turret)
                break
