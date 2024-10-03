import pygame

WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
GREY = (105, 105, 105)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (50, 60))