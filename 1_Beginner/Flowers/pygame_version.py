import random
import colorsys
import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
CELL_SIZE = 2
FPS = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

saturation = 0.8
lightness = 0.5

starting_flower_count = 2
neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

class Plant:
    def __init__(self):
        self.hue = random.uniform(0, 1)
        self.color = self.hsl_to_rgb(self.hue, lightness, saturation)
        # If the flower is drawn don't draw it again
        self.drawn = False
        # If the flower has no empty neighbors skips it during update
        self.has_empty_neighbors = True

    def clone(self):
        # Spread to a adjacent cell and mutate the color
        mutation = random.uniform(-0.01, 0.01)
        new_hue = min(1, max(0, self.hue + mutation))
        cloned_cell = Plant()
        cloned_cell.hue = new_hue
        cloned_cell.color = cloned_cell.hsl_to_rgb(new_hue, lightness, saturation)
        return cloned_cell

    def hsl_to_rgb(self, h, l, s):
        return tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, l, s))

def get_empty_neighbors(row, col, grid):
    empty_neighbors = []
    for dx, dy in neighbors:
        neighbor_row, neighbor_col = row + dx, col + dy
        # Check if the neighbor is inside the grid
        if 0 <= neighbor_row < ROWS and 0 <= neighbor_col < COLS:
            if not grid[neighbor_row][neighbor_col]:
                empty_neighbors.append((neighbor_row, neighbor_col))
    return empty_neighbors

def create_grid():
    # Create a grid with randomly placed flowers
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for _ in range(starting_flower_count):
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        grid[row][col] = Plant()
    return grid

def update_grid(grid):
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    for row in range(ROWS):
        for col in range(COLS):
            cell = grid[row][col]
            if cell:
                new_grid[row][col] = cell

                if cell.has_empty_neighbors:
                    empty_neighbors = get_empty_neighbors(row, col, grid)

                    if empty_neighbors:
                        # Pick a random neighbor and spread
                        target_row, target_col = random.choice(empty_neighbors)
                        if not new_grid[target_row][target_col]:
                            new_grid[target_row][target_col] = cell.clone()
                    else:
                        # If there are no empty neighbors, stop cheking this cell in the future
                        cell.has_empty_neighbors = False
    return new_grid

def draw(grid):
    for row in range(ROWS):
        # No need to calculate this again every row
        y_pos = row * CELL_SIZE
        for col in range(COLS):
            cell = grid[row][col]
            if cell and not cell.drawn:
                pygame.draw.rect(screen, cell.color, (col * CELL_SIZE, y_pos, CELL_SIZE, CELL_SIZE))
                # Stop drawing this cell in the future
                cell.drawn = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

grid = create_grid()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if not grid[row][col]:
                grid[row][col] = Plant()

    grid = update_grid(grid)
    draw(grid)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
