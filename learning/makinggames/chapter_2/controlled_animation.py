import pygame, sys
from pygame.locals import *

# Initialize Pygame
def main():
    pygame.init()

    # Set up the display
    DISPLAYSURF = pygame.display.set_mode((500, 400))
    pygame.display.set_caption('User Input Example')

    # Define colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Set initial position for the circle
    x, y = 250, 200
    speed = 5

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # Update circle position to mouse click location
                x, y = event.pos  # event.pos returns the (x, y) position of the mouse

        # Handle key press events for movement
        keys = pygame.key.get_pressed()  # Returns a list of all key states
        if keys[K_LEFT]:
            x -= speed
        if keys[K_RIGHT]:
            x += speed
        if keys[K_UP]:
            y -= speed
        if keys[K_DOWN]:
            y += speed


        # Redraw the screen
        DISPLAYSURF.fill(WHITE)  # Clear the screen
        pygame.draw.circle(DISPLAYSURF, RED, (x, y), 20)  # Draw the circle

        pygame.display.update()  # Refresh the display
        pygame.time.Clock().tick(60)  # Limit to 60 FPS

# Ensures that main() runs only when this file is executed directly
if __name__ == '__main__':
    main()