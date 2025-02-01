
import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
GROUND_LEVEL = HEIGHT - 10  # Define ground level
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airborne - Python Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 30)

# Game Variables
score = 0
gun_mode = 'air'  # 'air' for gun, 'ground' for mortar
shots_fired = 0
mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2
bullets = []
fire_delay = 200  # 0.2 second delay
turret_x, turret_y = 50, HEIGHT - 30
last_shot_time = 0
helicopter_frame = 0  # Animation frame for helicopter
helicopters = []
stick_figures = []
explosions = []
fire_held = False

# Load turret image
turret_img = pygame.Surface((20, 20))
turret_img.fill(BLACK)

# Explosion function
def create_explosion(x, y, num_pieces=6):
    for _ in range(num_pieces):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)
        vx, vy = math.cos(angle) * speed, math.sin(angle) * speed
        explosions.append({'x': x, 'y': y, 'vx': vx, 'vy': vy})

def update_explosions():
    for piece in explosions[:]:
        piece['x'] += piece['vx']
        piece['y'] += piece['vy']
        piece['vy'] += 0.2  # Simulate gravity
        if piece['y'] > HEIGHT:
            explosions.remove(piece)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet['x'], bullet['y'], 4, 4))

def draw_explosions():
    for piece in explosions:
        pygame.draw.circle(screen, RED, (int(piece['x']), int(piece['y'])), 3)

def check_bullet_collisions():
    global score
    for bullet in bullets[:]:
        for helicopter in helicopters[:]:
            if helicopter['x'] < bullet['x'] < helicopter['x'] + 40 and helicopter['y'] < bullet['y'] < helicopter['y'] + 20:
                create_explosion(helicopter['x'] + 20, helicopter['y'] + 10)
                helicopters.remove(helicopter)
                bullets.remove(bullet)
                score += 10
                break
        for figure in stick_figures[:]:
            if figure['x'] - 5 < bullet['x'] < figure['x'] + 5 and figure['y'] - 10 < bullet['y'] < figure['y']:
                create_explosion(figure['x'], figure['y'])
                stick_figures.remove(figure)
                bullets.remove(bullet)
                score += 5
                break

def spawn_helicopter():
    y = random.randint(20, HEIGHT - 100)
    helicopters.append({'x': WIDTH + 20, 'y': y, 'figures': 5, 'dropping': False})

def update_helicopters():
    global helicopter_frame
    helicopter_frame += 1
    if helicopter_frame > 10:  # Slows helicopter blade spinning
        helicopter_frame = 0
    for helicopter in helicopters[:]:
        helicopter['x'] -= 1
        if helicopter['figures'] > 0 and random.randint(0, 100) < 2:
            stick_figures.append({'x': helicopter['x'], 'y': helicopter['y'], 'falling': True})
            helicopter['figures'] -= 1
        if helicopter['figures'] == 0:
            helicopter['y'] -= 1
        if helicopter['y'] < 0:
            helicopters.remove(helicopter)

def update_bullets():
    for bullet in bullets[:]:
        bullet['x'] += bullet['vx']
        bullet['y'] += bullet['vy']
        if bullet['type'] == 'mortar':
            bullet['vy'] += 0.5  # Simulate gravity
        if bullet['y'] < 0 or bullet['x'] < 0 or bullet['x'] > WIDTH or bullet['y'] > HEIGHT:
            bullets.remove(bullet)
    check_bullet_collisions()

def fire_bullet():
    global shots_fired, score, last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= fire_delay:
        shots_fired += 1
        score -= 1
        dx, dy = mouse_x - turret_x, mouse_y - turret_y
        
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            if gun_mode == 'air':
                if mouse_y > GROUND_LEVEL - 30:
                    dy = GROUND_LEVEL - 30 - turret_y
                vx, vy = (dx / distance) * 10, (dy / distance) * 10
                bullets.append({'x': turret_x, 'y': turret_y, 'vx': vx, 'vy': vy, 'type': 'air'})
            else:
                angle = math.atan2(mouse_y, mouse_x)
                power = 20
                vx, vy = power * math.cos(angle), -power * math.sin(angle)
                bullets.append({'x': turret_x, 'y': turret_y, 'vx': vx, 'vy': vy, 'type': 'mortar'})
        last_shot_time = current_time

def draw_helicopters():
    for helicopter in helicopters:
        pygame.draw.rect(screen, BLUE, (helicopter['x'], helicopter['y'], 40, 20))

def update_stick_figures():
    for figure in stick_figures:
        if figure['falling']:
            figure['y'] += 2
        if figure['y'] >= GROUND_LEVEL:
            figure['falling'] = False
            figure['y'] = GROUND_LEVEL

def draw_turret():
    screen.blit(turret_img, (turret_x, turret_y))
    pygame.draw.line(screen, BLACK, (0, GROUND_LEVEL), (WIDTH, GROUND_LEVEL), 3)  # Ground line

def draw_hud():
    score_text = font.render(f"Score: {score}", True, BLACK)
    shots_text = font.render(f"Shots Fired: {shots_fired}", True, BLACK)
    mode_text = font.render(f"Mode: {gun_mode.upper()}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(shots_text, (10, 40))
    screen.blit(mode_text, (10, 70))

def draw_stick_figure(x, y):
    pygame.draw.circle(screen, BLACK, (x, y - 5), 3)  # Head
    pygame.draw.line(screen, BLACK, (x, y - 2), (x, y + 5), 2)  # Body
    pygame.draw.line(screen, BLACK, (x - 3, y + 10), (x, y + 5), 2)  # Left Leg
    pygame.draw.line(screen, BLACK, (x + 3, y + 10), (x, y + 5), 2)  # Right Leg
    pygame.draw.line(screen, BLACK, (x - 3, y + 2), (x + 3, y + 2), 2)  # Arms

def draw_stick_figures():
    for figure in stick_figures:
        draw_stick_figure(figure['x'], figure['y'])

def main():
    global score, gun_mode, shots_fired, mouse_x, mouse_y, fire_held
    clock = pygame.time.Clock()
    running = True
    spawn_timer = 0

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    fire_held = True
                elif event.button == 3:
                    gun_mode = 'ground' if gun_mode == 'air' else 'air'
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    fire_held = False
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

        if fire_held:
            fire_bullet()

        if pygame.time.get_ticks() - spawn_timer > 3000:
            spawn_helicopter()
            spawn_timer = pygame.time.get_ticks()

        update_bullets()
        update_helicopters()
        update_explosions()
        update_stick_figures()
        draw_turret()
        draw_bullets()
        draw_hud()
        draw_helicopters()
        draw_stick_figures()
        draw_explosions()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()