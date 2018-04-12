import random


class UnoCard:
    """represents an Uno card
    attributes:
      rank: int from 0 to 9
      color: string"""

    def __init__(self, rank=None, color=None, kind='standard'):
        """UnoCard(rank,color) -> UnoCard
        creates an Uno card with the given rank and color"""
        self.rank = rank
        self.color = color
        self.kind = kind

    def __str__(self):
        """str(Unocard) -> str"""
        # special card
        if self.color is None:
            return str(self.kind) + 'card'
        # wild card w dictated color
        elif self.kind == 'wild' or self.kind == 'wild4':
            return str(self.color)+' '+str(self.kind)
        elif self.kind != 'standard':
            return str(self.color) + ' ' + str(self.kind)
        # standard color
        else:
            return str(self.color)+' '+str(self.rank)

    def is_match(self, other):
        """UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not"""
        # placing a wild
        if not self.color == other.color:
            return self.kind == 'wild' or (self.kind == 'wild4')
        # all standard cards matching by number
        elif self.rank is not None and not self.color == other.color:
            return self.rank == other.rank
        # other action cards by color
        else:
            return True


class UnoDeck:
    """represents a deck of Uno cards
    attribute:
      deck: list of UnoCards"""

    def __init__(self):
        """UnoDeck() -> UnoDeck
        creates a new full Uno deck"""
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0, color, 'standard'))  # one 0 of each color
            for i in range(2):
                # other action couples
                self.deck.append(UnoCard(None, color, 'skip'))
                self.deck.append(UnoCard(None, color, 'reverse'))
                self.deck.append(UnoCard(None, color, 'draw2'))
                for n in range(1, 10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(n, color, 'standard'))
        for i in range(8):
            self.deck.append(UnoCard(None, None, 'wild'))
            self.deck.append(UnoCard(None, None, 'wild4'))
        random.shuffle(self.deck)  # shuffle the deck
        self.draw = False

    def __str__(self):
        """str(Unodeck) -> str"""
        return 'An Uno deck with '+str(len(self.deck))+' cards remaining.'

    def is_empty(self):
        """UnoDeck.is_empty() -> boolean
        returns True if the deck is empty, False otherwise"""
        return len(self.deck) == 0

    def deal_card(self):
        """UnoDeck.deal_card() -> UnoCard
        deals a card from the deck and returns it
        (the dealt card is removed from the deck)"""
        return self.deck.pop()

    def reset_deck(self, pile):
        """UnoDeck.reset_deck(pile)
        resets the deck from the pile"""
        self.deck = pile.reset_pile()  # get cards from the pile
        random.shuffle(self.deck)  # shuffle the deck


class UnoPile:
    """represents the discard pile in Uno
    attribute:
    pile: list of UnoCards"""

    def __init__(self, deck):
        """UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck"""
        card = deck.deal_card()
        self.pile = [card]  # all the cards in the pile

    def __str__(self):
        """str(UnoPile) -> str"""
        return 'The pile has ' + str(self.pile[-1]) + ' on top.'

    def top_card(self):
        """UnoPile.top_card() -> UnoCard
        returns the top card in the pile"""
        return self.pile[-1]

    def add_card(self, card):
        """UnoPile.add_card(card)
        adds the card to the top of the pile"""
        self.pile.append(card)

    def reset_pile(self):
        """UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards"""
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck


class UnoPlayer:
    """represents a player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards"""

    def __init__(self, name, deck):
        """UnoPlayer(name,deck) -> UnoPlayer
        creates a new player with a new 7-card hand"""
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        """str(UnoPlayer) -> UnoPlayer"""
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_name(self):
        """UnoPlayer.get_name() -> str
        returns the player's name"""
        return self.name

    def get_hand(self):
        """et_hand(self) -> str
        returns a string representation of the hand, one card per line"""
        output = ''
        for card in self.hand:
            output += str(card) + '\n'
        return output

    def has_won(self):
        """UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)"""
        return len(self.hand) == 0

    def draw_card(self, deck):
        """UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn"""
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)  # add this card to the hand
        return card

    def play_card(self, card, pile):
        """UnoPlayer.play_card(card,pile)
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!"""
        self.hand.remove(card)
        pile.add_card(card)

    def take_turn(self, deck, pile):
        """UnoPlayer.take_turn(deck,pile)
        takes the human player's turn in the game
        deck is an UnoDeck representing the current deck
        pile is an UnoPile representing the discard pile"""
        # print player info
        print(self.name + ", it's your turn.")
        print(pile)

        # get a list of cards that can be played
        topcard = pile.top_card()

        # check if need to draw 4 cards
        if topcard.kind == 'wild4':
            # draw cards
            for i in range(4):
                self.draw_card(deck)
            print("You must draw four cards.")
            # change for next player
            topcard.kind = 'wild'
            self.hand.append(topcard)
            self.play_card(topcard, pile)
            return  # skip turn

        if topcard.kind == 'skip':
            print(str(self.name) + " has been skipped!")
            # change for next player
            topcard.kind = 'wild'
            self.hand.append(topcard)
            self.play_card(topcard, pile)
            return

        if self.name == 'computer':
            self.take_comp_turn(deck, pile)
            return  # move on to next player

        print(self.name + " Your hand: " + str(len(self.hand)))
        print(self.get_hand())

        matches = [card for card in self.hand if card.is_match(topcard)]
        if len(matches) > 0:  # can play
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index+1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # play the chosen card from hand, add it to the pile
            self.play_card(matches[choice-1], pile)
            # chose a wild card
            if matches[choice-1].kind == 'wild' or matches[choice-1].kind == 'wild4':
                chosencolor = input("Which color would you like to change to? [red, green, yellow, blue]:")
                while chosencolor not in ['red', 'yellow', 'green', 'blue']:
                    chosencolor = input("Which color would you like to change to? [red, green, yellow, blue]: ")
                matches[choice-1].color = chosencolor
                print("The color is now " + str(chosencolor) + ".")
            print(str(self.name) + " played " + str(matches[choice-1]))

        else:  # can't play
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard):  # can be played
                print("Good -- you can play that!")
                self.play_card(newcard, pile)
                # drew a wild card
                if newcard.kind == 'wild':
                    chosencolor = input("Which color would you like to change to? [red, green, yellow, blue]: ")
                    newcard.color = chosencolor
                    print("The color is now " + str(chosencolor) + ".")
            else:   # still can't play
                print("Sorry, you still can't play.")
            input("Press enter to continue.")

    def take_comp_turn(self, deck, pile):
        """UnoPlayer.take_turn(deck,pile)
        takes the computer player's turn in the game
        deck is an UnoDeck representing the current deck
        pile is an UnoPile representing the discard pile"""
        matches = [card for card in self.hand if card.is_match(pile.top_card())]
        if len(matches) > 0:  # can play
            choice = random.randrange(len(matches))
            self.play_card(matches[choice-1], pile)
            if matches[choice - 1].kind == 'wild' or matches[choice - 1].kind == 'wild4':
                chosencolor = random.choice(['red', 'yellow', 'green', 'blue'])
                matches[choice - 1].color = chosencolor
                print("The color is now " + str(chosencolor) + ".")
            print(str(self.name) + " played " + str(matches[choice-1]))

        else:  # comp can't play
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("The computer drew: " + str(newcard))
            if newcard.is_match(pile.top_card()):  # can be played
                self.play_card(newcard, pile)
                if newcard.kind == 'wild':
                    chosencolor = random.choice(['red', 'yellow', 'green', 'blue'])
                    newcard.color = chosencolor
                    print("The color is now " + str(chosencolor) + ".")
                else:  # still can't play
                    print("Sorry, you still can't play.")
            print(str(self.name) + " played " + str(newcard))
            return


def play_uno(numPlayers):
    """play_uno(numPlayers)
    plays a game of Uno with numPlayers"""
    # set up full deck and initial discard pile
    deck = UnoDeck()
    pile = UnoPile(deck)
    # set up the players
    playerList = []
    for n in range(numPlayers):
        # get each player's name, then create an UnoPlayer
        name = input('Player #'+str(n+1)+', enter your name: ["computer" for computer player] ')
        playerList.append(UnoPlayer(name, deck))
    # randomly assign who goes first
    currentPlayerNum = random.randrange(numPlayers)
    # play the game
    while True:
        # print the game status
        print('-------')
        for player in playerList:
            print(player)
        print('-------')
        # take a turn
        playerList[currentPlayerNum].take_turn(deck, pile)
        # check for a winner
        if playerList[currentPlayerNum].has_won():
            print(playerList[currentPlayerNum].get_name()+" wins!")
            print("Thanks for playing!")
            break
        # go to the next player
        currentPlayerNum = (currentPlayerNum + 1) % numPlayers

play_uno(2)
