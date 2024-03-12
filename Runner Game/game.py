import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 50
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
COIN_SIZE = 30
FPS = 60
GRAVITY = 0.5
JUMP_POWER = -10
PLATFORM_SPEED = 5
COIN_SPEED = 5
COIN_INTERVAL = 60
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('One-Button Runner')

# Load images
player_img = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_img.fill(COLOR_GREEN)
platform_img = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
platform_img.fill(COLOR_BLUE)
coin_img = pygame.Surface((COIN_SIZE, COIN_SIZE))
coin_img.fill(COLOR_WHITE)

# Set up the clock
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity_y = 0

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Keep the player within the screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def jump(self):
        self.velocity_y = JUMP_POWER

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = PLATFORM_SPEED

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = COIN_SPEED

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game loop
running = True
coin_timer = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()

    # Spawn platforms
    if len(platforms) == 0 or platforms.sprites()[-1].rect.right < SCREEN_WIDTH - 300:
        platform_y = random.randint(0, SCREEN_HEIGHT - PLATFORM_HEIGHT)
        platform = Platform(SCREEN_WIDTH, platform_y)
        platforms.add(platform)
        all_sprites.add(platform)

    # Spawn coins
    coin_timer += 1
    if coin_timer == COIN_INTERVAL:
        coin_y = random.randint(0, SCREEN_HEIGHT - COIN_SIZE)
        coin = Coin(SCREEN_WIDTH, coin_y)
        coins.add(coin)
        all_sprites.add(coin)
        coin_timer = 0

    # Update
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollide(player, platforms, False):
        running = False

    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    # You can add scoring mechanism or other actions here

    # Draw
    screen.fill(COLOR_BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
