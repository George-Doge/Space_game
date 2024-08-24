import json
import load

# Link objects
from game_objects.asteroid import Asteroid
from game_objects.asteroidSpawner import AsteroidSpawner
from game_objects.button import Button
from game_objects.ship import Ship
from game_objects.station import Station

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


def move_objects(movement_x, movement_y, t):
    """move objects when the player is moving"""

    for asteroid in asteroid_group:
        asteroid.rect.center = (asteroid.rect.centerx + t*movement_x,
                                asteroid.rect.centery + t*movement_y)

    for debris in debris_group:
        debris.rect.center = (debris.rect.centerx + t*movement_x,
                              debris.rect.centery + t*movement_y)

    for laser in laser_group:
        laser.rect.center = (laser.rect.centerx + t*movement_x,
                             laser.rect.centery + t*movement_y)

    station_instance.rect.center = (station_instance.rect.centerx + t*movement_x,
                                    station_instance.rect.centery + t*movement_y)

    asteroidSpawnerInstance.spawnX, asteroidSpawnerInstance.spawnY = asteroidSpawnerInstance.spawnX + t*movement_x, asteroidSpawnerInstance.spawnY + t*movement_y


def get_screen_size():
    screen_info = pygame.display.Info()
    return screen_info.current_w, screen_info.current_h


screen_width, screen_height = pygame.display.get_surface().get_size()
# declare instances
Player = Ship(10)
station_instance = Station('Energy & Trade', 300, 415)
# asteroid things
asteroidSpawnerInstance = AsteroidSpawner()
asteroid = Asteroid(screen, "common", 487, 354)
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
    if main_menu_instance.menu_state == 0:  # loads things only when game is not paused

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
            if event.key == pygame.K_w:
                Player.moving_w = True

            if event.key == pygame.K_s:
                Player.moving_s = True

            if event.key == pygame.K_a:
                Player.moving_a = True

            if event.key == pygame.K_d:
                Player.moving_d = True

            if event.key == pygame.K_SPACE:
                Player.shooting = True

            # saving and loading
            if event.key == pygame.K_F5 and main_menu_instance.menu_state == 0:
                # check if the game is running, so player can't load/save when paused
                saving()

            if event.key == pygame.K_F9 and main_menu_instance.menu_state == 0:
                loading()

        if event.type == pygame.KEYUP:
            # ship movement
            if event.key == pygame.K_w:
                Player.moving_w = False

            if event.key == pygame.K_s:
                Player.moving_s = False

            if event.key == pygame.K_a:
                Player.moving_a = False

            if event.key == pygame.K_d:
                Player.moving_d = False

            if event.key == pygame.K_SPACE:
                Player.shooting = False

    pygame.display.update()

pygame.quit()
