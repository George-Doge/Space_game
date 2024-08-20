import json
import random
import load

import pygame

from menu import main_menu

# TODO: More stations
# TODO: bigger/more maps??
# TODO: clean up the UI and the world map
# * you can edit values where 'HERE' is written to suit your needs

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Space game v0.2.5")

# Load images
image = load.game_images()

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
STORAGE_BROWN = (187, 142, 81)
font_small = pygame.font.SysFont('Futura', 30)
font_big = pygame.font.SysFont('Futura', 80)


# Saving/loading functions
def saving():
    save_data = {
        'credits': Player.credits,
        'storage': Player.storage,
        'energy': Player.energy,
    }

    with open("save.json", "w") as file:
        json.dump(save_data, file, indent=4)

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


def draw_background():
    screen.fill(DARK_BLUE)

    if main_menu_instance.menu_state == 0:
        screen.blit(image['background'], (0, 0))

# sole purpose of this function is to move objects when the player is moving
def move_objects(movementX, movementY):
    for asteroid in asteroid_group:
        x, y = asteroid.rect.center[0] + movementX, asteroid.rect.center[1] + movementY
        asteroid.rect.center = (x, y)

    for debris in debris_group:
        x, y = debris.rect.center[0] + movementX, debris.rect.center[1] + movementY
        debris.rect.center = (x, y)

    stationX, stationY = station_instance.rect.center[0] + movementX, station_instance.rect.center[1] + movementY
    station_instance.rect.center = (stationX, stationY)

    asteroidSpawnerInstance.spawnX, asteroidSpawnerInstance.spawnY = asteroidSpawnerInstance.spawnX + movementX, asteroidSpawnerInstance.spawnY + movementY 


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
        self.image = image['ship_0']  # default ship frame (idle)
        self.render_state0 = image['ship_0']  # idle frame
        self.ship_animation_frames = [image['ship_1'], image['ship_2']]  # list of moving frames for the ship

        self.rect = self.image.get_rect()
        # this sets starting position
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        # variables
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.shooting = False

    def update(self):
        self.action()
        self.moving()

        if (self.moving_down or self.moving_up or self.moving_left or self.moving_right) and self.energy > 0 and not self.multiple_keys:
            self.render_ship_animation() # this runs ship animation logic

        else:
            self.image = image['ship_0']  # this resets ship's frame to idle if it is not moving

        self.draw_ship()

    def moving(self):

        energy_consumed = 0
        self.energy = round(self.energy, 2)
        movement_variable = round(self.speed * 0.75, 0)
        
        if self.energy > 0 and not self.multiple_keys:

            if self.moving_up: # and self.rect.top >= 10:
                # self.rect.y -= movement_variable
                energy_consumed -= 1
                move_objects(0, movement_variable)

                
            if self.moving_down: # and self.rect.bottom <= screen_height - 10:
                # self.rect.y += movement_variable
                energy_consumed -= 1
                move_objects(0, -movement_variable)


            if self.moving_left: # and self.rect.left >= 0:
                self.flip = True
                self.direction = -1
                # self.rect.x -= movement_variable
                energy_consumed -= 1
                move_objects(movement_variable, 0)



            if self.moving_right: # and self.rect.right <= screen_width:
                self.flip = False
                self.direction = 1
                # self.rect.x += movement_variable
                energy_consumed -= 1
                move_objects(-movement_variable, 0)


        if (self.moving_down and self.moving_up) or (self.moving_left and self.moving_right):
            energy_consumed = 0
            self.multiple_keys = True

        else:
            self.multiple_keys = False

        # handle energy consuming (so that it won't burn 2 units if pressing W and S for example)
        if energy_consumed <= -1:
            self.energy -= 0.3  # HERE change the parameter to adjust energy consuming speed

    def action(self):
        # check for low or max energy
        if self.energy <= self.energy_full * 0.3 and not self.energy <= 0:
            draw_text('WARNING, LOW ENERGY', font_small, RED, 70, 700)

        elif self.energy <= 0:
            draw_text('NO ENERGY', font_small, RED, 70, 700)

        if self.energy > self.energy_full:
            self.energy = self.energy_full

        # draw ENERGY gauge
        draw_text('ENERGY', font_small, WHITE, 70, 10)
        bar_length, bar_width = 48, 7
        energy_stor = pygame.Rect(25 + bar_length, 50 + bar_width, int(94 * (self.energy / 100)), 36)

        pygame.draw.rect(screen, EMPTY_BLACK, (25 + bar_length, 50 + bar_width, 94, 36))
        pygame.draw.rect(screen, ENERGY_BLUE, energy_stor)
        screen.blit(image['energy_bar'], (25, 50))

        # inventory and money
        self.credits = round(self.credits, 2)
        draw_text('COIN', font_small, WHITE, 300, 10)
        screen.blit(image['coin'], (300, 50))
        draw_text(f'{self.credits}', font_small, WHITE, 350, 55)

        if self.credits <= 0:
            self.credits = 0

        # cargo
        self.storage = round(self.storage, 2)
        draw_text('CARGO', font_small, WHITE, 545, 10)
        cargo_stored = pygame.Rect(500 + bar_length, 50 + bar_width, int(94 * (self.storage / 15)), 36)

        pygame.draw.rect(screen, EMPTY_BLACK, (500 + bar_length, 50 + bar_width, 94, 36))
        pygame.draw.rect(screen, STORAGE_BROWN, cargo_stored)
        screen.blit(image['storage_bar'], (500, 50))

        if self.storage >= self.storage_max * 0.75 and not self.storage == self.storage_max:
            draw_text(f'Reaching maximum capacity', font_small, RED, 500, 700)

        elif self.storage >= self.storage_max:
            draw_text(f'Maximum cargo capacity reached', font_small, RED, 500, 700)

        if self.storage < 0:
            self.storage = 0

        if self.storage > self.storage_max:
            self.storage = self.storage_max

        # shooting
        if self.shooting and self.cooldown <= 0 and self.energy > 0:
            laser = Laser(self.rect.centerx + (40 * self.direction), self.rect.centery, self.direction)
            laser_group.add(laser)
            Player.energy -= 1
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

    def draw_ship(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = image['laser']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 10

    def update(self):
        self.draw()
        screen_width = pygame.display.get_surface().get_size()[0]
        # move laser
        self.rect.x += (self.speed * self.direction)

        if self.rect.left >= screen_width or self.rect.right < 0:
            self.kill()
        # check for collision with asteroid
        for asteroid in asteroid_group:
            if pygame.sprite.spritecollide(asteroid, laser_group, False):
                asteroid.health -= 15  # set damage
                self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)


class Station(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image['station']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = pygame.Rect(0, 0, 500, 400) # HERE you can modify range of stations
        self.name = name
        # energy buy price
        self.energy_price = round(random.uniform(0.5, 2), 2)
        # material sell price
        self.asteroid_price = round(random.uniform(1, 3), 2)

    def update(self):
        self.action()
        self.draw()

    def energy_station(self):
        draw_text(f'Buy 10 energy for {self.energy_price} credits?', font_small, WHITE, self.rect.x - 100,
                  self.rect.y + 100)

        if energy_buying and Player.credits > 0 and not Player.energy >= Player.energy_full:
            Player.credits -= self.energy_price
            Player.energy += 10
        if energy_all_buying:
            while not Player.energy >= Player.energy_full and Player.credits > 0:
                Player.credits -= self.energy_price
                Player.energy += 10

    def trade_station(self):
        draw_text(f'Sell mined asteroids for {self.asteroid_price} credits per t?', font_small, WHITE,
                  self.rect.x - 100,
                  self.rect.y + 130)

        # selling
        if selling and Player.storage > 0:
            Player.storage -= 1
            Player.credits += self.asteroid_price
        if selling_all and Player.storage > 0:
            Player.credits += self.asteroid_price + Player.storage
            Player.storage = 0

    # interaction and actions of station are handled
    def action(self):
        self.range.center = self.rect.center

        if self.range.colliderect(Player.rect):
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
        # pygame.draw.rect(screen, RED, self.range, 3) debug line for station range


class AsteroidSpawner():
    def __init__(self):
        self.spawnX = 500
        self.spawnY = 120
        self.spawn_width = 1020
        self.spawn_height = 600

    def spawn_location(self):
        # select random spawn point
        self.randomx = random.randint(self.spawnX, self.spawn_width)
        self.randomy = random.randint(self.spawnY, self.spawn_height)

    def determine_type(self):
        choice = random.randint(1, 10)

        if choice > 7:
            rarity = "rare"
            return rarity

        else:
            rarity = "common"
            return rarity

    def update(self):
        # pygame.draw.rect(screen, RED, (self.spawnX, self.spawnY, self.spawn_width, self.spawn_height), 5) Debug to show asteroid spawn location
        spawn_new = False
        max_number_of_asteroids = 6  # HERE change to modify max number of asteroids
        number_of_asteroids = len(asteroid_group)

        # HERE you can change number of asteroids that need to be mined so new can be spawned
        if number_of_asteroids < 4:
            spawn_new = True

        if spawn_new:
            for i in range(number_of_asteroids, max_number_of_asteroids):
                self.spawn_location()
                rarity = self.determine_type()
                asteroid = Asteroid(rarity, self.randomx, self.randomy)
                asteroid_group.add(asteroid)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, rarity, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = rarity
        # determines what type of asteroid it should show and gives it properties
        if rarity == "common":
            self.image = image['asteroid']
            self.health = 30

        elif rarity == "rare":
            self.image = image['asteroid_2']
            self.health = 40
        # in case of error shows basic asteroid
        else:
            self.image = image['asteroid']
            self.type = "common"

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        self.draw()

        if self.health <= 0:

            if self.type == "common":  # add mined storage in case of a common asteroid
                debris_instance = Debris(self.type, self.rect.center[0], self.rect.center[1])
                debris_group.add(debris_instance)
                self.kill()

            elif self.type == "rare":  # add in case of a rare asteroid
                debris_instance = Debris(self.type, self.rect.center[0], self.rect.center[1])
                debris_group.add(debris_instance)
                self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)


class Debris(pygame.sprite.Sprite):
    def __init__(self, rarity, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rarity = rarity
        if self.rarity == "rare":
            self.image = image['debris_rare']

        else:
            self.image = image['debris_common']

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.draw()
        # check if the debris is collected by the player
        if (self.rect.colliderect(Player.rect) and Player.storage < Player.storage_max):
            if self.rarity == "rare":
                self.kill()
                Player.storage += 1.5 * round(random.uniform(1, 3), 2)

            elif self.rarity == "common":
                self.kill()
                Player.storage += 1.2 * round(random.uniform(0.6, 2), 2)

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

    def update_pos(self, new_x: int, new_y: int):
        self.rect.center = (new_x, new_y)


def get_screen_size():
    screen_info = pygame.display.Info()
    return screen_info.current_w, screen_info.current_h


screen_width, screen_height = pygame.display.get_surface().get_size()
# declare instances
Player = Ship(200, 600, 10)
station_instance = Station('Energy & Trade', 300, 415)
# asteroid things
asteroidSpawnerInstance = AsteroidSpawner()
asteroid = Asteroid("common", 487, 354)
asteroid_group = pygame.sprite.Group(asteroid)
# debris things
debris_group = pygame.sprite.Group()
# laser things
laser_group = pygame.sprite.Group()

# buttons
buyButton = Button(105, 760, image['buy_button'], 1)
buyMaxButton = Button(225, 760, image['max_button'], 1)
sellButton = Button(550, 760, image['sell_button'], 1)
sellMaxButton = Button(670, 760, image['max_button'], 1)

# main menu instance
main_menu_instance = main_menu()
run = True

while run:

    clock.tick(FPS)


    draw_background()
    # checks changed screen size
    screen_width, screen_height = pygame.display.get_surface().get_size()
    # updates instances of player and stations and more
    if main_menu_instance.menu_state == 0:  # loads things only when game is unpaused

        buyButton.update_pos(105, get_screen_size()[1] - 104)
        energy_buying = buyButton.draw(screen)
        buyMaxButton.update_pos(225, get_screen_size()[1] - 104)
        energy_all_buying = buyMaxButton.draw(screen)
        sellButton.update_pos(550, get_screen_size()[1] - 104)
        selling = sellButton.draw(screen)
        sellMaxButton.update_pos(670, get_screen_size()[1] - 104)
        selling_all = sellMaxButton.draw(screen)

        Player.update()

        asteroidSpawnerInstance.update()
        station_instance.update()
        asteroid_group.update()
        for debris in debris_group:
            debris.update()
        laser_group.update()

    if main_menu_instance.menu_state == 1:
        main_menu_instance.main_scene()

    if main_menu_instance.menu_state == 2:
        run = False

    if main_menu_instance.menu_state == 3:
        main_menu_instance.credits_scene()

    if main_menu_instance.menu_state == 4:
        main_menu_instance.license_scene()

    if main_menu_instance.menu_state == 5:
        main_menu_instance.controls_scene()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_menu_instance.menu_state = 1

            # ship movement
            if event.key == pygame.K_UP:
                Player.moving_up = True

            if event.key == pygame.K_DOWN:
                Player.moving_down = True

            if event.key == pygame.K_LEFT:
                Player.moving_left = True

            if event.key == pygame.K_RIGHT:
                Player.moving_right = True

            if event.key == pygame.K_SPACE:
                Player.shooting = True

            # saving and loading
            if event.key == pygame.K_s and main_menu_instance.menu_state == 0:
                # check if the game is running, so player can't load/save when paused
                saving()

            if event.key == pygame.K_l and main_menu_instance.menu_state == 0:
                loading()

        if event.type == pygame.KEYUP:
            # ship movement
            if event.key == pygame.K_UP:
                Player.moving_up = False

            if event.key == pygame.K_DOWN:
                Player.moving_down = False

            if event.key == pygame.K_LEFT:
                Player.moving_left = False

            if event.key == pygame.K_RIGHT:
                Player.moving_right = False

            if event.key == pygame.K_SPACE:
                Player.shooting = False

    pygame.display.update()

pygame.quit()
