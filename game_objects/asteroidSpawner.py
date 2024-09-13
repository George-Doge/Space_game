# Load packages
import random

# Link objects
from game_objects.asteroid import Asteroid


class AsteroidSpawner:
    def __init__(self):
        self.spawnX = 100
        self.spawnY = 120
        self.spawn_width = 1020
        self.spawn_height = 600
        self.randomy = None
        self.randomx = None

    @staticmethod
    def set_rarity():
        return "rare" if random.randint(1, 10) > 7 else "common"

    def spawn_location(self):
        """ Sets spawn location of the asteroid """
        self.randomx = random.randint(round(self.spawnX), round(self.spawnX + self.spawn_width))
        self.randomy = random.randint(round(self.spawnY), round(self.spawnY + self.spawn_height))

    def update(self, asteroid_group):
        # pygame.draw.rect(screen, RED, (self.spawnX, self.spawnY, self.spawn_width, self.spawn_height), 5) # Debug to show asteroid spawn location
        max_number_of_asteroids = 2  # HERE change to modify max number of asteroids
        number_of_asteroids = 0
        for asteroid in asteroid_group:
            if asteroid.is_rendered:
                number_of_asteroids += 1

        if number_of_asteroids < max_number_of_asteroids:
            for i in range(number_of_asteroids, max_number_of_asteroids):
                self.spawn_location()
                asteroid = Asteroid(self.set_rarity(), self.randomx, self.randomy)
                asteroid_group.add(asteroid)
