import pygame
from sys import exit

def game_images():
    """ Loads all game images into a dictionary and returns it """
    image: dict = {}
    try:
        image['background'] = pygame.image.load('images/background/space3.jpeg').convert_alpha()
        image['ship_0'] = pygame.image.load('images/sprites/ship/ship-state0.png').convert_alpha()
        image['ship_0'] = pygame.transform.rotate(image['ship_0'], 270)

        image['ship_1'] = pygame.image.load('images/sprites/ship/ship-state1.png').convert_alpha()
        image['ship_1'] = pygame.transform.rotate(image['ship_1'], 270)

        image['ship_2'] = pygame.image.load('images/sprites/ship/ship-state2.png').convert_alpha()
        image['ship_2'] = pygame.transform.rotate(image['ship_2'], 270)

        image['station'] = pygame.image.load('images/sprites/station.png').convert_alpha()
        image['station'] = pygame.transform.scale(image['station'], (100, 100))

        image['asteroid'] = pygame.image.load('images/sprites/asteroid/asteroid.png').convert_alpha()
        image['asteroid'] = pygame.transform.scale(image['asteroid'], (64, 64))

        image['debris_common'] = pygame.image.load('images/sprites/asteroid/debris.png').convert_alpha()

        image['asteroid_2'] = pygame.image.load('images/sprites/asteroid/asteroid-2.png').convert_alpha()
        image['asteroid_2'] = pygame.transform.scale(image['asteroid_2'], (64, 64))

        image['debris_rare'] = pygame.image.load('images/sprites/asteroid/debris_rare.png').convert_alpha()

        image['laser'] = pygame.image.load('images/sprites/laser.png').convert_alpha()

        image['energy_bar'] = pygame.image.load('images/buttons/energy_bar.png').convert_alpha()
        image['storage_bar'] = pygame.image.load('images/buttons/storage_bar.png').convert_alpha()
        image['coin'] = pygame.image.load('images/buttons/coin.png').convert_alpha()

        image['buy_button'] = pygame.image.load('images/buttons/buy.png').convert_alpha()
        image['max_button'] = pygame.image.load('images/buttons/max.png').convert_alpha()
        image['sell_button'] = pygame.image.load('images/buttons/sell.png').convert_alpha()

        return image

    except FileNotFoundError as message:
        print("An error occurred while loading images in load.py. One or more of them have not been "
              "found.\nDownload them again or check if they are in an images folder.")
        print(f"Error message:\n{message}")

        with open("errorLog.txt", "w") as file:
            file.write(str(message))

        exit(1)


def menu_images():
    """ Loads all menu images into a dictionary and returns it """
    image: dict = {}
    try:
        image['main_background'] = pygame.image.load('images/background/asteroid_belt.jpg')
        image['main_background'] = pygame.transform.scale(image['main_background'], (1920, 1080))

        image['play_button'] = pygame.image.load('images/buttons/PlayButton.png').convert_alpha()
        image['controls_button'] = pygame.image.load('images/buttons/ControlsButton.png').convert_alpha()
        image['quit_button'] = pygame.image.load('images/buttons/QuitButton.png').convert_alpha()
        image['credits_button'] = pygame.image.load('images/buttons/QuestionmarkSquareButton.png').convert_alpha()
        image['license_button'] = pygame.image.load('images/buttons/InfoSquareButton.png').convert_alpha()
        image['x_button'] = pygame.image.load('images/buttons/XSquareButton.png').convert_alpha()

        return image

    except FileNotFoundError as message:
        print(
            "An error occurred while loading images in menu.py. One or more of them have not been found.\nDownload them again or check if they are in an images folder.")
        print(f"Error message:\n{message}")

        with open("errorLog.txt", "w") as file:
            file.write(str(message))

        exit(1)
