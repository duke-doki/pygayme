import pygame
import sys
from pygame.locals import *


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    DISPLAYSURF = pygame.display.set_mode((500, 400))
    pygame.display.set_caption('Animation Example')

    # Define colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Set initial position and speed for the circle
    x, y = 50, 200
    speed_x, speed_y = 2, 1

    # Add a bouncing rectangle
    rect_x, rect_y = 100, 50
    rect_speed_x, rect_speed_y = 3, 2

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Update position
        x += speed_x
        y += speed_y

        # Inside the main loop, update the rectangle's position
        rect_x += rect_speed_x
        rect_y += rect_speed_y

        # Bounce the circle off the edges
        if x + 20 > 500 or x - 20 < 0:  # 20 is the circle's radius
            speed_x = -speed_x
        if y + 20 > 400 or y - 20 < 0:
            speed_y = -speed_y

        # Bounce the rectangle off edges
        if rect_x + 50 > 500 or rect_x < 0:  # 50 is the rectangle's width
            rect_speed_x = -rect_speed_x
        if rect_y + 30 > 400 or rect_y < 0:  # 30 is the rectangle's height
            rect_speed_y = -rect_speed_y

        # Redraw the screen
        DISPLAYSURF.fill(WHITE)  # Clear the screen
        pygame.draw.circle(DISPLAYSURF, RED, (x, y), 20)  # Draw the circle
        pygame.draw.rect(DISPLAYSURF, (0, 0, 255),
                         (rect_x, rect_y, 50, 30))  # Blue rectangle

        pygame.display.update()  # Refresh the display
        pygame.time.Clock().tick(60)  # Limit to 60 FPS


if __name__ == '__main__':
    main()