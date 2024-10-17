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

# randome decision to call/raise/fold since i havent implemented anything futher
def bot_move():
    return random.choice(['call', 'raise', 'fold'])

# players move
def player_bet():
    move = input("Your move (check, bet, fold): ").strip().lower()
    while move not in ['check', 'bet', 'fold']:
        # incase user doesn't say a normal move type
        move = input("Invalid move. Choose 'check', 'bet', or 'fold': ").strip().lower()
    return move

# individual game function
def texas_holdem():
    # creating a deck
    deck = Deck()
    # giving player cards
    player_hand = deck.deal(2)
    # giving bot cards
    bot_hand = deck.deal(2)
    community_cards = []

    print(f"Your hand: {player_hand}")
    print(f"Bot hand: [hidden]")

    # pre flop betting round 1
    print("Pre-flop betting")
    player_move = player_bet()
    bot_move_choice = bot_move()

    if player_move == 'fold':
        # easy enough lol
        print("You folded. Bot wins!")
        return
    elif bot_move_choice == 'fold':
        print("Bot folded. You win!")
        return

    # tell player what the bot did for turn
    print(f"Bot chooses to {bot_move_choice}")
    
    # the flop - just put 3 random cards into the community cards list and then tell the user what they are
    community_cards += deck.deal(3)
    print(f"Community cards after flop: {community_cards}")

    # after flop betting round 2
    print("Flop betting")
    player_move = player_bet()
    bot_move_choice = bot_move()

    if player_move == 'fold':
        print("You folded. Bot wins!")
        return
    elif bot_move_choice == 'fold':
        print("Bot folded. You win!")
        return

    print(f"Bot chooses to {bot_move_choice}")
    
    # burn and turn 1 - add another card to the community cards
    community_cards += deck.deal(1)
    print(f"Community cards after turn: {community_cards}")

    # betting round 3
    print("Turn betting")
    player_move = player_bet()
    bot_move_choice = bot_move()

    if player_move == 'fold':
        print("You folded. Bot wins!")
        return
    elif bot_move_choice == 'fold':
        print("Bot folded. You win!")
        return

    print(f"Bot chooses to {bot_move_choice}")

    # burn and turn final community card - should be 5 total cards in the community cards list
    community_cards += deck.deal(1)
    print(f"Community cards after river: {community_cards}")

    # betting round 4 (should be final one)
    print("Final betting (river)")
    player_move = player_bet()
    bot_move_choice = bot_move()

    if player_move == 'fold':
        print("You folded. Bot wins!")
        return
    elif bot_move_choice == 'fold':
        print("Bot folded. You win!")
        return

    print(f"Bot chooses to {bot_move_choice}")

    # if the game is still going after final betting round do the showdown aka show the players cards
    print("Showdown!")
    player_best_hand = evaluate_hand(player_hand, community_cards)
    bot_best_hand = evaluate_hand(bot_hand, community_cards)

    print(f"Your hand: {player_best_hand}")
    print(f"Bot hand: {bot_hand}")

    # compare the hands, should return the higher hand - i havent added this yet right now its random still lol
    if random.choice([True, False]):
        print("You win the round!")
    else:
        print("Bot wins the round!")

# start a game
texas_holdem()
