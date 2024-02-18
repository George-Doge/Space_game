import pygame
import random, json
from menu import main_menu

#TODO maybe more stations, !MAKE PAUSE MENU BETTER!
#TODO add some animations, so it doesn't look static; bigger/more maps?? I don't know
pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT =  int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space game v0.2.3")

# load pictures
bg_img = pygame.image.load('images/background/space.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT - 270))

ship_img = pygame.image.load('images/sprites/ship.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (60, 75))
ship_img = pygame.transform.rotate(ship_img, 270)

station_img = pygame.image.load('images/sprites/station.png').convert_alpha()
station_img = pygame.transform.scale(station_img, (100, 100))

asteroid_img = pygame.image.load('images/sprites/asteroid.png').convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (60, 60))

asteroid2_img = pygame.image.load('images/sprites/asteroid-2.png').convert_alpha()
asteroid2_img = pygame.transform.scale(asteroid2_img, (60, 60))

laser_img = pygame.image.load('images/sprites/laser.png').convert_alpha()

#button images
buy_img = pygame.image.load('images/buttons/buy.png').convert_alpha()
sell_img = pygame.image.load('images/buttons/sell.png').convert_alpha()


# set framerate
clock = pygame.time.Clock()
FPS = 60

#COLOURS and fonts
YELLOW = (211, 174, 54)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 48, 78)
DARK_BLUE_2 = (0, 3, 66)
font = pygame.font.SysFont('Futura', 30)
font2 = pygame.font.SysFont('Futura', 80)

#variables
moving_up = False
moving_down = False
moving_left = False
moving_right = False
fuel_buying = False
selling = False
shooting = False
bg_offset = 0
first_run = True

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
		print("!!!SAVE NOT FOUND!!!")

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_bg(x):
	screen.fill(DARK_BLUE)
	if main_menu_instance.state == 1: #for now there will be just one image printed 3 times which will be moving. Then it will reset
		for i in range(2): 
			screen.blit(bg_img, (x + SCREEN_WIDTH * i, 0))


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
		self.storage_max = 15 #adjust to change maximum storage
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
		self.fuel = round(self.fuel, 2)
		
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
			self.fuel -= 1 * 0.3 # change the parameter to adjust fuel burning speed

			
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
		self.credits = round(self.credits, 2)
		draw_text(f'{self.credits} credits', font, WHITE, 280, 620)
		
		if self.credits <= 0:
			self.credits = 0
			
		# cargo
		self.storage = round(self.storage, 2)
		draw_text(f'Cargo: {self.storage} t ', font, WHITE, 500, 620)
		
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
				asteroid.health -= 15 #set damage
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
	def __init__(self, type):
		pygame.sprite.Sprite.__init__(self)
		self.type = type
		#determines what type of asteroid it should show and gives it properties
		if type == "common":
			self.image = asteroid_img
			self.health = 30

		elif type == "rare":
			self.image = asteroid2_img
			self.health = 40
		# in case of error shows basic asteroid
		else:
			self.image = asteroid_img
			self.type = "common"

		self.rect = self.image.get_rect()
		# select random spawnpoint
		self.randomx = random.randint(500, SCREEN_WIDTH - 60)
		self.randomy = random.randint(60, SCREEN_HEIGHT - 300)
		self.rect.center = (self.randomx, self.randomy)


	def determine_type(self):
		choice = random.randint(1, 10)

		if choice > 7:
			type = "rare"
			return type

		else:
			type = "common"
			return type


	def update(self):
		self.draw()
		spawn_new = False
		max_number_of_asteroids = 6 #HERE change to modify max number of asteroids
		number_of_asteroids = len(asteroid_group)

		if self.health <= 0:

			if self.type == "common": #add mined storage in case of a common asteroid
				Player.storage += 1.2 * round(random.uniform(0.6, 2), 2)
				self.kill()

			elif self.type == "rare": #add in case of a rare asteroid
				Player.storage += 1.5 * round(random.uniform(1, 3), 2)
				self.kill()

		if number_of_asteroids < 4: #HERE you can change number of asteroids that need to be mined so new can be spawned
			spawn_new = True
		
		if spawn_new:
			for i in range(number_of_asteroids, max_number_of_asteroids):
				type = self.determine_type()
				asteroid = Asteroid(type)
				asteroid_group.add(asteroid)

			spawn_new = False

	def draw(self):
		screen.blit(self.image, self.rect)

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


# declare instances
Player = Ship(500, 200, 10)
station = Station('Fuel & Trade', 200, 400)
#asteroid things
asteroid_group = pygame.sprite.Group()
asteroid = Asteroid("common")
asteroid_group.add(asteroid)
#laser things
laser_group = pygame.sprite.Group()

#buttons
buyButton = Button(105, 760, buy_img, 3)
sellButton = Button(550, 760, sell_img, 3)

#main menu instance
main_menu_instance = main_menu()
run = True

while run:

	clock.tick(FPS)

		# moves bg a little bit and updates it

	if main_menu_instance.state == 1:
		bg_offset -= 0.35 #here you can change the value to make it slower/faster. I found values around 0.35 to be fine

	if bg_offset < -SCREEN_WIDTH: #reset bg_offset so it loops forever
		bg_offset = 0

	draw_bg(bg_offset)
		
	# updates instances of player and stations and more
	if main_menu_instance.state == 1: #loads thing only when game is unpaused
		fuel_buying = buyButton.draw(screen)
		selling = sellButton.draw(screen)

		station.update()
			
		Player.update()
		asteroid_group.update()
		asteroid_group.draw(screen)
		laser_group.update()
		laser_group.draw(screen)
	
	if main_menu_instance.state != 1:
		main_menu_instance.controller()

	if main_menu_instance.state == 3: #quit button
		run = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				main_menu_instance.state = 0

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
				
			#saving and loading
			if event.key == pygame.K_s and main_menu_instance.state == 1:
				#check if the game is running, so player can't load/save when paused
				saving()
				
			if event.key == pygame.K_l and main_menu_instance.state == 1:
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
				
	pygame.display.update()

pygame.quit()
