import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set clock for controlling the frame rate
clock = pygame.time.Clock()

# Set font for displaying text
font = pygame.font.Font(None, 36)

# Define snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.radius = 10
        self.dx = 10
        self.dy = 0
        self.score = 0

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, WHITE, element, self.radius)

    def move(self):
        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy

    def add_element(self):
        self.elements.append([0, 0])
        self.size += 1

    def increase_score(self):
        self.score += 10

# Define food class
class Food:
    def __init__(self):
        self.position = [random.randrange(1, (SCREEN_WIDTH - 20) // 10) * 10,
                         random.randrange(1, (SCREEN_HEIGHT - 20) // 10) * 10]
        self.radius = 10

    def draw(self):
        pygame.draw.circle(screen, RED, self.position, self.radius)

# Define game over function
def game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 18))
    pygame.display.flip()
    pygame.time.wait(2000)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Create snake and food objects
snake = Snake()
food = Food()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx == 0:
                snake.dx = 10
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx == 0:
                snake.dx = -10
                snake.dy = 0
            elif event.key == pygame.K_UP and snake.dy == 0:
                snake.dy = -10
                snake.dx = 0
            elif event.key == pygame.K_DOWN and snake.dy == 0:
                snake.dy = 10
                snake.dx = 0

    # Check for collisions with food
    if (food.position[0] - snake.radius < snake.elements[0][0] < food.position[0] + snake.radius) and \
            (food.position[1] - snake.radius < snake.elements[0][1] < food.position[1] + snake.radius):
        snake.add_element()
        food.position = [random.randrange(1, (SCREEN_WIDTH - 20) // 10) * 10,
                         random.randrange(1, (SCREEN_HEIGHT - 20) // 10) * 10]
        snake.increase_score()

    # Check for collisions with the window borders
    if (not 0 < snake.elements[0][0] < SCREEN_WIDTH) or (not 0 < snake.elements[0][1] < SCREEN_HEIGHT):
        running = False

    # Check for collisions with itself
    for block in snake.elements[1:]:
        if (block[0] == snake.elements[0][0]) and (block[1] == snake.elements[0][1]):
            running = False

    # Move snake
    snake.move()

    # Clear the screen
    screen.fill(BLACK)

    # Draw snake and food
    snake.draw()
    food.draw()

    # Draw score
    score_text = font.render("Score: " + str(snake.score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Refresh the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(15)

# Display game over screen
game_over()

# Quit Pygame
pygame.quit()
