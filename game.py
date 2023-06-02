from deck import Deck
from hand import Hand


class Game:
    MINIMUM_BET = 1

    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.bet = None
        self.deck = Deck()

    def start_game(self):
        player = self.player
        dealer = self.dealer
        start_choice = input("You are starting with ${}. Would you like to play a hand? (y/n) ".format(player.balance))
        while start_choice.lower() == "y":
            self.bet = self.get_bet()
            self.deal_cards()
            self.print_hands()
            self.player_turn()
            self.dealer_turn()
            self.print_hands()
            self.print_results()
            start_choice = input("Would you like to play another hand? (y/n) ")

    def get_bet(self):
        player = self.player
        bet = input("How much would you like to bet? ")
        while not bet.isdigit() or int(bet) < Game.MINIMUM_BET or int(bet) > player.balance:
            if not bet.isdigit():
                print("Please enter a number.")
            elif int(bet) < Game.MINIMUM_BET:
                print("The minimum bet is ${}.".format(Game.MINIMUM_BET))
            else:
                print("You only have ${}.".format(player.balance))
            bet = input("How much would you like to bet? ")
        player.balance -= int(bet)
        return int(bet)

    def deal_cards(self):
        player = self.player
        dealer = self.dealer
        deck = self.deck
        player_hand = Hand([deck.deal(), deck.deal()])
        dealer_hand = Hand([deck.deal(), deck.deal()])
        player.hand = player_hand
        dealer.hand = dealer_hand

    def print_hands(self):
        player = self.player
        dealer = self.dealer
        if len(player.hand) == 2 and len(dealer.hand) == 2:
            print("Your hand: {}".format(player.hand))
            print("Dealer's hand: {}, Unknown".format(dealer.hand[0]))
            return
        print("Your hand: {}".format(player.hand))
        print("Dealer's hand: {}".format(dealer.hand))

    def player_turn(self):
        player = self.player
        player_hand = player.hand
        deck = self.deck

        while player_hand.get_value() < 21:
            choice = input("Would you like to hit or stay? (h/s) ")
            if choice == "h":
                player_hand.add_to_hand(deck.deal())
                print("You are dealt: {}".format(player_hand))
            elif choice == "s":
                break
            else:
                print("Please enter h or s.")

    def dealer_turn(self):
        dealer = self.dealer
        dealer_hand = dealer.hand
        deck = self.deck
        while dealer_hand.get_value() < 17:
            dealer_hand.add_to_hand(deck.deal())
            print("The dealer hits.")
            print("Dealer is dealt: {}".format(dealer_hand))

    def print_results(self):
        player = self.player
        dealer = self.dealer
        player_hand = player.hand
        dealer_hand = dealer.hand
        if player_hand.get_value() > 21:
            print("You bust! You lose ${}.".format(self.bet))
        elif dealer_hand.get_value() > 21:
            print("The dealer busts! You win ${}.".format(self.bet))
            player.balance += 2 * self.bet
        elif player_hand.get_value() > dealer_hand.get_value():
            print("You win ${}.".format(self.bet))
            player.balance += 2 * self.bet
        elif dealer_hand.get_value() > player_hand.get_value():
            print("You lose ${}.".format(self.bet))
        else:
            print("You push.")