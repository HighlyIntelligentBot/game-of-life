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
    def __init__(self, width=800, height=800, size=50):
        self.screen_width = width
        self.screen_height = height
        self._running = True
        self._paused = False
        self.cellsize = size

    def initialize(self):
        global root
        root = tk.Tk()

        # binding keys
        root.bind('<Escape>', self.close)
        root.protocol('WM_DELETE_WINDOW', self.close)
        root.bind('<space>', self.pause)
        root.bind('<Button-1>', self.click)

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
        self.cellids = [(i, n) for i in range(self.maxrows)
                        for n in range(self.maxcols)]
        self.cells = []

        # Generate the CellObjects as a grid
        for i in self.cellids:
            nrow, ncol = i
            self.cells.append(Cell(self.cv, nrow, ncol, self.cellsize))

        # Create the Cell instances in a dict that with
        # {<Cellid>: Cell(cv, row, col)}
        self.board = dict(zip(self.cellids, self.cells))

        # For now, this is the place to choose which cells should be alive from
        # the start.
        self.board[(2, 0)].alive = True
        self.board[(2, 1)].alive = True
        self.board[(2, 2)].alive = True
        self.board[(1, 2)].alive = True
        self.board[(0, 1)].alive = True

    def nextgen(self):
        """Calculate the next generation of cells by updating each cell.
        """
        sleep(0.2)
        livingcells = [i for i in self.board.keys() if self.board[i].alive]
        for i in self.board.keys():
            self.board[i].update(livingcells)

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

    def pause(self, *ignore):
        """Pause when the spacebar is pressed
        """
        if not self._paused:
            self._paused = True
        else:
            self._paused = False

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

        self.alive = False

        if self.alive:
            self.color = 'white'
        else:
            self.color = 'black'

        # realized too late that width of a square = height.. Too lazy to
        # change it now..
        self.width = size
        self.height = size
        self.row = row
        self.col = column
        self.x = column * self.width
        self.y = row * self.height
        self.corn = [self.x, self.y, self.x + self.width, self.y + self.height]
        self.cid = self.cv.create_rectangle(self.corn[0], self.corn[1],
                                            self.corn[2], self.corn[3],
                                            fill=self.color, outline='white')

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
        self.livinpeers = [n for n in self.peers if n in lc]
        if not self.alive:
            if len(self.livinpeers) == 3:
                self.alive = True
            else:
                pass
        else:
            if len(self.livinpeers) < 2 or len(self.livinpeers) > 3:
                self.alive = False
            else:
                pass
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


# TODO: Implement third colour for cells that recently died
