# Load packages
import pygame
import random
import config

# Load graphics
from game_logic.load import game_images


class Station(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.asset = game_images()
        self.image = self.asset['station']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = pygame.Rect(0, 0, 500, 400)  # HERE you can modify range of stations
        self.name = name
        # energy buy price
        self.energy_price = round(random.uniform(0.5, 2), 2)
        # material sell price
        self.asteroid_price = round(random.uniform(1, 3), 2)

    def update(self, screen, ship, energy_buying, energy_all_buying, selling, selling_all):
        self.action(screen, ship, energy_buying, energy_all_buying, selling, selling_all)
        self.draw(screen)

    def energy_station(self, screen, ship, energy_buying, energy_all_buying):
        config.draw_text(screen, f'Buy 10 energy for {self.energy_price} credits?',
                         config.font_small, config.WHITE,
                         self.rect.x - 100,
                         self.rect.y + 100)

        if energy_buying and ship.credits > 0 and not ship.energy >= ship.energy_full:
            ship.credits -= self.energy_price
            ship.energy += 10
        if energy_all_buying:
            while not ship.energy >= ship.energy_full and ship.credits > 0:
                ship.credits -= self.energy_price
                ship.energy += 10

    def trade_station(self, screen, ship, selling, selling_all):
        config.draw_text(screen, f'Sell mined asteroids for {self.asteroid_price} credits per t?',
                         config.font_small, config.WHITE,
                         self.rect.x - 100,
                         self.rect.y + 130)

        # selling
        if selling and ship.storage > 0:
            ship.storage -= 1
            ship.credits += self.asteroid_price
        if selling_all and ship.storage > 0:
            ship.credits += self.asteroid_price + ship.storage
            ship.storage = 0

    # interaction and actions of station are handled
    def action(self, screen, ship, energy_buying, energy_all_buying, selling, selling_all):
        self.range.center = self.rect.center

        if self.range.colliderect(ship.rect):
            config.draw_text(screen, f'{self.name} Station',
                             config.font_small, config.WHITE,
                             self.rect.x - len(self.name) * 3,
                             self.rect.y - 30)

            # check what type of station it is

            if self.name == 'Energy':
                self.energy_station(screen, ship, energy_buying, energy_all_buying,)

            if self.name == 'Trade':
                self.trade_station(screen, ship, selling, selling_all)

            if self.name == 'Energy & Trade':
                self.energy_station(screen, ship, energy_buying, energy_all_buying)
                self.trade_station(screen, ship, selling, selling_all)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, RED, self.range, 3) debug line for station range
