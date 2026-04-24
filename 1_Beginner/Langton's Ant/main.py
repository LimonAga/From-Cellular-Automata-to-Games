import pygame

pygame.init()
info = pygame.display.Info()

FPS = 120
CELL_SIZE = 6

# Get the ROWS and COLS using the screen size
WIDTH, HEIGHT = info.current_w, info.current_h
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Directions are ordered clock-wise. This way we can increase the index to go clockwise or decrese to go anti-clockwise
directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
direction_index = 0

# Create an empty grid and set thr ant pos to middle
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
ant_pos = [ROWS // 2, COLS // 2]

def update(grid, direction_index, ant_pos):

    # If the ant is on a white cell
    if grid[ant_pos[0]][ant_pos[1]] == 1:
        # Change the current cell to black
        grid[ant_pos[0]][ant_pos[1]] = 0
        
        # Turn clockwise
        direction_index += 1
        if direction_index >= len(directions):
            direction_index = 0
    
    # If the ant is on a black cell        
    else:
        # Change the current cell to white
        grid[ant_pos[0]][ant_pos[1]] = 1
        
        # Turn anti-clokwise
        direction_index -= 1
        if direction_index < 0:
            direction_index = len(directions) -1

    # Draw ant's current position
    color = 'white' if grid[ant_pos[0]][ant_pos[1]] else 'black'
    pygame.draw.rect(screen, color, [ant_pos[1] * CELL_SIZE, ant_pos[0] * CELL_SIZE, CELL_SIZE -1, CELL_SIZE -1])
    
    # Move forward. Devide the coordinates by the grid size to loop around the edges
    direction = directions[direction_index]
    ant_pos = (ant_pos[0] + direction[0]) % ROWS, (ant_pos[1] + direction[1]) % COLS
    
    return grid, direction_index, ant_pos
    
# Create the window and the timer
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

screen.fill('black')
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit when the window is closed
            run = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Quit when esc has been pressed
                run = False

    grid, direction_index, ant_pos = update(grid, direction_index, ant_pos)

    # Refresh the screen and cap the FPS
    pygame.display.flip()
    clock.tick(FPS)

# When the main loop stops uninitilize pygame
pygame.quit()