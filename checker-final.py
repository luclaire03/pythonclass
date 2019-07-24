from tkinter import *


class CheckerSquare(Canvas):
    '''represents a square on a checkerboard'''

    def __init__(self, master, r, c, color):
        '''CheckerSquare(master,r,c,color) -> CheckerSquare
        creates a new empty checkers square
        (r,c) is the row,column coordinates of the square
        color is the background color'''
        Canvas.__init__(self, master, width=50, height=50, bd=0, \
                        highlightthickness=5, highlightbackground=color, \
                        highlightcolor='black', bg=color)
        self.grid(row=r, column=c, ipadx=0, ipady=0, padx=0, pady=0)
        # set the coorindates
        self.row = r
        self.column = c
        # allow the squares being used to be clicked upon
        if (r + c) % 2 == 1:  # only squares whose coords sum to an odd number are used
            self.bind('<Button>', master.on_click)
        self.player = None  # stores which player's piece is on the square
        self.isKing = False  # stores whether a king is on the square

    def get_pos(self):
        '''CheckerSquare.get_pos() -> (int,int)
        returns the coordinates of the square'''
        return (self.row, self.column)

    def get_player(self):
        '''CheckerSquare.get_player() -> int/None
        returns the number of the player whose piece is on the square
        (None if the square is empty)'''
        return self.player

    def is_king(self):
        '''CheckerSquare.is_king() -> bool
        returns True if a king is on the square, False otherwise'''
        return self.isKing

    def is_empty(self):
        '''CheckerSquare.is_empty() -> bool
        returns True is the square is empty, False if it contains a piece'''
        return not isinstance(self.player, int)

    def clear_checker(self):
        '''CheckerSquare.clear_checker()
        removes a piece (if any) from the square'''
        self.player = None
        # clear all canvas items
        objectList = self.find_all()
        for obj in objectList:
            self.delete(obj)

    def set_checker(self, player, color, isKing):
        '''CheckerSquare.set_checker(player,color,isKing)
        places a piece on the square
        player is the player number
        color is the player color
        isKing is True if the piece is a king, False if a normal piece'''
        # clear old checker (if any)
        self.clear_checker()
        # set attributes
        self.player = player
        self.isKing = isKing
        # draw new checker
        self.create_oval(10, 10, 50, 50, fill=color)
        # draw king if necessary
        if isKing:
            self.create_text(30, 40, text='*', font=('Arial', 48))

    def no_click(self):
        '''CheckerSquare.no_click()
        make the square not respond to clicks'''
        self.unbind('<Button>')


class CheckersGame(Frame):
    '''represents a game of checkers'''

    def __init__(self, master):
        '''CheckersGame(master) -> CheckersGame
        creates a new game of checkers'''
        # initialize and display the Frame
        Frame.__init__(self, master)
        self.grid()
        # set up attributes
        self.squares = {}  # dictionary to store the square
        # game colors
        self.boardColors = ['blanched almond', 'dark green']
        self.colors = ['red', 'white']
        self.direction = [1, -1]  # the directions of "forward" motion
        self.turn = 0  # who goes first
        self.pieceSelected = None  # keeps track of whether a piece has been clicked on
        self.jumpInProgress = False  # keeps track of whether a piece is in mid-jump
        # set up the empty board
        for row in range(8):
            for column in range(8):
                color = self.boardColors[(row + column) % 2]
                self.squares[(row, column)] = CheckerSquare(self, row, column, color)
        # place the pieces for player 0
        for row in range(3):
            for index in range(4):
                square = (row, 2 * index + ((row + 1) % 2))
                self.squares[square].set_checker(0, self.colors[0], False)
        # place the pieces for player 1
        for row in range(5, 8):
            for index in range(4):
                square = (row, 2 * index + ((row + 1) % 2))
                self.squares[square].set_checker(1, self.colors[1], False)
        # set up the display below the board
        self.rowconfigure(8, minsize=3)  # leave some space
        Label(self, text='Turn:', font=('Arial', 18)).grid(row=9, column=0, columnspan=2, sticky=E)
        # set up indicator for whose turn it is
        self.turnChecker = CheckerSquare(self, 9, 2, 'gray')
        self.turnChecker.set_checker(0, self.colors[0], False)
        self.turnChecker.unbind('<Button>')  # don't allow it to be clicked
        # set up message label (initially blank)
        self.message = Label(self, text="", font=('Arial', 18))
        self.message.grid(row=9, column=4, columnspan=4)

    def on_click(self, event):
        '''CheckersGame.on_click(event)
        event handler for a mouse click
        If clicked on a piece of the player's color:
          Sets that piece as the piece to be moved
        If clicked on a blank square
          Attempts to move the previously selected piece to the blank square'''
        # get the coordinates of the clicked square and highlight it
        (row, col) = event.widget.get_pos()
        event.widget.focus_set()
        # check for click on a current player's piece, not in the middle of a multi-jump move
        if self.squares[(row, col)].get_player() == self.turn and not self.jumpInProgress:
            # set this square as the piece selected to move
            self.pieceSelected = (row, col)
        # check for click on a blank square if a piece has already been selected to move
        elif self.pieceSelected and self.squares[(row, col)].is_empty():
            # landing space selected -- check for valid move
            (currentRow, currentCol) = self.pieceSelected
            isKing = self.squares[(currentRow, currentCol)].is_king()  # piece is a king
            # check for a valid normal move (no jump)
            if ((row - currentRow == self.direction[self.turn]) or \
                (isKing and row - currentRow == -self.direction[self.turn])) and \
                    abs(col - currentCol) == 1:
                # not allowed to make a normal move if a jump is possible
                if self.player_can_jump():
                    self.message['text'] = 'Must jump!'
                else:
                    # legal move into empty space
                    self.move(currentRow, currentCol, row, col)
                    self.next_turn()
            # check for a valid jump
            elif ((row - currentRow == (2 * self.direction[self.turn])) or \
                  (isKing and row - currentRow == -(2 * self.direction[self.turn]))) and \
                    abs(col - currentCol) == 2:
                # check for jumped piece
                jumpedRow = (row + currentRow) // 2
                jumpedCol = (col + currentCol) // 2
                if self.squares[(jumpedRow, jumpedCol)].get_player() == 1 - self.turn:
                    # valid jump
                    # also check that a non-king becomes a king -- this ends the turn
                    self.jump(currentRow, currentCol, row, col)
                    newKing = self.squares[(row, col)].is_king()
                    if self.piece_can_jump(row, col) and (isKing or not newKing):
                        # the piece just moved can still jump; must jump again
                        self.jumpInProgress = True
                        self.pieceSelected = (row, col)
                    else:
                        # no more jumps -- go to the next player's turn
                        self.next_turn()
        elif not self.jumpInProgress:
            # clear the selected piece if a "bad" square is clicked
            self.pieceSelected = None
        if self.jumpInProgress:
            # don't clear the piece -- it must continue jumping
            #  instead display a message
            self.message['text'] = 'Must continue jump!'

    def piece_can_jump(self, row, col):
        '''CheckersGame.piece_can_jump(row,col) -> bool
        returns True if the piece at (row,col) can jump, False if not'''
        direction = self.direction[self.turn]
        # forward directions
        if (0 <= row + 2 * direction < 8) and (0 <= col + 2 < 8) and \
                (self.squares[(row + direction, col + 1)].get_player() == 1 - self.turn) and \
                (self.squares[(row + 2 * direction, col + 2)].is_empty()):
            return True
        if (0 <= row + 2 * direction < 8) and (0 <= col - 2 < 8) and \
                (self.squares[(row + direction, col - 1)].get_player() == 1 - self.turn) and \
                (self.squares[(row + 2 * direction, col - 2)].is_empty()):
            return True
        # backwards directions -- only check if the piece is a king
        if self.squares[(row, col)].is_king():
            if (0 <= row - 2 * direction < 8) and (0 <= col + 2 < 8) and \
                    (self.squares[(row - direction, col + 1)].get_player() == 1 - self.turn) and \
                    (self.squares[(row - 2 * direction, col + 2)].is_empty()):
                return True
            if (0 <= row - 2 * direction < 8) and (0 <= col - 2 < 8) and \
                    (self.squares[(row - direction, col - 1)].get_player() == 1 - self.turn) and \
                    (self.squares[(row - 2 * direction, col - 2)].is_empty()):
                return True
        return False

    def player_can_jump(self):
        '''CheckersGame.player_can_jump() -> bool
        returns True if any of the player's pieces can jump, False if not'''
        # loop over the board, only looking at the dark squares
        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 1 and \
                        self.squares[(row, column)].get_player() == self.turn and \
                        self.piece_can_jump(row, column):
                    # found a player's piece that can jump, so return True
                    return True
        return False

    def piece_can_move(self, row, col):
        '''CheckersGame.piece_can_move(row,col) -> bool
        returns True if the piece at (row,col) can make a normal move, False if not'''
        direction = self.direction[self.turn]
        # forward directions
        if (0 <= row + direction < 8) and (0 <= col + 1 < 8) and \
                (self.squares[(row + direction, col + 1)].is_empty()):
            return True
        if (0 <= row + direction < 8) and (0 <= col - 1 < 8) and \
                (self.squares[(row + direction, col - 1)].is_empty()):
            return True
        # backwards directions -- only check if the piece is a king
        if self.squares[(row, col)].is_king():
            if (0 <= row - direction < 8) and (0 <= col + 1 < 8) and \
                    (self.squares[(row - direction, col + 1)].is_empty()):
                return True
            if (0 <= row - direction < 8) and (0 <= col - 1 < 8) and \
                    (self.squares[(row - direction, col - 1)].is_empty()):
                return True
        return False

    def player_can_move(self):
        '''CheckersGame.player_can_move() -> bool
        returns True if any of the player's pieces can make a normal move, False if not'''
        # loop over the board, only looking at the dark squares
        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 1 and \
                        self.squares[(row, column)].get_player() == self.turn and \
                        self.piece_can_move(row, column):
                    # found a player's piece that can move, so return True
                    return True
        return False

    def move(self, oldr, oldc, newr, newc):
        '''CheckersGame.move(oldr,oldc,newr,newc)
        moves the piece that's on square (oldr,oldc) to square (newr,newc)'''
        # check if the piece is a king
        isKing = self.squares[(oldr, oldc)].is_king()
        if newr == 7 * (1 - self.turn):  # made to last row, make it a king
            isKing = True
        # erase the piece from the old square, and place it in the new square
        self.squares[(oldr, oldc)].clear_checker()
        self.squares[(newr, newc)].set_checker(self.turn, self.colors[self.turn], isKing)

    def jump(self, oldr, oldc, newr, newc):
        '''CheckersGame.jump(oldr,oldc,newr,newc)
        jumps the piece that's on square (oldr,oldc) to square (newr,newc)
        and removes the piece in between that got jumped over'''
        # move the piece
        self.move(oldr, oldc, newr, newc)
        # remove jumped piece
        jumpr = (oldr + newr) // 2
        jumpc = (oldc + newc) // 2
        self.squares[(jumpr, jumpc)].clear_checker()

    def next_turn(self):
        '''CheckersGame.next_turn()
        goes to the other player's turn
        if that player can't move, the game is over and the previous player wins'''
        # switch to other player and update the status indicators
        self.turn = 1 - self.turn
        self.turnChecker.set_checker(self.turn, self.colors[self.turn], False)
        self.message['text'] = ''
        # reset the status attributes
        self.pieceSelected = None
        self.jumpInProgress = False
        # check for a legal move
        if not self.player_can_move() and not self.player_can_jump():
            # no legal move, so the game is over
            self.turn = 1 - self.turn  # previous player won
            self.turnChecker.set_checker(self.turn, self.colors[self.turn], False)
            self.message['text'] = self.colors[self.turn].title() + ' wins!'
            # unbind all squares so winning player can't move anymore
            for square in self.squares.values():
                square.no_click()


def play_checkers():
    '''play_checkers()
    starts a new 2-player game of checkers'''
    root = Tk()
    root.title('Checkers')
    CG = CheckersGame(root)
    CG.mainloop()


play_checkers()
