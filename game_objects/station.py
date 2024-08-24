# TODO: fix errors

class Station(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image['station']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = pygame.Rect(0, 0, 500, 400)  # HERE you can modify range of stations
        self.name = name
        # energy buy price
        self.energy_price = round(random.uniform(0.5, 2), 2)
        # material sell price
        self.asteroid_price = round(random.uniform(1, 3), 2)

    def update(self):
        self.action()
        self.draw()

    def energy_station(self):
        draw_text(f'Buy 10 energy for {self.energy_price} credits?', font_small, WHITE, self.rect.x - 100,
                  self.rect.y + 100)

        if energy_buying and Player.credits > 0 and not Player.energy >= Player.energy_full:
            Player.credits -= self.energy_price
            Player.energy += 10
        if energy_all_buying:
            while not Player.energy >= Player.energy_full and Player.credits > 0:
                Player.credits -= self.energy_price
                Player.energy += 10

    def trade_station(self):
        draw_text(f'Sell mined asteroids for {self.asteroid_price} credits per t?', font_small, WHITE,
                  self.rect.x - 100,
                  self.rect.y + 130)

        # selling
        if selling and Player.storage > 0:
            Player.storage -= 1
            Player.credits += self.asteroid_price
        if selling_all and Player.storage > 0:
            Player.credits += self.asteroid_price + Player.storage
            Player.storage = 0

    # interaction and actions of station are handled
    def action(self):
        self.range.center = self.rect.center

        if self.range.colliderect(Player.rect):
            draw_text(f'{self.name} Station', font_small, WHITE, self.rect.x - len(self.name) * 3, self.rect.y - 30)

            # check what type of station it is

            if self.name == 'Energy':
                self.energy_station()

            if self.name == 'Trade':
                self.trade_station()

            if self.name == 'Energy & Trade':
                self.energy_station()
                self.trade_station()

    def draw(self):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, RED, self.range, 3) debug line for station range