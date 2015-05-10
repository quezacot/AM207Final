#-------------------------------------------------------------------------------
# Name:        gameflow
# Purpose:
#
# Author:      Yj
#
# Created:     09/05/2015
# Copyright:   (c) Yj 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np
import pickle
import roundcontrol
import preflop_table
from preflop_table import card_prob
import math
import winningprob
from winningprob import bestfive
import preflop
import postFlop
import Strength_HMM as hmm
import Bluff_Bayesian_new as bluff


def main():
    game = roundcontrol.roundcontrol(2)
    game.player(1).isComputer = True
    game.player(0).isComputer = False

    # random dealer
    alterDealer = np.random.randint(2)
    for i in xrange(100):
        print "\n\n\n"
        print "######################################################"
        print "##################### Game Start! ####################"
        #game.publicCards = ['6S', 'QH', '8S', 'JH', 'KS']
        #game.player(0).holeCards = ['TH', '8D']
        #game.player(1).holeCards = ['QD', 'JD']
        check, winIndex = preflop.preflop(game, alterDealer)
        if check:
            winIndex = postFlop.afterPreFlop(game, alterDealer)
        postFlop.distributeMoney(game, winIndex)

        game.cleanHistory()
        game.resetGame()
        #game.addMoney()
        alterDealer = 1 - alterDealer
        if game.player(0).moneyInHand <= 0:
            print "You lost out..."
            break
        elif game.player(1).moneyInHand <= 0:
            print "Computer lost out..."
            break
        else:
            nextgame = raw_input("Do you want to play next round? 'Y' or 'N'\n")
            while not (nextgame == 'Y' or nextgame == 'N'):
                nextgame = raw_input("Please type in 'Y' or 'N'. Do you want to play next round?\n")
            if nextgame == 'N':
                break


if __name__ == '__main__':
    main()
