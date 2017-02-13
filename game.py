import tkinter as tk
from time import time, sleep
import sys


class App:
    """The main class
        Args:
            width (int): display width
            height (int): display height
            size (int): size of the cells
    """
    def __init__(self, width=1000, height=1000, size=10):
        self.screen_width = width
        self.screen_height = height
        self._running = True
        self._paused = False
        self.cellsize = size

    def initialize(self):
        global root
        root = tk.Tk()
        root.wm_title("Game of Life")

        # binding keys
        root.bind('<Escape>', self.close)
        root.protocol('WM_DELETE_WINDOW', self.close)
        root.bind('<c>', self.clear)
        root.bind('<space>', self.pause)
        root.bind('<Button-1>', self.click)
        root.bind('<B1-Motion>', self.drag)
        root.bind('<Shift-Button-1>', self.mk_glider)

        self.cv = tk.Canvas(root, height=self.screen_height,
                            width=self.screen_width, background='black')
        self.init_board()
        self.cv.pack()

    def init_board(self):
        """Constructs the game board.
        """
        self.maxcols = self.screen_width // self.cellsize
        self.maxrows = self.screen_height // self.cellsize

        # the cell ids are represented by tuples containing the coords in the
        # form of (x, y)
        self.cellids = [(i, n) for i in range(self.maxrows+1)
                        for n in range(self.maxcols+1)]
        self.cells = []

        # Generate the CellObjects as a grid
        for i in self.cellids:
            nrow, ncol = i
            self.cells.append(Cell(self.cv, nrow, ncol, self.cellsize))

        # Create the Cell instances in a dict that with
        # {<Cellid>: Cell(cv, row, col)}
        self.board = dict(zip(self.cellids, self.cells))

        # Starting seed
        midcol, midrow = self.maxcols // 2, self.maxrows // 2
        seedpoints = [(midrow-1, midcol-3), (midrow-1, midcol-2),
                      (midrow-1, midcol-1), (midrow, midcol-3),
                      (midrow-1, midcol+3), (midrow-1, midcol+2),
                      (midrow-1, midcol+1), (midrow, midcol+3),
                      (midrow+1, midcol-3), (midrow+1, midcol-2),
                      (midrow+1, midcol-1), (midrow+1, midcol-3),
                      (midrow+1, midcol+3), (midrow+1, midcol+2),
                      (midrow+1, midcol+1)]
        for i in seedpoints:
            self.board[i].alive = True

    def nextgen(self):
        """Calculate the next generation of cells by updating each cell.
        """
        livingcells = [i for i in self.board.keys() if self.board[i].alive]
        if len(livingcells) < 200:
            sleep(0.05)
        for i in livingcells:
            row, col = i
            self.board[(row, col)].update(livingcells)
            if col < self.maxcols:
                self.board[(row, col+1)].update(livingcells)
            if col > 0:
                self.board[(row, col-1)].update(livingcells)
            if row < self.maxrows:
                self.board[(row+1, col)].update(livingcells)
                if col > 0:
                    self.board[(row+1, col-1)].update(livingcells)
                if col < self.maxcols:
                    self.board[(row+1, col+1)].update(livingcells)
            if row > 0:
                self.board[(row-1, col)].update(livingcells)
                if col < self.maxcols:
                    self.board[(row-1, col+1)].update(livingcells)
                if col > 0:
                    self.board[(row-1, col-1)].update(livingcells)

    def mainloop(self):
        """Application Mainloop
        """
        while self._running:
            if not self._paused:
                self.nextgen()
            self.cv.update()

    def click(self, event):
        """Make a clicked Cell alive if it's dead and vice versa
        """
        col = event.x // self.cellsize
        row = event.y // self.cellsize
        if not self.board[(row, col)].alive:
            self.board[(row, col)].alive = True
            self.cv.itemconfig(self.board[(row, col)].cid, fill='white')
        else:
            self.board[(row, col)].alive = False
            self.cv.itemconfig(self.board[(row, col)].cid, fill='black')

    def drag(self, event):
        col = event.x // self.cellsize
        row = event.y // self.cellsize
        if not self.board[(row, col)].alive:
            self.board[(row, col)].alive = True
            self.cv.itemconfig(self.board[(row, col)].cid, fill='white')

    def mk_glider(self, event):
        """Make a glider at the clicked position
        """
        col = event.x // self.cellsize
        row = event.y // self.cellsize
        cells = [(row+1, col-1), (row+1, col), (row+1, col+1), (row, col+1),
                 (row-1, col)]
        for i in cells:
            if not self.board[i].alive:
                self.board[i].alive = True
                self.cv.itemconfig(self.board[i].cid, fill='white')
            else:
                pass

    def pause(self, *ignore):
        """Pause when the spacebar is pressed
        """
        if not self._paused:
            self._paused = True
        else:
            self._paused = False

    def clear(self, *ignore):
        """Clear the board
        """
        livingcells = [i for i in self.board.keys() if self.board[i].alive]
        for i in livingcells:
            self.board[i].alive = False
            self.cv.itemconfig(self.board[i].cid, fill='black')

    def close(self, *ignore):
        """Close Application
        """
        self._running = False
        root.destroy()


class Cell(App):
    """A cell. Can be alive or dead.
    Args:
        cv (canvas): the canvas on which to draw on
        row (int): the row of the Cell
        column (int): the column of the Cell
    """
    def __init__(self, cv, row, column, size):
        super().__init__()
        self.cv = cv
        self.ocolor = 'grey'

        self.alive = False

        if self.alive:
            self.color = 'white'
        else:
            self.color = 'black'

        self.width = size
        self.height = size
        self.row = row
        self.col = column
        self.x = column * self.width
        self.y = row * self.height
        self.corn = [self.x, self.y, self.x + self.width, self.y + self.height]
        self.cid = self.cv.create_rectangle(self.corn[0], self.corn[1],
                                            self.corn[2], self.corn[3],
                                            fill=self.color,
                                            outline=self.ocolor)

        self.peers = [(row+1, column), (row-1, column),
                      (row, column+1), (row, column-1),
                      (row+1, column+1), (row+1, column-1),
                      (row-1, column+1), (row-1, column-1)]

    def update(self, lc):
        """Updates the Cell by applying the following rules:
            1. A cell with exactly 3 neighbours is born
            2. A cell with less than 2 and more than 3 neighbours dies.
            Then the color of ther cell is updated.

            Args:
                lc (lst): A list of the living Cells on the board
        """
        livingpeers = [n for n in self.peers if n in lc]
        if self.alive:
            livingpeers.append((self.row, self.col))
        if len(livingpeers) == 3:
            self.alive = True
        elif len(livingpeers) == 4:
            pass
        else:
            self.alive = False
        if self.alive:
            self.cv.itemconfig(self.cid, fill='white')
        else:
            self.cv.itemconfig(self.cid, fill='black')


def main():
    try:
        app = App(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    except IndexError:
        app = App()
    app.initialize()
    app.mainloop()


if __name__ == '__main__':
    main()


# TODO: Fix the keyerror bug, that sometimes occurs
#       Make the board wrap
#       Record the living cells and graph them
