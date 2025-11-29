import pygame
import random
import math
import time

class Leaf:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image_orig = image  # original PNG image
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.base_speed = random.uniform(6.5, 10.5)
        self.angle = random.uniform(0, 2 * math.pi)  # horizontal wobble
        self.angle_speed = random.uniform(0.02, 0.05)
        self.amplitude = random.uniform(20, 60)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-3, 3)

    def update(self):
        # Horizontal drifting
        self.x += math.sin(self.angle) * self.amplitude * 0.02
        self.angle += self.angle_speed

        # Falling with slight vertical wobble
        self.y += self.base_speed + math.sin(self.angle * 2) * 0.5

        # Rotate leaf
        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.image_orig, self.rotation)
        self.rect = self.image.get_rect(center=(int(self.x + self.rect.width // 2),
                                                int(self.y + self.rect.height // 2)))

def run_minigame(screen, clock):
    WIDTH, HEIGHT = screen.get_size()

    # Load leaf PNG (transparent background)
    leaf_image = pygame.image.load("../Assets/Leaves.png").convert_alpha()
    leaf_image = pygame.transform.scale(leaf_image, (50, 50))

    cup_width, cup_height = 100, 20
    cup_y = HEIGHT - 50
    leaves = []

    leaf_spawn_timer = 0
    score = 0
    font = pygame.font.Font(None, 36)

    start_time = time.time()
    game_duration = 20  # seconds

    running = True
    while running:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, int(game_duration - elapsed_time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if elapsed_time >= game_duration:
            # Time's up
            leaves.clear()
            running = False
            break

        # Logic
        mouse_x, _ = pygame.mouse.get_pos()
        cup_rect = pygame.Rect(mouse_x - cup_width // 2, cup_y, cup_width, cup_height)

        # Spawn new leaves
        leaf_spawn_timer += 1
        if leaf_spawn_timer > 30:
            x = random.randint(0, WIDTH - leaf_image.get_width())
            leaves.append(Leaf(x, 0, leaf_image))
            leaf_spawn_timer = 0

        # Update and check collisions
        for leaf in leaves[:]:
            leaf.update()
            if leaf.rect.colliderect(cup_rect):
                leaves.remove(leaf)
                score += 1
            elif leaf.rect.y > HEIGHT:
                leaves.remove(leaf)

        # Draw
        screen.fill((200, 255, 200))
        pygame.draw.rect(screen, (150, 75, 0), cup_rect)
        for leaf in leaves:
            screen.blit(leaf.image, leaf.rect.topleft)

        # Draw score and timer
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        timer_text = font.render(f"Time: {remaining_time}s", True, (0, 0, 0))
        screen.blit(timer_text, (WIDTH - 150, 10))

        exit_text = font.render("Press ESC to return", True, (0, 0, 0))
        screen.blit(exit_text, (WIDTH // 2 - 120, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)

    # Show final score summary for 3 seconds
    screen.fill((200, 255, 200))
    summary_text = font.render(f"Time's up! Final Score: {score}", True, (0, 0, 0))
    screen.blit(summary_text, (WIDTH // 2 - summary_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

    return score
