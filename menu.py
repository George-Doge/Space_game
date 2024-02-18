import pygame

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT =  int(SCREEN_WIDTH * 0.8)
#TODO find 'X' button
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space game v-menu")

# load pictures
bg_main_img = pygame.image.load('images/background/asteroid_belt.jpg')
bg_main_img = pygame.transform.scale(bg_main_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

play_button_img = pygame.image.load('images/buttons/PlayButton.png').convert_alpha()
controls_button_img = pygame.image.load('images/buttons/ControlsButton.png').convert_alpha()
quit_button_img = pygame.image.load('images/buttons/QuitButton.png').convert_alpha()

# set framerate
# clock = pygame.time.Clock()
# FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont('Futura', 30)
font2 = pygame.font.SysFont('Futura', 80)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


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


class main_menu():
	def __init__(self):
		self.state = 0
		self.playButton = Button(540, 300, play_button_img, 0.35)
		self.controlsButton = Button(540, 400, controls_button_img, 0.35)
		self.quitButton = Button(540, 600, quit_button_img, 0.35)

	def controller(self):
		self.logic()

		if self.state == 0: #pauses the game
			self.main_scene()

		if self.state == 1: #starts game
			pass 

		if self.state == 2: #shows controls
			self.controls_scene()


	def logic(self):

		if self.playButton.draw(screen): #start game
			self.state = 1

		elif self.controlsButton.draw(screen):#show controls
			self.state = 2

		elif self.quitButton.draw(screen): #quit game
			self.state = 3

		# print(self.state)


	def main_scene(self):
		screen.blit(bg_main_img, (0, 0))
		draw_text('SPACE GAME', font2, WHITE, SCREEN_WIDTH//2 - 200, 20)
		self.playButton.draw(screen)
		self.controlsButton.draw(screen)
		self.quitButton.draw(screen)


	def controls_scene(self):
		screen.blit(bg_main_img, (0, 0))
		draw_text('SPACE GAME', font2, WHITE, SCREEN_WIDTH//2 - 200, 20)
		draw_text('CONTROLS', font, WHITE, SCREEN_WIDTH//2 - 200, 110)
		draw_text('Arrow keys - movement, SPACEBAR - shoot', font, WHITE, SCREEN_WIDTH//2 - 200, 140)
		draw_text('ESC - pause/main menu, S - save, L - load', font, WHITE, SCREEN_WIDTH//2 - 200, 170)


'''
run = True

main_menu_instance = main_menu()
while run:

	clock.tick(FPS)

	screen.fill(WHITE)
	draw_text('SAMPLE GAME', font2, BLACK, SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 40)

	if main_menu_instance.state != 1:
		main_menu_instance.controller()

	if main_menu_instance.state == 3: #quit button
		run = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				main_menu_instance.state = 0 #pause game and show main menu

	pygame.display.update()

pygame.quit()
'''