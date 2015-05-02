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
        self.betHistory = []
        self.betMoney = []
        self.moneyInHand = int(initalMoney)
        self.potMoney = 0
        self.lastBet = 0
        self.isComputer = isComputer
        

    def holdcards(self):
        cards = list(self.holeCards)
        return cards

    def bet(self, newbet):
        self.betMoney.append(int(newbet))
        self.moneyInHand -= int(newbet)
        self.potMoney += int(newbet)
        self.lastBet = newbet
        return self.moneyInHand

    def resetCards(self, holeCards):
        self.holeCards = list(holeCards)
        self.potMoney = 0
        self.lastBet = 0

class roundcontrol:
    def __init__(self, numPlayer = 2):
        self.numPlayer = numPlayer
        pubcards, plycards = dc.texassim(self.numPlayer) #deal
        self.publicCards = pubcards #board cards
        self.playerList = []
        
        isComputer = False
        for onehand in plycards:
            self.playerList.append(player(isComputer, onehand))
            isComputer = True

    def resetGame(self):
        pubcards, plycards = dc.texassim(self.numPlayer) #deal
        self.publicCards = pubcards
        i = 0
        for onehand in plycards:
            self.playerList[i].resetCards(onehand)
            i += 1

    def boardcard(self, round=TOTAL_ROUND-1):
        if round == 0:
            cards = []
        else:
            cards = list( self.publicCards[:2+round] )
        return cards

    def player(self, no):
        return self.playerList[no]

    def currentmoneyinpot(self):
        total = 0
        for player in self.playerList:
            total += player.potMoney
        return total


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
