#!/usr/bin/env python

"""
Description: Simulates the game Blackjack, but textual format.
"""

import random
import sys

"""
Class: Creates Card Objects.
"""
class Cards(object):
    """
    Function: Initializes the values of the object.
    ----------
    Parameters
    ----------
    self : Object
      The card itself.
    name : String
      The name of the card.
    value : Integer
      How much the card is worth.
    amount : Integer
      How many of these cards are left in the deck.
    """
    def __init__(self, name, value, amount):
        self.name = name
        self.value = value
        self.amount = amount
    '''
    Function: Deletes the card from the deck.
    '''
    def delCard(self):
        self.amount -= 1
    '''
    Function: Re-adds all of the cards into the deck.
    '''
    @classmethod
    def shuffle(cls):
        for c in cList:
            c.amount = 4
        print('- The deck was shuffled.')
    '''
      Function: Checks if the all of the cards are empty.
    '''
    @classmethod
    def empty(cls):
        cardAmts = 0  # Amount of cards.
        # For every card, add amount to cardAmts.
        for c in cList:
            cardAmts += c.amount
        return cardAmts == 0  # Checks if cardAmts = 0; returns true/false.


"""
Global Variables
"""
# Initializing the cards.
ACE = Cards('A', 0, 4)
TWO = Cards('2', 2, 4)
THREE = Cards('3', 3, 4)
FOUR = Cards('4', 4, 4)
FIVE = Cards('5', 5, 4)
SIX = Cards('6', 6, 4)
SEVEN = Cards('7', 7, 4)
EIGHT = Cards('8', 8, 4)
NINE = Cards('9', 9, 4)
TEN = Cards('10', 10, 4)
KING = Cards('K', 10, 4)
QUEEN = Cards('Q', 10, 4)
JACK = Cards('J', 10, 4)

# Regular variables.
cList = [ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, KING, QUEEN, JACK]  # List of Cards.
uInput = None  # User input.
uCards = []  # User's Cards.
dCards = []  # Dealer's Cards.
ongoing = True


"""
Function: Divides the console.
"""
def divider():
    print('──────────────────────────────────────────')


"""
Function: Resets the global variables.
"""
def resetGame():
    global uInput, uCards, dCards, ongoing
    uInput = None
    uCards = []
    dCards = []
    ongoing = True
    divider()


"""
Function: Draws a card.
----------
Parameters
----------
player : String
  Player that is drawing.
  Possible choices: 'u' user.
                    'd' dealer.
                    'df' dealer face down.
"""
def draw(player):
    card = cList[random.randrange(1, 14) - 1]  # Draws a card.
    while card.amount < 1:  # No more of this card in deck.
        if Cards.empty():  # if deck is empty.
            print('There are no more cards left.')
            Cards.shuffle()
            divider()
        card = cList[random.randrange(1, 14) - 1]  # Redraw another card.
    if player == 'd' or player == 'df':  # Dealer.
        dCards.append(card)  # Adds the card to the dealer's hand.
        dCards[-1].delCard()  # Removes the card from the deck.
        # Prints out what the dealer drew.
        if player == 'd':  # Regular
            print(f"- Dealer drew a(n) {card.name}.")
        else:  # Facedown
            print('- Dealer drew a card faced down.')
    elif player == 'u':
        uCards.append(card)  # Adds the card to the user's hand.
        uCards[-1].delCard()  # Removes the card from the deck.
        # Prints out what the user drew.
        print(f"- User drew a(n) {card.name}.")


"""
Function: Calculates the total.
----------
Parameters
----------
tType : String
  Total type for the dealer; facedown or regular.
  tTypes: 'fd' (face down)
          'None' (nothing, can be anything else.)
fType : String
  Function type; return or print.
  fTypes: 'rd' (return dealer)
          'ru' (return user)
          'p' (print)
-------
Returns
-------
return dTotal : Integer
  Returns the dealer's total.
return uTotal : Integer
  Returns the user's total.
"""
def total(tType, fType):
    global ongoing
    uTotal = 0
    dTotal = 0

    # Calculates the total for the user.
    for c in uCards:
        if c == ACE:
            if uTotal + 11 > 21:  # If ACE goes over.
                uTotal += 1  # ACE value = 1.
            elif uTotal + 11 <= 21:  # If ACE is fine.
                uTotal += 11  # ACE value = 11.
        else:  # Else card is not ACE.
            uTotal += c.value  # Add card value to user's total.

    # Type = Faced down.
    if tType == 'fd':
        if dCards[0] == ACE:
            dTotal = 11
        else:
            dTotal = dCards[0].value
        if fType == 'p':
            divider()
            print(f"~ User's Total: {uTotal}.")
            print(f"~ Dealer's Total: {dTotal} with a card faced down.")
            divider()
    else:  # Regular draw.
        for c in dCards:
            if c == ACE:
                if dTotal + 11 > 21:  # If ACE goes over.
                    dTotal += 1  # ACE value = 1.
                elif dTotal + 11 <= 21:  # If ACE is fine.
                    dTotal += 11  # ACE value = 11.
            else:  # Else card is not ACE.
                dTotal += c.value  # Add card value to user's total.
        # Prints out the total for the dealer.
        if fType == 'p':
            divider()
            print(f"~ User's Total: {uTotal}.")
            print(f"~ Dealer's Total: {dTotal}.")
            divider()

    # If user went overboard.
    if uTotal > 21:
        print('= User bust.')
        ongoing = False  # End game.

    if fType == 'rd':  # Returns Dealer's Total.
        return dTotal
    elif fType == 'ru':  # Returns User's Total.
        return uTotal


"""
Function: Stand action.
"""
def stand():
    global ongoing

    # Local Variables
    dTotal = total('', 'rd')  # Gets the total for the dealer.
    uTotal = total('', 'ru')  # Gets the total for the user.
    # Reveals dealer's total.
    divider()
    print(f"- Dealer's unknown card was a(n) {dCards[1].name}.")
    while dTotal < 17:  # Dealer's total is less than 17.
        draw('d')  # Draws a card for the dealer.
        dTotal = total('', 'rd')  # Updating the dealer's total.
    total('', 'p')  # Prints out the total.
    # Did dealer bust?
    if dTotal > 21:  # Dealer busted.
        print('= Dealer busts.\n= User wins!')
    # Dealer did not bust.
    elif uTotal == dTotal:  # Tied.
        print("= It's a push.")
    elif uTotal > dTotal:  # User won.
        print('= User wins!')
    elif dTotal > uTotal:  # Dealer won.
        print('= Dealer wins!')
    # Game ended.
    ongoing = False


"""
Function: Exits the program.
"""
def exitGame():
    sys.exit('Thank you for playing, goodbye!')


"""
Function: Asks the user a question.
----------
Parameters
----------
question : String
  Contains the question to ask the user.
answers : String *Arg
  Contains the list of possible answers.
"""
def question(toAsk, *answers):
    global uInput

    while True:  # Infinite loop.
        print(toAsk)  # Asks the user the question.
        # Prints out the possible answers.
        for i in range(0, len(answers)):
            print(f"[{i + 1}] {answers[i]}")
        # Accepts the input.
        uInput = input("Input: ")
        try:
            uInput = int(uInput)  # Tries to turn the input into an integer.
            if 0 < uInput <= len(answers):  # Input was between limit; valid input.
                break  # Break out of infinite loop.
            else:  # Input was over/under limit; invalid input.
                print('\nPlease enter a valid choice.')
                divider()
        except:  # Input was not an integer; invalid input.
            print('\nPlease enter a valid choice.')
            divider()


"""
Main code begins here.
"""
# Part 1: Play or Quit
question('Welcome to Blackjack!\nPlease choose an option.', "Play", "Quit")

while True:  # Infinite loop.
    if uInput == 1:  # User chose to play.
        resetGame()  # Restarts the game.
        # Part 2: Begins the game by drawing the cards.
        draw('u')  # Draws a card for the user.
        draw('d')  # Draws a card for the dealer.
        draw('u')  # Draws a card for the user.
        draw('df')  # Draws a card for the dealer, faced down.

        # Part 3: Calculates the total.
        total('fd', 'p')

        while ongoing:
            # Part 4: User's move.
            question('Would you like to hit, stand, or quit?', 'Hit', 'Stand', 'Quit')

            # Part 5: User's previous move.
            if uInput == 1:
                # User chose to hit.
                divider()
                draw('u')
                total('fd', 'p')
            elif uInput == 2:
                # User chose to stand.
                stand()
            else:
                # User chose to quit.
                exitGame()

        # Part 6: Play again?
        divider()
        question('What would you like to do?', 'Play Again', 'Shuffle Deck', 'Quit')
        if uInput == 1 or uInput == 2:  # Yes, user wants to play again.
            ongoing = True  # Reactivate loop.
            if uInput == 2:  # User chose to shuffle.
                divider()
                Cards.shuffle()  # Shuffles the deck.
                uInput = 1
        else:  # No, user does not want to play again.
            exitGame()
    else:  # User chose to quit.
        exitGame()
