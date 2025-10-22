import os, random, time

# Get terminal size and awt it as ROWS an COLS
size = os.get_terminal_size()
ROWS, COLS = size.lines, size.columns

# Randomize the line. Normally you would start with a 1 in the middle but this has more variation.
line = [random.randint(0, 1) for _ in range(COLS)]

# Get a random number between 0 and 255 and turn it into a list of bits
rule = [int(bit) for bit in format(random.randint(0, 255), '08b')]

# Genarate all the patterns (order must be from 7 to 0) so we reverse the range
neighbor_patterns = [bin(i)[2:].zfill(3) for i in reversed(range(8))]

#  Match patterns with the rule
rule_dict = {a: b for (a, b) in zip(neighbor_patterns, rule)}

def update():
    new_line = [0 for _ in range(COLS)]
    for i in range(COLS):
        # Loop over the left corner
        if i == 0:
            left = line[-1]
        else: 
            left = line[i-1]

        middle = line[i]

        # Loop over the right corner
        if i == COLS - 1:
            right = line[0]
        else: 
            right = line[i+1]
        
        # Get the new cell
        new_line[i] = rule_dict[f"{left}{middle}{right}"]
    return new_line

def print_line():
    # Put all the chars into a single line and print them
    result = ""
    for char in line:
        if char:
            result +=  "#"
        else:
            result += " "
    print(result)

while True:
    print_line()
    line = update()
    time.sleep(0.1)
