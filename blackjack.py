from os import system
import random

class card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if rank == "K" or rank == "Q" or rank =="J":
            self.score = 10
        elif rank == "A":
            self.score = 1
        else:
            self.score = int(rank)
    def show(self):
        print(self.suit + self.rank)

class dealer_deck:
    def __init__(self, deck):
        self.deck = deck
    def count(self):
        return len(self.deck)
    def display_deck(self):
        for suit,rank in self.deck:
            c = card(suit, rank)
            c.show()
    def create_deck(self):
        self.deck = []
        for suit in suit_list:
            for rank in rank_list:
                self.deck.append((suit , rank))
    def shuffle_deck(self):
        system("cls")
        print("The Dealer is shuffling...")
        random.shuffle(self.deck)
    def deal_a_card(self):
        card_deal = self.deck.pop()
        return card(card_deal[0], card_deal[1])
class hand:
    def __init__(self, card_list, player):
        self.card_list = card_list
        self.player = player
        self.ace = False

        for card in self.card_list:
            if card.rank =="A":
                self.ace = True
    def get_score(self):
        total = 0
        for cards in self.card_list:
            total += cards.score
        return total
    def show_hand(self, mask_dealer):
        print('\n{}s Hand:'.format(self.player))
        if mask_dealer is True:
            self.card_list[0].show()
            print('???')
        else:
            for i in range(0, len(self.card_list)):
                self.card_list[i].show()
    def hit(self):
        new = card_deck.deal_a_card()
        self.card_list.append(new)
        if new.rank == "A":
            self.ace = True
    def bust_check(self):
        if self.get_score() > 21:
            print("{} busted".format(self.player))
            return True
        else:
            return False
    def bj_check(self):
        if (self.get_score() == 10 and len(self.card_list) == 2 and self.ace is True):
            return True
        else:
            return False
def game_state(player_cond, dealer_cond):
    system('cls')
    dealer_hand.show_hand(dealer_cond)
    score = dealer_hand.get_score()
    bust = dealer_hand.bust_check()
    if dealer_hand.bj_check() is True and dealer_cond is False:
        print("Uh Oh! The Dealer has BlackJack!")
    elif (dealer_cond is False and dealer_hand.ace is True and bust is False and score + 10 < 22):
        print("Total: " + str(score) + "or" + str(score + 10))
    elif dealer_cond is False:
        print("Total: " + str(score))
    
    plyr_hand.show_hand(player_cond)
    score = plyr_hand.get_score()
    plyr_hand.bust_check()
    if plyr_hand.bj_check() is True:
        print("Congrats! You have Blackjack!!")
    elif plyr_hand.ace is True and bust is False and score + 10 < 22:
        print("Total: " + str(score) + "or" + str(score + 10))
    else:
        print("Total: " + str(score))

def plyr_turn():
    game_state(False, True)
    if plyr_hand.bj_check() is True:
        return True
    while plyr_hand.get_score() < 22:
        turn = input("Press 'H' to hit or 'S' to Stand: ")
        if turn.lower() == "h":
            plyr_hand.hit()
            game_state(False, True)
        elif turn.lower() == "s":
            return False

def dealer_turn():
    game_state(False, True)
    if dealer_hand.bj_check() is True:
        return
    while dealer_hand.get_score() < 33:
        if dealer_hand.get_score() < 17:
            dealer_hand.hit()
            game_state(False, False)
        else:
            game_state(False, False)
            return

def ace_score_adjust(hand):
    if hand.ace is False:
        return hand.get_score()
    else:
        unadjusted = hand.get_score()
        if (unadjusted + 11) > 21 and unadjusted < 22:
            return hand.get_score()
        elif (unadjusted + 11) < 22:
            return (unadjusted + 11)

def win_check(pot, blackjack):
    if ace_score_adjust(plyr_hand) > 21:
        winner = "Dealer"
        pot -= float(bet)
    elif blackjack is True:
        winner = "Player"
        pot += float(bet)
    elif ace_score_adjust(dealer_hand) > 21:
        winner = "Player"
        pot += float(bet)
    elif ace_score_adjust(dealer_hand) > ace_score_adjust(plyr_hand):
        winner = "Dealer"
        pot -= float(bet)
    elif ace_score_adjust(dealer_hand) < ace_score_adjust(plyr_hand):
        winner = "Player"
        pot += float(bet)
    else:
        winner = "Draw"
        print("Player and Dealer Draw")
    if winner != "Draw":
        print("{} wins this hand".format(winner))
    return pot 

heart = "Hrt"    
club = "Clb"
spade = "Spd"
diamond = "Dmnd"


suit_list = [heart, club, spade, diamond]
pic_cards = ["J", "Q", "K", "A"]
rank_list = [str(x) for x in range(2, 11)] + pic_cards

card_deck = dealer_deck([])
card_deck.create_deck()
card_deck.shuffle_deck()

game_flag = True
pot = 200.00

while game_flag is True:
    valid_bet = False
    message = ""
    bet = 0.00
    plyr_bj_check = False

    while valid_bet is False:

        if card_deck.count() < 10:
            card_deck.create_deck()
            card_deck.shuffle_deck()

        system('cls')
        print(f'Cash Pot is £{pot:.2f} {message}')
        bet = input('Please Place Your Bet: ')

        if bet.isalpha() is True:
            message = 'Last Bet Was Invalid.'
        elif float(bet) > pot:
            message = 'Last Bet Was Too High.Try again.'
        else:
            bet = float(bet)
            valid_bet = True
    
    plyr_hand = (hand([card_deck.deal_a_card(), card_deck.deal_a_card()], 'Player'))
    
    dealer_hand = (hand([card_deck.deal_a_card(), card_deck.deal_a_card()], 'Dealer'))
 
    blackjack = plyr_turn()

    if plyr_hand.get_score() > 21 or blackjack is True:
        pass

    else:
        dealer_turn()
    
    pot = win_check(pot, blackjack)
    another_game = input("Would you Like to play Another Game? (Y/N)")
    if another_game.lower() == 'n':
        game_flag = False
    elif pot <= 0.00:
        print("Game Over! No Money Left!")
        game_flag = False
    else:
        continue

