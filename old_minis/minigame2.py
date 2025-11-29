# minigame2.py
import pygame
import math
import random

def run_minigame2(screen, clock):
    WIDTH, HEIGHT = screen.get_size()
    center = (WIDTH // 2, HEIGHT // 2)
    radius = 150
    rect_size = (20, 40)

    # Game variables
    arc_center = 90  # start at bottom (degrees)
    arc_width = 30   # width of the green arc (degrees)
    rotation_angle = 0
    rotation_speed = 1.0
    speed_increment = 0.05
    direction = 1  # 1 = clockwise, -1 = counterclockwise
    score = 0

    font = pygame.font.Font(None, 50)
    running = True

    while running:
        screen.fill((240, 230, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Calculate where the red marker (12 o'clock) is relative to arc
                    marker_angle = (-rotation_angle) % 360
                    arc_start = (arc_center - arc_width / 2) % 360
                    arc_end = (arc_center + arc_width / 2) % 360

                    # Check if marker is within arc
                    in_arc = (
                        arc_start < marker_angle < arc_end
                        if arc_start < arc_end
                        else marker_angle > arc_start or marker_angle < arc_end
                    )

                    if in_arc:
                        score += 1
                        # Move arc to new random location and reverse direction
                        arc_center = random.randint(0, 359)
                        direction *= -1
                        rotation_speed += speed_increment
                    else:
                        # Missed → reset game or deduct points
                        score = 0
                        rotation_speed = 1.0
                        direction = 1
                        arc_center = random.randint(0, 359)
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Draw circle
        pygame.draw.circle(screen, (0, 0, 0), center, radius, 5)

        # Draw rotating arc
        for angle_deg in range(int(arc_center - arc_width / 2), int(arc_center + arc_width / 2)):
            rotated_angle = (angle_deg + rotation_angle) % 360
            angle_rad = math.radians(rotated_angle)
            x = center[0] + radius * math.sin(angle_rad)
            y = center[1] - radius * math.cos(angle_rad)
            pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), 4)

        # Draw fixed red rectangle at 12 o’clock
        rect_x = center[0]
        rect_y = center[1] - radius
        rect = pygame.Rect(0, 0, *rect_size)
        rect.center = (rect_x, rect_y)
        pygame.draw.rect(screen, (255, 0, 0), rect)

        # Draw score
        score_surface = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        # Update rotation
        rotation_angle += rotation_speed * direction
