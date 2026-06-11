import random

suits = ( "Hearts", "Diamonds", "Clubs", "Spades")
ranks = ( "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace" )
values = {"Two":2, "Three":3, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8, "Nine":9, "Ten":10, "Jack":11, "Queen":12, "King":13, "Ace":14}

playing = True

# Game Classes

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
           
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()
    
class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def remove_card(self):
        return self.cards.pop()
    
class Chips:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

### Game Functions ###

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Sorry, a bet must be an integer!")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, you do not have enough chips! You have: {chips.total}")
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal_one())

def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's': ")

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(player_hand, dealer_hand):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer_hand.cards[1])
    print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')

def show_all(player_hand, dealer_hand):
    print("\nDealer's Hand:", *dealer_hand.cards, sep='\n ')
    print("Dealer's Hand =", dealer_hand.cards[0].value + dealer_hand.cards[1].value)
    print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')
    print("Player's Hand =", player_hand.cards[0].value + player_hand.cards[1].value)

def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and Player tie! It's a push.")

### Game Logic ###

while True:
    print("Welcome to Blackjack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal_one())
    player_hand.add_card(deck.deal_one())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_one())
    dealer_hand.add_card(deck.deal_one())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing: 

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.cards[0].value + player_hand.cards[1].value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.cards[0].value + player_hand.cards[1].value <= 21:

        while dealer_hand.cards[0].value + dealer_hand.cards[1].value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.cards[0].value + dealer_hand.cards[1].value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.cards[0].value + dealer_hand.cards[1].value > player_hand.cards[0].value + player_hand.cards[1].value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.cards[0].value + dealer_hand.cards[1].value < player_hand.cards[0].value + player_hand.cards[1].value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)
