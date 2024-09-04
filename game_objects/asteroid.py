import pygame

# Link objects
from game_objects.debris import Debris
from load import game_images

# TODO: load only asteroid resources
image = game_images()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen, rarity, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
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
                # TODO: fix debris_group
                debris_group.add(debris_instance)
                self.kill()

            elif self.type == "rare":  # add in case of a rare asteroid
                debris_instance = Debris(self.type, self.rect.center[0], self.rect.center[1])
                debris_group.add(debris_instance)
                self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)
