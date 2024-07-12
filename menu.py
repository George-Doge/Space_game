import pygame
from sys import exit 

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT =  int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Space game menu")

# load pictures
try:
	bg_main_img = pygame.image.load('images/background/asteroid_belt.jpg')
	bg_main_img = pygame.transform.scale(bg_main_img, (1920, 1080))

	play_button_img = pygame.image.load('images/buttons/PlayButton.png').convert_alpha()
	controls_button_img = pygame.image.load('images/buttons/ControlsButton.png').convert_alpha()
	quit_button_img = pygame.image.load('images/buttons/QuitButton.png').convert_alpha()
	credits_button_img = pygame.image.load('images/buttons/QuestionmarkSquareButton.png').convert_alpha()
	license_button_img = pygame.image.load('images/buttons/InfoSquareButton.png').convert_alpha()
	x_button_img = pygame.image.load('images/buttons/XSquareButton.png').convert_alpha()

except FileNotFoundError as message:
	print("An error occured while loading images in menu.py. One or more of them have not been found.\nDownload them again or check if they are in an images folder.")
	print(f"Error message:\n{message}")

	with open("errorLog.txt", "w") as file:
		file.write(str(message))

	exit(1)

# set framerate
clock = pygame.time.Clock()
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (105, 105, 105)
font1 = pygame.font.SysFont('Futura', 30)
font2 = pygame.font.SysFont('Futura', 80)
font_small = pygame.font.SysFont('Futura', 10)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


# button class
class Button:
	def __init__(self, x, y, image, size):
		self.image = pygame.transform.scale(image, ( int(image.get_width()*size), int(image.get_height()*size) ))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.pressed = False


	def action(self):
		pressed = self.click()
		self.draw()

		return pressed

	def click(self):
		mouse_position = pygame.mouse.get_pos()
		mouse_press = pygame.mouse.get_pressed()[0]
        
		if self.rect.collidepoint(mouse_position) and self.pressed == False and mouse_press == 1:
			self.pressed = True
			return True

		if mouse_press == 0:
			self.pressed = False


	def draw(self):
		screen.blit(self.image, self.rect)


	def resize_coords(self, x, y):
		self.rect.x, self.rect.y = x, y


class main_menu():
	def __init__(self):
		self.menu_state = 1 # sets default menu state

		self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
		
		self.playButton = Button(self.screen_width//2, self.screen_height//2 - 160, play_button_img, 0.35)
		self.controlsButton = Button(self.screen_width//2, self.screen_height//2 - 60, controls_button_img, 0.35)
		self.quitButton = Button(self.screen_width//2, self.screen_height//2 + 140, quit_button_img, 0.35)
		self.creditsButton = Button(self.screen_width - 50, self.screen_height - 100, credits_button_img, 0.35)
		self.licenseButton = Button(self.screen_width - 150, self.screen_height - 100, license_button_img, 0.35)
		self.XButton = Button(self.screen_width - 50, 50, x_button_img, 0.35)

		# windows size change variables
		self.old_screen_width, self.old_screen_height = pygame.display.get_surface().get_size()


	def main_scene(self):
		screen.blit(bg_main_img, (0, 0))
		draw_text('SPACE GAME', font2, WHITE, self.screen_width//2 - 200, 20)
		
		if self.playButton.action() and self.menu_state == 1:
			self.menu_state = 0 # PAUSE STATE

		if self.quitButton.action() and self.menu_state == 1:
			self.menu_state = 2 # QUIT STATE

		if self.creditsButton.action() and self.menu_state == 1:
			self.menu_state = 3 # CREDITS STATE

		if self.licenseButton.action() and self.menu_state == 1:
			self.menu_state = 4 # LICENSE STATE

		if self.controlsButton.action() and self.menu_state == 1:
			self.menu_state = 5 # CONTROLS STATE

	def controls_scene(self):
		screen.blit(bg_main_img, (0, 0))
		draw_text('SPACE GAME', font2, WHITE, self.screen_width//2 - 200, 20)
		draw_text('CONTROLS', font1, WHITE, self.screen_width//2 - 200, 110)
		draw_text('Arrow keys - movement, SPACEBAR - shoot', font1, WHITE, self.screen_width//2 - 200, 140)
		draw_text('ESC - pause/main menu, S - save, L - load', font1, WHITE, self.screen_width//2 - 200, 170)
		
		if self.XButton.action():
			self.menu_state = 1


	def credits_scene(self):
		screen.blit(bg_main_img, (0, 0))
		# changes position for fulscreen mode
		if self.screen_width > SCREEN_WIDTH:
			draw_text('SPACE GAME', font2, WHITE, self.screen_width//2 - 200, 20)
			pygame.draw.rect(screen, BLACK, (self.screen_width//4, 110, 1000, 570))
			y_offset = 120  # Starting y position for text
			for line in credits_lines:
				draw_text(line, font1, WHITE, self.screen_width//4 + 10, y_offset)
				y_offset += 40  # Increase y position for next line
		# default windowed resolution
		else:
			draw_text('SPACE GAME', font2, WHITE, SCREEN_WIDTH//2 - 200, 20)
			pygame.draw.rect(screen, BLACK, (20, 110, 1040, 570))
			y_offset = 120  # Starting y position for text
			for line in credits_lines:
				draw_text(line, font1, WHITE, 30, y_offset)
				y_offset += 40  # Increase y position for next line

		if self.XButton.action():
			self.menu_state = 1


	def license_scene(self):
		screen.blit(bg_main_img, (0, 0))
		# changes position for fulscreen mode
		if self.screen_width > SCREEN_WIDTH:
			pygame.draw.rect(screen, BLACK, (self.screen_width//4, 70, 950, 920))
			draw_text('SPACE GAME', font2, WHITE, self.screen_width//2 - 200, 20)
			y_offset = 70  # Starting y position for text
			for line in license_lines:
				draw_text(line, font1, WHITE, self.screen_width//4 + 10, y_offset)
				y_offset += 40  # Increase y position for next line
		# default windowed mode
		else:
			pygame.draw.rect(screen, BLACK, (20, 10, 1040, 870))
			draw_text('SPACE GAME', font2, WHITE, self.screen_width//2 - 200, 20)
			y_offset = 20  # Starting y position for text
			for line in license_lines:
				draw_text(line, font1, WHITE, 30, y_offset)
				y_offset += 40  # Increase y position for next line

		if self.XButton.action():
			self.menu_state = 1

	# changes position for buttons and things if it is resized
	def resize_position(self):

		self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
		
		if self.screen_width != self.old_screen_width or self.screen_height != self.old_screen_height:

			self.playButton.resize_coords(self.screen_width//2 - 100, self.screen_height//2 - 160)
			self.controlsButton.resize_coords(self.screen_width//2 - 100, self.screen_height//2 - 60)
			self.quitButton.resize_coords(self.screen_width//2 - 100, self.screen_height//2 + 140)

			self.creditsButton.resize_coords(self.screen_width - 100, self.screen_height - 100)
			self.licenseButton.resize_coords(self.screen_width - 200, self.screen_height - 100)

			self.XButton.resize_coords(self.screen_width - 100, 50)

		self.old_screen_width, self.old_screen_height = self.screen_width, self.screen_height


# get data from credits
try:
	credits_file = open("CREDITS.md", "r")
	credits_text = credits_file.read().strip()
	credits_lines = credits_text.split("\n")
	credits_file.close()

except FileNotFoundError:
	credits_text = "An error occured\nCREDITS.md was not found. Check if it is in the same folder as\nthe space_game.py and menu.py or if it is downloaded"
	credits_lines = credits_text.split("\n")

# get data from license
try:
	license_file = open("LICENSE.txt", "r")
	license_text = license_file.read().strip()
	license_lines = license_text.split("\n")
	license_file.close()

except FileNotFoundError:
	license_text = "An error occured\nLICENSE.txt was not found. Check if it is in the same folder as\nthe space_game.py and menu.py or if it is downloaded"
	license_lines = license_text.split("\n")

if __name__ == "__main__":
	run = True

	main_menu_instance = main_menu()


	while run:

		clock.tick(FPS)

		screen.fill(WHITE)
		draw_text('SAMPLE GAME', font2, BLACK, main_menu_instance.screen_width//2 - 200, SCREEN_HEIGHT//2 - 40)

		if main_menu_instance.menu_state == 1:
			main_menu_instance.main_scene()

		if main_menu_instance.menu_state == 2: # quit
			run = False

		if main_menu_instance.menu_state == 3:
			main_menu_instance.credits_scene()

		if main_menu_instance.menu_state == 4:
			main_menu_instance.license_scene()

		if main_menu_instance.menu_state == 5:
			main_menu_instance.controls_scene()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					main_menu_instance.menu_state = 1 # pause game and show main menu
					# main_menu_instance.clicked = False

		pygame.display.update()

	pygame.quit()
