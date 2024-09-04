import json
import load
import config

import pygame

# Link objects
from game_objects.asteroid import Asteroid, load_asteroid_resources
from game_objects.asteroidSpawner import AsteroidSpawner
from game_objects.button import Button
from game_objects.ship import Ship
from game_objects.station import Station

from menu import main_menu

# TODO: More stations
# TODO: bigger/more maps??
# TODO: clean up the UI and the world map
# * you can edit values where 'HERE' is written to suit your needs

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Space game v0.2.5")


# Load images
image = load.game_images()

# set framerate
clock = pygame.time.Clock()
FPS = 60


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


def draw_background():
    screen.fill(config.DARK_BLUE)

    if main_menu_instance.menu_state == 0:
        screen.blit(image['background'], (0, 0))


def get_screen_size():
    screen_info = pygame.display.Info()
    return screen_info.current_w, screen_info.current_h


screen_width, screen_height = pygame.display.get_surface().get_size()

# Create empty object groups
asteroid_group = pygame.sprite.Group()
debris_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()

# Create objects
Player = Ship(10)
station_instance = Station('Energy & Trade', 300, 415)
asteroidSpawnerInstance = AsteroidSpawner()
asteroid = Asteroid("common", 487, 354)

asteroid.add(asteroid_group)

map_objects = [asteroid_group, debris_group, laser_group, station_instance]

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

        Player.update(screen, laser_group, map_objects, asteroidSpawnerInstance)

        asteroidSpawnerInstance.update(asteroid_group)
        station_instance.update(screen, Player)
        asteroid_group.update(screen, debris_group)
        debris_group.update(screen, Player)
        laser_group.update(screen, asteroid_group, laser_group)

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
