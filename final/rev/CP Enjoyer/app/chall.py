import pygame
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys
import os

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

folder_path = os.path.join(base_path, 'assets')
pygame.init()

WIDTH, HEIGHT = 700, 600
INFO_WIDTH = 100
GAME_WIDTH = WIDTH - INFO_WIDTH
INITIAL_HEALTH = 128
SECRET = open(os.path.join(folder_path, "secret.txt"), "r").read().strip()

pygame_icon = pygame.image.load(os.path.join(folder_path, "cp.png"))
pygame.display.set_icon(pygame_icon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game CP")

font = pygame.font.SysFont('Calibri', 18)
CURR_LEVEL = 1

def initialize_game():
    global player_pos, health, visited_cells, visited_paths, path_costs, start_cell_visited, history, ROWS, COLS, CELL_SIZE, CIRCLE_RADIUS
    if CURR_LEVEL == 1:
        random.seed(0x2024)
        history = []
    else:
        history.append(health)
    
    ROWS, COLS = 4, 4
    CELL_SIZE = GAME_WIDTH // COLS
    CIRCLE_RADIUS = CELL_SIZE // 4
  
    player_pos = [0, 0]
    health = INITIAL_HEALTH
    visited_cells = set()
    visited_cells.add(tuple(player_pos))
    visited_paths = set()
    start_cell_visited = False
  
    path_costs = {}
    for row in range(ROWS):
        for col in range(COLS):
            if col < COLS - 1:
                path_costs[((row, col), (row, col + 1))] = random.randint(1, 10)
                path_costs[((row, col + 1), (row, col))] = path_costs[((row, col), (row, col + 1))]
            if row < ROWS - 1:
                path_costs[((row, col), (row + 1, col))] = random.randint(1, 10)
                path_costs[((row + 1, col), (row, col))] = path_costs[((row, col), (row + 1, col))]

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2

            if (row, col) == (0, 0) and start_cell_visited and len(visited_cells) < ROWS * COLS - 1:
                color = RED
            elif (row, col) in visited_cells:
                color = BLUE
            else:
                color = WHITE
             
            if col < COLS - 1:
                next_x = (col + 1) * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(screen, GRAY, (INFO_WIDTH + x, y), (INFO_WIDTH + next_x, y), 20)
                cost_text = font.render(str(path_costs[((row, col), (row, col + 1))]), True, WHITE)
                screen.blit(cost_text, ((INFO_WIDTH + x + 2*CIRCLE_RADIUS), y - cost_text.get_height() // 2))

            if row < ROWS - 1:
                next_y = (row + 1) * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(screen, GRAY, (INFO_WIDTH + x, y + CIRCLE_RADIUS), (INFO_WIDTH + x, next_y - CIRCLE_RADIUS), 20)
                cost_text = font.render(str(path_costs[((row, col), (row + 1, col))]), True, WHITE)
                screen.blit(cost_text, (INFO_WIDTH + x - cost_text.get_width() // 2, (y + next_y) // 2 - cost_text.get_height() // 2))
            
            pygame.draw.circle(screen, color, (INFO_WIDTH + x, y), CIRCLE_RADIUS, 0)
            pygame.draw.circle(screen, BLACK, (INFO_WIDTH + x, y), CIRCLE_RADIUS, 2)

def draw_player():
    x, y = player_pos[1] * CELL_SIZE + CELL_SIZE // 2, player_pos[0] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, GREEN, (INFO_WIDTH + x, y), CIRCLE_RADIUS, 0)

def draw_health():
    health_text = font.render(f"Health: {health}", True, WHITE)
    screen.blit(health_text, (20, 45))

def draw_level():
    level_text = font.render(f"Level: {CURR_LEVEL}", True, WHITE)
    screen.blit(level_text, (20, 65))

def move_player(direction):
    global health, start_cell_visited
    row, col = player_pos
    next_pos = list(player_pos)

    if direction == "UP" and row > 0:
        next_pos[0] -= 1
    elif direction == "DOWN" and row < ROWS - 1:
        next_pos[0] += 1
    elif direction == "LEFT" and col > 0:
        next_pos[1] -= 1
    elif direction == "RIGHT" and col < COLS - 1:
        next_pos[1] += 1

    if tuple(next_pos) not in visited_cells:
        if tuple(next_pos) != tuple(player_pos):
            path = (tuple(player_pos), tuple(next_pos))
            health = max(health - path_costs[path], 0)
            visited_paths.add(path)
            player_pos[:] = next_pos
            visited_cells.add(tuple(player_pos))
            
            if not start_cell_visited and tuple(player_pos) != (0, 0):
                start_cell_visited = True

def get_flag():
    keys = [bytes(((b1 + b2) for b1, b2 in zip(history[x:x+32], history[x+32:x+64]))) for x in range(len(history)//64)]

    enc_data = bytes.fromhex(SECRET)
    plaintext = ""
    for key in keys:
        decipher = AES.new(key, AES.MODE_ECB)
        plaintext = unpad(decipher.decrypt(enc_data), AES.block_size)
        enc_data = plaintext
    
    m = hashlib.sha256()
    m.update(plaintext.encode())

    if m.hexdigest() == "aa2a9def8edd8d23244fd5a9745159a67985025c54024f9a9b7f34b5f31a22a7":
        return plaintext
    return "Now What?"

def check_goal():
    if len(visited_cells) == ROWS * COLS - 1:
      
        if (0, 0) in visited_cells:
            visited_cells.remove((0, 0))
    return len(visited_cells) == ROWS * COLS

def end_screen():
    if health <= 0 or isStuck():
        msg1 = "Game Over"
        msg2 = "Press \"Enter\" to Restart!"
        color = RED
    else:
        msg1 = "Congratulation!"
        msg2 = get_flag()
        color = GREEN

    font = pygame.font.Font(None, 36)
    end_text = font.render(msg1, True, color, WHITE)
    screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
    
    font = pygame.font.Font(None, 25)
    end_text = font.render(msg2, True, color, WHITE)
    screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 + end_text.get_height()))
    pygame.display.flip()
    font = pygame.font.Font(None, 15)
  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def isStuck():
    if len(visited_cells) == ROWS * COLS:
        return False
    x = player_pos[0]
    y = player_pos[1]
    if x > 0 and (x-1, y) not in visited_cells:
        return False
    if x < ROWS-1 and (x+1, y) not in visited_cells:
        return False
    if y > 0 and (x, y-1) not in visited_cells:
        return False
    if y < COLS-1 and (x, y+1) not in visited_cells:
        return False
    return True

if __name__ == "__main__":
    initialize_game()
    running = True
    while running:
        screen.fill(BLACK)
    
        draw_grid()
        draw_player()
        draw_health()
        draw_level()
    
        if health == 0 or isStuck():
            end_screen()
            CURR_LEVEL = 1
            initialize_game()
        elif check_goal() and CURR_LEVEL % 0x3200:
            CURR_LEVEL += 1
            initialize_game()
        elif check_goal():
            end_screen()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player("UP")
                elif event.key == pygame.K_DOWN:
                    move_player("DOWN")
                elif event.key == pygame.K_LEFT:
                    move_player("LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_player("RIGHT")
        pygame.display.flip()
    pygame.quit()