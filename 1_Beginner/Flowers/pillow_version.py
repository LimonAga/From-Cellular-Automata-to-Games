import random, time
from PIL import Image, ImageDraw
import colorsys

WIDTH, HEIGHT = 1920, 1080
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

saturation = 0.5
lightness = 0.8

starting_flower_count = 2
neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

def hsl_to_rgb(h, l, s):
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
    # Create an empty grid
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # Place flowers with random hue values at random positions
    for _ in range(starting_flower_count):
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        hue = random.uniform(0, 1)
        grid[row][col] = hue
    return grid

def update_grid(grid):
    run = True
    while run:
        new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        # Set the run flag to False. If there are no empty spaces, the loop will end.
        run = False
        for row in range(ROWS):
            for col in range(COLS):
                if grid[row][col]:
                    # Copy the hue to the new grid
                    new_grid[row][col] = grid[row][col]
                    empty_neighbors = get_empty_neighbors(row, col, grid)

                    if empty_neighbors:
                        # If there are still empty neighbors, keep looping
                        run = True
                        target_row, target_col = random.choice(empty_neighbors)
                        # Get the current hue and add a small variation
                        new_hue = grid[row][col] + random.uniform(-0.01, 0.01)
                        new_grid[target_row][target_col] = new_hue
        grid = new_grid
    return grid

def create_image(grid):
    # Create an empty image
    img = Image.new('RGB', (WIDTH, HEIGHT), color='black')
    
    # Create a drawing object
    img_draw = ImageDraw.Draw(img)
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]:
                hue = grid[row][col]
                color = hsl_to_rgb(hue, saturation, lightness)
                rect = [col * CELL_SIZE, row * CELL_SIZE, (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE]
                img_draw.rectangle(rect, color)

    current_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    img.save(f'{current_time}.png')

start_time = time.time()
grid = create_grid()
print("Updating grid...")
grid = update_grid(grid)
print("Creating image...")
create_image(grid)
print("Image created in:", round(time.time() - start_time, 4), "seconds")
