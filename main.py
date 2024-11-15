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

    
// custom betting amounts for front end dev
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
def bot_move(bot_balance, current_bet, total_pot, current_player_bet):
    bet_to_call = current_player_bet - current_bet  # amount bot needs to call
    
    if bot_balance <= bet_to_call:
        return "call", 0  # bot goes all in if it can't call
    
    decision = random.choice(['call', 'raise', 'fold'])
    if decision == 'raise':
        raise_amount = random.choice([5, 10, 50])
        # bot needs to call first, then add raise amount
        total_raise = bet_to_call + raise_amount
        if bot_balance >= total_raise:
            return 'raise', raise_amount
        else:
            return 'call', 0
    return decision, 0

def format_bot_message(move, bet_amount, current_player_bet, bot_current_bet):
    bet_to_call = current_player_bet - bot_current_bet
    if move == 'call':
        if bet_to_call > 0:
            return f"Bot decides to call ${bet_to_call}"
        return "Bot decides to check"
    elif move == 'raise':
        if bet_to_call > 0:
            return f"Bot decides to call ${bet_to_call} and raise ${bet_amount}"
        return f"Bot decides to raise ${bet_amount}"
    elif move == 'fold':
        return "Bot decides to fold"
    return ""

def player_bet(player_balance, current_bet, total_pot, current_bot_bet):
    bet_to_call = current_bot_bet - current_bet  # amount needed to call
    
    if current_bot_bet == 0:
        move = input(f"Your move (check, bet, fold). Your balance: ${player_balance}, Pot: ${total_pot}: ").strip().lower()
        while move not in ['check', 'bet', 'fold']:
            move = input("Invalid move. Choose 'check', 'bet', or 'fold': ").strip().lower()
    else:
        move = input(f"Your move (call, raise, fold). Need ${bet_to_call} to call. Your balance: ${player_balance}, Pot: ${total_pot}: ").strip().lower()
        while move not in ['call', 'raise', 'fold']:
            move = input("Invalid move. Choose 'call', 'raise', or 'fold': ").strip().lower()

    if move == 'bet' or move == 'raise':
        if move == 'raise':
            print(f"You need to call ${bet_to_call} plus your raise amount")
        bet_amount = int(input("Choose your bet/raise amount (5, 10, 50): "))
        while bet_amount not in [5, 10, 50] or (bet_amount + bet_to_call) > player_balance:
            bet_amount = int(input("Invalid amount. Choose 5, 10, or 50 within your balance (including call amount): "))
        return move, bet_amount
    return move, 0

def texas_holdem():
    deck = Deck()
    player_hand = deck.deal(2)
    bot_hand = deck.deal(2)
    community_cards = []
    player_balance = 500
    bot_balance = 500
    total_pot = 0

    # define betting rounds here
    betting_rounds = ['pre-flop', 'flop', 'turn', 'river']

    print(f"Your hand: {player_hand}")
    print(f"Bot hand: [hidden]")

    # track individual bets for this round
    player_current_bet = 0
    bot_current_bet = 0

    for round_name in betting_rounds:
        print(f"\n{round_name.upper()} betting round")

        if round_name == 'pre-flop':
            # pre-flop phase: no community cards
            community_cards = []
        elif round_name == 'flop':
            community_cards += deck.deal(3)
            print(f"Community cards after flop: {community_cards}")
        elif round_name in ['turn', 'river']:
            community_cards += deck.deal(1)
            print(f"Community cards after {round_name}: {community_cards}")

        # reste round-specific bets
        player_current_bet = 0
        bot_current_bet = 0
        betting_active = True
        last_raiser = None
        consecutive_checks = 0  # track if both players check consecutively

        while betting_active:
            # player's turn
            player_move, player_bet_amount = player_bet(player_balance, player_current_bet, total_pot, bot_current_bet)

            if player_move == 'fold':
                print("You folded. Bot wins!")
                bot_balance += total_pot
                return
            elif player_move in ['call', 'check']:
                amount_to_call = bot_current_bet - player_current_bet
                if player_balance <= amount_to_call:
                    amount_to_call = player_balance  # all-in
                player_balance -= amount_to_call
                player_current_bet += amount_to_call
                total_pot += amount_to_call

                if player_move == 'check':
                    consecutive_checks += 1
                else:
                    consecutive_checks = 0
            elif player_move in ['bet', 'raise']:
                amount_to_call = bot_current_bet - player_current_bet
                total_bet = amount_to_call + player_bet_amount
                player_balance -= total_bet
                player_current_bet += total_bet
                total_pot += total_bet
                last_raiser = 'player'
                consecutive_checks = 0  # reset if player raises

            # bot's turn
            bot_move_choice, bot_raise_amount = bot_move(bot_balance, bot_current_bet, total_pot, player_current_bet)
            print("\n" + format_bot_message(bot_move_choice, bot_raise_amount, player_current_bet, bot_current_bet))

            if bot_move_choice == 'fold':
                print("Bot folded. You win!")
                player_balance += total_pot
                return
            elif bot_move_choice in ['call', 'check']:
                amount_to_call = player_current_bet - bot_current_bet
                if bot_balance <= amount_to_call:
                    amount_to_call = bot_balance  # all-in
                    print(f"Bot is ALL IN with ${amount_to_call}!")
                bot_balance -= amount_to_call
                bot_current_bet += amount_to_call
                total_pot += amount_to_call

                if bot_move_choice == 'check':
                    consecutive_checks += 1
                else:
                    consecutive_checks = 0
            elif bot_move_choice == 'raise':
                amount_to_call = player_current_bet - bot_current_bet
                total_bet = amount_to_call + bot_raise_amount
                bot_balance -= total_bet
                bot_current_bet += total_bet
                total_pot += total_bet
                last_raiser = 'bot'
                consecutive_checks = 0  # reset if bot raises

            print(f"Current pot: ${total_pot}")
            print(f"Your balance: ${player_balance}, Bot balance: ${bot_balance}")

            # check if both players have checked consecutively or one has called and the other checked
            if consecutive_checks >= 2 or (player_move == 'call' and bot_move_choice == 'check') or (bot_move_choice == 'call' and player_move == 'check'):
                print(f"\nBoth players have completed the betting round. Moving to the next stage: {round_name.upper()}.")
                betting_active = False

        # after betting round, move to next stage by dealing community cards (if necessary)
        if round_name == 'pre-flop':  # if it's the pre-flop, go to the flop round
            print("Both players checked or completed their actions. Moving to the next stage: the flop.")
        else:
            print(f"Dealing community cards after {round_name}.")
            continue  # next stage (flop, turn, river)

    # showdown logic
    print("\nShowdown!")
    print(f"Your hand: {player_hand}")
    print(f"Bot hand: {bot_hand}")
    print(f"Community cards: {community_cards}")

    player_best_hand = evaluate_hand(player_hand, community_cards)
    bot_best_hand = evaluate_hand(bot_hand, community_cards)

    print(f"Your best hand: {player_best_hand}")
    print(f"Bot best hand: {bot_best_hand}")

    # comparison logic
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

    # award pot to winner
    if whoWon == "player":
        print("You win the round!")
        player_balance += total_pot
    elif whoWon == "bot":
        print("Bot wins the round!")
        bot_balance += total_pot
    else:
        print("Tie! Splitting the pot")
        split_amount = total_pot // 2
        player_balance += split_amount
        bot_balance += split_amount
        # handle odd chip if pot is odd
        if total_pot % 2 == 1:
            player_balance += 1  # give odd chip to player

    print(f"Final balances - You: ${player_balance}, Bot: ${bot_balance}")

# start a game
texas_holdem()
