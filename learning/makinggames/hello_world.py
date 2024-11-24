import pygame, sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
DISPLAYSURF = pygame.display.set_mode((400, 300))  # Window size: 400x300
pygame.display.set_caption('Hello World!')

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:  # Handle window close
            pygame.quit()
            sys.exit()
    pygame.display.update()  # Refresh the screen