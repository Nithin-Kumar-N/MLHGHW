import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE
LINE_COLOR = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.Font(None, 60)

# Define game states
PLAYER_VS_PLAYER = 1
PLAYER_VS_AI = 2
AI_VS_AI = 3

# Function to draw the grid
def draw_grid():
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

# Function to draw X or O
def draw_mark(row, col, player):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 3
    if player == 1:
        pygame.draw.circle(screen, RED, (x, y), radius, 2)
    else:
        pygame.draw.line(screen, BLUE, (x - radius, y - radius), (x + radius, y + radius), 2)
        pygame.draw.line(screen, BLUE, (x + radius, y - radius), (x - radius, y + radius), 2)

# Function to check win condition
def check_win(board, row, col, player):
    # Check row
    if all([cell == player for cell in board[row]]):
        return True
    # Check column
    if all([board[i][col] == player for i in range(BOARD_SIZE)]):
        return True
    # Check diagonal
    if row == col and all([board[i][i] == player for i in range(BOARD_SIZE)]):
        return True
    # Check anti-diagonal
    if row + col == BOARD_SIZE - 1 and all([board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)]):
        return True
    return False

# Function to initialize game
def initialize_game():
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Function to draw the game
def draw_game(board):
    screen.fill(WHITE)
    draw_grid()
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != 0:
                draw_mark(row, col, board[row][col])
    pygame.display.update()

# Function to check if the board is full
def is_board_full(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return False
    return True

# Function for AI move
def ai_move(board, player):
    empty_cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if board[row][col] == 0]
    row, col = random.choice(empty_cells)
    board[row][col] = player
    return row, col

# Function to display game over message
def display_game_over(message):
    text = FONT.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    game_mode = PLAYER_VS_PLAYER
    board = initialize_game()
    player = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and game_mode == PLAYER_VS_PLAYER:
                x, y = pygame.mouse.get_pos()
                row = y // CELL_SIZE
                col = x // CELL_SIZE
                if board[row][col] == 0:
                    board[row][col] = player
                    draw_game(board)
                    if check_win(board, row, col, player):
                        display_game_over(f"Player {player} wins!")
                        running = False
                        break
                    if is_board_full(board):
                        display_game_over("It's a tie!")
                        running = False
                        break
                    player = 3 - player  # Switch player
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = PLAYER_VS_PLAYER
                    board = initialize_game()
                    player = 1
                    running = True
                elif event.key == pygame.K_2:
                    game_mode = PLAYER_VS_AI
                    board = initialize_game()
                    player = 1
                    running = True
                elif event.key == pygame.K_3:
                    game_mode = AI_VS_AI
                    board = initialize_game()
                    player = 1
                    running = True

            # AI move in Player vs AI and AI vs AI modes
            if game_mode != PLAYER_VS_PLAYER and player == 2 and running:
                row, col = ai_move(board, player)
                draw_game(board)
                if check_win(board, row, col, player):
                    display_game_over("AI wins!")
                    running = False
                    break
                if is_board_full(board):
                    display_game_over("It's a tie!")
                    running = False
                    break
                player = 3 - player  # Switch player

    pygame.quit()

if __name__ == "__main__":
    main()
