import random
import copy

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def to_dict(self):
        return {
            'rank': self.rank,
            'suit': self.suit
        }

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal(self, num):
        dealt_cards = []
        for _ in range(num):
            dealt_cards.append(self.cards.pop())
        return dealt_cards

def evaluate_hand(hand, board_cards):
    combined = copy.deepcopy(hand) + copy.deepcopy(board_cards)
    for i in range(len(combined)):
        newRank = ranks.index(str(combined[i].rank)) + 2
        combined[i].rank = newRank
    SC = sorted(combined, key=lambda x: x.rank, reverse=False)
    print("Sorted Total Cards: ", SC)

    isFlush = False
    HeartCount, DiaCount, ClubCount, SpadeCount = 0, 0, 0, 0
    isStraight1, isStraight2, isStraight3, isStraight = False, False, False, False
    rankFreqDict = {}

    # Check for straights only if we have enough cards
    if len(SC) >= 5:
        isStraight1 = True
        isStraight2 = True
        isStraight3 = True
        for i in range(4):
            if i + 1 < len(SC) and SC[i].rank != (SC[i + 1].rank - 1):
                isStraight1 = False
            if i + 2 < len(SC) and SC[i + 1].rank != (SC[i + 2].rank - 1):
                isStraight2 = False
            if i + 3 < len(SC) and SC[i + 2].rank != (SC[i + 3].rank - 1):
                isStraight3 = False

    # Count suits and build rank frequency dictionary
    for card in SC:
        rankFreqDict[card.rank] = rankFreqDict.get(card.rank, 0) + 1
        if card.suit == 'Hearts':
            HeartCount += 1
        elif card.suit == 'Clubs':
            ClubCount += 1
        elif card.suit == 'Spades':
            SpadeCount += 1
        elif card.suit == 'Diamonds':
            DiaCount += 1

    if (isStraight1 or isStraight2 or isStraight3):
        if (isStraight3 and len(SC) >= 7):
            straightHigh = SC[6].rank
        elif (isStraight2 and len(SC) >= 6):
            straightHigh = SC[5].rank
        elif (isStraight1 and len(SC) >= 5):
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

    if isStraightFlush:
        if (checkListForSF[len(checkListForSF) - 1].rank == 14):
            isRoyal = True

    isQuads, hasTrips, isFull, hasPair, isTwoPair = False, False, False, False, False
    quadRank, tripRank, pairRankMax, pairRankSecond, highCard = 0, 0, 0, 0, SC[len(SC) - 1].rank
    numOfPairs = 0

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

    if (hasTrips and hasPair):
        isFull = True
    if (numOfPairs >= 2):
        isTwoPair = True

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
    scoreIndex.append(highCard)
    scoreIndex.append(SC[len(SC) - 2].rank)
    scoreIndex.append(SC[len(SC) - 3].rank)
    scoreIndex.append(SC[len(SC) - 4].rank)

    scoreIndex.sort(reverse=True)
    return scoreIndex

def bot_move(bot_balance, player_bet_stage, bot_bet_stage):
    decision = None
    amount = 0

    if player_bet_stage > bot_bet_stage:
        decision = random.choice(['call', 'raise', 'fold'])
    elif player_bet_stage == bot_bet_stage or player_bet_stage == 0:
        decision = random.choice(['check', 'bet'])

    if decision in ['raise', 'bet']:
        amount = random.choice([5, 10, 50])
        if bot_balance < amount:
            if bot_balance <= 5:
                decision = 'call'
                amount = bot_balance
            else:
                decision = 'fold'
                amount = 0

    return {
        'action': decision,
        'amount': amount
    }

class PokerGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.deck = Deck()
        self.player_hand = []
        self.bot_hand = []
        self.community_cards = []
        self.pot = 0
        self.player_bet = 0
        self.bot_bet = 0
        self.player_balance = 1000
        self.bot_balance = 1000
        self.stage = 'pre-deal'

    def deal_new_hand(self):
        self.reset_game()
        self.player_hand = self.deck.deal(2)
        self.bot_hand = self.deck.deal(2)
        self.stage = 'pre-flop'
        return self.player_hand

    def deal_flop(self):
        if self.stage == 'pre-flop':
            self.community_cards = self.deck.deal(3)
            self.stage = 'flop'
            return self.community_cards
        return None

    def deal_turn(self):
        if self.stage == 'flop':
            self.community_cards += self.deck.deal(1)
            self.stage = 'turn'
            return self.community_cards
        return None

    def deal_river(self):
        if self.stage == 'turn':
            self.community_cards += self.deck.deal(1)
            self.stage = 'river'
            return self.community_cards
        return None

    def determine_winner(self):
        player_score = evaluate_hand(self.player_hand, self.community_cards)
        bot_score = evaluate_hand(self.bot_hand, self.community_cards)

        for i in range(min(len(player_score), len(bot_score))):
            if player_score[i] > bot_score[i]:
                return 'player'
            elif bot_score[i] > player_score[i]:
                return 'bot'
        return 'tie'
