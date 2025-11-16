import pygame
import sys
from buttons import *   # or your functions specifically

pygame.init()

# Window 
width = 1280
height = 720 
mainScreen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame GUI")

# Font
FONT = pygame.font.SysFont("arial", 30)

# Images
startImage = pygame.image.load("images/startScreen.png")

# Game State
gameState = "start"

def main():
    global gameState
    clock = pygame.time.Clock()

    if (gameState == "start"):#Start Screen 
        pygame.mixer.music.load("sounds/startBGM.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    while True:
        mainScreen.blit(startImage, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
