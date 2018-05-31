from tkinter import *


class CheckerTile(Canvas):
    """ represents a square in checkers
       - has a piece of not
       --- color
       - coordinates
       - selected or not
       -- bolded
    """

    def __init__(self, master, r, c):
        Canvas.__init__(self, master, width=50, height=50,
                bg='blanched almond', highlightthickness=0)
        odd = [1, 3, 5, 7]
        even = [0, 2, 4, 6, 8]
        if r in odd and c not in odd:
            self['bg'] = 'dark green'
        if r in even and c not in even:
            self['bg'] = 'dark green'
        self.grid(row=r, column=c)
        self.coord = (r, c)
        self.selected = False
        self.bind('<Button-1>', master.get_click)
        self.rect_id = 0    # objectId for rectangle frame
        self.oval_id = 0    # objectId for oval
        self.color = 'blanched almond'

    def get_color(self):
        return self.color

    def get_coord(self):
        return self.coord

    def has_piece(self):
        if self.oval_id == 0:
            return False
        else:
            return True

    def place_piece(self, color):
        '''ReversiSquare.make_color(color)
        changes color of piece on square to specified color'''
        if self.oval_id == 0:
            self.oval_id = self.create_oval(9, 9, 40, 40, fill=color)
            self.color = color

    def remove_piece(self):
        if self.oval_id != 0:
            self.delete(self.oval_id)
            self.oval_id = 0
        self.color = 'blanched almond'


class CheckerGame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, bg='white')
        self.grid()
        self.current_player = 0
        self.board = CheckerBoard(self)
        self.board.update_turn(self)
        self.starting_coord = ()
        self.last_coord = ()
        self.colors = ['red', 'white']

    def get_click(self, event):
        coord = event.widget.get_coord()
        square = self.board.tiles[coord]

        # first click or second click?
        if self.starting_coord is not ():
            # move to next
            # check whether it is the same square
            if self.starting_coord == coord:
                self.deselect(coord)
            else:  # different square
                # first validate the move is legal
                if self.validate(self.starting_coord, coord):
                    # move piece
                    self.move_piece(self.starting_coord, coord)
                    self.starting_coord = ()
                    self.current_player = (self.current_player + 1) % 2
                    self.board.update_turn(self)
                    self.last_coord = coord
                else:
                    print("illegal move, validation failed")
        else:
            # first click
            # cancel selection of last player
            if self.last_coord != ():
                self.deselect(self.last_coord)
            if square.color != self.colors[self.current_player]:
                print("illegal move, must pick your own color")
            elif self.board.tiles[coord].has_piece():
                self.starting_coord = coord
                self.select(coord)
            else:
                print("illegal move: must select your piece")

    def select(self, coord):
        self.starting_coord = coord
        self.board.tiles[coord].rect_id = self.board.tiles[coord].create_rectangle(0,0,49,49,width=5)
        return

    def deselect(self, coord):
        self.starting_coord = ()
        if self.board.tiles[coord].rect_id != 0:
            self.board.tiles[coord].delete(self.board.tiles[coord].rect_id)
        return

    def move_piece(self, start, end):
        starting_square = self.board.tiles[start]
        square = self.board.tiles[end]
        color = starting_square.color
        self.deselect(start)
        starting_square.remove_piece()
        self.select(end)
        square.place_piece(color)


    def validate(self, start, coord):
        if self.board.tiles[coord].has_piece():
            return False
        else:
            return True


class CheckerBoard():
    def __init__(self, master):
        # create tiles in the frame
        self.tiles = {}
        for row in range(8):
            for column in range(8):
                rc = (row, column)
                self.tiles[rc] = CheckerTile(master, row, column)
        # place pieces on the board
        for tile in self.tiles:
            if self.tiles[tile]['bg'] != 'blanched almond':
                if self.tiles[tile].coord[0] in range(3):
                    self.tiles[tile].place_piece('red')
                if self.tiles[tile].coord[0] in range(5, 8):
                    self.tiles[tile].place_piece('white')
        # create indicator squares and score labels
        self.colors = ['red', 'white']
        self.turnSquare = CheckerTile(master, 9, 2)
        self.turnSquare.place_piece(self.colors[master.current_player])
        self.turnLabel = CheckerTile(master, 9, 1)
        self.turnLabel.create_text(25,25,text='Turn')
        self.starting_coord = None

    def update_turn(self, master):
        if self.turnSquare.oval_id != 0:
            self.turnSquare.delete(self.turnSquare.oval_id)
            self.turnSquare.oval_id = 0
        else:
            self.turnSquare.place_piece(self.colors[master.current_player])


def play_checkers():
    root = Tk()
    root.title('Checkers')
    C = CheckerGame(root)
    C.mainloop()


play_checkers()
