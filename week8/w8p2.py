# Python Class 1699
# Lesson 8 Problem 2
# Author: luclaire (336193)

# Python Class 1699
# Lesson 8 Problem 1 Part (b)
# Author: luclaire (336193)

from tkinter import *
import random


class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self, master, valueList=[1, 2, 3, 4, 5, 6], colorList=['black'] * 6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self, master, width=60, height=60, bg='white',
                        bd=5, relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top - 1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1, 7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1, 1)],
                   [(0, 0), (2, 2)],
                   [(0, 0), (1, 1), (2, 2)],
                   [(0, 0), (0, 2), (2, 0), (2, 2)],
                   [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
                   [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]]
        for location in pipList[self.top - 1]:
            self.draw_pip(location, self.colorList[self.top - 1])

    def draw_pip(self, location, color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx, centery) = (17 + 20 * location[1], 17 + 20 * location[0])  # center
        self.create_oval(centerx - 5, centery - 5, centerx + 5, centery + 5, fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)




class Decath1500MFrame(Frame):
    '''frame for a game of 400 Meters'''

    def __init__(self, master, name):
        '''Decath400MFrame(master,name) -> Decath400MFrame
        creates a new 400 Meters frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self, master)
        self.grid()
        # label for player's name
        Label(self, text=name, font=('Arial', 18)).grid(columnspan=3, sticky=W)
        # set up score and rerolls
        self.scoreLabel = Label(self, text='Score: 0', font=('Arial', 18))
        self.scoreLabel.grid(row=0, column=3, columnspan=2)
        self.highscoreLabel = Label(self, text='High Score: 0', font=('Arial', 18))
        self.highscoreLabel.grid(row=0, column=5, columnspan=3, sticky=E)
        # initialize game data
        self.score = 0
        self.highscore = 0
        self.attempts = 3
        self.gameround = 0
        self.dice = []
        self.setup()

    def setup(self):
        # set up dice
        if len(self.dice) > 0:
            # clean up first
            self.dice.clear()

        for n in range(8):
            self.dice.append(GUIDie(self, ['foul', 2, 3, 4, 5, 6], ['red']+['black']*5))
            self.dice[n].grid(row=1, column=n)

        # set up buttons
        self.rollButton = Button(self, text='Roll', state=ACTIVE, command=self.roll)
        self.rollButton.grid(row=2, columnspan=1)
        self.stopButton = Button(self, text='Stop', state=DISABLED, command=self.stop)
        self.stopButton.grid(row=3, columnspan=1)

    def roll(self):
        '''Decath400MFrame.roll()
        handler method for the roll button click'''
        # roll both dice
        if self.gameround == 0:
            self.stopButton['state'] = ACTIVE
        self.dice[self.gameround].roll()
        if self.dice[self.gameround].get_top() == 'foul':
            self.scoreLabel['text'] = 'ATTEMPT FOULED'
            self.rollButton['state'] = DISABLED
            self.stopButton['text'] = 'FOUL'
            self.score = 0
            self.gameround = 0
            self.attempts += 1
            return
        self.score += int(self.dice[self.gameround].get_top())
        self.gameround += 1
        self.scoreLabel['text'] = 'Score: ' + str(self.score)
        if self.gameround == 8:
            self.attempts += 1
            self.gameround = 0
        # move buttons to next pair of dice
        self.rollButton.grid(row=2, column=self.gameround, columnspan=1)
        self.stopButton.grid(row=3, column=self.gameround, columnspan=1)
        self.rollButton['state'] = ACTIVE

    def stop(self):
        '''Decath400MFrame.keep()
        handler method for the keep button click'''
        # add dice to score and update the scoreboard
        self.attempts += 1
        self.highscore = self.score
        self.highscoreLabel['text'] = 'High Score: ' + str(self.highscore)
        if self.attempts == 3:
            self.stopButton.grid_remove()
            self.rollButton.grid_remove()
            self.scoreLabel['text'] = 'Game over'
        else:  # figure out how to reset this!
            self.gameround = 0
            self.score = 0
            self.stopButton.grid_remove()
            self.rollButton.grid_remove()
            self.setup()



# play the game
name = input("Enter your name: ")
root = Tk()

root.title('1500 Meters')
game = Decath1500MFrame(root, name)
game.mainloop()
