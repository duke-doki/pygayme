import pygame, sys
from pygame.locals import *

def main():
    pygame.init()

    # Set up the display
    DISPLAYSURF = pygame.display.set_mode((500, 400))
    pygame.display.set_caption('Fonts Example')

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Set up a font
    font = pygame.font.Font('freesansbold.ttf', 32)  # Font name and size
    text_surface = font.render('Hello, Pygame!', True, BLACK)  # Text, anti-aliasing, color
    text_rect = text_surface.get_rect()
    text_rect.center = (250, 200)

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(WHITE)  # Clear the screen
        DISPLAYSURF.blit(text_surface, text_rect)  # Draw the text at the specified position

        pygame.display.update()  # Refresh the display

if __name__ == '__main__':
    main()