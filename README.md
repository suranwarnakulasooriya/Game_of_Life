# Conway's Game of Life
A Python application that allows users to create a configuration of cells and run the Game of Life simulation.

## Dependencies
Pygame is the only dependency for this project. To install it, do:
```
pip install pygame
```

## Usage
The program defaults to a 50x50 grid of cells each wth a size of 35x35 pixels. If this configuration is not optimal for you, you can change these values in the following lines:
```
135 p = 35 # cell size in pixels
136 w = 50 # width of grid in cells
137 h = 50 # height of grid in cells
```

All cells start dead. Click on cells to toggle them between alive and dead. When you are done with your configuration, press space to run the Game of Life on it. Press space again to return to the configuration editor. You can toggle the lines on the grid with the L key.

The PDF in this repository explains the origins and logic of the Game of Life along with some patterns you can try out.
