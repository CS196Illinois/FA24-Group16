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
import copy

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
    # Combines hand cards and board cards, then sorts it
    combined = copy.deepcopy(hand) + copy.deepcopy(board_cards)
    for i in range(len(combined)):
        newRank = ranks.index(str(combined[i].rank)) + 2
        combined[i].rank = newRank
    SC = sorted(combined, key=lambda x: x.rank, reverse=False)
    print("Sorted Total Cards: ", SC)


    # Block 1: Checks for Flush and Straight (and records in a dictionary the frequency of each rank)
    isFlush = False
    HeartCount, DiaCount, ClubCount, SpadeCount = 0, 0, 0, 0
    isStraight1, isStraight2, isStraight3, isStraight = True, True, True, False
    rankFreqDict = {}
    for i in range(len(SC)):
        rankFreqDict.update({SC[i].rank : rankFreqDict.get(SC[i].rank, 0) + 1})

        if (i < 4):
            if SC[0 + i].rank != (SC[1 + i].rank - 1):
                isStraight1 = False
                
            if SC[1 + i].rank != (SC[2 + i].rank - 1):
                isStraight2 = False
                
            if SC[2 + i].rank != (SC[3 + i].rank - 1):
                isStraight3 = False
        
        if (SC[i].suit == 'Hearts'):
            HeartCount += 1
        if (SC[i].suit == 'Clubs'):
            ClubCount += 1
        if (SC[i].suit == 'Spades'):
            SpadeCount += 1
        if (SC[i].suit == 'Diamonds'):
            DiaCount += 1
        
    if (isStraight1 or isStraight2 or isStraight3):
        if (isStraight3):
            straightHigh = SC[6].rank
        elif (isStraight2):
            straightHigh = SC[5].rank
        elif (isStraight1):
            straightHigh = SC[4].rank
        isStraight = True
    
    if (DiaCount >= 5 or HeartCount >= 5 or ClubCount >= 5 or SpadeCount >= 5):
        isFlush = True
        checkListForSF = []
        for i in range(len(SC)):
            if (DiaCount >= 5 and SC[i].suit == 'Diamonds'):
                checkListForSF.append(SC[i])
            if (HeartCount >= 5 and SC[i].suit == 'Hearts'):
                checkListForSF.append(SC[i]) 
            if (ClubCount >= 5 and SC[i].suit == 'Clubs'):
                checkListForSF.append(SC[i]) 
            if (SpadeCount >= 5 and SC[i].suit == 'Spades'):
                checkListForSF.append(SC[i])            
        flushHigh = checkListForSF[len(checkListForSF) - 1].rank
    
    # If isFlush is true, check for Straight flush
    isStraightFlush, isRoyal = False, False
    if isFlush == True:
        isStraightFlush1 = True
        isStraightFlush2 = True
        isStraightFlush3 = True
        if (len(checkListForSF) < 5):
            raise Exception("checkListForSF should have a length of at least 5!")
        for i in range(4):
            if ((len(checkListForSF) >= 5) and (checkListForSF[0 + i].rank != (checkListForSF[1 + i].rank - 1))):
                isStraightFlush1 = False
            
            if ((len(checkListForSF) >= 6) and (checkListForSF[1 + i].rank != (checkListForSF[2 + i].rank - 1))):
                isStraightFlush2 = False
            
            if ((len(checkListForSF) >= 7) and (checkListForSF[2 + i].rank != (checkListForSF[3 + i].rank - 1))):
                isStraightFlush3 = False
        
        if (len(checkListForSF) == 5 and isStraightFlush1):
            isStraightFlush = True
            sfHigh = checkListForSF[4].rank
        if (len(checkListForSF) == 6 and (isStraightFlush1 or isStraightFlush2)):
            isStraightFlush = True
            if (isStraightFlush1):
                sfHigh = checkListForSF[4].rank
            if (isStraightFlush2):
                sfHigh = checkListForSF[5].rank
        if (len(checkListForSF) == 7 and (isStraightFlush1 or isStraightFlush2 or isStraightFlush3)):
            isStraightFlush = True
            if (isStraightFlush1):
                sfHigh = checkListForSF[4].rank
            if (isStraightFlush2):
                sfHigh = checkListForSF[5].rank
            if (isStraightFlush3):
                sfHigh = checkListForSF[6].rank
        

    # If isStraightFlush is true, check for Royal flush
    if isStraightFlush:
        if (checkListForSF[len(checkListForSF - 1)].rank == 14):
            isRoyal == True




    # Block 2: Checks everything else: is it Quads? Full House? Etc?

    ## Initializes booleans/indicatorRanks. The indicatorRanks (exact rank of cards in the hand type) are used in the final calculation of the exact index - distinguishes between pair of Aces, and pair of Jacks, for example.
    isQuads, hasTrips, isFull, hasPair, isTwoPair = False, False, False, False, False
    quadRank, tripRank, pairRankMax, pairRankSecond, highCard = 0, 0, 0, 0, SC[len(SC) - 1].rank
    numOfPairs = 0

    # Initial Loop. Checks for quads/pairs/trips.
    for item in rankFreqDict:
        if rankFreqDict[item] == 4:
            isQuads = True
            quadRank = item
        if rankFreqDict[item] == 3: 
            hasTrips = True
            tripRank = item
        if rankFreqDict[item] == 2:
            hasPair = True
            if (numOfPairs == 0):
                pairRankMax = item
            elif (numOfPairs == 1):
                pairRankSecond = pairRankMax
                pairRankMax = item
            elif (numOfPairs >= 2):
                pairRankSecond = pairRankMax
                pairRankMax = item
            numOfPairs += 1
    
    # If hasTrips or hasPair is true, this code will distinguish Full Houses and Two Pairs
    if (hasTrips and hasPair):
        isFull = True
    if (numOfPairs >= 2):
        isTwoPair = True
    

    # Block 3: Final Score Calculator!
    scoreIndex = []
    if isRoyal:
        scoreIndex.append(840)
    
    if isStraightFlush:
        scoreIndex.append(814 + sfHigh)
    elif isFlush:
        scoreIndex.append(421 + flushHigh)
    elif isStraight:
        scoreIndex.append(407 + straightHigh)

    if isQuads:
        scoreIndex.append(800 + quadRank)
    elif isFull:
        scoreIndex.append(435 + (14 * tripRank) + (13 * pairRankMax))
    elif hasTrips:
        scoreIndex.append(393 + tripRank)
    elif isTwoPair:
        scoreIndex.append(28 + (14 * pairRankMax) + (13* pairRankSecond))
    elif hasPair:
        scoreIndex.append(14 + pairRankMax)
    else:
        scoreIndex.append(highCard)
        scoreIndex.append(SC[len(SC) - 2].rank)
        scoreIndex.append(SC[len(SC) - 3].rank)
        scoreIndex.append(SC[len(SC) - 4].rank)
    
    scoreIndex.sort(reverse=True)
    return scoreIndex

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

    # if the game is still going after final betting round do the showdown aka show the players cards
    print("Showdown!")
    player_best_hand = evaluate_hand(player_hand, community_cards)
    bot_best_hand = evaluate_hand(bot_hand, community_cards)

    print(f"Your hand: {player_best_hand}")
    print(f"Bot hand: {bot_best_hand}")

    # compare the hands, should return the higher hand - i havent added this yet right now its random still lol
    # -- updated to change player/bot balances no need for subtraction since thats done by making bets in the first place
    lenOfCompare = min(len(player_best_hand), len(bot_best_hand))
    whoWon = "player"
    for i in range(lenOfCompare):
        if (player_best_hand[i] > bot_best_hand[i]):
            whoWon = "player"
            break
        elif (bot_best_hand[i] > player_best_hand[i]):
            whoWon = "bot"
            break
        else:
            whoWon = "draw"

    if (whoWon == "player"):
        print("You win the round!")
        player_balance += current_bet * 2 # just multiplied times the number of players aka 2
    elif (whoWon == "bot"):
        print("Bot wins the round!")
        bot_balance += current_bet * 2 # same logic as ^
    elif (whoWon == "draw"):
        print("Tie!")
        player_balance += current_bet
        bot_balance += current_bet

    print(f"Your balance: ${player_balance}, Bot balance: ${bot_balance}")
# start a game
texas_holdem()
