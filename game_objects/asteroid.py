# Load packages
import pygame

# Link objects
from game_objects.debris import Debris

# Load graphics
from load import asteroid_resources


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, rarity, x, y):
        super().__init__()
        self.type = rarity
        self.asset = asteroid_resources()
        # determines what type of asteroid it should show and gives it properties
        if rarity == "common":
            self.image = self.asset['asteroid']
            self.health = 30

        elif rarity == "rare":
            self.image = self.asset['asteroid_2']
            self.health = 40
        # in case of error shows basic asteroid
        else:
            self.image = self.asset['asteroid']
            self.type = "common"

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, screen, group):
        self.draw(screen)

        if self.health <= 0:

            if self.type == "common":  # add mined storage in case of a common asteroid
                debris_instance = Debris(self.type, self.rect.center[0], self.rect.center[1])
                group.add(debris_instance)
                self.kill()

            elif self.type == "rare":  # add in case of a rare asteroid
                debris_instance = Debris(self.type, self.rect.center[0], self.rect.center[1])
                group.add(debris_instance)
                self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
