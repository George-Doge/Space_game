# Load packages
import pygame
import random

# Load graphics
from game_logic.load import asteroid_resources


class Debris(pygame.sprite.Sprite):
    def __init__(self, rarity, x, y):
        super().__init__()
        self.rarity = rarity
        self.asset = asteroid_resources()
        if self.rarity == "rare":
            self.image = self.asset['debris_rare']

        else:
            self.image = self.asset['debris_common']

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, screen, ship):
        self.draw(screen)
        # check if the debris is collected by the ship
        if self.rect.colliderect(ship.rect) and ship.storage < ship.storage_max:
            if self.rarity == "rare":
                self.kill()
                ship.storage += 1.5 * round(random.uniform(1, 3), 2)

            elif self.rarity == "common":
                self.kill()
                ship.storage += 1.2 * round(random.uniform(0.6, 2), 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
