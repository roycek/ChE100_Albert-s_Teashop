import pygame
import sys
from old_minis.minigame1 import run_minigame
from old_minis.minigame2 import run_minigame2
from minigame3 import run_minigame3

pygame.init()

# Window setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tea Shop")

# Button setup
button_color = (255, 0, 0)
button_rect = pygame.Rect(WIDTH // 2 - 325, 50, 200, 50)
second_button_rect = pygame.Rect(WIDTH // 2 - 100, 50, 200, 50)
third_button_rect = pygame.Rect(WIDTH // 2 + 125, 50, 200, 50)
font = pygame.font.Font(None, 40)
text_surface = font.render("Minigame 1", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=button_rect.center)
text_surface2 = font.render("Minigame 2", True, (255, 255, 255))
text_rect2 = text_surface2.get_rect(center=second_button_rect.center)
text_surface3 = font.render("Minigame 3", True, (255, 255, 255))
text_rect3 = text_surface3.get_rect(center=third_button_rect.center)

clock = pygame.time.Clock()


def main():
    running = True
    while running:
        screen.fill((240, 230, 200))  # light tea color background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    run_minigame(screen, clock)  # existing minigame
                elif second_button_rect.collidepoint(event.pos):
                    run_minigame2(screen, clock)  # new minigame
                elif third_button_rect.collidepoint(event.pos):
                    run_minigame3(screen, clock)  # titration simulator

        # Draw buttons
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, button_color, second_button_rect)
        pygame.draw.rect(screen, button_color, third_button_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface2, text_rect2)
        screen.blit(text_surface3, text_rect3)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
