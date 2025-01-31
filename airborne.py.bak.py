import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airborne - Python Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Game Variables
score = 0
gun_mode = 'air'  # 'air' for gun, 'ground' for mortar
shots_fired = 0
mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2
bullets = []
fire_delay = 500  # 0.5 second delay between shots
turret_x, turret_y = 50, HEIGHT - 30  # Bottom-left position
last_shot_time = 0

def draw_text(text, color, x, y):
    font = pygame.font.SysFont(None, 36)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Load turret image
turret_img = pygame.Surface((20, 20))
turret_img.fill(BLACK)

def draw_turret():
    screen.blit(turret_img, (turret_x, turret_y))
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 10), (WIDTH, HEIGHT - 10), 3)  # Ground line

# Draw stick figure
def draw_stick_figure(x, y):
    pygame.draw.circle(screen, BLACK, (x, y - 5), 3)  # Head
    pygame.draw.line(screen, BLACK, (x, y - 2), (x, y + 5), 2)  # Body
    pygame.draw.line(screen, BLACK, (x - 3, y + 10), (x, y + 5), 2)  # Left Leg
    pygame.draw.line(screen, BLACK, (x + 3, y + 10), (x, y + 5), 2)  # Right Leg
    pygame.draw.line(screen, BLACK, (x - 3, y + 2), (x + 3, y + 2), 2)  # Arms

def fire_bullet():
    global shots_fired, score, last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= fire_delay:
        shots_fired += 1
        score -= 1  # Each shot costs 1 point
        dx, dy = mouse_x - turret_x, mouse_y - turret_y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            vx, vy = (dx / distance) * 10, (dy / distance) * 10
            if gun_mode == 'air':
                bullets.append({'x': turret_x, 'y': turret_y, 'vx': vx, 'vy': vy, 'type': 'air'})
            else:
                bullets.append({'x': turret_x, 'y': turret_y, 'vx': vx / 2, 'vy': -15, 'type': 'mortar'})
        last_shot_time = current_time

def update_bullets():
    for bullet in bullets[:]:
        bullet['x'] += bullet['vx']
        bullet['y'] += bullet['vy']
        if bullet['type'] == 'mortar':
            bullet['vy'] += 1  # Simulate gravity
        if bullet['y'] < 0 or bullet['x'] < 0 or bullet['x'] > WIDTH or bullet['y'] > HEIGHT:
            bullets.remove(bullet)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet['x'], bullet['y'], 4, 4))

def draw_helicopter(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, 40, 15))  # Helicopter body
    pygame.draw.line(screen, BLUE, (x + 10, y), (x + 30, y - 5), 2)  # Rotor blades
    pygame.draw.rect(screen, BLUE, (x + 5, y + 5, 30, 5))  # Tail

# Game Loop
def main():
    global score, gun_mode, shots_fired, mouse_x, mouse_y
    clock = pygame.time.Clock()
    running = True
    mouse_held = False

    while running:
        screen.fill(WHITE)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gun_mode = 'ground' if gun_mode == 'air' else 'air'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to shoot
                    mouse_held = True
                    fire_bullet()
                if event.button == 3:  # Right click to switch gun mode
                    gun_mode = 'ground' if gun_mode == 'air' else 'air'
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_held = False

        if mouse_held:
            fire_bullet()

        update_bullets()

        # Display Score and Gun Mode
        draw_text(f'Score: {score}', BLACK, 10, 10)
        draw_text(f'Gun Mode: {gun_mode.upper()}', BLACK, 10, 50)
        draw_text(f'Shots Fired: {shots_fired}', BLACK, 10, 90)

        # Draw elements
        draw_turret()
        draw_stick_figure(WIDTH // 4, HEIGHT - 20)
        draw_bullets()
        draw_helicopter(WIDTH // 2, HEIGHT // 4)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
