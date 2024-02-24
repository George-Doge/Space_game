import json
import random

import pygame

from menu import main_menu

# TODO: More stations
# TODO: add some animations, so it doesn't look static
# TODO: bigger/more maps??

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space game v0.2.4")

# load pictures
background_img = pygame.image.load('images/background/space.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT - 270))

ship_img = pygame.image.load('images/sprites/ship.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (60, 75))
ship_img = pygame.transform.rotate(ship_img, 270)

ship0_img = pygame.image.load('images/sprites/ship-state0.png').convert_alpha()
ship0_img = pygame.transform.rotate(ship0_img, 270)

ship1_img = pygame.image.load('images/sprites/ship-state1.png').convert_alpha()
ship1_img = pygame.transform.rotate(ship1_img, 270)

ship2_img = pygame.image.load('images/sprites/ship-state2.png').convert_alpha()
ship2_img = pygame.transform.rotate(ship2_img, 270)

station_img = pygame.image.load('images/sprites/station.png').convert_alpha()
station_img = pygame.transform.scale(station_img, (100, 100))

asteroid_img = pygame.image.load('images/sprites/asteroid.png').convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (60, 60))

asteroid2_img = pygame.image.load('images/sprites/asteroid-2.png').convert_alpha()
asteroid2_img = pygame.transform.scale(asteroid2_img, (60, 60))

laser_img = pygame.image.load('images/sprites/laser.png').convert_alpha()

energy_bar_img = pygame.image.load('images/buttons/energy_bar.png').convert_alpha()

# button images
buy_img = pygame.image.load('images/buttons/buy.png').convert_alpha()
max_img = pygame.image.load('images/buttons/max.png').convert_alpha()
sell_img = pygame.image.load('images/buttons/sell.png').convert_alpha()

# set framerate
clock = pygame.time.Clock()
FPS = 60

# COLOURS and fonts
YELLOW = (211, 174, 54)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 48, 78)
DARK_BLUE_2 = (0, 3, 66)
ENERGY_BLUE = (33, 150, 243)
EMPTY_BLACK = (26, 24, 26)
font_small = pygame.font.SysFont('Futura', 30)
font_big = pygame.font.SysFont('Futura', 80)

# variables
moving_up = False
moving_down = False
moving_left = False
moving_right = False
energy_buying = False
energy_all_buying = False
selling = False
selling_all = False
shooting = False
background_offset = 0


# Saving/loading function
def saving():
    save_data = {
        'credits': Player.credits,
        'storage': Player.storage,
        'energy': Player.energy,
    }

    with open("save.json", "w") as file:
        json.dump(save_data, file)

    print("GAME SAVED")


def loading():
    try:
        with open("save.json", "r") as file:
            save_data = json.load(file)
            Player.credits = save_data.get('credits')
            Player.storage = save_data.get('storage')
            Player.energy = save_data.get('energy')

        print("GAME LOADED")

    except FileNotFoundError:
        print("!!!SAVE NOT FOUND!!!")


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_background(x):
    screen.fill(DARK_BLUE)
    # for now there will be just one image printed 3 times which will be moving. Then it will reset
    if main_menu_instance.state == 1:
        for i in range(2):
            screen.blit(background_img, (x + SCREEN_WIDTH * i, 0))


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.energy_stor = None
        self.flip = False
        self.speed = speed
        self.direction = 1
        # energy things and rectangles
        self.energy_full = 100
        self.energy = 100
        self.energy_max = pygame.Rect(70, 650, 100, 40)
        # initial credits
        self.credits = 10
        # storage
        self.storage_max = 15  # adjust to change maximum storage
        self.storage = 0
        # shooting
        self.cooldown = 30
        self.damage = 1

        # Render ship
        self.render_state0 = ship0_img
        self.render_state1 = ship1_img
        self.render_state2 = ship2_img

        self.state0_rect = self.render_state0.get_rect()
        self.state1_rect = self.render_state1.get_rect()
        self.state2_rect = self.render_state2.get_rect()

        self.state2_rect.center = (x, y)

    def update(self):
        self.action()
        self.moving()
        if moving_down or moving_up or moving_left or moving_right:
            self.render_ship_moving()
        else:
            self.render_ship_stationary()

    def moving(self):

        energy_consumed = 0
        self.energy = round(self.energy, 2)

        if self.energy > 0:

            if moving_up and self.state2_rect.top >= 10:
                self.state2_rect.y -= self.speed * 0.75
                energy_consumed -= 1

            if moving_down and self.state2_rect.bottom <= SCREEN_HEIGHT - 280:
                self.state2_rect.y += self.speed * 0.75
                energy_consumed -= 1

            if moving_left and self.state2_rect.left >= 10:
                self.flip = True
                self.direction = -1
                self.state2_rect.x -= self.speed
                energy_consumed -= 1

            if moving_right and self.state2_rect.right <= SCREEN_WIDTH - 10:
                self.flip = False
                self.direction = 1
                self.state2_rect.x += self.speed
                energy_consumed -= 1

        if moving_down and moving_up or moving_left and moving_right:
            energy_consumed = 0

        # handle energy consuming (so that it won't burn 2 units if pressing W and S for example)
        if energy_consumed <= -1:
            self.energy -= 0.3  # change the parameter to adjust energy consuming speed

    def action(self):
        # check for low or max energy
        if self.energy <= self.energy_full * 0.3 and not self.energy <= 0:
            draw_text('WARNING, LOW ENERGY', font_small, RED, 70, 700)

        elif self.energy <= 0:
            draw_text('NO ENERGY', font_small, RED, 70, 700)

        if self.energy > self.energy_full:
            self.energy = self.energy_full

        # draw ENERGY gauge
        draw_text('ENERGY', font_small, WHITE, 70, 620)
        bar_length, bar_width = 48, 7
        energy_stor = pygame.Rect(25 + bar_length, 660 + bar_width, int(94 * (self.energy / 100)), 36)

        pygame.draw.rect(screen, EMPTY_BLACK, (25 + bar_length, 660 + bar_width, 94, 36))
        pygame.draw.rect(screen, ENERGY_BLUE, energy_stor)
        screen.blit(energy_bar_img, (25, 660))

        # inventory and money
        self.credits = round(self.credits, 2)
        draw_text(f'{self.credits} credits', font_small, WHITE, 280, 620)

        if self.credits <= 0:
            self.credits = 0

        # cargo
        self.storage = round(self.storage, 2)
        draw_text(f'Cargo: {self.storage} t ', font_small, WHITE, 500, 620)

        if self.storage >= self.storage_max * 0.75 and not self.storage == self.storage_max:
            draw_text(f'Reaching maximum capacity', font_small, RED, 500, 650)

        elif self.storage >= self.storage_max:
            draw_text(f'Maximum cargo capacity reached', font_small, RED, 500, 650)

        if self.storage < 0:
            self.storage = 0

        if self.storage > self.storage_max:
            self.storage = self.storage_max

        # shooting
        if shooting and self.cooldown <= 0:
            laser = Laser(self.state2_rect.centerx + (40 * self.direction), self.state2_rect.centery, self.direction)
            laser_group.add(laser)
            Player.energy -= 1
            self.cooldown = 30

        self.cooldown -= 1

    def render_ship_stationary(self):
        screen.blit(pygame.transform.flip(self.render_state0, self.flip, False), self.state2_rect)

    def render_ship_moving(self):
        screen.blit(pygame.transform.flip(self.render_state2, self.flip, False), self.state2_rect)


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 10

    def update(self):
        # move laser
        self.rect.x += (self.speed * self.direction)

        if self.rect.left >= SCREEN_WIDTH or self.rect.right < 0:
            self.kill()
        # check for collision with asteroid
        for asteroid in asteroid_group:
            if pygame.sprite.spritecollide(asteroid, laser_group, False):
                asteroid.health -= 15  # set damage
                self.kill()


class Station(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = station_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = pygame.Rect(0, 0, 300, 300)
        self.name = name
        # energy buy price
        self.energy_price = round(random.uniform(0.5, 2), 2)
        # material sell price
        self.asteroid_price = round(random.uniform(1, 3), 2)

    def update(self):
        self.action()
        self.draw()

    def energy_station(self):
        draw_text(f'Buy 10 energy for {self.energy_price} credits?', font_small, WHITE, self.rect.x - 100, self.rect.y + 100)

        if energy_buying and Player.credits > 0 and not Player.energy >= Player.energy_full:
            Player.credits -= self.energy_price
            Player.energy += 10
        if energy_all_buying:
            while not Player.energy >= Player.energy_full and Player.credits > 0:
                Player.credits -= self.energy_price
                Player.energy += 10

    def trade_station(self):
        draw_text(f'Sell mined asteroids for {self.asteroid_price} credits per t?', font_small, WHITE, self.rect.x - 100,
                  self.rect.y + 130)

        # selling
        if selling and Player.storage > 0:
            Player.storage -= 1
            Player.credits += self.asteroid_price
        if selling_all and Player.storage > 0:
            Player.credits += self.asteroid_price + Player.storage
            Player.storage = 0


    # here, interaction and actions of station are handled
    def action(self):
        self.range.center = self.rect.center

        if self.range.colliderect(Player.state2_rect):
            draw_text(f'{self.name} Station', font_small, WHITE, self.rect.x - len(self.name) * 3, self.rect.y - 30)

            # check what type of station it is

            if self.name == 'Energy':
                self.energy_station()

            if self.name == 'Trade':
                self.trade_station()

            if self.name == 'Energy & Trade':
                self.energy_station()
                self.trade_station()

    def draw(self):
        screen.blit(self.image, self.rect)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, rarity):
        pygame.sprite.Sprite.__init__(self)
        self.type = rarity
        # determines what type of asteroid it should show and gives it properties
        if rarity == "common":
            self.image = asteroid_img
            self.health = 30

        elif rarity == "rare":
            self.image = asteroid2_img
            self.health = 40
        # in case of error shows basic asteroid
        else:
            self.image = asteroid_img
            self.type = "common"

        self.rect = self.image.get_rect()
        # select random spawnpoint
        self.randomx = random.randint(500, SCREEN_WIDTH - 60)
        self.randomy = random.randint(60, SCREEN_HEIGHT - 300)
        self.rect.center = (self.randomx, self.randomy)

    def determine_type(self):
        choice = random.randint(1, 10)

        if choice > 7:
            rarity = "rare"
            return rarity

        else:
            rarity = "common"
            return rarity

    def update(self):
        self.draw()
        spawn_new = False
        max_number_of_asteroids = 6  # HERE change to modify max number of asteroids
        number_of_asteroids = len(asteroid_group)

        if self.health <= 0:

            if self.type == "common":  # add mined storage in case of a common asteroid
                Player.storage += 1.2 * round(random.uniform(0.6, 2), 2)
                self.kill()

            elif self.type == "rare":  # add in case of a rare asteroid
                Player.storage += 1.5 * round(random.uniform(1, 3), 2)
                self.kill()

            # HERE you can change number of asteroids that need to be mined so new can be spawned
        if number_of_asteroids < 4:
            spawn_new = True

        if spawn_new:
            for i in range(number_of_asteroids, max_number_of_asteroids):
                rarity = self.determine_type()
                asteroid = Asteroid(rarity)
                asteroid_group.add(asteroid)

        # spawn_new = False

    def draw(self):
        screen.blit(self.image, self.rect)


# button class
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# declare instances
Player = Ship(500, 200, 10)
station = Station('Energy & Trade', 200, 400)
# asteroid things
asteroid = Asteroid("common")
asteroid_group = pygame.sprite.Group(asteroid)
# laser things
laser_group = pygame.sprite.Group()

# buttons
buyButton = Button(105, 760, buy_img, 1)
buyMaxButton = Button(225, 760, max_img, 1)
sellButton = Button(550, 760, sell_img, 1)
sellMaxButton = Button(670, 760, max_img, 1)

# main menu instance
main_menu_instance = main_menu()
run = True

while run:

    clock.tick(FPS)

    # moves bg a little bit and updates it

    if main_menu_instance.state == 1:
        # here you can change the value to make it slower/faster. I found values around 0.35 to be fine
        background_offset -= 2

    if background_offset < -SCREEN_WIDTH:  # reset bg_offset so it loops forever
        background_offset = 0

    draw_background(background_offset)

    # updates instances of player and stations and more
    if main_menu_instance.state == 1:  # loads thing only when game is unpaused
        energy_buying = buyButton.draw(screen)
        energy_all_buying = buyMaxButton.draw(screen)
        selling = sellButton.draw(screen)
        selling_all = sellMaxButton.draw(screen)

        station.update()

        Player.update()
        asteroid_group.update()
        asteroid_group.draw(screen)
        laser_group.update()
        laser_group.draw(screen)

    if main_menu_instance.state != 1:
        main_menu_instance.controller()

    if main_menu_instance.state == 3:  # quit button
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_menu_instance.state = 0
                main_menu_instance.clicked = False

            # ship movement
            if event.key == pygame.K_UP:
                moving_up = True

            if event.key == pygame.K_DOWN:
                moving_down = True

            if event.key == pygame.K_LEFT:
                moving_left = True

            if event.key == pygame.K_RIGHT:
                moving_right = True

            if event.key == pygame.K_SPACE:
                shooting = True

            # saving and loading
            if event.key == pygame.K_s and main_menu_instance.state == 1:
                # check if the game is running, so player can't load/save when paused
                saving()

            if event.key == pygame.K_l and main_menu_instance.state == 1:
                loading()

        if event.type == pygame.KEYUP:
            # ship movement
            if event.key == pygame.K_UP:
                moving_up = False

            if event.key == pygame.K_DOWN:
                moving_down = False

            if event.key == pygame.K_LEFT:
                moving_left = False

            if event.key == pygame.K_RIGHT:
                moving_right = False

            if event.key == pygame.K_SPACE:
                shooting = False

    pygame.display.update()

pygame.quit()
