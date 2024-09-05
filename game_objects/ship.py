# Load packages
import pygame
import config
import math
from fractions import Fraction

# Link objects
from game_objects.laser import Laser

# Load graphics
from game_logic.load import game_images
from game_logic.render import move_objects


class Ship(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.asset = game_images()
        self.energy_stor = None
        self.flip = False
        self.max_speed = speed
        self.speed = 0
        self.inertia_factor = 0.02
        self.angle = 0
        self.moving_direction = []  # dir_vector
        # energy things and rectangles
        self.energy_full = 100
        self.energy = 100
        self.energy_max = pygame.Rect(70, 650, 100, 40)
        self.multiple_keys = False
        # initial credits
        self.credits = 10
        # storage
        self.storage_max = 15  # HERE adjust to change maximum storage
        self.storage = 0
        # shooting
        self.cooldown = 30
        self.damage = 1

        # Render ship
        self.update_time = pygame.time.get_ticks()
        self.index = 0
        self.image = self.asset['ship_0']  # default ship frame (idle)
        self.render_state0 = self.asset['ship_0']  # idle frame
        self.ship_animation_frames = [self.asset['ship_1'], self.asset['ship_2']]  # list of moving frames for the ship

        self.rect = self.image.get_rect()
        # this sets starting position
        self.rect.center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        # variables
        self.moving_w = False
        self.moving_s = False
        self.moving_a = False
        self.moving_d = False
        self.shooting = False

    def update(self, screen, laser_group, map_objects, asteroid_spawner):
        self.action(screen, laser_group)
        self.moving(map_objects, asteroid_spawner)

        # print(f'Current speed: {self.speed}')

        if (self.moving_s or self.moving_w or self.moving_a or self.moving_d) and self.energy > 0 and not self.multiple_keys:
            self.render_ship_animation()  # this runs ship animation logic
            if self.speed < self.max_speed:
                self.speed += self.max_speed * self.inertia_factor
            else:
                self.speed = self.max_speed
        else:
            self.image = self.asset['ship_0']  # this resets ship's frame to idle if it is not moving
            if self.speed > 0:
                self.speed -= self.max_speed * self.inertia_factor
                t = self.speed / math.sqrt(self.moving_direction[0] ** 2 + self.moving_direction[1] ** 2)                
                move_objects(map_objects, asteroid_spawner, *self.moving_direction, t)
            else:
                self.speed = 0

        self.draw_ship(screen)

    def moving(self, map_objects, asteroid_spawner):

        energy_consumed = 0
        self.energy = round(self.energy, 2)
        # movement variable is calculated (and rounded down to prevent floating position coords), and then used to move objects
        movement_variable = round(self.speed * 0.75, 0)

        if self.energy > 0 and not self.multiple_keys:
            direction_vector = self.get_mouse_vector()
            t = movement_variable / math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)

            if self.moving_w:
                energy_consumed -= 1
                move_objects(map_objects, asteroid_spawner, -direction_vector[0], -direction_vector[1], t)
                self.moving_direction = [-direction_vector[0], -direction_vector[1]]

            if self.moving_s:
                energy_consumed -= 1
                move_objects(map_objects, asteroid_spawner, direction_vector[0], direction_vector[1], t)
                self.moving_direction = [direction_vector[0], direction_vector[1]]

            if self.moving_a:
                energy_consumed -= 1
                move_objects(map_objects, asteroid_spawner, -direction_vector[1], 0, t)
                self.moving_direction = [-direction_vector[1], 0]

            if self.moving_d:
                energy_consumed -= 1
                move_objects(map_objects, asteroid_spawner, direction_vector[1], 0, t)
                self.moving_direction = [direction_vector[1], 0]

        if (self.moving_s and self.moving_w) or (self.moving_a and self.moving_d):
            energy_consumed = 0
            self.multiple_keys = True

        else:
            self.multiple_keys = False

        # handle energy consuming (so that it won't burn 2 units if pressing W and S for example)
        if energy_consumed <= -1:
            self.energy -= 0.3  # HERE change the parameter to adjust energy consuming speed

    def action(self, screen, laser_group):
        # check for low or max energy
        if self.energy <= self.energy_full * 0.3 and not self.energy <= 0:
            config.draw_text(screen, 'WARNING, LOW ENERGY', config.font_small, config.RED, 25, 105)

        elif self.energy <= 0:
            config.draw_text(screen, 'NO ENERGY', config.font_small, config.RED, 25, 105)

        if self.energy > self.energy_full:
            self.energy = self.energy_full

        # draw ENERGY gauge
        config.draw_text(screen, 'ENERGY', config.font_small, config.WHITE, 70, 10)
        bar_length, bar_width = 48, 7
        energy_stor = pygame.Rect(25 + bar_length, 50 + bar_width, int(94 * (self.energy / 100)), 36)

        pygame.draw.rect(screen, config.EMPTY_BLACK, (25 + bar_length, 50 + bar_width, 94, 36))
        pygame.draw.rect(screen, config.ENERGY_BLUE, energy_stor)
        screen.blit(self.asset['energy_bar'], (25, 50))

        # inventory and money
        self.credits = round(self.credits, 2)
        config.draw_text(screen, 'COIN', config.font_small, config.WHITE, 300, 10)
        screen.blit(self.asset['coin'], (300, 50))
        config.draw_text(screen, f'{self.credits}', config.font_small, config.WHITE, 350, 55)

        if self.credits <= 0:
            self.credits = 0

        # cargo
        self.storage = round(self.storage, 2)
        config.draw_text(screen, 'CARGO', config.font_small, config.WHITE, 545, 10)
        cargo_stored = pygame.Rect(500 + bar_length, 50 + bar_width, int(94 * (self.storage / 15)), 36)

        pygame.draw.rect(screen, config.EMPTY_BLACK, (500 + bar_length, 50 + bar_width, 94, 36))
        pygame.draw.rect(screen, config.STORAGE_BROWN, cargo_stored)
        screen.blit(self.asset['storage_bar'], (500, 50))

        if self.storage >= self.storage_max * 0.75 and not self.storage == self.storage_max:
            config.draw_text(screen, f'Reaching maximum capacity', config.font_small, config.RED, 500, 105)

        elif self.storage >= self.storage_max:
            config.draw_text(screen, f'Maximum cargo capacity reached', config.font_small, config.RED, 500, 105)

        if self.storage < 0:
            self.storage = 0

        if self.storage > self.storage_max:
            self.storage = self.storage_max

        if self.shooting and self.cooldown <= 0 < self.energy:
            # Spawns a laser sprite in the direction the ship is facing

            spawn_dist_from_player = 40
            dir_vector = self.get_mouse_vector()
            t = spawn_dist_from_player / math.sqrt(dir_vector[0] ** 2 + dir_vector[1] ** 2)
            parametric_equation_x = self.rect.centerx + (t * dir_vector[0])
            parametric_equation_y = self.rect.centery + (t * dir_vector[1])

            laser = Laser(parametric_equation_x, parametric_equation_y, dir_vector, self.angle)
            laser_group.add(laser)
            self.energy -= 1
            self.cooldown = 30

        self.cooldown -= 1

    def render_ship_animation(self):
        animation_cooldown = 300  # HERE you set up animation speed
        self.image = self.ship_animation_frames[self.index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.index += 1
            self.update_time = pygame.time.get_ticks()

            if self.index > 1:
                self.index = 0

    def get_mouse_vector(self):
        """Returns a reduced direction vector of the line between the cursor and player position"""
        mouse_pos = pygame.mouse.get_pos()
        player_pos = self.rect.center

        x_component = mouse_pos[0] - player_pos[0]
        y_component = mouse_pos[1] - player_pos[1]

        if x_component != 0 and y_component != 0:
            reduced_fraction = Fraction(x_component, y_component)
            if (x_component < 0 and y_component < 0) or (x_component > 0 > y_component):
                x_component = reduced_fraction.numerator * -1
                y_component = reduced_fraction.denominator * -1

        return [x_component, y_component]

    def determine_direction(self):
        """Determines the ship direction in degrees based on the cursor position and returns a rotated image"""
        mouse_pos = pygame.mouse.get_pos()
        adjacent = mouse_pos[0] - self.rect.centerx
        opposite = self.rect.centery - mouse_pos[1]

        if adjacent == 0 and opposite >= 0:
            radian_angle = math.pi / 2
        elif adjacent == 0 and opposite < 0:
            radian_angle = (3 * math.pi) / 2
        elif adjacent > 0 and opposite >= 0:
            radian_angle = math.atan(opposite / adjacent)
        elif adjacent > 0 >= opposite:
            radian_angle = 2 * math.pi - abs(math.atan(opposite / adjacent))
        elif adjacent < 0 and opposite <= 0:
            radian_angle = math.pi + math.atan(opposite / adjacent)
        elif adjacent < 0 <= opposite:
            radian_angle = math.pi - abs(math.atan(opposite / adjacent))
        else:
            radian_angle = 0

        self.angle = math.degrees(radian_angle)

        return pygame.transform.rotate(self.image, self.angle)

    def draw_ship(self, screen):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect.center = (screen_width // 2, screen_height // 2)
        rotated_ship = self.determine_direction()
        ship_rect = rotated_ship.get_rect(center=self.rect.center)

        screen.blit(rotated_ship, ship_rect)
