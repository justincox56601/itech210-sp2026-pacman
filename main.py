import pygame
import random


pygame.init()
WIDTH = 600
HEIGHT = 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ITECH 210 PACMAN")
clock = pygame.time.Clock()

#background music
pygame.mixer.music.load("bg_music.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

font = pygame.font.SysFont("arial", 30)
message_font = pygame.font.SysFont("arial", 60)

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

LEFT = [-1, 0]
RIGHT = [1, 0]
UP = [0, -1]
DOWN = [0, 1]
ZERO = [0, 0]

MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

TILE_SIZE = 30
ROWS = len(MAP)
COLS = len(MAP[0])

player_x = 1
player_y = 1
player_dir = ZERO
next_dir = ZERO
score = 0
win = False
gameover = False

ghosts = [[18,1],[18,11], [1,11]]
ghost_dirs = [DOWN, UP, RIGHT]

def can_move(position):
    if position[0] < 0:
        return False
    if position[0] >= len(MAP[0]):
        return False
    if position[1] < 0:
        return False
    if position[1] >= len(MAP):
        return False

    if MAP[position[1]][position[0]] == 1:
        return False

    return True

def quit_game():
    global running
    running = False

def move_player(event):
    global next_dir
    if event.key == pygame.K_UP:
        next_dir = UP
    if event.key == pygame.K_DOWN:
        next_dir = DOWN
    if event.key == pygame.K_LEFT:
        next_dir = LEFT
    if event.key == pygame.K_RIGHT:
        next_dir = RIGHT

def draw_border(screen, x, y):
    pygame.draw.rect(screen, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_pellet(screen, x, y):
    pygame.draw.circle(screen, WHITE, (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), 4)

def draw_ghost(screen, x, y):
    pygame.draw.circle(screen, RED, (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), 12)

#main loop
running = True
while running:
    
    #check for pygame events

    
    #check for end of game
    if win or gameover:
        continue
    
    #update player position
    temp_x = player_x + next_dir[0]
    temp_y = player_y + next_dir[1]
    if can_move([temp_x, temp_y]):
        player_x += next_dir[0]
        player_y += next_dir[1]
        next_dir = [0,0]


    #update ghost position
    for i, ghost in enumerate(ghosts):
        if random.random() < 0.10:
            #randomly changes direction
            dirs = [LEFT, RIGHT, UP, DOWN]
            random.shuffle(dirs)
            ghost_dirs[i] = dirs[0] 
        
        temp_x = ghost[0] + ghost_dirs[i][0]
        temp_y = ghost[1] + ghost_dirs[i][1]
        if can_move([temp_x, temp_y]):
            ghost[0] += ghost_dirs[i][0]
            ghost[1] += ghost_dirs[i][1]
        else:
            dirs = [LEFT, RIGHT, UP, DOWN]
            random.shuffle(dirs)
            ghost_dirs[i] = dirs[0] 

    #check ghosts collisions
    

    #check for pellet
    if MAP[player_y][player_x] == 0:
        MAP[player_y][player_x] = 2
        score += 10
    
    count = sum(row.count(0) for row in MAP)
    if count == 0:
        win = True

    

    #draw to screen
    screen.fill(BLACK)

    #draw map
    #draw map border
    #draw map pellet

    #draw pacman
    pygame.draw.circle(screen, YELLOW, (player_x*TILE_SIZE + TILE_SIZE//2, player_y*TILE_SIZE + TILE_SIZE//2), 12)

    #draw ghosts
        
    #draw score
    score_font = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_font.get_rect(bottomleft=(10, HEIGHT-10))
    screen.blit(score_font, score_rect)

    if win:
        message_text = message_font.render("YOU WIN!!!", True, WHITE)
        message_rect = message_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(message_text, message_rect)
    if gameover:
        message_text = message_font.render("GAME OVER", True, WHITE)
        message_rect = message_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(message_text, message_rect)

    pygame.display.flip()
    dt = clock.tick(8) #8 frames per second

pygame.quit()