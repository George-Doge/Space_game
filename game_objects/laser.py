# TODO: add imports
# TODO: fix asteroid_group and laser_group

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction: list, angle: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(image['laser'], angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 10

    def update(self):
        self.draw()
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

    def draw(self):
        screen.blit(self.image, self.rect)

