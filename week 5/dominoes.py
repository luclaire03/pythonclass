import random

HEAD = 0
TAIL = 1

class Domino:
    """represents a domino tile
    attributes:
      num1: int from 0 to 6
      num2: it from 0 to 6"""

    def __init__(self, num1, num2):
        """UnoCard(rank,color) -> UnoCard
        creates an Uno card with the given rank and color"""
        self.num1 = num1
        self.num2 = num2

    def __str__(self):
        """str(Domino) -> str"""
        return str(self.num1)+'-'+str(self.num2)

    def is_match(self, first, last):
        """Domino.is_match(first, last) -> boolean
        returns True if the ends match in number, False if not"""
        if self.num1 == last.num2:
            return TAIL
        elif self.num2 == first.num1:
            return HEAD
        else:
            return -1


class DominoStash:
    """represents a stash of dominoes
    attribute:
      deck: list of dominoes"""

    def __init__(self):
        """DominoStash() -> DominoStash
        creates a new full set of dominoes"""
        self.stash = []
        # double number cards
        for i in range(7):
            self.stash.append(Domino(i, i))
        # all other combinations
        for number in range(7):
            for i in range(number+1, 7):
                self.stash.append(Domino(number, i))
        random.shuffle(self.stash)  # shuffle the deck

    def __str__(self):
        """str(DominoStash) -> str"""
        return 'A set of dominoes with '+str(len(self.stash))+' dominoes remaining.'

    def deal_domino(self):
        """DominoStash.deal_domino() -> Domino
        deals a domino from the deck and returns it
        (the dealt card is removed from the deck)"""
        return self.stash.pop()


class DominoChain:
    """represents the domino chain in Dominoes
    attribute:
    chain: list of dominoes"""

    def __init__(self, dominolist):
        """DominoChain(domino) -> DominoChain
        creates a new chain using a domino from the deck"""
        self.chain = dominolist  # all the cards in the pile

    def __str__(self):
        """str(DominoChain) -> str"""
        chain = ''
        for domino in self.chain:
            chain += str(domino) + ', '
        chain = chain[:-2]
        return chain

    def add_to_end(self, domino):
        """DominoChain.add_domino(domino)
        adds the domino to the end of the chain"""
        self.chain.append(domino)

    def add_to_beginning(self, domino):
        """DominoChain.add_domino(domino)
        adds the domino to the beginning of the chain"""
        self.chain.insert(0, domino)


class DominoPlayer:
    """represents a player of dominoes
    attributes:
      name: a string with the player's name
      hand: a list of dominoes"""

    def __init__(self, name, type, stash):
        """UnoPlayer(name,deck) -> UnoPlayer
        creates a new player with a new 7-card hand"""
        self.name = name
        self.type = type
        self.hand = [stash.deal_domino() for i in range(7)]

    def __str__(self):
        """str(UnoPlayer) -> UnoPlayer"""
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_name(self):
        """UnoPlayer.get_name() -> str
        returns the player's name"""
        return self.name

    def get_type(self):
        """UnoPlayer.get_name() -> str
        returns the player's name"""
        return self.type

    def get_hand(self):
        """et_hand(self) -> str
        returns a string representation of the hand, one card per line"""
        output = ''
        for domino in self.hand:
            output += str(domino) + '\n'
        return output

    def has_won(self):
        """UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)"""
        return len(self.hand) == 0

    def draw_domino(self, stash):
        """UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn"""
        domino = stash.deal_domino()  # get card from the deck
        self.hand.append(domino)  # add this card to the hand
        return domino

    def play_domino(self, domino, chain):
        """UnoPlayer.play_card(card,pile)
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!"""
        self.hand.remove(domino)
        chain.add_card(domino)

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
            print("You have been skipped.")
            # change for next player
            topcard.kind = 'wild'
            self.hand.append(topcard)
            self.play_card(topcard, pile)
            return  # skip turn

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
        matches = [card for card in self.hand if card.is_match(pile.top_card() != 0)]
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

starting = Domino(0, 0)
ending = Domino(3, 5)
rando = Domino(2,4)
sampleChain = DominoChain([starting, ending])
print(sampleChain)
sampleChain.add_to_beginning(rando)
print(sampleChain)
