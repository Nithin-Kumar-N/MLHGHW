import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = 600
GRID_SIZE = 4
GRID_SPACING = 10
CELL_SIZE = (SCREEN_SIZE - (GRID_SPACING * (GRID_SIZE + 1))) // GRID_SIZE
FONT_SIZE = 40
FONT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Create the screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048')

# Initialize the grid
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Add initial tiles
def add_initial_tiles():
    for _ in range(2):
        add_tile()

# Add a new tile (either 2 or 4) to a random empty cell
def add_tile():
    empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[x][y] = 2 if random.random() < 0.9 else 4

# Check if the game is over
def is_game_over():
    return not any(0 in row for row in grid) and not any(grid[x][y] == grid[x + 1][y] or grid[x][y] == grid[x][y + 1] for x in range(GRID_SIZE - 1) for y in range(GRID_SIZE - 1))

# Draw the grid
def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pygame.draw.rect(screen, CELL_COLORS[grid[x][y]], (GRID_SPACING + y * (CELL_SIZE + GRID_SPACING), GRID_SPACING + x * (CELL_SIZE + GRID_SPACING), CELL_SIZE, CELL_SIZE))
            if grid[x][y] != 0:
                font = pygame.font.SysFont(None, FONT_SIZE)
                text = font.render(str(grid[x][y]), True, FONT_COLOR)
                text_rect = text.get_rect(center=(GRID_SPACING + y * (CELL_SIZE + GRID_SPACING) + CELL_SIZE / 2, GRID_SPACING + x * (CELL_SIZE + GRID_SPACING) + CELL_SIZE / 2))
                screen.blit(text, text_rect)

# Shift the grid in a specified direction (left, right, up, or down)
def shift_grid(direction):
    global grid
    if direction == 'left':
        grid = [merge(row) for row in grid]
    elif direction == 'right':
        grid = [merge(row[::-1])[::-1] for row in grid]
    elif direction == 'up':
        grid = [merge([grid[x][y] for x in range(GRID_SIZE)]) for y in range(GRID_SIZE)]
    elif direction == 'down':
        grid = [merge([grid[x][y] for x in range(GRID_SIZE)][::-1])[::-1] for y in range(GRID_SIZE)]

# Merge adjacent cells with the same value
def merge(row):
    new_row = [cell for cell in row if cell != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [cell for cell in new_row if cell != 0]
    return new_row + [0] * (len(row) - len(new_row))

# Main game loop
add_initial_tiles()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shift_grid('left')
                add_tile()
            elif event.key == pygame.K_RIGHT:
                shift_grid('right')
                add_tile()
            elif event.key == pygame.K_UP:
                shift_grid('up')
                add_tile()
            elif event.key == pygame.K_DOWN:
                shift_grid('down')
                add_tile()
    draw_grid()
    pygame.display.flip()

# Quit Pygame
pygame.quit()
