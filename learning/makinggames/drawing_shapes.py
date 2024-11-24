import pygame, sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
DISPLAYSURF = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Drawing Shapes')

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fill the screen with white
DISPLAYSURF.fill(WHITE)

# Draw shapes
pygame.draw.rect(DISPLAYSURF, RED, (100, 50, 200, 100))  # Red rectangle
pygame.draw.circle(DISPLAYSURF, BLUE, (250, 200), 50)    # Blue circle
pygame.draw.line(DISPLAYSURF, GREEN, (50, 300), (450, 300), 5)  # Green line

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()