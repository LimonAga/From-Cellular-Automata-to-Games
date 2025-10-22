import random
import pygame

pygame.init()
info = pygame.display.Info()

FPS = 30
CELL_SIZE = 10
DEAD_COLOR = 'black'
ALIVE_COLOR = 'white'

# Get the ROWS and COLS using the screen size
WIDTH, HEIGHT = info.current_w, info.current_h
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, 1),(1, 1), (1, 0), (1, -1), (0, -1)]

def update_grid(grid):
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    for row in range(ROWS):
        for col in range(COLS):
            # Count alive neighbors
            alive_neighbors = 0
            for dx, dy in neighbors:
                # Divide neighbor coordinates by the grid size so they loop over
                neighbor_row, neighbor_col = (row + dx) % ROWS, (col + dy) % COLS
                if grid[neighbor_row][neighbor_col]:
                    alive_neighbors += 1

            # Rules
            if grid[row][col]:
                # If an alive cell has 2 or 3 alive neighbors it survives, otherwise it dies
                if alive_neighbors in [2, 3]:
                    new_grid[row][col] = 1
            else:
                # If a dead cell has exactly 3 alive neighbors it becomes alive
                if alive_neighbors == 3:
                    new_grid[row][col] = 1

    return new_grid

def draw():
    # Clear the previous image 
    screen.fill(DEAD_COLOR)

    for row in range(ROWS):
        for col in range(COLS):
            # Draw only if the cell is alive beacuse we have already filled rest of the screen with the other color
            if grid[row][col]:
                # Define the size of the rectangle
                rectangle = [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE]
                pygame.draw.rect(screen, ALIVE_COLOR, rectangle)

# Randomize the grid
grid = [[random.randint(0, 1) for _ in range(COLS)] for _ in range(ROWS)]

# Create the window and the timer
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Add a 15 second timer so grid resets on a timer
reset_timer = pygame.USEREVENT + 1
pygame.time.set_timer(reset_timer, 15000)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit when the window is closed
            run = False

        if event.type == reset_timer:
            # Randomize the grid every time reset_timer event triggers
            grid = [[random.randint(0, 1) for _ in range(COLS)] for _ in range(ROWS)]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Quit when esc has been pressed
                run = False

    grid = update_grid(grid)
    draw()

    # Refresh the screen and cap the FPS
    pygame.display.flip()
    clock.tick(FPS)

# When the main loop stops uninitilize pygame
pygame.quit()
