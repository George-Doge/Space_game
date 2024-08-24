# TODO: add imports
# TODO: fix asteroid_group

class AsteroidSpawner():
    def __init__(self):
        self.spawnX = 500
        self.spawnY = 120
        self.spawn_width = 1020
        self.spawn_height = 600

    def spawn_location(self):
        # select random spawn point
        self.randomx = random.randint(self.spawnX, self.spawnX + self.spawn_width)
        self.randomy = random.randint(self.spawnY, self.spawnY + self.spawn_height)

    def determine_type(self):
        choice = random.randint(1, 10)

        if choice > 7:
            rarity = "rare"
            return rarity

        else:
            rarity = "common"
            return rarity

    def update(self):
        # pygame.draw.rect(screen, RED, (self.spawnX, self.spawnY, self.spawn_width, self.spawn_height), 5) # Debug to show asteroid spawn location
        spawn_new = False
        max_number_of_asteroids = 13  # HERE change to modify max number of asteroids
        number_of_asteroids = len(asteroid_group)

        # HERE you can change number of asteroids that need to be mined so new can be spawned
        if number_of_asteroids < 8:
            spawn_new = True

        if spawn_new:
            for i in range(number_of_asteroids, max_number_of_asteroids):
                self.spawn_location()
                rarity = self.determine_type()
                asteroid = Asteroid(rarity, self.randomx, self.randomy)
                asteroid_group.add(asteroid)