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
# the 'get' specifier tells the function to return the coordinates of the neighbor instead of its value

# find north neighbor
def find_N(grid,r,c,get=False):
    R = r-1
    if r == 0: R = h-1
    if get: return (R,c)
    return grid[R][c]

# find south neighbor
def find_S(grid,r,c,get=False):
    R = r+1
    if r == h-1: R = 0
    if get: return (R,c)
    return grid[R][c]

# find east neighbor
def find_E(grid,r,c,get=False):
    C = c+1
    if c == w-1: C = 0
    if get: return (r,C)
    return grid[r][C]

# find west neighbor
def find_W(grid,r,c,get=False):
    C = c-1
    if c == 0: C = w-1
    if get: return (r,C)
    return grid[r][C]

# find northeast neighbor
def find_NE(grid,r,c,get=False):
    R = r-1; C = c+1
    if r == 0: R = h-1
    if c == w-1: C = 0
    if get: return (R,C)
    return grid[R][C]

# find northwest neighbor
def find_NW(grid,r,c,get=False):
    R = r-1; C = c-1
    if r == 0: R = h-1
    if c == 0: C = w-1
    if get: return (R,C)
    return grid[R][C]

# find southeast neighbor
def find_SE(grid,r,c,get=False):
    R = r+1; C = c+1
    if r == h-1: R = 0
    if c == w-1: C = 0
    if get: return (R,C)
    return grid[R][C]

# find southwest neighbor
def find_SW(grid,r,c,get=False):
    R = r+1; C = c-1
    if r == h-1: R = 0
    if c == 0: C = w-1
    if get: return (R,C)
    return grid[R][C]

# ============================================================================================================

# ============================================================================================================
# OTHER FUNCTIONS

# return number of live neighbors of a cell
def live_neighbors(grid,pos):
    count = 0
    for neighbor in neighbors: count += neighbor(grid,pos[0],pos[1])
    return count

# return list of neighbors
def get_neighbors(grid,pos):
    l = [pos]
    for neighbor in neighbors: l.append(neighbor(grid,pos[0],pos[1],get=True))
    return l

# return an empty wxh grid
def empty_grid(w,h):
    return [[0]*w for _ in range(h)]

# update grid to next generation using neighbor search
def optimize(grid,lc):
    newgrid = empty_grid(w,h) # next generation of grid starts empty (all dead)
    C = [] # list of cells to check is the live cells and their neighbors
    for r,c in lc: C += get_neighbors(grid,(r,c))
    C = list(set(C)) # remove repeats
    l = [] # new list of live neighbors
    for r,c in C:
        N = live_neighbors(grid,(r,c)) # L is the number of live neighbors
        if grid[r][c] == 0: # if the current cell is dead...
            if N == 3: # come to life in condition met
                newgrid[r][c] = 1; l.append((r,c))
        elif grid[r][c] == 1: # if the current cell is alive...
            if 2 <= N <= 3: # stay alive if condidion met
                newgrid[r][c] = 1; l.append((r,c))
    return newgrid, l

# draw grid on screen
def draw_grid(grid,w,h,p):
    for (r,c) in live_cells:
        if evolve: pygame.draw.rect(screen, ('#c678dd'), (c*p,r*p,p,p))
        else: pygame.draw.rect(screen, ('#e5c07b'), (c*p,r*p,p,p))

# draw gridlines if permitted
def draw_lines(w,h):
    for i in range(h):
        pygame.draw.line(screen, '#1e222a', (0, i*p), (sw, i*p))
        for j in range(w):
            pygame.draw.line(screen, '#1e222a', (j*p, 0), (j*p, sh))

# ============================================================================================================

# ============================================================================================================
# CONFIGURABLE VARIABLES

p = 20 # cell size in pixels
w = 100; h = 100 # width and height of grid in cells
gridlines = False # whether gridlines appear at the start or not, gridlines affect framerate considerably

# ============================================================================================================

# ============================================================================================================
# SETUP

import pygame
sw = w*p; sh = h*p # with and height of screen in pixels
neighbors = [find_N, find_S, find_E, find_W, find_NE, find_NW, find_SE, find_SW] # list all neighbor functions
grid = empty_grid(w,h) # initialize grid
mode = 'Editor'; evolve = False; generation = 0; run = True
live_cells = [] # starts with no live cells
pygame.init(); screen = pygame.display.set_mode((sw,sh))

# ============================================================================================================

# ============================================================================================================
# EVENT LOOP

while run:
    if evolve: mode = f'Generation {generation}'
    else: mode = 'Editor'

    if evolve: pygame.time.delay(40) # delay so movement is readable
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: run = False
    if keys[pygame.K_l]: pygame.time.delay(30); gridlines = not gridlines 

    screen.fill('#282c34')
    draw_grid(grid,w,h,p)
    if gridlines: draw_lines(w,h)
    pygame.display.update()

    if evolve:
        grid, live_cells = optimize(grid,live_cells); generation += 1
        if keys[pygame.K_SPACE]: # reset data
            pygame.time.delay(60); evolve = False; grid = empty_grid(w,h); generation = 0; live_cells = []

    else:
        if keys[pygame.K_SPACE]:
            pygame.time.delay(60); evolve = True
        if pygame.mouse.get_pressed()[0]: # toggle cell on click
            pygame.time.delay(80)
            pos = pygame.mouse.get_pos()
            r, c = pos[1]//p, pos[0]//p
            grid[r][c] ^= 1 # bitwise xor with 1 to toggle between 1 and 0
            # update list of live cells
            if grid[r][c] == 1: live_cells.append((r,c))
            else: live_cells.remove((r,c))

    pygame.display.set_caption(f"Conway's Game of Life - {mode}")

pygame.quit; exit()

# ============================================================================================================
