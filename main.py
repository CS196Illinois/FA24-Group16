"""
Ok guys, right now i have a basic poker game setup with python, this is meant to be a one v one against a bot.
right now, all of the bots decisions are random, like e.g. check, bet, fold and at the end of a full round aka
the river/community are all shown and a showdown has occured or someone has folded, it randomly decides the
winner with a simpel true or false.

Also, I have not added in bet size logic or the logic for evaluating_hands() which would be run when a showdown
occurs. i think the evaluating hands should not be too bad to implement, but i am working on the bet size right
now, i think i will just need to initilize each player with a ceratin total money value and then increment/decrement
the value by the bet - a little restuctruing of my player_bet(), bot_move(), evaluate_hand() function and the main
texas_holdem() function.
"""

"""
10/17/24 v2 update
-- implemented a money system

-- still need to implement cycles aka when i bet and bot raisees we go again in the same stage
=======
>>>>>>> 47581553507fd4ef1d489fa318a546f0ea29c1c5
-- still need card evaluation logic
-- still need bot betting logic (can be based on card evalutaion logic)
-- still need to implement a database for storing past games for modeltraining purposes
"""

'''
final showdown:
current hand + community cards - sum up the ranks
    - run is_sraight() and is_flush() if both == true we have a royal_flush()
    - run is...

'''

import random

# formating the deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# card object
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        # displaying a card like 'A of Spades'
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal(self, num):
        dealt_cards = []
        # stack like structure to deal cards out
        for _ in range(num):
            dealt_cards.append(self.cards.pop())
        return dealt_cards

# not sure how we want to do it yet but evaluate the hand strength
def evaluate_hand(hand, community_cards):
    # simple strength value that is the sum of hand + community cards right now
    combined = hand + community_cards
    return combined

# bot decision to call/raise/fold, considering the current bet size and balance
def bot_move(bot_balance, current_bet):
    if bot_balance <= current_bet:
        return "call", 0  # bot goes all in if it can't raise further
    decision = random.choice(['call', 'raise', 'fold'])
    if decision == 'raise':
        raise_amount = random.choice([5, 10, 50])
        if bot_balance >= current_bet + raise_amount:
            return 'raise', raise_amount
        else:
            return 'call', 0  # calls if raise attempt isn't affordable
    return decision, 0  # default is to call or fold

# player's move with option to call the current bet or raise it
def player_bet(player_balance, current_bet):
    if current_bet == 0:
        move = input(f"Your move (check, bet, fold). Your balance: ${player_balance}: ").strip().lower()
        while move not in ['check', 'bet', 'fold']:
            move = input("Invalid move. Choose 'check', 'bet', or 'fold': ").strip().lower()
    else:
        move = input(f"Your move (call, raise, fold). Current bet: ${current_bet}, Your balance: ${player_balance}: ").strip().lower()
        while move not in ['call', 'raise', 'fold']:
            move = input("Invalid move. Choose 'call', 'raise', or 'fold': ").strip().lower()

    if move == 'bet' or move == 'raise':
        bet_amount = int(input("Choose your bet/raise amount (5, 10, 50): "))
        while bet_amount not in [5, 10, 50] or bet_amount > player_balance:
            bet_amount = int(input("Invalid amount. Choose 5, 10, or 50 within your balance: "))
        return move, bet_amount
    return move, 0

# individual game function
def texas_holdem():
    # creating a deck
    deck = Deck()
    # giving player cards
    player_hand = deck.deal(2)
    # giving bot cards
    bot_hand = deck.deal(2)
    community_cards = []
    # giving the player and bot a starting balance
    player_balance = 500  # $500 usd
    bot_balance = 500

    print(f"Your hand: {player_hand}")
    print(f"Bot hand: [hidden]")

    # pre flop betting round 1
    current_bet = 0
    print("Pre-flop betting")
    last_move = None  # track last move to determine the turn
    player_move = None
    player_bet_amount = 0
    bot_bet_amount = 0

    while True:
        if last_move == "bot":
            player_move, player_bet_amount = player_bet(player_balance, current_bet)
            last_move = "player"

            if player_move == "fold":
                print("You folded. Bot wins!")
                return
            elif player_move == "call":
                player_balance -= current_bet  # match the current bet
                current_bet += bot_raise_amount
                break  # end the betting loop if player calls
            elif player_move == "raise":
                current_bet += player_bet_amount
                player_balance -= player_bet_amount
        else:
            bot_move_choice, bot_raise_amount = bot_move(bot_balance, current_bet)
            print(f"Bot chooses to {bot_move_choice}, Bet: {bot_raise_amount}")
            last_move = "bot"

            if bot_move_choice == "fold":
                print("Bot folded. You win!")
                return
            elif bot_move_choice == "call":
                bot_balance -= current_bet  # match the current bet
                break  # end the betting loop if bot calls
            elif bot_move_choice == "raise":
                current_bet += bot_raise_amount
                bot_balance -= bot_raise_amount

    # the flop - deal 3 community cards
    community_cards += deck.deal(3)
    print(f"Community cards after flop: {community_cards}")

    # flop betting round 2
    print("Flop betting")
    player_move, player_bet_amount = player_bet(player_balance, current_bet)
    bot_move_choice, bot_raise_amount = bot_move(bot_balance, current_bet)

    if player_move == 'fold':
        print("You folded. Bot wins!")
        return
    elif bot_move_choice == 'fold':
        print("Bot folded. You win!")
        return
    else:
        current_bet += max(player_bet_amount, bot_raise_amount)
        player_balance -= player_bet_amount
        bot_balance -= bot_raise_amount

    print(f"Bot chooses to {bot_move_choice}, Bet: {bot_raise_amount}")

    # turn - deal another community card
    community_cards += deck.deal(1)
    print(f"Community cards after turn: {community_cards}")

    # turn betting round 3
    print("Turn betting")
    player_move, player_bet_amount = player_bet(player_balance, current_bet)
    bot_move_choice, bot_raise_amount = bot_move(bot_balance, current_bet)

    if player_move == 'fold':
        print("You folded. Bot wins!")
        return
    elif bot_move_choice == 'fold':
        print("Bot folded. You win!")
        return
    else:
        current_bet += max(player_bet_amount, bot_raise_amount)
        player_balance -= player_bet_amount
        bot_balance -= bot_raise_amount

    print(f"Bot chooses to {bot_move_choice}, Bet: {bot_raise_amount}")

    # river - deal final community card
    community_cards += deck.deal(1)
    print(f"Community cards after river: {community_cards}")

    # river betting round 4
    print("Final betting (river)")
    player_move, player_bet_amount = player_bet(player_balance, current_bet)
    bot_move_choice, bot_raise_amount = bot_move(bot_balance, current_bet)

    if player_move == 'fold':
        print("You folded. Bot wins!")
        return
    elif bot_move_choice == 'fold':
        print("Bot folded. You win!")
        return
    else:
        current_bet += max(player_bet_amount, bot_raise_amount)
        player_balance -= player_bet_amount
        bot_balance -= bot_raise_amount

    print(f"Bot chooses to {bot_move_choice}, Bet: {bot_raise_amount}")

    # showdown phase
    print("Showdown!")
    player_best_hand = evaluate_hand(player_hand, community_cards)
    bot_best_hand = evaluate_hand(bot_hand, community_cards)

    print(f"Your hand: {player_best_hand}")
    print(f"Bot hand: {bot_best_hand}")

    # determine winner (currently random)
    if random.choice([True, False]):
        print("You win the round!")
        player_balance += current_bet * 2
    else:
        print("Bot wins the round!")
        bot_balance += current_bet * 2

    print(f"Your balance: ${player_balance}, Bot balance: ${bot_balance}")

# start a game
texas_holdem()
