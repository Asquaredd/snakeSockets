import pygame
import random
import threading
import time
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 100
GRID_CELL_SIZE = 10
SCREEN_SIZE = (GRID_SIZE * GRID_CELL_SIZE, GRID_SIZE * GRID_CELL_SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Create the game window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snake Game")

# Initialize font for displaying text
font = pygame.font.Font(None, 36)

# Snake initial position and speed
snake = [(5, 5)]
snake_speed = (1, 0)

# Food initial position
food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

# Control directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initial direction
current_direction = RIGHT

# Function to update coordinates and print to console with color
def update_coordinates(snake):
    while True:
        # Extract the coordinates and size information here
        snake_head_coordinates = snake[0]
        snake_size = len(snake)

        # Format the text with ANSI escape codes for color
        colored_text = f"\r\033[93mCoordinates: {snake_head_coordinates}\033[0m, \033[91mSize: {snake_size}\033[0m"
        sys.stdout.write(colored_text)
        sys.stdout.flush()

        # Sleep for a short interval to control the update rate
        time.sleep(1)

# Create a thread to run the coordinate updater
coordinate_thread = threading.Thread(target=update_coordinates, args=(snake,))
coordinate_thread.daemon = True
coordinate_thread.start()

# Function to display text on the game screen
def display_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                if current_direction != DOWN:  # Avoid reversing direction
                    current_direction = UP
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                if current_direction != UP:
                    current_direction = DOWN
            elif event.key == pygame.K_LEFT or event.key == ord('a'):
                if current_direction != RIGHT:
                    current_direction = LEFT
            elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                if current_direction != LEFT:
                    current_direction = RIGHT

    # Update snake's position
    snake_head = (snake[0][0] + current_direction[0], snake[0][1] + current_direction[1])
    snake.insert(0, snake_head)

    # Check for collisions
    if snake_head == food:
        # Increase snake size and respawn food
        food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    else:
        snake.pop()

    # Clear the screen
    screen.fill(WHITE)

    # Draw grid with black outlines
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK, pygame.Rect(x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))
            pygame.draw.rect(screen, WHITE, pygame.Rect(x * GRID_CELL_SIZE + 1, y * GRID_CELL_SIZE + 1, GRID_CELL_SIZE - 2, GRID_CELL_SIZE - 2))

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * GRID_CELL_SIZE, segment[1] * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

    # Draw food in red
    pygame.draw.rect(screen, RED, pygame.Rect(food[0] * GRID_CELL_SIZE, food[1] * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

    # Display coordinates and size at the top left corner
    display_text(f"Coordinates: {snake[0]}", 10, 10, GOLD)
    display_text(f"Size: {len(snake)}", 10, 50, RED)

    # Update the display
    pygame.display.flip()

    # Control game speed
    pygame.time.delay(100)

# Quit Pygame
pygame.quit()
