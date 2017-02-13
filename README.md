# Comways Game of Life
My version of John Comways "Game Of Life", written completely object oriented.

Tkinter is used for the graphics

To launch, simply run game.py. You can use command line arguments to set the screen size and cell size:

The first argument is the screen width, the second is the screen height and the third one is the cell size. Example:

      ~$ game.py 1200 1200 5

This runs the app with a resolution of 1200x1200 and a cell size of 5.

The default values are 1000x1000 with a cell size of 10.

The controls are:
  Spacebar: Pauses the game
  C: Clears the board
  Left mouse Button: Turns the clicked cell alive if its dead and vice versa
  Shift+Left mouse: Spawn a glider
  Escape: Closes the game


TODO: 
   Fix the keyerror bug, that sometimes occurs
   Make the board wrap
   Record the living cells and graph them
