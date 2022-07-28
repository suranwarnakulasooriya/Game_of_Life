# THE CONCEPT AND RULES OF CONWAY'S GAME OF LIFE (STATED BELOW) WERE DEVELOPED BY JOHN CONWAY IN 1970
# ALL PROGRAM CODE EXCLUDING IMPORTED LIBRARIES WAS SELF-DEVELOPED

# ============================================================================================================
# RULES FOR CONWAY'S GAME OF LIFE

# 1: the grid begins with a certain arrangement of live cells
# 2: the 8 cells that form the immediate perimeter of a cell are its neighbors
#    (if the cell is on a corner or edge of the playfield, the cells on the other side of the playfield become
#    its neighbors, so topologically, the playfield is a torus)
# 3: if a live cell has less than 2 neighbors, it dies next generation (loneliness)
# 4: if a live cell has more than 3 neighbors, it dies next generation (overcrowding)
# 5: if a dead cell has exactly 3 neighbors, it is born next generation (reproduction)
# NOTE: deaths and births happen simultaneously
# NOTE: live cells are marked with 1, dead cells are marked with 0

# ============================================================================================================

# ============================================================================================================
# USER INSTRUCTIONS

# press L to toggle grid lines
# press esc to close the simulation

# in editor mode, click on cells to toggle them between live and dead
# when you are done with your configuration, press space to run the simulation in evolve mode
# in evolve mode, press space again to return to editor mode

# ============================================================================================================

# ============================================================================================================
# NEIGHBORS
# each function returns the neighbor of a specified cell in a certain direction

# find north neighbor
def find_N(grid,r,c):
    R = r-1
    if r == 0: R = h-1
    return grid[R][c]

# find south neighbor
def find_S(grid,r,c):
    R = r+1
    if r == h-1: R = 0
    return grid[R][c]

# find east neighbor
def find_E(grid,r,c):
    C = c+1
    if c == w-1: C = 0
    return grid[r][C]

# find west neighbor
def find_W(grid,r,c):
    C = c-1
    if c == 0: C = w-1
    return grid[r][C]

# find northeast neighbor
def find_NE(grid,r,c):
    R = r-1; C = c+1
    if r == 0: R = h-1
    if c == w-1: C = 0
    return grid[R][C]

# find northwest neighbor
def find_NW(grid,r,c):
    R = r-1; C = c-1
    if r == 0: R = h-1
    if c == 0: C = w-1
    return grid[R][C]

# find southeast neighbor
def find_SE(grid,r,c):
    R = r+1; C = c+1
    if r == h-1: R = 0
    if c == w-1: C = 0
    return grid[R][C]

# find southwest neighbor
def find_SW(grid,r,c):
    R = r+1; C = c-1
    if r == h-1: R = 0
    if c == 0: C = w-1
    return grid[R][C]

# ============================================================================================================

# ============================================================================================================
# OTHER FUNCTIONS

# return number of live neighbors of a cell
def live_neighbors(grid,pos):
    r,c = pos
    count = 0
    for neighbor in neighbors: count += neighbor(grid,r,c)
    return count

# return an empty wxh grid
def empty_grid(w,h):
    return [[0]*w for _ in range(h)]

# update grid to next generation
def next_gen(grid):
    newgrid = empty_grid(w,h) # next generation of grid starts empty (all dead)
    for r in range(h):     # go through every row and column, effectively covering every cell in the grid
        for c in range(w):
            L = live_neighbors(grid,(r,c)) # L is the number of live neighbors
            if grid[r][c] == 0: # if the current cell is dead...
                if L == 3: newgrid[r][c] = 1 # come to life if condition met
            elif grid[r][c] == 1: # if the current cell is alive...
                if 2 <= L <= 3: newgrid[r][c] = 1 # stay alive if condition met
    return newgrid

# draw grid on screen
def draw_grid(grid,w,h,p):
    for r in range(h):
        for c in range(w):
            if evolve: pygame.draw.rect(screen, cols_evolve[grid[r][c]], (c*p,r*p,p,p))
            else: pygame.draw.rect(screen, cols_editor[grid[r][c]], (c*p,r*p,p,p))

# draw gridlines if permitted
def draw_lines(w,h,permit):
    if permit:
        for i in range(h):
            pygame.draw.line(screen, linecol, (0, i*p), (sw, i*p))
            for j in range(w):
                pygame.draw.line(screen, linecol, (j*p, 0), (j*p, sh))

# ============================================================================================================

# ============================================================================================================
# CONFIGURABLE VARIABLES

p = 35 # cell size in pixels
w = 50 # width of grid in cells
h = 50 # height of grid in cells
cols_editor = {0:(20,20,20), 1:(247, 208, 32)} # colors that represent the live and dead cells in the simulation
cols_evolve = {0:(20,20,20), 1:(208, 32, 247)} # same but when in evolve mode
linecol = (40,50,50)
gridlines = True # whether gridlines appear at the start or not

# ============================================================================================================

# ============================================================================================================
# SETUP

import pygame
sw = w*p # width of grid in pixels
sh = h*p # height of grid in pixels
neighbors = [find_N, find_S, find_E, find_W, find_NE, find_NW, find_SE, find_SW] # list of all neighbor functions
grid = empty_grid(w,h) # initialize grid
mode = 'editor'
evolve = False
user_grid = grid
mousedown = False
generation = 0

pygame.init()
screen = pygame.display.set_mode((sw,sh))

# ============================================================================================================

# ============================================================================================================
# EVENT LOOP

while True:

    pygame.display.set_caption(f"Conway's Game of Life - {mode}")

    if evolve: mode = f'Generation {generation}'
    else: mode = 'Editor'

    if evolve: pygame.time.delay(40) # delays by speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: pygame.quit(); exit()
    if keys[pygame.K_l]: pygame.time.delay(30); gridlines = not gridlines 

    draw_grid(grid,w,h,p)
    draw_lines(w,h,gridlines)

    pygame.display.update()

    if evolve:
        grid = next_gen(grid); generation += 1
        if keys[pygame.K_SPACE]:
            pygame.time.delay(30)
            evolve = False
            grid = empty_grid(w,h)
            generation = 0

    else:
        if keys[pygame.K_SPACE]:
            pygame.time.delay(30)
            evolve = True
        if pygame.mouse.get_pressed()[0]:
            pygame.time.delay(60)
            pos = pygame.mouse.get_pos()
            pr = pos[0]; pc = pos[1]
            for r in range(h):
                for c in range(w):
                    if p*c < pr < p*c+p and p*r < pc < p*r+p:
                        grid[r][c] ^= 1 # bitwise xor with 1 to toggle between 1 and 0
                        user_grid = grid; break

# ============================================================================================================