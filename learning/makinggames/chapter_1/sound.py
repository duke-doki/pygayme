import pygame, sys
from pygame.locals import *

def main():
    pygame.init()

    # Set up the display
    DISPLAYSURF = pygame.display.set_mode((500, 400))
    pygame.display.set_caption('Sound Example')

    # Load and play a sound
    sound = pygame.mixer.Sound('media/match4.wav')  # Replace with your sound file
    sound.play()

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((255, 255, 255))  # Clear the screen
        pygame.display.update()

if __name__ == '__main__':
    main()