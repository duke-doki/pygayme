import pygame, sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
DISPLAYSURF = pygame.display.set_mode((500, 400))  # Window size: 500x400
pygame.display.set_caption('Event Handling')

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            print(f"Mouse clicked at {event.pos}")
        elif event.type == KEYDOWN:
            print(f"Key pressed: {event.key}")

    pygame.display.update()