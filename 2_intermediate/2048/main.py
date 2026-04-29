import sys
import random
import pygame

pygame.init()

#! Constants
WIDTH, HEIGHT = 405, 405
FPS = 30
ANIMATION_FPS = 120
ROWS, COLS = 4, 4
CELL_SIZE = 100

possible_moves = ['left', 'right', 'up', 'down']
game_state = 'playing'

font = pygame.font.Font(None, 60)

colors = {
    0: '#E3E3E3',    # Light Gray
    2: '#EEE4DA',    # Light beige
    4: '#EDE0C8',    # Beige
    8: '#F2B179',    # Light orange
    16: '#F59563',   # Orange
    32: '#F67C5F',   # Dark orange
    64: '#F65E3B',   # Red-orange
    128: '#EDCF72',  # Light yellow
    256: '#EDCC61',  # Yellow
    512: '#EDC850',  # Dark yellow
    1024: '#EDC53F', # Yellow-brown
    2048: '#EDC22E'  # Dark brown
}

def place_random_numbers(amount, board):
    empty_spaces = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 0:
                empty_spaces.append((row, col))

    random.shuffle(empty_spaces)
    for i in range(min(amount, len(empty_spaces))):
        row, col = empty_spaces[i]
        board[row][col] = 2 if random.randint(0, 9) else 4

    return board

def transpose(board):
    # Swap the rows and columns
    return [list(row) for row in zip(*board)]

# Instead of making 4 separate move functions, make 1 and re-use it by transforming grid and transform it back after
def move_left(board):
    # Create a copy of the grid so the original grid isn't effected while checking for avaible moves
    board2 = [row[:] for row in board]

    for row_i in range(ROWS):
        new_row = [i for i in board2[row_i] if i != 0] # Remove zeros to shift everyting to the left
        for i in range(len(new_row) - 1):  # Merge tiles
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0

        new_row = [i for i in new_row if i != 0]  # Remove zeros again
        for i in range(COLS - len(new_row)): # Fill the remaing space with zeros
            new_row.append(0)
        board2[row_i] = new_row

    return board2

def move_right(board):
    # Reverse the grid and move left
    board2 = [row[::-1] for row in board]
    board2 = move_left(board2)

    return [row[::-1] for row in board2]

def move_up(board):
    board2 = transpose(board)
    board2 = move_left(board2)

    return transpose(board2)

def move_down(board):
    board2 = transpose(board)
    board2 = move_right(board2)

    return transpose(board2)

def check_moves(board):
    # Create a temporary grid and make the move, then check if the grid has changed
    possible_moves = []

    left_grid = move_left(board)
    if board != left_grid:
        possible_moves.append('left')

    right_grid = move_right(board)
    if board != right_grid:
        possible_moves.append('right')

    up_grid = move_up(board)
    if board != up_grid:
        possible_moves.append('up')

    down_grid = move_down(board)
    if board != down_grid:
        possible_moves.append('down')

    return possible_moves

def check_win(board):
    global possible_moves
    possible_moves = ['left', 'right', 'up', 'down']
    # Check for win
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 2048:
                return 'win'

    # Check if there is empty spaces left
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 0:
                return 'playing'

    possible_moves = check_moves(board)

    if possible_moves:
        return 'playing'

    return 'lose'

def animate(direction, old_surf, new_surf):
    offsets = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
    dx, dy = offsets[direction]
    
    total_frames = 10
    max_dist = 40
    
    for i in range(1, total_frames + 1):
        # Normalised time (0.0 to 1.0)
        t = i / total_frames
        
        # Easing function
        easing = 1 - (1 - t) ** 3
        
        # Calculate current alpha and distance based on easing
        alpha = 255 * (1 - easing)
        current_dist = max_dist * easing
        
        # Draw the new surface (fading in and sliding from offset to zero)
        # It starts at max_dist and ends at 0
        new_surf.set_alpha(255 - alpha)
        incoming_offset = max_dist * (1 - easing)
        screen.blit(new_surf, (dx * -incoming_offset, dy * -incoming_offset))
        
        # Draw the old surface (fading out and sliding away)
        old_surf.set_alpha(alpha)
        screen.blit(old_surf, (dx * current_dist, dy * current_dist))
        
        pygame.display.flip()
        clock.tick(ANIMATION_FPS)

def draw(board, direction):
    # Copy the old frame
    old_surface = screen.copy()
    # Draw the new frame on a temporary surface
    new_surface = pygame.Surface((WIDTH, HEIGHT))
    new_surface.fill('white')

    for row in range(ROWS):
        for col in range(COLS):
      
            x_pos, y_pos = col * CELL_SIZE + 5, row * CELL_SIZE + 5
            pygame.draw.rect(new_surface, colors[board[row][col]],[x_pos, y_pos, CELL_SIZE -5 , CELL_SIZE-5], border_radius=5)

            if board[row][col]:
                text = str(board[row][col])
                if board[row][col] < 32:
                    font_color = '#716F63'
                else:
                    font_color = 'white'

                # Generate the text surface and center it to the cell
                text_surf = font.render(text, True, font_color)
                text_rect = text_surf.get_rect()
                text_rect.center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)

                # Blit the text surface onto the display surface
                new_surface.blit(text_surf, text_rect)

    # Transition between the old and the new frame
    animate(direction, old_surface, new_surface)

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
board = place_random_numbers(2, board)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
clock = pygame.time.Clock()

draw(board, 'up')
run = True
while run:
    #! Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if game_state == 'playing':
                if event.key == pygame.K_LEFT:
                    if 'left' in possible_moves:
                        board = move_left(board)
                        board = place_random_numbers(1, board)

                        draw(board, 'left')
                        possible_moves = check_moves(board)

                elif event.key == pygame.K_RIGHT:
                    if 'right' in possible_moves:
                        board = move_right(board)
                        board = place_random_numbers(1, board)

                        draw(board, 'right')
                        possible_moves = check_moves(board)

                elif event.key == pygame.K_UP:
                    if 'up' in possible_moves:
                        board = move_up(board)
                        board = place_random_numbers(1, board)

                        draw(board, 'up')
                        possible_moves = check_moves(board)

                elif event.key == pygame.K_DOWN:
                    if 'down' in possible_moves:
                        board = move_down(board)
                        board = place_random_numbers(1, board)

                        draw(board, 'down')
                        possible_moves = check_moves(board)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
