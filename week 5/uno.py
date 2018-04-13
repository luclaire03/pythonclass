import random


class UnoCard:
    """represents an Uno card
    attributes:
      rank: int from 0 to 9
      color: string"""

    def __init__(self, rank=None, color=None, kind='standard'):
        """UnoCard(rank,color) -> UnoCard
        creates an Uno card with the given rank and color"""
        self.rank = rank  # can be number in string or actions
        self.color = color
        self.kind = kind  # should be wild, wild4, action, standard

    def __str__(self):
        """str(Unocard) -> str"""
        # special card
        # wild card does not have color, nor rank
        if self.color is None:
            return str(self.kind) + 'card'
        # wild card w dictated color
        elif self.kind == 'wild' or self.kind == 'wild4':
            return str(self.color)+' '+str(self.kind)
        elif self.kind == 'action':
            return str(self.color) + ' ' + str(self.rank)
        else: # standard color
            return str(self.color)+' '+str(self.rank)

    def is_match(self, other):
        """
        UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not

        The logic will be first check wild card, then check color match,
        then rank match.
        """
        match = False  # default value

        # placing a wild
        if self.kind == 'wild' or self.kind == 'wild4':  # wild card matches everything
            match = True
        elif self.color == other.color:  # color match
            match = True
        elif other.rank is not None:  # be careful about top wild card with no rank
            match = self.rank == other.rank  # rank match, including action types

        return match


class UnoDeck:
    """represents a deck of Uno cards
    attribute:
      deck: list of UnoCards"""

    def __init__(self):
        """UnoDeck() -> UnoDeck
        creates a new full Uno deck"""
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard('0', color, 'standard'))  # one 0 of each color
            for i in range(2):
                # other action couples
                self.deck.append(UnoCard('skip', color, 'action'))
                self.deck.append(UnoCard('reverse', color, 'action'))
                self.deck.append(UnoCard('draw2', color, 'action'))
                for n in range(1, 10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(str(n), color, 'standard'))
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
        self.direction = 1  # initial direction
        self.action_done = True  # initial flag

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

    def get_direction(self):
        return self.direction

    def reverse_direction(self):
        self.direction = -self.direction

    def get_action_done(self):
        return self.action_done

    def set_action_done(self, cond):
        self.action_done = cond


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
            output += '\t' + str(card) + '\n'
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

        # check action_done flag
        action_done = pile.get_action_done()

        if not action_done:  # if an action is not performed
            # process special cards
            # this applies to both human being and computer
            # once done pass to next player
            if topcard.kind == 'wild4':
                # draw cards
                for i in range(4):
                    self.draw_card(deck)
                print("You must draw four cards.")
                # reset action_done so that next player don't do it again
                pile.set_action_done(True)
            elif topcard.kind == 'action':
                if topcard.rank == 'skip':
                    print(str(self.name) + " has been skipped!")
                    # do nothing, change for next player
                elif topcard.rank == 'draw2':
                    print("Draw two cards!")
                    self.draw_card(deck)
                    self.draw_card(deck)
                pile.set_action_done(True)

            return  # done, next player
        else:  # no need to consider actions

            matches = [card for card in self.hand if card.is_match(topcard)]

            # keep drawing until found match
            while len(matches) == 0:
                print("You can't play, so you have to draw.")
                input("Press enter to draw.")

                # check if deck is empty -- if so, reset it
                if deck.is_empty():
                    deck.reset_deck(pile)

                # draw a new card from the deck
                newcard = self.draw_card(deck)

                print("You drew: "+str(newcard))
                print(pile)

                matches = [card for card in self.hand if card.is_match(topcard)]

            (choice, chosencolor) = self.pick_card(matches)

            matches[choice-1].color = chosencolor

            # play the chosen card from hand, add it to the pile
            self.play_card(matches[choice-1], pile)

            # do not forget to reset the action flag
            # for wild4, skip, and draw 2
            # but not for reverse since it needs to be
            # handled immediately
            if matches[choice-1].kind == 'action':
                if matches[choice-1].rank == 'reverse':
                    pile.reverse_direction()
                else:
                    pile.set_action_done(False)
            elif matches[choice-1].kind == 'wild4':
                pile.set_action_done(False)

            return

    def pick_card(self, matches):
        # validate input, if no match return -1
        choice = -1
        chosencolor = ''

        if len(matches) == 0:
            return choice, chosencolor

        # print out current hand
        print(self.name + ' current matches are: ')
        for i in range(len(matches)):
            print('  ' + str(i+1) + ':' + str(matches[i]))

        # handle computer
        if self.name == 'computer':
            choice = random.randrange(len(matches))

            chosenkind = matches[choice-1].kind

            if chosenkind == 'wild' or chosenkind == 'wild4':
                chosencolor = random.choice(['red', 'yellow', 'green', 'blue'])
            else:  # non-wild card all have colors
                chosencolor = matches[choice-1].color

            print(self.name + 'chosen ' + str(matches[choice-1]) + ', color: ' + chosencolor)

        else:  # human being
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)

            chosenkind = matches[choice-1].kind
            # chose a wild card, we need to set the color
            if chosenkind == 'wild' or chosenkind == 'wild4':
                while chosencolor not in ['red', 'yellow', 'green', 'blue']:
                    chosencolor = input("Which color would you like to change to? [red, green, yellow, blue]: ")
            else:  # non-wild card has a color
                chosencolor = matches[choice-1].color

            print(str(self.name) + " chosen " + str(matches[choice - 1]) + ' color: ' + chosencolor)

        return choice, chosencolor


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
        print('pile direction is ' + str(pile.get_direction()))
        currentPlayerNum = (currentPlayerNum + pile.get_direction()) % numPlayers

play_uno(3)
