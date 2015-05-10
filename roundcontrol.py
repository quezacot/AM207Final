#-------------------------------------------------------------------------------
# Name:        roundcontrol
# Purpose:
#
# Author:      Yj
#
# Created:     19/04/2015
# Copyright:   (c) Yj 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import deal_compare as dc
import numpy as np

TOTAL_ROUND = int(4)

class player:
    #betting = ["fold","call","raise"]
    def __init__(self, isComputer, holeCards, initalMoney = 500):
        self.holeCards = list(holeCards)
        self.betHistory = [[[] for i in range(4)]]
        self.moneyInHand = int(initalMoney)
        self.potMoney = 0
        self.lastBet = 0
        self.isComputer = isComputer
        self.lastAction = ""
        self.numOfGames = 0
        self.currentStageIndex = -1

    def holdcards(self):
        cards = list(self.holeCards)
        return cards

    def bet(self, newbet, actionType, pi = 0, potMoneyTotal = 0):
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

    def resetCards(self, holeCards):
        self.holeCards = list(holeCards)
        self.potMoney = 0
        self.lastBet = 0
        self.lastAction = ""
        self.numOfGames += 1
        self.currentStageIndex = -1
        self.betHistory.append([[] for i in range(4)])

    def cleanHistory(self):
        self.betHistory[self.numOfGames] = []

    def addMoney(self, money = 500):
        self.moneyInHand += int(money)
        self.potMoney = 0

class roundcontrol:
    def __init__(self, numPlayer = 2):
        self.numPlayer = numPlayer
        pubcards, plycards = dc.texassim(self.numPlayer) #deal
        self.publicCards = pubcards #board cards
        self.playerList = []
        self.stageIndex = -1

        isComputer = False
        for onehand in plycards:
            self.playerList.append(player(isComputer, onehand))
            isComputer = True

    def resetGame(self):
        pubcards, plycards = dc.texassim(self.numPlayer) #deal
        self.publicCards = pubcards
        self.stageIndex = -1
        i = 0
        for onehand in plycards:
            self.playerList[i].resetCards(onehand)
            i += 1

    def increStageIndex(self):
        self.stageIndex += 1
        for i in xrange(2):
            self.playerList[i].currentStageIndex += 1

    def boardcard(self):
        #print "self.stageIndex", self.stageIndex

        if self.stageIndex == 0 or self.stageIndex == -1:
            cards = []
        else:
            cards = list( self.publicCards[:2+self.stageIndex] )
        return cards

    def player(self, no):
        return self.playerList[no]

    def currentmoneyinpot(self):
        total = 0
        for player in self.playerList:
            total += player.potMoney
        return total

    def cleanHistory(self):
        if self.player(0).lastAction == "F" or self.player(1).lastAction == "F":
            self.player(0).cleanHistory()
            self.player(1).cleanHistory()
            print "No cards shown because game ended early!"
        return

    def addMoney(self, money = 500):
        self.player(0).addMoney(money)
        self.player(1).addMoney(money)
        print "Money", money, "added for each player"

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
