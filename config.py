SCREEN_WIDTH = 1080
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# COLOURS and fonts
YELLOW = (211, 174, 54)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 48, 78)
DARK_BLUE_2 = (0, 3, 66)
ENERGY_BLUE = (33, 150, 243)
EMPTY_BLACK = (26, 24, 26)
STORAGE_BROWN = (187, 142, 81)


def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

