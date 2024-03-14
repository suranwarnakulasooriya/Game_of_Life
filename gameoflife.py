# DEPENDENCIES ========================================================================================================

from datetime import datetime # to manage frame rate
from time import sleep #        ^
from random import randint # to create random noise
import curses # i/o
import argparse # to parse args

# RULES FOR CONWAY'S GAME OF LIFE =====================================================================================

# 1: the grid begins with a certain arrangement of live cells
# 2: the 8 cells that form the immediate perimeter of a cell are its neighbors
#    (if the cell is on a corner or edge of the playfield, the neighbors wrap around the edges,
#    so topologically, the playfield is a torus)
# 3: if a live cell has less than 2 neighbors, it dies on the next generation (loneliness)
# 4: if a live cell has more than 3 neighbors, it dies on the next generation (overcrowding)
# 5: if a dead cell has exactly 3 neighbors, it is born on the next generation (reproduction)
# deaths and births happen simultaneously
# live cells are marked with 1, dead cells are marked with 0

# SIMULATION LOGIC ====================================================================================================

def get_neighbors(grid:list[list[int]],pos:(int,int)) -> list[(int,int)]: # return list of neighbor coords
    r, c = pos
    return [(r,(c-1)%w), (r,(c+1)%w), ((r+1)%h,(c-1)%w), ((r+1)%h,(c+1)%w),
            ((r-1)%h,(c-1)%w), ((r-1)%h,(c+1)%w), ((r+1)%h,c), ((r-1)%h,c)]

# return a random wxh grid
def random_grid(w:int,h:int) -> (list[list[int]],list[int]):
    G = []; L = [] # new grid and new list of live cells start empty
    for r in range(h):
        G.append([])
        for c in range(w):
            cell = randint(0,1); G[-1].append(cell) # add a randint from 0 to 1 to the grid
            if cell: L.append((r,c)) # if the random cell is alive, add it to the live cell list
    return G, L

# update grid to next generation using neighbor search
def next_gen(grid:list[list[int]],lc:list[(int,int)]) -> (list[list[int]],list[(int,int)]):
    newgrid = [[0]*w for _ in range(h)] # next generation of grid starts empty (all 0)
    C = [] # list of cells to check is the live cells and their neighbors
    for r,c in lc: C += get_neighbors(grid,(r,c))
    C = list(set(C)) # remove repeats
    l = [] # new list of live cells starts empty
    for r,c in C:
        N = sum(grid[neighbor[0]][neighbor[1]] for neighbor in get_neighbors(grid,(r,c)))
        if grid[r][c] == 0 and N == 3: # come to life if condition met
                newgrid[r][c] = 1; l.append((r,c))
        elif grid[r][c] == 1 and 2 <= N <= 3: # stay alive if condition met
                newgrid[r][c] = 1; l.append((r,c))
    return newgrid, l

def init_dimens(screen:curses.window) -> (bool,int,int): # get dimensions of game from terminal
    h,w = screen.getmaxyx()[0]-2,screen.getmaxyx()[1]-2; f = True
    if w < 20 or h < 20: f = False # the screen is not functional if the dimensions are too small
    return f,w,h

def reset(w:int,h:int) -> (list[list[int]],list[(int,int)],int):
    return [[0]*w for _ in range(h)], [], 0 # return empty grid, no live cells, and generation 0

def close() -> None: stdscr.erase(); stdscr.keypad(0); curses.nocbreak(); curses.endwin(); exit() # end curses and quit

# SETUP ===============================================================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='GameOfLife',
        description="A terminal-based interaction simulation of Conway's Game of Life.")
    parser.add_argument('-fps','--framerate',type=int,default=60,help='target frame rate')
    args = parser.parse_args(); target_fps = max(1,min(300,args.framerate)) # parse frame rate
    target_frametime = 1/target_fps # target time per frame in seconds (1/frame rate)
    
    stdscr = curses.initscr(); curses.noecho(); stdscr.nodelay(True) # init screen, no echo, make getch() nonblocking
    stdscr.keypad(True); curses.mousemask(True); curses.curs_set(0) # accept keyboard and mouse input, hide curser

    f,w,h = init_dimens(stdscr) # get screen dimensions
    grid,live_cells,generation = reset(w,h) # start with empty grid with no live cells, editor mode, gen 0

# EVENT LOOP ==========================================================================================================

while __name__ == "__main__":
    try: 
        # INPUT AND LOGIC =============================================================================================

        dt1 = datetime.now() # get current time

        input_char = stdscr.getch(); mouse = curses.getmouse() # get key and mouse input
        y = mouse[2]-1; x = mouse[1]-1 # mouse coords are shifted by 1 since the border is 1 cell thick

        if input_char == curses.KEY_RESIZE:
            stdscr.erase(); f,w,h = init_dimens(stdscr); grid,live_cells,generation = reset(w,h)

        if input_char == curses.KEY_MOUSE and not generation and f: # update grid and live_cells on click
            if 0 <= y <= h-1 and 0 <= x <= w-1:
                grid[y][x] ^= 1 # toggle cell in grid
                if grid[y][x]: live_cells.append((y,x)) # toggle cell in live_cells
                else: live_cells.remove((y,x)) #          ^

        if generation: # when simulation is running
            grid, live_cells = next_gen(grid,live_cells); generation += 1 # update grid and live cells, change mode
            if input_char == ord(' '): grid,live_cells,generation = reset(w,h); curses.mousemask(True)
        else: # in editor
            if input_char == ord(' '): generation = 1; curses.mousemask(False) # change mode
            elif input_char == ord('r'): grid, live_cells = random_grid(w,h) # random noise on r

        if input_char == ord('q'): close() # quit on q

        # OUTPUT ======================================================================================================

        stdscr.erase() # wipe screen

        if f: # if the window is large enough to draw on
            stdscr.border() # border
            for r,c in live_cells: stdscr.addstr(r+1,c+1,'█') # live cells
            stdscr.addstr(0,1,f' Gen {generation} ') # show generation #
            dims = f' {w}x{h} '
            stdscr.addstr(0,w+1-len(dims),dims) # show dimens
        else: stdscr.addstr('Window is not big enough (need at least 20x20).') # don't draw otherwise

        sleep(max(0,target_frametime-(datetime.now()-dt1).microseconds/1e6)) # maintain frame rate
        stdscr.refresh()

    except KeyboardInterrupt: close() # quit on ^C

# =====================================================================================================================
