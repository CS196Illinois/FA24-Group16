import random
import copy
import csv
import numpy as np
from numpy.linalg import norm

# formating the deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Parameter List for AI evaluation. Right now, they will be: handStrength, boardRisk, oppBetPF, then more oppBets depending on the stage
aiParameterList = [0, 0, 0]
numBaseParameters = 3

preFlopDatabase = []
preFlopEVs = {}
flopDatabase = []
flopEVs = {}
turnDatabase = []
turnEVs = {}
riverDatabase = []
riverEVs = {}

with open("preFlop.csv", 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting each data row one by one
    for row in csvreader:
        preFlopDatabase.append(row[0:3])

with open("Flop.csv", 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting each data row one by one
    for row in csvreader:
        flopDatabase.append(row[0:3])

with open("Turn.csv", 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting each data row one by one
    for row in csvreader:
        turnDatabase.append(row[0:3])

with open("River.csv", 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting each data row one by one
    for row in csvreader:
        riverDatabase.append(row[0:3])

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
        if (type(combined[i].rank) != type(0)):
            newRank = ranks.index(str(combined[i].rank)) + 2
            combined[i].rank = newRank
    SC = sorted(combined, key=lambda x: x.rank, reverse=False)


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
        if (checkListForSF[len(checkListForSF) - 1].rank == 14):
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
        scoreIndex.append(28 + (14 * pairRankMax) + (pairRankSecond))
    elif hasPair:
        scoreIndex.append(14 + pairRankMax)
    scoreIndex.append(highCard)
    scoreIndex.append(SC[len(SC) - 2].rank)
    scoreIndex.append(SC[len(SC) - 3].rank)
    scoreIndex.append(SC[len(SC) - 4].rank)
    
    scoreIndex.sort(reverse=True)
    return scoreIndex

def calcHandEquity(hand, board_cards, deck, otherHand):
    handCopy = copy.deepcopy(hand)
    bashFrom = copy.deepcopy(deck.cards) + copy.deepcopy(otherHand)
    if (len(board_cards) == 0):
        return calcHandEquityPreFlop(handCopy)
    else:
        if (len(board_cards) == 3):
            count = 0
            sum = 0
            for i in range(len(bashFrom)):
                for j in range(i, len(bashFrom)):
                    bashList = copy.deepcopy(board_cards)
                    bashList.append(bashFrom[i])
                    bashList.append(bashFrom[j])
                    if len(bashList) != 5:
                        print("Error at bash")
                    scoresList = []
                    scoresList = scoresList + evaluate_hand(handCopy, bashList)
                    sum += scoresList[0]
                    count += 1
            return (sum / count)
        elif (len(board_cards) == 4):
            count = 0
            sum = 0
            for i in range(len(bashFrom)):
                bashList = copy.deepcopy(board_cards)
                bashList.append(bashFrom[i])
                scoresList = []
                scoresList = scoresList + evaluate_hand(handCopy, bashList)
                sum = sum + scoresList[0]
                count = count + 1
            return (sum / count)
        else:
            return evaluate_hand(handCopy, board_cards)

# This uses a neat little approximation from this website: https://steemit.com/poker/@daniel.dalo/how-to-calculate-preflop-equity-in-less-than-10-seconds#:~:text=The%20way%20to%20come%20up,if%20you%20hold%20a%20pair.
def calcHandEquityPreFlop(hand):
    handCopy = copy.deepcopy(hand)
    for i in range(2):
        newRank = ranks.index(str(handCopy[i].rank)) + 2
        if (newRank == 14):
            newRank = 15
        handCopy[i].rank = newRank
    SC = sorted(handCopy, key=lambda x: x.rank, reverse=False)
    score = (2 * SC[1].rank) + SC[0].rank + 20
    if (SC[0].rank == SC[1].rank): 
        score += 20
    if (SC[1].suit == SC[0].suit):
        score += 2
    return score

def calcBoardRisk(hand, board_cards, deck, otherHand):






































    return 

# Should return move and amount
def AI(parameterList):
    bleh = [0,0]
    np.array(bleh)
    bleh2 = [0,10]
    np.array(bleh2)
    cosine = np.dot(bleh, bleh2) / (norm(bleh) * norm(bleh2))
    if (len(parameterList) == 3):
        return
    if (len(parameterList) == 4):
        return 

































    if (len(parameterList) == 5):
        return


# bot decision to call/raise/fold, considering the current bet size and balance
def bot_move(bot_balance, playerBetStage, botBetStage):
    # this is where it gets janky. the AI will be given the game states handEquity, boardRisk, oppBet sizes, etc.
    if (playerBetStage > botBetStage):
        decision = random.choice(['call', 'raise', 'fold'])
    # this will likely where the AI is implemented later. This will involve adding an AI method that is called here 
    if (playerBetStage == botBetStage or playerBetStage == 0):
        decision = random.choice(['check', 'bet'])
    if decision == 'raise' or decision == 'bet':
        raise_amount = random.choice([5, 10, 50])
        if bot_balance >= raise_amount:
            return decision, raise_amount
        else:
            if (bot_balance <= 5):
                return 'call', bot_balance  # calls if raise attempt isn't affordable
    return decision, 0  # default is to call, check, or fold

# player's move with option to call the current bet or raise it
def player_bet(player_balance, playerBetStage, botBetStage):
    if (botBetStage > playerBetStage):
        decision = input(f"Your move (call, raise, fold). Current bet: ${playerBetStage}, Your balance: ${player_balance}: ").strip().lower()
        while decision not in ['call', 'raise', 'fold']:
            decision = input("Invalid move. Choose 'call', 'raise', or 'fold': ").strip().lower()
    elif (botBetStage == playerBetStage or botBetStage == 0):
        decision = input(f"Your move (check, bet). Your balance: ${player_balance}: ").strip().lower()
        while decision not in ['check', 'bet']:
            decision = input("Invalid move. Choose 'check' or 'bet': ").strip().lower()
    else:
        print("ERROR \n ERROR \n ERROR")
    
    if decision == 'bet' or decision == 'raise':
        bet_amount = int(input("Choose your bet/raise amount (5, 10, 50): "))
        while bet_amount not in [5, 10, 50] or bet_amount > player_balance:
            bet_amount = int(input("Invalid amount. Choose 5, 10, or 50 within your balance: "))
        return decision, bet_amount
    return decision, 0

# individual game function
player_balance = 200
bot_balance = 200
def texas_holdem(player_bal, bot_bal):
    # creating a deck
    deck = Deck()
    # giving player cards
    player_hand = deck.deal(2)
    # giving bot cards
    bot_hand = deck.deal(2)
    community_cards = []
    # giving the player and bot a starting balance
    playerBetContribution = 0
    botBetContribution = 0
    totalPot = 0
    player_balance = player_bal
    bot_balance = bot_bal


    print(f"Your hand: {player_hand}")
    print(f"Bot hand: [hidden]")

    # pre flop betting round 1
    playerBetPreFlop = 0
    botBetPreFlop = 0
    print("\n\nPre-flop betting")
    last_move = random.choice(["player","bot"])  # track last move to determine the turn
    initialPlays = 2

    # At the preflop, these two parameters are just handEquity and oppBetPreFlop, which occupy the first and third indices.
    # the second index is reserved for boardRisk, which is obviously not applicable right now
    aiParameterList = [0, 0, 0]
    aiParameterList[0] = calcHandEquity(bot_hand, [], deck, player_hand)

    # Right now it uses this while loop, which is the same throughout all the betting stages.
    # We should probably make this into a separate method in the future, but that's not really important right now.
    print("Your hand: ", player_hand)
    while (initialPlays > 0) or (playerBetPreFlop != botBetPreFlop):
        if last_move == "bot":
            player_move, player_bet_amount = player_bet(player_balance, playerBetPreFlop, botBetPreFlop)
            last_move = "player"

            if player_move == "fold":
                print("You folded. Bot wins!")
                bot_balance += playerBetPreFlop + botBetPreFlop + playerBetContribution + botBetContribution
                return player_balance, bot_balance
            elif player_move == "call":
                betDiff = botBetPreFlop - playerBetPreFlop
                player_balance -= betDiff  # match the current bet
                playerBetPreFlop += betDiff
                aiParameterList[2] = playerBetPreFlop
                break  # end the betting loop if player calls
            elif player_move == "raise" or player_move == "bet":
                if (player_move == "bet"):
                    playerBetPreFlop = player_bet_amount
                    player_balance -= playerBetPreFlop
                    aiParameterList[2] = playerBetPreFlop
                elif (player_move == "raise"):
                    betDiff = botBetPreFlop - playerBetPreFlop
                    player_balance -= (betDiff + player_bet_amount)
                    playerBetPreFlop = botBetPreFlop + player_bet_amount
                    aiParameterList[2] = playerBetPreFlop
        else:
            bot_move_choice, bot_raise_amount = bot_move(bot_balance, playerBetPreFlop, botBetPreFlop)
            last_move = "bot"

            if bot_move_choice == "check":
                print(f"Bot chooses to {bot_move_choice}")
            elif bot_move_choice == "fold":
                print("Bot folded. You win!")
                player_balance += playerBetPreFlop + botBetPreFlop + playerBetContribution + botBetContribution
                return player_balance, bot_balance
            elif bot_move_choice == "call":
                betDiff = playerBetPreFlop - botBetPreFlop
                bot_balance -= betDiff  # match the current bet
                botBetPreFlop += betDiff
                print(f"Bot chooses to {bot_move_choice}, Bet: {botBetPreFlop}")
                break  # end the betting loop if bot calls
            elif bot_move_choice == "raise" or bot_move_choice == "bet":
                if bot_move_choice == "bet":
                    botBetPreFlop = bot_raise_amount
                    bot_balance -= botBetPreFlop
                    print(f"Bot chooses to {bot_move_choice} {bot_raise_amount}")
                elif bot_move_choice == "raise":
                    betDiff = playerBetPreFlop - botBetPreFlop
                    bot_balance -= (betDiff + bot_raise_amount)
                    botBetPreFlop = playerBetPreFlop + bot_raise_amount
                    print(f"Bot chooses to {bot_move_choice} by {bot_raise_amount}")
        initialPlays -= 1
    
    playerBetContribution += playerBetPreFlop
    botBetContribution += botBetPreFlop
    totalPot += (playerBetPreFlop + botBetPreFlop)
    print("Pot Size: ", totalPot)
    print("Your current bet: ", playerBetContribution)
    print("Bot current bet: ", botBetContribution)



    # the flop - deal 3 community cards
    community_cards += deck.deal(3)

    # flop betting round 2
    print("\n\nFlop betting")
    print(f"Community cards after flop: {community_cards}")
    playerBetFlop = 0
    botBetFlop = 0
    initialPlays = 2

    # Appends the index for oppBetFlop
    aiParameterList.append(0)
    aiParameterList[0] = calcHandEquity(bot_hand, community_cards, deck, player_hand)
    # aiParameterList[1] = calcBoardRisk(bot_hand, community_cards, deck, player_hand)

    print("Your hand: ", player_hand)
    while (initialPlays > 0) or (playerBetFlop != botBetFlop):
        if last_move == "bot":
            player_move, player_bet_amount = player_bet(player_balance, playerBetFlop, botBetFlop)
            last_move = "player"

            if player_move == "fold":
                print("You folded. Bot wins!")
                bot_balance += playerBetFlop + botBetFlop + playerBetContribution + botBetContribution
                return player_balance, bot_balance
            elif player_move == "call":
                betDiff = botBetFlop - playerBetFlop
                player_balance -= betDiff  # match the current bet
                playerBetFlop += betDiff
                aiParameterList[3] = playerBetFlop
                break  # end the betting loop if player calls
            elif player_move == "raise" or player_move == "bet":
                if (player_move == "bet"):
                    playerBetFlop = player_bet_amount
                    player_balance -= playerBetFlop 
                    aiParameterList[3] = playerBetFlop
                elif (player_move == "raise"):
                    betDiff = botBetFlop - playerBetFlop
                    player_balance -= (betDiff + player_bet_amount)
                    playerBetFlop = botBetFlop + player_bet_amount
                    aiParameterList[3] = playerBetFlop
        else:
            bot_move_choice, bot_raise_amount = bot_move(bot_balance, playerBetFlop, botBetFlop)
            last_move = "bot"

            if bot_move_choice == "check":
                print(f"Bot chooses to {bot_move_choice}")
            if bot_move_choice == "fold":
                print("Bot folded. You win!")
                player_balance += playerBetFlop + botBetFlop + playerBetContribution + botBetContribution
                return player_balance, bot_balance
            elif bot_move_choice == "call":
                betDiff = playerBetFlop - botBetFlop
                bot_balance -= betDiff  # match the current bet
                botBetFlop += betDiff
                print(f"Bot chooses to {bot_move_choice}, Bet: {botBetFlop}")
                break  # end the betting loop if bot calls
            elif bot_move_choice == "raise" or bot_move_choice == "bet":
                if bot_move_choice == "bet":
                    botBetFlop = bot_raise_amount
                    bot_balance -= botBetFlop
                    print(f"Bot chooses to {bot_move_choice} {bot_raise_amount}")
                elif bot_move_choice == "raise":
                    betDiff = playerBetFlop - botBetFlop
                    bot_balance -= (betDiff + bot_raise_amount)
                    botBetFlop = playerBetFlop + bot_raise_amount
                    print(f"Bot chooses to {bot_move_choice} by {bot_raise_amount}")
        initialPlays -= 1

    playerBetContribution += playerBetFlop
    botBetContribution += botBetFlop
    totalPot += (playerBetFlop + botBetFlop)
    print("Pot Size: ", totalPot)
    print("Your current bet: ", playerBetContribution)
    print("Bot current bet: ", botBetContribution)



    # turn - deal another community card
    community_cards += deck.deal(1)

    # turn betting round 3
    print("\n\nTurn betting")
    print(f"Community cards after turn: {community_cards}")
    playerBetTurn = 0
    botBetTurn = 0
    initialPlays = 2

    aiParameterList.append(0)
    aiParameterList[0] = calcHandEquity(bot_hand, community_cards, deck, player_hand)
    # aiParameterList[1] = calcBoardRisk(bot_hand, community_cards, deck, player_hand)

    print("Your hand: ", player_hand)
    while (initialPlays > 0) or (playerBetTurn != botBetTurn):
        if last_move == "bot":
            player_move, player_bet_amount = player_bet(player_balance, playerBetTurn, botBetTurn)
            last_move = "player"

            if player_move == "fold":
                print("You folded. Bot wins!")
                bot_balance += playerBetTurn + botBetTurn + playerBetContribution + botBetContribution
                return player_balance, bot_balance
            elif player_move == "call":
                betDiff = botBetTurn - playerBetTurn
                player_balance -= betDiff  # match the current bet
                playerBetTurn += betDiff
                aiParameterList[4] = playerBetTurn
                break  # end the betting loop if player calls
            elif player_move == "raise" or player_move == "bet":
                if (player_move == "bet"):
                    playerBetTurn = player_bet_amount
                    player_balance -= playerBetTurn
                    aiParameterList[4] = playerBetTurn
                elif (player_move == "raise"):
                    betDiff = botBetTurn - playerBetTurn
                    player_balance -= (betDiff + player_bet_amount)
                    playerBetTurn = botBetTurn + player_bet_amount
                    aiParameterList[4] = playerBetTurn
        else:
            bot_move_choice, bot_raise_amount = bot_move(bot_balance, playerBetTurn, botBetTurn)
            last_move = "bot"

            if bot_move_choice == "check":
                print(f"Bot chooses to {bot_move_choice}")
            if bot_move_choice == "fold":
                print("Bot folded. You win!")
                player_balance += playerBetTurn + botBetTurn + playerBetContribution + botBetContribution
                return player_balance, bot_balance
            elif bot_move_choice == "call":
                betDiff = playerBetTurn - botBetTurn
                bot_balance -= betDiff  # match the current bet
                botBetTurn += betDiff
                print(f"Bot chooses to {bot_move_choice}, Bet: {botBetTurn}")
                break  # end the betting loop if bot calls
            elif bot_move_choice == "raise" or bot_move_choice == "bet":
                if bot_move_choice == "bet":
                    botBetTurn = bot_raise_amount
                    bot_balance -= botBetTurn
                    print(f"Bot chooses to {bot_move_choice} {bot_raise_amount}")
                elif bot_move_choice == "raise":
                    betDiff = playerBetTurn - botBetTurn
                    bot_balance -= (betDiff + bot_raise_amount)
                    botBetTurn = playerBetTurn + bot_raise_amount
                    print(f"Bot chooses to {bot_move_choice} by {bot_raise_amount}")
        initialPlays -= 1
    
    playerBetContribution += playerBetTurn
    botBetContribution += botBetTurn
    totalPot += (playerBetTurn + botBetTurn)
    print("Pot Size: ", totalPot)
    print("Your current bet: ", playerBetContribution)
    print("Bot current bet: ", botBetContribution)




    # river - deal final community card
    community_cards += deck.deal(1)

    # river betting round 4
    print("\n\nRiver betting (final round of betting)")
    print(f"Community cards after river: {community_cards}")
    playerBetRiver = 0
    botBetRiver = 0
    initialPlays = 2

    aiParameterList.append(0)
    aiParameterList[0] = calcHandEquity(bot_hand, community_cards, deck, player_hand)
    # aiParameterList[1] = calcBoardRisk(bot_hand, community_cards, deck, player_hand)

    print("Your hand: ", player_hand)
    while (initialPlays > 0) or (playerBetRiver != botBetRiver):
        if last_move == "bot":
            player_move, player_bet_amount = player_bet(player_balance, playerBetRiver, botBetRiver)
            last_move = "player"

            if player_move == "fold":
                print("You folded. Bot wins!")
                bot_balance += playerBetRiver + botBetRiver + playerBetContribution + botBetContribution
                return player_balance, bot_balance
            elif player_move == "call":
                betDiff = botBetRiver - playerBetRiver
                player_balance -= betDiff  # match the current bet
                playerBetRiver += betDiff
                aiParameterList[5] = playerBetRiver
                break  # end the betting loop if player calls
            elif player_move == "raise" or player_move == "bet":
                if (player_move == "bet"):
                    playerBetRiver = player_bet_amount
                    player_balance -= playerBetRiver
                    aiParameterList[5] = playerBetRiver
                elif (player_move == "raise"):
                    betDiff = botBetRiver - playerBetRiver
                    player_balance -= (betDiff + player_bet_amount)
                    playerBetRiver = botBetRiver + player_bet_amount
                    aiParameterList[5] = playerBetRiver
        else:
            bot_move_choice, bot_raise_amount = bot_move(bot_balance, playerBetRiver, botBetRiver)
            last_move = "bot"

            if bot_move_choice == "check":
                print(f"Bot chooses to {bot_move_choice}")
            if bot_move_choice == "fold":
                print("Bot folded. You win!")
                player_balance += playerBetRiver + botBetRiver + playerBetContribution + botBetContribution
                return player_balance, bot_balance
            elif bot_move_choice == "call":
                betDiff = playerBetRiver - botBetRiver
                bot_balance -= betDiff  # match the current bet
                botBetRiver += betDiff
                print(f"Bot chooses to {bot_move_choice}, Bet: {botBetRiver}")
                break  # end the betting loop if bot calls
            elif bot_move_choice == "raise" or bot_move_choice == "bet":
                if bot_move_choice == "bet":
                    botBetRiver = bot_raise_amount
                    bot_balance -= botBetRiver
                    print(f"Bot chooses to {bot_move_choice} {bot_raise_amount}")
                elif bot_move_choice == "raise":
                    betDiff = playerBetRiver - botBetRiver
                    bot_balance -= (betDiff + bot_raise_amount)
                    botBetRiver = playerBetRiver + bot_raise_amount
                    print(f"Bot chooses to {bot_move_choice} by {bot_raise_amount}")
        initialPlays -= 1
    
    playerBetContribution += playerBetRiver
    botBetContribution += botBetRiver
    totalPot += (playerBetRiver + botBetRiver)
    print("Pot Size: ", totalPot)
    print("Your current bet: ", playerBetContribution)
    print("Bot current bet: ", botBetContribution)

    # if the game is still going after final betting round do the showdown aka show the players cards
    print("\n\nShowdown!")
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
        player_balance += totalPot # just multiplied times the number of players aka 2
    elif (whoWon == "bot"):
        print("Bot wins the round!")
        bot_balance += totalPot # same logic as ^
    elif (whoWon == "draw"):
        print("Tie!")
        player_balance += playerBetContribution
        bot_balance += botBetContribution

    print(f"Your balance: ${player_balance}, Bot balance: ${bot_balance}")
    return player_balance, bot_balance

# start a game
player_balance, bot_balance = texas_holdem(player_balance, bot_balance)
if (player_balance > 0 and bot_balance > 0):
    keepPlaying = input("Would you like to keep playing? (yes, no): ")
    while keepPlaying not in ["yes", "no", "y", "n", "Yes", "No"]:
        keepPlaying = input("Invalid input, please try again (yes, no): ")
    while (keepPlaying == "yes" or keepPlaying == "Yes" or keepPlaying == "y"):
        print("\n\n\n")
        player_balance, bot_balance = texas_holdem(player_balance, bot_balance)
        keepPlaying = input("Would you like to keep playing? (yes, no): ")
        while keepPlaying not in ["yes", "no", "y", "n", "Yes", "No"]:
            keepPlaying = input("Invalid input, please try again (yes, no): ")
elif (bot_balance < 0):
    print("You busted the bot! Good job!")
elif (player_balance < 0):
    print("Sorry, you have no money left. Try again next time!")
