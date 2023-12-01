import pygame
import random, json

#TODO maybe more stations 
#TODO ADD LOAD, AND FORMAT STORAGE AND MONEY, BECAUSE IT DOES NOT ROUND DOWN!!!!!
pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT =  int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Playtest-space game")

# load pictures
bg_img = pygame.image.load('images/space.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT - 270))

ship_img = pygame.image.load('images/ship.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (60, 75))
ship_img = pygame.transform.rotate(ship_img, 270)

station_img = pygame.image.load('images/station.png').convert_alpha()
station_img = pygame.transform.scale(station_img, (80, 80))

asteroid_img = pygame.image.load('images/asteroid.png').convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (60, 60))

laser_img = pygame.image.load('images/laser.png').convert_alpha()

# set framerate
clock = pygame.time.Clock()
FPS = 60

#COLOURS and fonts
YELLOW = (211, 174, 54)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
font = pygame.font.SysFont('Futura', 30)
font2 = pygame.font.SysFont('Futura', 80)

#variables
moving_up = False
moving_down = False
moving_left = False
moving_right = False
fuel_buying = False
selling = False
paused = True #zmenit na true, ked to bude hotove
shooting = False

#Saving/loading function
def saving():
	save_data = {
		'credits': Player.credits,
		'storage': Player.storage,
		'fuel': Player.fuel,
	}

	with open("save.json", "w") as file:
		json.dump(save_data, file)

	print("GAME SAVED")

def loading():
	try:
		with open("save.json", "r") as file:
			save_data = json.load(file)
			Player.credits = save_data.get('credits')
			Player.storage = save_data.get('storage')
			Player.fuel = save_data.get('fuel')

		print("GAME LOADED")

	except FileNotFoundError:
		print("SAVE NOT FOUND")

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_bg():
	screen.fill(YELLOW)
	screen.blit(bg_img, (0, 0))


class Ship(pygame.sprite.Sprite):
	def __init__(self, x, y, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = ship_img
		self.flip = False
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.speed = speed
		self.direction = 1
		# fuel things and rectangles
		self.fuel_full = 100
		self.fuel = 100
		self.fuel_max = pygame.Rect(70, 650, 100, 40)
		# credits
		self.credits = 10
		# storage
		self.storage_max = 7
		self.storage = 0
		#shooting
		self.cooldown = 30
		self.damage = 1

	def update(self):
		self.action()
		self.moving()
		self.draw()
		
	def moving(self):
		
		fueld = 0
		
		if self.fuel > 0:
		
			if moving_up and self.rect.top >= 10:
				self.rect.y -= self.speed * 0.75
				fueld -= 1
				
			if moving_down and self.rect.bottom <= SCREEN_HEIGHT - 280:
				self.rect.y += self.speed * 0.75
				fueld -= 1
		
			if moving_left and self.rect.left >= 10:
				self.flip = True
				self.direction = -1
				self.rect.x -= self.speed
				fueld -= 1
		
			if moving_right and self.rect.right <= SCREEN_WIDTH - 10:
				self.flip = False
				self.direction = 1
				self.rect.x += self.speed
				fueld -= 1
				
		if moving_down and moving_up or moving_left and moving_right:
			fueld = 0
				
		# handle fuel burning (so that it won't burn 2 units if pressing W and S for example)			
		if fueld <= -1:
			self.fuel -= 1 * 0.4

			
	def action(self):
		# check for low or max fuel
		if self.fuel <= self.fuel_full * 0.3 and not self.fuel <= 0:
			draw_text('WARNING, LOW FUEL', font, RED, 70, 700)
			
		elif self.fuel <= 0:
			draw_text('NO FUEL', font, RED, 70, 700)
			
		if self.fuel > self.fuel_full:
			self.fuel = self.fuel_full
		
		# draw fuel gauge
		draw_text('FUEL', font, WHITE, 70, 620)
		self.fuel_stor = pygame.Rect(70, 650, self.fuel, 40)
		pygame.draw.rect(screen, RED, self.fuel_max)
		pygame.draw.rect(screen, GREEN, self.fuel_stor)
		
		# inventory and money
		draw_text(f'{round(self.credits, 2)} credits', font, WHITE, 280, 620)
		
		if self.credits <= 0:
			self.credits = 0
			
		# cargo
		draw_text(f'Cargo: {round(self.storage, 2)} t ', font, WHITE, 500, 620)
		
		if self.storage >= self.storage_max * 0.75 and not self.storage == self.storage_max:
			draw_text(f'Reaching maximum capacity', font, RED, 500, 650)
		
		elif self.storage >= self.storage_max:
			draw_text(f'Maximum cargo capacity reached', font, RED, 500, 650)
			
		if self.storage < 0:
			self.storage = 0
			
		if self.storage > self.storage_max:
			self.storage = self.storage_max
			
		
		#shooting
		if shooting and self.cooldown <= 0:
			laser = Laser(self.rect.centerx + (40 * self.direction), self.rect.centery, self.direction)
			laser_group.add(laser)
			self.cooldown = 30
			
		self.cooldown -= 1
		

	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
		

class Laser(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.image = laser_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction
		self.speed = 10
	
	def update(self):
		# move laser
		self.rect.x += (self.speed * self.direction)
		
		if self.rect.left >= SCREEN_WIDTH or self.rect.right < 0:
			self.kill()
		#check for collision with asteroid
		for asteroid in asteroid_group:
			if pygame.sprite.spritecollide(asteroid, laser_group, False):
				asteroid.health -= 10
				self.kill()


class Station(pygame.sprite.Sprite):
	def __init__(self, name, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = station_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.range = pygame.Rect(0, 0, 300, 300)
		self.name = name
		# fuel buy price
		self.fuel_price = round(random.uniform(0.5, 2), 2)
		# material sell price
		self.asteroid_price = round(random.uniform(1, 3), 2)
		
	def update(self):
		self.action()
		self.draw()
		
	def fuel_station(self):
		draw_text(f'Buy 10 fuel for {self.fuel_price} credits?', font, WHITE, self.rect.x -100, self.rect.y + 100)
		
		if fuel_buying and Player.credits > 0 and not Player.fuel >= Player.fuel_full:
			Player.credits -= self.fuel_price
			Player.fuel += 10
		
	def trade_station(self):
		draw_text(f'Sell mined asteroids for {self.asteroid_price} credits per t?', font, WHITE, self.rect.x -100, self.rect.y + 130)

		#selling
		if selling and Player.storage > 0:
			Player.storage -= 1
			Player.credits += self.asteroid_price
		
# here, interaction and actions of station are handled
	def action(self):
		self.range.center = self.rect.center
		
		if self.range.colliderect(Player.rect):
			draw_text(f'{self.name} Station', font, WHITE, self.rect.x - len(self.name) * 3, self.rect.y - 30)
			
			#check what type of station it is
			
			if self.name == 'Fuel':
				self.fuel_station()
				
			if self.name == 'Trade':
				self.trade_station()
			
			if self.name == 'Fuel & Trade':
				self.fuel_station()
				self.trade_station()
		
		
	def draw(self):
		screen.blit(self.image, self.rect)


class Asteroid(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = asteroid_img
		self.rect = self.image.get_rect()
		# select random spawnpoint
		self.randomx = random.randint(500, SCREEN_WIDTH - 60)
		self.randomy = random.randint(60, SCREEN_HEIGHT - 300)
		self.rect.center = (self.randomx, self.randomy)
		self.health = 30
		
		
	def update(self):
		self.draw()
		
		if self.health <= 0:
			Player.storage += 1.2 * round(random.uniform(0.6, 3), 2)
			self.kill()
			
		if len(asteroid_group) < 3: #TODO ADD MORE ASTEROIDS
			asteroid = Asteroid()
			asteroid_group.add(asteroid)
		
	def draw(self):
		screen.blit(self.image, self.rect)


# declare instances
Player = Ship(500, 200, 10)
station = Station('Fuel & Trade', 200, 400)
#asteroid things
asteroid_group = pygame.sprite.Group()
asteroid = Asteroid()
asteroid_group.add(asteroid)
#laser things
laser_group = pygame.sprite.Group()

run = True

while run:

	clock.tick(FPS)
	draw_bg()
	
	# pauses the game
	if paused:
		draw_text('Move using arrow keys. When near a station you can: buy fuel - F sell cargo - H, shoot - SPACEBAR', font, WHITE, 0, 20)
		draw_text('Press ESC to enter this menu and pause game, press S to save and L to load.', font, WHITE, 0, 50)

	else:

		# updates instances of player and stations and more
		
		station.update()
	
		Player.update()
		asteroid_group.update()
		asteroid_group.draw(screen)
		laser_group.update()
		laser_group.draw(screen)
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if not paused:
					paused = True
				else:
					paused = False

			#ship movement
			if event.key == pygame.K_UP:
				moving_up = True
				
			if event.key == pygame.K_DOWN:
				moving_down = True				

			if event.key == pygame.K_LEFT:
				moving_left = True
	
			if event.key == pygame.K_RIGHT:
				moving_right = True
				
			if event.key == pygame.K_SPACE:
				shooting = True
			#selling and buying
			if event.key == pygame.K_f:
				fuel_buying = True
				
			if event.key == pygame.K_h:
				selling = True
			
			if event.key == pygame.K_s:
				saving()
				
			if event.key == pygame.K_l:
				loading()


		if event.type == pygame.KEYUP:
			#ship movement
			if event.key == pygame.K_UP:
				moving_up = False

			if event.key == pygame.K_DOWN:
				moving_down = False				

			if event.key == pygame.K_LEFT:
				moving_left = False

			if event.key == pygame.K_RIGHT:
				moving_right = False
				
			if event.key == pygame.K_SPACE:
				shooting = False
				
			if event.key == pygame.K_f:
				fuel_buying = False

			if event.key == pygame.K_h:
				selling = False
				
	pygame.display.update()

pygame.quit()
