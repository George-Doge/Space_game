"""
MAIN MENU implementation file
"""
import pygame
import config
import game_logic.load as load
from game_objects.button import Button



def get_screen_size():
    screen_info = pygame.display.Info()
    return screen_info.current_w, screen_info.current_h

class main_menu():
    def __init__(self):
        self.asset = load.menu_images()
        self.menu_state = 1 # sets default menu state

        self.screen_width, self.screen_height = get_screen_size()

        self.playButton = Button(self.screen_width//2, self.screen_height//2 - 160, self.asset['play_button'], 0.35)
        self.controlsButton = Button(self.screen_width//2, self.screen_height//2 - 60, self.asset['controls_button'], 0.35)
        self.quitButton = Button(self.screen_width//2, self.screen_height//2 + 140, self.asset['quit_button'], 0.35)
        self.creditsButton = Button(self.screen_width - 50, self.screen_height - 100, self.asset['credits_button'], 0.35)
        self.licenseButton = Button(self.screen_width - 150, self.screen_height - 100, self.asset['license_button'], 0.35)
        self.XButton = Button(self.screen_width - 50, 50, self.asset['x_button'], 0.35)

        # windows size change variables
        self.old_screen_width, self.old_screen_height = get_screen_size()


    def main_scene(self):
        config.screen.blit(self.asset['main_background'], (0, 0))
        config.draw_text('SPACE GAME', config.font_big, config.WHITE, self.screen_width//2 - 200, 20)

        if self.playButton.draw(config.screen) and self.menu_state == 1:
            self.menu_state = 0 # PAUSE STATE

        if self.quitButton.draw(config.screen) and self.menu_state == 1:
            self.menu_state = 2 # QUIT STATE

        if self.creditsButton.draw(config.screen) and self.menu_state == 1:
            self.menu_state = 3 # CREDITS STATE

        if self.licenseButton.draw(config.screen) and self.menu_state == 1:
            self.menu_state = 4 # LICENSE STATE

        if self.controlsButton.draw(config.screen) and self.menu_state == 1:
            self.menu_state = 5 # CONTROLS STATE

        self.resize_position()

    def controls_scene(self):
        config.screen.blit(self.asset['main_background'], (0, 0))
        pygame.draw.rect(config.screen, config.BLACK, (self.screen_width//2 - 220, 110, 460 , 130))
        config.draw_text('SPACE GAME', config.font_big, config.WHITE, self.screen_width//2 - 200, 20)
        config.draw_text('CONTROLS', config.font_big, config.WHITE, self.screen_width//2 - 200, 110)
        config.draw_text('WASD - movement, Mouse - direction', config.font_small, config.WHITE, self.screen_width//2 - 200, 140)
        config.draw_text('SPACEBAR - shoot', config.font_small, config.WHITE, self.screen_width//2 - 200, 170)
        config.draw_text('ESC - pause/main menu, F5 - save, F9 - load', config.font_small, config.WHITE, self.screen_width//2 - 200, 200)

        if self.XButton.draw(config.screen):
            self.menu_state = 1

        self.resize_position()


    def credits_scene(self):
        config.screen.blit(self.asset['main_background'], (0, 0))
        # changes position for fulscreen mode
        if self.screen_width > config.SCREEN_WIDTH:
            config.draw_text('SPACE GAME', config.font_big, config.WHITE, self.screen_width//2 - 200, 20)
            pygame.draw.rect(config.screen, config.BLACK, (self.screen_width//4, 110, 1000, 650))
            y_offset = 120  # Starting y position for text
            for line in credits_lines:
                config.draw_text(line, config.font_small, config.WHITE, self.screen_width//4 + 10, y_offset)
                y_offset += 40  # Increase y position for next line
        # default windowed resolution
        else:
            config.draw_text('SPACE GAME', config.font_big, config.WHITE, config.SCREEN_WIDTH//2 - 200, 20)
            pygame.draw.rect(config.screen, config.BLACK, (20, 110, 1040, 650))
            y_offset = 120  # Starting y position for text
            for line in credits_lines:
                config.draw_text(line, config.font_small, config.WHITE, 30, y_offset)
                y_offset += 40  # Increase y position for next line

        if self.XButton.draw(config.screen):
            self.menu_state = 1

        self.resize_position()


    def license_scene(self):
        config.screen.blit(self.asset['main_background'], (0, 0))
        # changes position for fulscreen mode
        if self.screen_width > config.SCREEN_WIDTH:
            pygame.draw.rect(config.screen, config.BLACK, (self.screen_width//4, 70, 950, 920))
            config.draw_text('SPACE GAME', config.font_big, config.WHITE, self.screen_width//2 - 200, 20)
            y_offset = 70  # Starting y position for text
            for line in license_lines:
                config.draw_text(line, config.font_small, config.WHITE, self.screen_width//4 + 10, y_offset)
                y_offset += 40  # Increase y position for next line
        # default windowed mode
        else:
            pygame.draw.rect(config.screen, config.BLACK, (20, 10, 1040, 870))
            config.draw_text('SPACE GAME', config.font_big, config.WHITE, self.screen_width//2 - 200, 20)
            y_offset = 20  # Starting y position for text
            for line in license_lines:
                config.draw_text(line, config.font_small, config.WHITE, 30, y_offset)
                y_offset += 40  # Increase y position for next line

        if self.XButton.draw(config.screen):
            self.menu_state = 1

        self.resize_position()

    # changes position for buttons and things if it is resized
    def resize_position(self):

        self.screen_width, self.screen_height = get_screen_size()

        if self.screen_width != self.old_screen_width or self.screen_height != self.old_screen_height:

            self.playButton.resize_coords(self.screen_width//2 - 100, self.screen_height//2 - 160)
            self.controlsButton.resize_coords(self.screen_width//2 - 100, self.screen_height//2 - 60)
            self.quitButton.resize_coords(self.screen_width//2 - 100, self.screen_height//2 + 140)

            self.creditsButton.resize_coords(self.screen_width - 100, self.screen_height - 100)
            self.licenseButton.resize_coords(self.screen_width - 200, self.screen_height - 100)

            self.XButton.resize_coords(self.screen_width - 100, 50)

        self.old_screen_width, self.old_screen_height = self.screen_width, self.screen_height



# get data from credits
try:
    credits_file = open("CREDITS.md", "r")
    credits_text = credits_file.read().strip()
    credits_lines = credits_text.split("\n")
    credits_file.close()

except FileNotFoundError:
    credits_text = "An error occured\nCREDITS.md was not found. Check if it is in the same folder as\nthe space_game.py and menu.py or if it is downloaded"
    credits_lines = credits_text.split("\n")

# get data from license
try:
    license_file = open("LICENSE.txt", "r")
    license_text = license_file.read().strip()
    license_lines = license_text.split("\n")
    license_file.close()

except FileNotFoundError:
    license_text = "An error occured\nLICENSE.txt was not found. Check if it is in the same folder as\nthe space_game.py and menu.py or if it is downloaded"
    license_lines = license_text.split("\n")
