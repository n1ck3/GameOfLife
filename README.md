# gameoflife
Conway's game of life (implemented in Python 2)

## Prerequisites
```
virtualenv
```

## Running the Game of Life
```
mkdir -p ~/git
cd ~/git
git clone https://github.com/n1ck3/GameOfLife
cd GameOfLife
virtualenv env
source /env/bin/activate
python gol.py
```

## Features
* The game will initiate in a stopped state. 
* Press ```SPACEBAR``` to toggle STOPPED / RUNNING state
* Press ```c``` to clear the grid
* Press ```r``` to reset the grid to its initial setup
* When the game is STOPPED, use the mouse to toggle the state of any individual tile
