import random

# initialise constants
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10,'Q':10, 'K':10, 'A':11}

playing = True # boolean to control game state

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return "[{} of {}]".format(self.rank, self.suit)

class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                new_card = Card(suit,rank)
                self.deck.append(new_card)
    
    def __str__(self):
        return "".join([str(card) for card in self.deck])

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def __str__(self):
        return "".join([str(card) + " " for card in self.cards])
    
    def add_card(self,card):
        self.cards.append(card)
        self.value = self.value + values[card.rank]
        
        if card.rank == 'A':
            self.aces += 1
         
        self.adjust_for_ace()
        
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 1000  # starting value of $1,000
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

# Function to set bet amount
def take_bet(chips_total):
    while True:
        try:
            bet_amount = int(input("Please enter your bet amount: "))
        except:
            print("Invalid entry. Please try again.")
        else:
            if bet_amount <= chips_total:
                return bet_amount
                break
            else:
                print("Bet amount exceeds your total chips. Pleae try again.")

# Hit card function
def hit(deck,hand):
    hand.add_card(deck.deal())

# Retrieve input from player
def hit_or_stand(deck,hand):
    global playing
    
    while True:
        player_action = input("Would you like to Hit or Stand: ")

        if player_action == 'hit' or player_action == 'Hit':
            hit(deck,hand)
            break
        elif player_action == 'stand' or player_action == 'Stand':
            playing = False # toggle to end of player stage
            break
        else:
            print("Invalid choice. Please try again.")

# Display functions
def show_some(player,dealer):
    print("\n***DEALER***")
    print("Hand: " + str(dealer.cards[0]) + " [  ]")
    print("Value: ")
    print("\n\n")
    print("***PLAYER***")
    print("Hand: " + str(player))
    print("Value: " + str(player.value))
    print("\n--------------------")
    
def show_all(player,dealer):
    print("***DEALER***")
    print("Hand: " + str(dealer))
    print("Value: " + str(dealer.value))
    print("\n\n")
    print("***PLAYER***")
    print("Hand: " + str(player))
    print("Value: " + str(player.value))
    print("\n--------------------\n")

# end game scenarios
def player_busts():
    chip_stack.lose_bet()
    print("You are bust.")

def player_wins():
    chip_stack.win_bet()
    print("You won.")

def dealer_busts():
    chip_stack.win_bet()
    print("Dealer bust.")
    
def dealer_wins():
    chip_stack.lose_bet()
    print("Dealer won.")
    
def push():
    print("You and the Dealer tied.")


if __name__ == "__main__": 
    print("Welcome to Blackjack. \nThe aim of the game is to beat the Dealer! \n\n")
    print("Rules: Each card is worth their face value. Picture cards are worth 10. Ace is worth 1 or 11.")
    print("       If your hand value is greater than the Dealer then you win. If you exceed 21 then you lose. \n")

    # Set up the Player's chips. Default 1000
    chip_stack = Chips()

    while True:
        
        # Create & shuffle the deck
        new_deck = Deck()
        new_deck.shuffle()
        
        # Deal out starting cards
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_card(new_deck.deal())
        player_hand.add_card(new_deck.deal())
        dealer_hand.add_card(new_deck.deal())
        dealer_hand.add_card(new_deck.deal())
            
        # Prompt the Player for their bet
        chip_stack.bet = take_bet(chip_stack.total)
        
        # Show initial cards
        show_some(player_hand,dealer_hand)
        
        while playing:
            
            # Prompt for Player to Hit or Stand
            hit_or_stand(new_deck, player_hand)

            # Updated cards
            show_some(player_hand, dealer_hand)

            # If player's hand exceeds 21, player is bust
            if player_hand.value > 21:
                player_busts()
                break
        
        # If Player hasn't busted, play Dealer's hand 
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(new_deck, dealer_hand)

            # Show all cards
            show_all(player_hand, dealer_hand)
        
            # Check for different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts()
            elif player_hand.value > dealer_hand.value:
                player_wins()
            elif player_hand.value == dealer_hand.value:
                push()
            else:
                dealer_wins()

        # Inform Player of their chips total 
        print("Your current chip total is: " + str(chip_stack.total))

        # Ask to play again
        response = input("\nWould you like to play again? (Y/N)")
        if response == 'N' or response == 'n':
            print("Thanks for playing!")
            break
        else:
            playing = True