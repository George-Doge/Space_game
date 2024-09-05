# Load packages
import pygame
import math

# Load graphics
from game_logic.load import game_images


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction: list, angle: int):
        super().__init__()
        self.asset = game_images()
        self.image = pygame.transform.rotate(self.asset['laser'], angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 10

    def update(self, screen, asteroid_group, laser_group):
        self.draw(screen)
        screen_width = pygame.display.get_surface().get_size()[0]

        # move laser
        t = self.speed / math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2)
        self.rect.centerx += t * self.direction[0]
        self.rect.centery += t * self.direction[1]

        if self.rect.left >= screen_width or self.rect.right < 0:
            self.kill()
        # check for collision with asteroid
        for asteroid in asteroid_group:
            if pygame.sprite.spritecollide(asteroid, laser_group, False):
                asteroid.health -= 15  # set damage
                self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
