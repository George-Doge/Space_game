# TODO: add imports
# TODO: check merge-ability with Asteroid class

class Debris(pygame.sprite.Sprite):
    def __init__(self, rarity, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rarity = rarity
        if self.rarity == "rare":
            self.image = image['debris_rare']

        else:
            self.image = image['debris_common']

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.draw()
        # check if the debris is collected by the player
        if (self.rect.colliderect(Player.rect) and Player.storage < Player.storage_max):
            if self.rarity == "rare":
                self.kill()
                Player.storage += 1.5 * round(random.uniform(1, 3), 2)

            elif self.rarity == "common":
                self.kill()
                Player.storage += 1.2 * round(random.uniform(0.6, 2), 2)

    def draw(self):
        screen.blit(self.image, self.rect)
