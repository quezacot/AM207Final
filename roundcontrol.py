#-------------------------------------------------------------------------------
# Name:        roundcontrol.py
# Purpose:     Define two classes 'player' and 'roundcontrol'
#              player class stores all parameters and handles all actions related to a player.
#              roundcontrol class stores all parameters and handles all actions related to the table.
#-------------------------------------------------------------------------------
import deal_compare as dc
import numpy as np

TOTAL_ROUND = int(4)

# Player class store all parameters and handles all actions related to a player.
class player:
    #betting = ["fold","call","raise"]
    # Initialize a player
    def __init__(self, isComputer, holeCards, initalMoney = 500):
        self.holeCards = list(holeCards) # two hole cards in hand
        self.betHistory = [[[] for i in range(4)]] # an empty list to store bet history after
        self.moneyInHand = int(initalMoney) # the budget this player has in hand
        self.potMoney = 0 # the money this player put in the pot in this game
        self.lastBet = 0 # the last bet amout this player put (amount of money)
        self.isComputer = isComputer # whether this player is a computer
        self.lastAction = "" # the last bet action this player did (fold, call, raise, or check)
        self.numOfGames = 0 # store number of games this player played
        self.currentStageIndex = -1 # stage count: preflop:0; flop:1; turn:2; river:3

    # Return this player's hole cards
    def holdcards(self):
        cards = list(self.holeCards)
        return cards

    # player bets
    def bet(self, newbet, actionType, pi = 0, potMoneyTotal = 0):
        '''
        newbet: bet amount
        actionType: bet action(fold, call, raise, or check)
        pi: winning probability
        potMoneyTotal: current amount of money in pot
        return: the player's money in hand after bet
        '''
        self.moneyInHand -= int(newbet)
        self.potMoney += int(newbet)
        self.lastBet = int(newbet)
        self.lastAction = actionType

        if self.currentStageIndex != -1:
            myTuple = (actionType, pi, float(newbet)/float(potMoneyTotal))
            self.betHistory[self.numOfGames][self.currentStageIndex].append(myTuple)

        #if actionType == "F":
        #    self.betHistory[self.numOfGames] = []

        if self.isComputer:
            print "Computer's money in hand now is", self.moneyInHand
            print "Computer's in pot now total is", self.potMoney
            print "-------------------------------"
            print
        else:
            print "Your money in hand now is", self.moneyInHand
            print "Your in pot now total is", self.potMoney
            print "-------------------------------"
            print

        return self.moneyInHand

    # Reset this player for a new game. Reset everything except the money in this player's hand.
    # The number of games advanced one.
    def resetCards(self, holeCards):
        '''
        holeCards: new hole cards dealt to this player in the new game.
        '''
        self.holeCards = list(holeCards)
        self.potMoney = 0
        self.lastBet = 0
        self.lastAction = ""
        self.numOfGames += 1
        self.currentStageIndex = -1
        self.betHistory.append([[] for i in range(4)])

    # Clean thi player's bet history. Used when the game is ended due to fold because the hold cards are not revealed.
    def cleanHistory(self):
        self.betHistory[self.numOfGames] = []

    # Add money to this player's hand
    def addMoney(self, money = 500):
        self.moneyInHand += int(money)
        self.potMoney = 0

# roundcontrol class stores all parameters and handles all actions related to the table.
class roundcontrol:
    # Initialize a new table
    def __init__(self, numPlayer = 2):
        self.numPlayer = numPlayer # number of players
        pubcards, plycards = dc.texassim(self.numPlayer) #deal cards to obtain board cards and hole cards of each player
        self.publicCards = pubcards #board cards
        self.playerList = [] # create a list to contain all players
        self.stageIndex = -1 # initial stage

        isComputer = False
        # create players
        for onehand in plycards:
            self.playerList.append(player(isComputer, onehand))
            isComputer = True

    # Reset and start a new game
    def resetGame(self):
        pubcards, plycards = dc.texassim(self.numPlayer) #deal
        self.publicCards = pubcards
        self.stageIndex = -1
        i = 0
        for onehand in plycards:
            self.playerList[i].resetCards(onehand)
            i += 1

    # Advance to next stage of game
    def increStageIndex(self):
        self.stageIndex += 1
        for i in xrange(2):
            self.playerList[i].currentStageIndex += 1

    # Return boardcard according to current game stage
    def boardcard(self):
        #print "self.stageIndex", self.stageIndex

        if self.stageIndex == 0 or self.stageIndex == -1:
            cards = []
        else:
            cards = list( self.publicCards[:2+self.stageIndex] )
        return cards

    # Return the player with number no.
    def player(self, no):
        return self.playerList[no]

    # Return pot size.
    def currentmoneyinpot(self):
        total = 0
        for player in self.playerList:
            total += player.potMoney
        return total

    # Clear bet history of all players'
    def cleanHistory(self):
        if self.player(0).lastAction == "F" or self.player(1).lastAction == "F":
            self.player(0).cleanHistory()
            self.player(1).cleanHistory()
            print "No cards shown because game ended early!"
        return

    # Add money to all players.
    def addMoney(self, money = 500):
        self.player(0).addMoney(money)
        self.player(1).addMoney(money)
        print "Money", money, "added for each player"

# This main function is only to test this code and not used in the over all game flow.
def main():
    numplayers = 2
    playerID = np.random.randint(numplayers)
    dealer = roundcontrol()
    for curound in xrange(TOTAL_ROUND):
        print "===============round", curound, "======================="
        print "The current board cards are:"
        print dealer.boardcard(curound)
        print "Your hold cards are:",
        playerobj = dealer.player(playerID)
        print playerobj.holdcards()
        newbet = raw_input('Enter your bet: ')
        playerobj.bet(newbet)
        print ""

    maxhands = []
    for i in xrange(numplayers):
        maxhands.append(dc.maxeach(dealer.boardcard(), dealer.player(i).holdcards()) )

    print "Your best hand is: ",
    print maxhands[playerID]


if __name__ == '__main__':
    main()
