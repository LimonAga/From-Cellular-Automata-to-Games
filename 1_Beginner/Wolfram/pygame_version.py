import random
import pygame

pygame.init()
info = pygame.display.Info()

WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 60
CELL_SIZE = 5
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Randomize the first line for variety
line = [random.randint(0, 1) for _ in range(COLS)]

# Get a random number between 0 and 255 and turn it into a list of bits
rule = [int(bit) for bit in bin(random.randint(0, 255))[2:].zfill(8)]

# Generate all the patterns in binary (order must be from 111 to 000)
neighbor_patterns = [bin(i)[2:].zfill(3) for i in reversed(range(8))]

# Put them together into a dictionary
rule_dict = {a: b for (a, b) in zip(neighbor_patterns, rule)}

colors = [
    "#00FFFF",  # Electric Blue
    "#FF0033",  # Vivid Red
    "#32CD32",  # Lime Green
    "#FF69B4",  # Hot Pink
    "#FFFF00",  # Bright Yellow
    "#FFA500",  # Orange
    "#8000FF",  # Purple
    "#FF00FF",  # Magenta
    "#40E0D0",  # Turquoise
    "#7FFF00",  # Chartreuse
    "#DC143C",  # Crimson
    "#00BFFF",  # Sky Blue
]

color0 = 'black'
color1 = random.choice(colors)

def update(line, rule_dict):
    new_line = [0 for _ in range(COLS)]
    for i in range(COLS):
        if i == 0: # Loop the left corner
            left = line[-1]
        else: 
            left = line[i -1]

        middle = line[i]

        if i == COLS -1: # Loop the right corner
            right = line[0]
        else: 
            right = line[i +1]

        # Get the new cell using 
        new_line[i] = rule_dict[f"{left}{middle}{right}"]
    return new_line

def draw(line_index, line):
    # Draw the line using the line_index
    for col in range(COLS):
        if line[col]:
            rect = [col * CELL_SIZE, line_index * CELL_SIZE, CELL_SIZE, CELL_SIZE]
            pygame.draw.rect(screen, color1, rect)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('1D Cellular Automata')
clock = pygame.time.Clock()

screen.fill(color0)

RESET_TIMER = pygame.USEREVENT + 1
resetting = False

line_index = 0
run = True
while run:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == RESET_TIMER:
            # Randomize the line
            line = [random.randint(0, 1) for _ in range(COLS)]
            line_index = 0
            
            # Clear the screen and get a new color
            screen.fill(color0)
            color1 = random.choice(colors)
            
            # Generate the new rule_dict
            rule = [int(bit) for bit in bin(random.randint(0, 255))[2:].zfill(8)]
            rule_dict = {a: b for (a, b) in zip(neighbor_patterns, rule)}

            # Stop the REST_TIMER event
            resetting = False
            pygame.time.set_timer(RESET_TIMER, 0)

    if not resetting:
        if line_index < ROWS:
            draw(line_index, line)
            line = update(line, rule_dict)
            line_index += 1

        # After reaching bottom of the screen, start the reset timer
        else:
            pygame.time.set_timer(RESET_TIMER, 2500)
            resetting = True

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
