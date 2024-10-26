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

<<<<<<< HEAD
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

def evaluate_hand(hand, board_cards):
    # simple strength value that is the sum of hand + community cards right now
    combined = copy.deepcopy(hand) + copy.deepcopy(board_cards)
    for i in range(len(combined)):
        newRank = ranks.index(str(combined[i].rank)) + 2
        combined[i].rank = newRank
    SC = sorted(combined, key=lambda x: x.rank, reverse=False)
    print("Sorted Total Cards: ", SC)

    # Checks for Flush
    isFlush = False
    HeartCount = 0
    DiaCount = 0
    ClubCount = 0
    SpadeCount = 0
    for i in range(len(SC)):
        if (SC[i].suit == 'Hearts'):
            HeartCount += 1
        if (SC[i].suit == 'Clubs'):
            ClubCount += 1
        if (SC[i].suit == 'Spades'):
            SpadeCount += 1
        if (SC[i].suit == 'Diamonds'):
            DiaCount += 1
    if (DiaCount >= 5 or HeartCount >= 5 or ClubCount >= 5 or SpadeCount >= 5):
        isFlush = True
        # Insert code that takes all the cards that belong to the Flush, and add it to a separate list to check for Straight Flush
    
    # If isFlush is true, check for Straight flush
    if isFlush == True:
        isStraightFlush = False
        while i in range(4):
            if SC[0 + i].rank != (SC[1 + i].rank + 1):
                isStraight1 = False

    # if isFlush is False, check for just straight
    isStraight1 = True
    isStraight2 = True
    isStraight3 = True
    isStraight = False
    i = 0
    while i in range(4):
        if SC[0 + i].rank != (SC[1 + i].rank - 1):
            isStraight1 = False
        
        if SC[1 + i].rank != (SC[2 + i].rank - 1):
            isStraight2 = False
        
        if SC[2 + i].rank != (SC[3 + i].rank - 1):
            isStraight3 = False
        
        i += 1
    if (isStraight1 or isStraight2 or isStraight3):
        isStraight = True

    
    return isStraight, isFlush

# randome decision to call/raise/fold since i havent implemented anything futher
# adding logic for a bet size basic adding and subtracting from current balance and current bet
def bot_move(bot_balance, current_bet):
    # check logic here****
    if bot_balance <= current_bet:
        return "call", 0 # if you dont have enough to raise just call it all in
    decision = random.choice(['call', 'raise', 'fold'])
    if decision == 'raise':
        raise_amount = random.choice([5, 10, 50])
        if bot_balance >= current_bet + raise_amount:
            return 'raise', raise_amount
        else:
            return 'call', 0 # cant afford the raise attempt
    return decision, 0 # defualt is to call or fold

# players move
def player_bet(player_balance, current_bet):
    move = input(f"Your move (check, bet, fold). Current bet: ${current_bet}, Your balance: ${player_balance}: ").strip().lower()

    while move not in ['check', 'bet', 'fold']:
        # incase user doesn't say a normal move type
        move = input("Invalid move. Choose 'check', 'bet', or 'fold': ").strip().lower()

    if move == 'bet':
        # im putting 'USD' outside of the bet amount for simplicity don't want to edit if if people put $5...
        bet_amount = int(input(f"Choose your bet (5, 10, 50) USD. Your balance: ${player_balance}: "))
        while bet_amount not in [5, 10, 50] or bet_amount >= player_balance:
            bet_amount = int(input(f"Invalid bet amount, choose 5, 10, 50 within your balance: "))
        return "bet", bet_amount
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
    player_balance = 500 # $500usd
    bot_balance = 500

    print(f"Your hand: {player_hand}")
    print(f"Bot hand: [hidden]")

    # pre flop betting round 1
    current_bet = 0
    print("Pre-flop betting")
    # updated the moves to take in the move and bet amounts
    player_move, player_bet_amount = player_bet(player_balance, current_bet)
    bot_move_choice, bot_raise_amount = bot_move(bot_balance, current_bet)

    if player_move == 'fold':
        # easy enough lol
        print("You folded. Bot wins!")
        return
    elif bot_move_choice == 'fold':
        print("Bot folded. You win!")
        return
    else:
        current_bet += max(player_bet_amount, bot_raise_amount)
        player_balance -= current_bet
        bot_balance -= current_bet

    # tell player what the bot did for turn
    print(f"Bot chooses to {bot_move_choice}, Bet: {bot_raise_amount}")
    
    # the flop - just put 3 random cards into the community cards list and then tell the user what they are
    community_cards += deck.deal(3)
    print(f"Community cards after flop: {community_cards}")

    # after flop betting round 2
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
        player_balance -= current_bet
        bot_balance -= current_bet

    print(f"Bot chooses to {bot_move_choice}, Bet: {bot_raise_amount}")
    
    # burn and turn 1 - add another card to the community cards
    community_cards += deck.deal(1)
    print(f"Community cards after turn: {community_cards}")

    # betting round 3
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
        player_balance -= current_bet
        bot_balance -= current_bet

    print(f"Bot chooses to {bot_move_choice}, Bet: {bot_raise_amount}")

    # burn and turn final community card - should be 5 total cards in the community cards list
    community_cards += deck.deal(1)
    print(f"Community cards after river: {community_cards}")

    # betting round 4 (should be final one)
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
        player_balance -= current_bet
        bot_balance -= current_bet


    print(f"Bot chooses to {bot_move_choice}, Bet: {bot_raise_amount}")

    # ---------------- this stage is different then previous ones ----------------------------------

    # if the game is still going after final betting round do the showdown aka show the players cards
    print("Showdown!")
    player_best_hand = evaluate_hand(player_hand, community_cards)
    bot_best_hand = evaluate_hand(bot_hand, community_cards)

    print(f"Your hand: {player_best_hand}")
    print(f"Bot hand: {bot_best_hand}")

    # compare the hands, should return the higher hand - i havent added this yet right now its random still lol
    # -- updated to change player/bot balances no need for subtraction since thats done by making bets in the first place
    if random.choice([True, False]):
        print("You win the round!")
        player_balance += current_bet * 2 # just multiplied times the number of players aka 2
    else:
        print("Bot wins the round!")
        bot_balance += current_bet * 2 # same logic as ^

    print(f"Your balance: ${player_balance}, Bot balance: ${bot_balance}")
# start a game
texas_holdem()
