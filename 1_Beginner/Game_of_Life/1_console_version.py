import os, random, time

# Get the terminal size and set it to ROWS and COLS
terminal_size = os.get_terminal_size()
ROWS, COLS = terminal_size.lines, terminal_size.columns

neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, 1),(1, 1), (1, 0), (1, -1), (0, -1)]

# Randomize the grid
grid = [[random.randint(0, 1) for _ in range(COLS)] for _ in range(ROWS)]

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

def print_grid(grid):
    # Put all the lines together into 1 line by using \n so we can print everything at once
    lines = []
    for row in grid:
        line = ""
        for cell in row:
            if cell:
                line += "@"
            else:
                line += " "
        lines.append(line)
    print("\n".join(lines))

while True:
    grid = update_grid(grid)
    
    # Moves the cursor to the top left side of the console and allows you to print the new frame over the old one
    # This better than cleaning the console first because it causes flashing
    print("\033[H", end="")

    print_grid(grid)
    
    # Sleep some amount
    time.sleep(0.05)
