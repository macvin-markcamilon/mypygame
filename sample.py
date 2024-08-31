import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0

# Load images
bird_surface = pygame.image.load('flappy_bird.png').convert_alpha()
bird_rect = bird_surface.get_rect(center=(50, HEIGHT//2))

bg_surface = pygame.image.load('background.png').convert()
floor_surface = pygame.image.load('floor.png').convert()
floor_x_pos = 0

pipe_surface = pygame.image.load('pipe.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

font = pygame.font.Font('freesansbold.ttf', 32)

# Functions
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, HEIGHT - 100))
    screen.blit(floor_surface, (floor_x_pos + WIDTH, HEIGHT - 100))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(WIDTH + 100, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(WIDTH + 100, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= HEIGHT - 100:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def score_display():
    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
    screen.blit(score_surface, score_rect)

def update_score(pipes):
    global score
    for pipe in pipes:
        if pipe.centerx == 50:
            score += 1
            break

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, HEIGHT//2)
                bird_movement = 0
                score = 0
        
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game_active = check_collision(pipe_list)
        
        update_score(pipe_list)
        score_display()
    else:
        screen.blit(font.render("Game Over", True, WHITE), (100, HEIGHT//2 - 50))
        screen.blit(font.render(f"Final Score: {score}", True, WHITE), (80, HEIGHT//2 + 10))

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)
