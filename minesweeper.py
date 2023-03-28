import pygame
import random

# Set up Pygame
pygame.init()

# Set up game window
screen_width, screen_height = 400, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

# Set up game variables
tile_size = 40
num_cols = screen_width // tile_size
num_rows = screen_height // tile_size
num_mines = 10
board = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
revealed = [[False for _ in range(num_cols)] for _ in range(num_rows)]
game_over = False

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set up fonts
font = pygame.font.SysFont(None, 30)

# Function to count the number of neighboring mines
def count_mines(row, col):
    count = 0
    for r in range(max(0, row - 1), min(num_rows, row + 2)):
        for c in range(max(0, col - 1), min(num_cols, col + 2)):
            if board[r][c] == -1:
                count += 1
    return count

# Function to reveal a tile and recursively reveal neighboring tiles
def reveal_tile(row, col):
    if revealed[row][col]:
        return
    revealed[row][col] = True
    if board[row][col] == -1:
        global game_over
        game_over = True
        return
    elif board[row][col] == 0:
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                reveal_tile(r, c)

# Generate the mines
mine_coords = random.sample([(r, c) for r in range(num_rows) for c in range(num_cols)], num_mines)
for row, col in mine_coords:
    board[row][col] = -1

# Count the number of neighboring mines for each tile
for row in range(num_rows):
    for col in range(num_cols):
        if board[row][col] != -1:
            board[row][col] = count_mines(row, col)

# Main game loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // tile_size
                row = mouse_pos[1] // tile_size
                reveal_tile(row, col)

    # Draw the board
    screen.fill(WHITE)
    for row in range(num_rows):
        for col in range(num_cols):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if revealed[row][col]:
                if board[row][col] == -1:
                    pygame.draw.circle(screen, BLUE, rect.center, tile_size // 3)
                elif board[row][col] > 0:
                    text = font.render(str(board[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

    # Check if the game is over
    if not game_over and all(all(revealed[row][col] or board[row][col] == -1 for col in range(num_cols)) for row in range(num_rows)):
        game_over = True
        text = font.render("You Win!", True, RED)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

    # Update the screen
    pygame.display.update()
