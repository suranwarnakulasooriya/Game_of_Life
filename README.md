# Conway's Game of Life
A Python application that allows users to create a configuration of cells and run the Game of Life simulation in the terminal.

## Dependencies
Curses is the only dependency for this project, to install it, do:
```
pip install curses
```

## Usage
The simulation automatically sets the grid dimensions to those of the terminal window, with a minimum of 20x20. Resize the window to change the size of the grid.

## Controls
|Key|Action|
|---|------|
|q|exit|
|r|generate random noise|
|click|toggle cell alive/dead|
|space|toggle between editor and live simulation|

The PDF in this repository explains the origins and logic of the Game of Life along with some patterns you can try out.
