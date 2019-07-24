from tkinter import *
from tkinter import messagebox
import random


class MineCell(Label):
    '''represents a minesweeper cell'''

    def __init__(self, master, coord, neighbors=0):
        '''MineCell(master) -> mineCell
        creates a mineSweeper cell'''
        Label.__init__(self, master, width=2, height=1, bg='white',
                       text='', bd=2, relief='raised')
        self.coord = coord
        self.master = master
        self.hasBomb = False
        self.marked = False
        self.exposed = False
        self.autoexposed = False
        # int of # of nearby bombs
        self.neighbors = neighbors
        self.bind('<Button-1>', self.expose)
        self.bind('<Button-2>', self.mark)

    def expose(self, event):
        '''MineCell.expose()
        exposes a minesweeper cell
        uses auto expose if possible'''
        # replay game
        if self.master.gameover:
            self.master.restart()

        if self.marked or self.exposed:
            return

        if self.hasBomb:
            # lost game
            messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)
            self.master.expose_all_bombs()
        else:
            self.uncover()
            # blank square clicked
            if self.neighbors == 0:
                self.master.auto_expose(self)
            return

    def uncover(self):
        '''MineCell.uncover()
        updates exposed cell'''
        # unallowed cases
        if self.exposed or self.marked or self.hasBomb:
            return

        self['relief'] = 'sunken'
        self['bg'] = 'gray'
        colormap = ['', 'blue', 'darkgreen', 'red', 'purple', 'maroon',
                    'cyan', 'black', 'dim gray']

        # not a blank cell
        if self.neighbors != 0:
            self['text'] = str(self.neighbors)
            self['fg'] = colormap[self.neighbors]
        self.exposed = True

    def mark(self, event):
        '''mineCell.mark()
        marks a minesweeper cell'''
        # do nothing if exposed or no more to mark
        if self.exposed or self.master.numBombs == 0:
            return

        # allow mark and unmark
        self.marked = not self.marked
        if self.marked:
            self['text'] = '*'
            # communicate change to bottom label
            self.master.numBombs -= 1
        else:
            # unmark cell
            self['text'] = ''
            self.master.numBombs += 1

        self.master.update_counter()


class MineGrid(Frame):
    '''represents the minesweeper frame'''

    def __init__(self, master, width, height, numBombs):
        '''MineGrid(master) -> mineGrid
        initializes a mineSweeper game'''
        self.gameover = False
        self.master = master
        self.width = width
        self.height = height
        self.numBombs = numBombs
        # for restarting the game
        self.origBombs = numBombs
        Frame.__init__(self, self.master, bg='black')
        self.labelframe = Frame(self, bg='white')
        self.grid()
        self.cells = {}
        self.init_frame()

    def restart(self):
        '''MineGrid.restart()
        resets frame for another play'''
        self.gameover = False
        # reset # of bombs
        self.numBombs = self.origBombs
        self.init_frame()

    def init_frame(self):
        '''MineGrid.initi_frame()
        initializes actual mineSweeper frame'''
        # create all cells
        for row in range(self.height):
            for column in range(self.width):
                coord = (row, column)
                self.cells[coord] = MineCell(self, coord)
                self.cells[coord].grid(row=row, column=column)

        # randomly scatter bombs
        bombsplaced = 0
        while bombsplaced < self.numBombs:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            coord = (x, y)
            cell = self.cells[coord]
            # no repeats
            if not cell.hasBomb:
                self.cells[coord].hasBomb = True
                bombsplaced += 1

        # initialize numbers in all cells
        for cell in self.cells:
            self.find_neighbors(self.cells[cell])

        # creates bomb label
        self.update_counter()

    def update_counter(self):
        '''MineGrid.update_counter()
        updates label of remaining bombs'''
        counter = Label(self.labelframe, width=3, height=2,
                        text=str(self.numBombs), font=('Arial', 18))
        counter.grid(row=0, column=self.width//2)
        self.labelframe.grid(row=self.height+1, column=0, columnspan=self.width)

    def list_neighbors(self, cell):
        '''MineGrid.list_neighbors(cell) -> list
        creates a list of all the
        neighboring cells of one cell'''
        cellneighbors = []
        x = cell.coord[0]
        y = cell.coord[1]

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                # not counting itself
                if i == 0 and j == 0:
                    continue
                newx = x + i
                newy = y + j
                # within frame boundaries
                if newx < 0 or newx >= self.width:
                    continue
                if newy < 0 or newy >= self.height:
                    continue
                cellneighbors.append(self.cells[(newx, newy)])

        return cellneighbors

    def find_neighbors(self, cell):
        '''MineGrid.find_neighbors(cell)
        counts # of neighboring cells w bombs
        and sets as cell attribute'''
        # gather a list
        neighbors = self.list_neighbors(cell)

        for neighbor in neighbors:
            if neighbor.hasBomb:
                cell.neighbors += 1

    def expose_all_bombs(self):
        '''MineGrid.expose_all_bombs()
        shows all bombs after losing game'''
        for cell in self.cells:
            if self.cells[cell].hasBomb:
                self.cells[cell]['text'] = '*'
                self.cells[cell]['bg'] = 'red'

        self.gameover = True

    def auto_expose(self, cell):
        '''MineGrid.auto_expose()
        exposes empty cells at once'''
        # list of empty cells
        emptycells = [cell]

        # keep going until no more blank cells
        while len(emptycells) > 0:
            cur_cell = emptycells[0]
            # gather all neighboring blank cells
            # not already auto-exposed
            if not cur_cell.autoexposed:
                _neighbors = self.list_neighbors(cur_cell)
                for cell in _neighbors:
                    cell.uncover()
                    # already uncovered
                    if cell.autoexposed:
                        continue
                    if cell.neighbors == 0:
                        emptycells.append(cell)
            # cell has been auto-exposed
            cur_cell.autoexposed = True

            # remove first blank cell in list
            emptycells = emptycells[1:]

    def verify(self):
        '''MineGrid.verify()
        detect if player won
        or just marked cells'''
        error = 0
        for i in range(self.width):
            for j in range(self.height):
                cell = self.cells[(i, j)]
                if not cell.hasBomb and cell.marked:
                    error += 1
        # player did win
        if error == 0:
            messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent=self)
            self.gameover = True


def play_minesweeper(w, h, numBombs):
    '''play_minesweeper(w, h, numBombs)
    plays minesweeper game with
    w x h cells, numBombs bombs'''
    root = Tk()
    root.title('Minesweeper')
    test = MineGrid(root, w, h, numBombs)
    root.mainloop()


play_minesweeper(10, 10, 10)
