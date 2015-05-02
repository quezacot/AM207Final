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
import pickle
import initial_52

TOTAL_TURN = int(4)

class player:
    #betting = ["fold","call","raise"]
    def __init__(self, hands, initalMoney = 100):
        self.hands = list(hands)
        self.betHistory = []
        self.betMoney = []
        self.moneyInHand = int(initalMoney)

    def holdcards(self):
        cards = list(self.hands)
        return cards

    def bet(self, newbet):
        self.betMoney.append(int(newbet))
        self.moneyInHand -= int(newbet)
        return self.moneyInHand

    def currentMoney(self):
        return self.moneyInHand

    def resetCards(self, hands):
        self.hands = list(hands)

class roundcontrol:
    def __init__(self, players):
        self.numply = players
        pubcards, plycards = dc.texassim(players) #deal
        self.pub = pubcards #board cards
        self.plys = [] #players
        for onehand in plycards:
            self.plys.append( player(onehand) )

    def boardcard(self, round=TOTAL_TURN-1):
        if round == 0:
            cards = []
        else:
            cards = list( self.pub[:2+round] )
        return cards

    def player(self, no):
        return self.plys[no]

# constants
allCards = initial_52.cards_vec()
card2n = dict(zip(allCards, np.arange(52)))
n2card = dict(zip(np.arange(52), allCards))

Comparedresult= pickle.load(open('Comparedresult.pcl', 'r'))
rankresult= pickle.load(open('rankresult.pcl', 'r'))

def main():
    numplayers = 2
    playerID = np.random.randint(numplayers)
    dealer = roundcontrol(numplayers)
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
