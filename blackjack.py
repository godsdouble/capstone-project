import random


class Chips():

    def __init__(self):
        self.stack = 1000

    def __str__(self):
        return f'Player has {self.stack} chips.'

    # Check if player has enough chips in stack
    def place_bet(self, player_bet):
        self.player_bet = player_bet
        self.stack -= self.player_bet
        print(f'Player now has {self.stack} chips.\n')

    def win(self, winnings):
        self.winnings = 2 * winnings
        self.stack += self.winnings
        print(f'Player now has {self.stack} chips.\n')


class Card():

    # Creates a card
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank, self.value = rank

    def __str__(self):
        return f'[{self.rank}{self.suit}]'


class Deck():

    # Create empty deck holder
    deck = []
    # Define four suits
    suits = ('♥', '♠', '♦', '♣')
    # Define ranks and their associated value
    ranks = (('2', 2), ('3', 3), ('4', 4), ('5', 5),
             ('6', 6), ('7', 7), ('8', 8), ('9', 9),
             ('10', 10), ('J', 10), ('Q', 10), ('K', 10),
             ('A', 11))

    def __init__(self, nod=1):
        # pass in number of decks (nod) used to shuffle (default is 1 deck)
        self.nod = nod
        self.generate_deck()
        self.mix_it()

    def __str__(self):
        full_deck = ''
        for card in self.deck:
            full_deck += f'{card.__str__()}'
        return f'{full_deck}'

    def generate_deck(self):
        # Create a deck in order from 2 to A for all 4 suits. Total 52 cards.
        for i in range(self.nod):
            for suit in Deck.suits:
                for rank in Deck.ranks:
                    self.deck.append(Card(suit, rank))

    def mix_it(self):
        # Shuffle the deck.
        random.shuffle(self.deck)

    def deal_it(self):
        try:
            # Return one card and remove it from deck.
            return self.deck.pop()
        except:
            # If no more cards in deck, re initialize deck the deck.
            self.__init__()
            return self.deck.pop()


class Hand():

    # Initialize the hand with two random cards (remove it from deck)
    def __init__(self):
        self.card1, self.card2 = deck.deal_it(), deck.deal_it()
        self.hand = [self.card1, self.card2]

    def __str__(self):
        cards_in_hand = ''
        for card in self.hand:
            cards_in_hand += card.__str__()
        return f'{cards_in_hand}'

    # Ask for new card in hand (remove it from deck)
    def new_card(self):
        self.hand.append(deck.deal_it())

    # Check value of hand
    def total_value(self):
        sum_of = 0
        for card in self.hand:
            sum_of += card.value
        bust = sum_of > 21
        aces = self.n_ace()

        # If hand value is over 21 and Ace exists in hand,
        # reduce Ace to value of 1 and check if bust again
        # until there are no Aces.
        while bust and aces != 0:
            if sum_of > 21 and aces != 0:
                sum_of -= 10
                aces -= 1
        return sum_of

    # Count number of Aces in hand.
    # Ace value is 11 but can also be 1 if player exceeds 21.
    def n_ace(self):
        self.num_ace = 0
        for card in self.hand:
            if card.rank == 'A':
                self.num_ace += 1
        return self.num_ace


class DealerHand(Hand):

    # Keep first card hidden from user
    def __str__(self):
        cards_in_hand = ''
        for i in range(1, len(self.hand)):
            cards_in_hand += self.hand[i].__str__()
        return f'[?]{cards_in_hand}'

    def revealed_card(self):
        return self.hand[1]

    # If player does not bust and selects stand,
    # Reveal card before dealer plays
    def reveal(self):
        cards_in_hand = ''
        for card in self.hand:
            cards_in_hand += card.__str__()
        return f'{cards_in_hand}'


def player_bet():
    print("Welcome to BlackJack!\n")
    print(f"{player_stack}\n")
    while True:
        try:
            bet = int(input('How much would you like to bet?: \n'))
        except:
            print('Please enter valid amount.\n')
            continue
        else:
            if bet >= 0 and bet <= player_stack.stack:
                return bet
            else:
                print("You don't have enough chips! \n")


def display_hands():
    print(
        f"Player's hand: {player_hand}, \
        total value: {player_hand.total_value()}\n")
    print(
        f"Dealer's hand: {dealer_hand}, \
        card value: {dealer_hand.revealed_card().value}\n")


def display_both_hands():
    print(
        f"Player's hand: {player_hand}, \
        total value: {player_hand.total_value()}\n")
    print(
        f"Dealers's hand: {dealer_hand.reveal()}, \
        total value: {dealer_hand.total_value()}\n")


def hit_me():
    while True:
        choice = input('Hit or Stand: \n').lower()
        if choice == 'hit':
            player_hand.new_card()
            if player_hand.total_value() > 21:
                choice = 'bust'
                display_both_hands()
            else:
                display_hands()
            return choice
        elif choice == 'stand':
            return choice
        else:
            print('Please select one of the following options: \n')
            continue


if __name__ == '__main__':

    player_stack = Chips()
    deck = Deck(6)

    game_on = True

    while game_on:
        if player_stack.stack == 0:
            print('You have no more chips!\n')
            break

        # Initialize hands
        player_hand = Hand()
        dealer_hand = DealerHand()

        # Take player bet
        this_turn_bet = player_bet()
        player_stack.place_bet(this_turn_bet)

        # Show player hand and dealer hidden hand
        display_hands()

        player_turn = True

        while player_turn:
            # Allow player to hit or stand
            choice = hit_me()
            if choice == 'hit':
                print('Player hits!\n')
                continue
            elif choice == 'bust':
                print('Player busts!\n')
                player_turn = False
            elif choice == 'stand':
                print('Player stands!\n')
                print('--------------------')
                player_turn = False

        if choice == 'bust':
            dealer_turn = False
        else:
            dealer_turn = True

        dealer_stand = False
        dealer_bust = False

        while dealer_turn:
            if dealer_hand.total_value() < 17:
                print('Dealer hits!\n')
                dealer_hand.new_card()
                display_both_hands()
                continue
            elif dealer_hand.total_value() > 21:
                print('Dealer busts!\n')
                dealer_bust = True
                dealer_turn = False
            else:
                print('Dealer stands!\n')
                display_both_hands()
                print('--------------------')
                dealer_stand = True
                dealer_turn = False

        if choice == 'bust':
            print(f'Player loses!\n')
        elif dealer_bust:
            print(f'Player wins {this_turn_bet}!\n')
            player_stack.win(this_turn_bet)
        elif dealer_stand and \
                dealer_hand.total_value() < player_hand.total_value():
            print(f'Player wins {this_turn_bet}!\n')
            player_stack.win(this_turn_bet)
        elif dealer_stand and \
                dealer_hand.total_value() > player_hand.total_value():
            print(f'Player loses!\n')
        elif dealer_stand and \
                dealer_hand.total_value() == player_hand.total_value():
            print(f'Push.\n')
            player_stack.win(int((this_turn_bet + 1) / 2))

        replay = input('Would you like to place a bet? (Y/N): ').lower()
        if replay == 'n':
            game_on = False
        else:
            continue

    print('Thanks for playing.')
