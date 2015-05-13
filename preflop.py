#-------------------------------------------------------------------------------
# Name:        preflop.py
# Purpose:     Controls the game of the preflop stage. (only two hole cards are known)
#-------------------------------------------------------------------------------

import numpy as np
import pickle
import roundcontrol
import preflop_table
from preflop_table import card_prob
import math
import winningprob


# Calculate the bet value that maximizes expections
def calcBetValue(pi, potSize):
    assert(pi < 0.5)
    return int(float(potSize)/(1/pi-2))

# Player makes the bet action.
def preflopMakeAction(game, playerIndex, tableIndex = 1):
    '''
    game: an object of all imformation of the game
    playerIndex: indicate which player is making action
    tableIndex: indicate which table to use in preflop_table.py
    return: modified tableIndex.
    '''
    pi = card_prob(game.player(playerIndex).holdcards()[0], game.player(playerIndex).holdcards()[1], tableIndex)
    # if this player is computer, use our AI.
    # if the player is computer, use our AI.
    if game.player(playerIndex).isComputer:
        # when two players has different money in pot, the opponent raised
        if abs(game.player(0).potMoney - game.player(1).potMoney) != 0:
            callValue = abs(game.player(0).potMoney - game.player(1).potMoney)
            # different strategies based on pi
            if pi < 0.5:
                betValue = calcBetValue(pi, game.currentmoneyinpot())

                if betValue < callValue:
                    print "Computer", playerIndex, "Fold......"
                    game.player(playerIndex).bet(0, "F", pi, game.currentmoneyinpot())
                    print
                    return False, 1-playerIndex, tableIndex

                if betValue <= 2*callValue:
                    print "Computer", playerIndex, "Call Value", int(min(callValue, game.player(playerIndex).moneyInHand))
                    game.player(playerIndex).bet(min(callValue, game.player(playerIndex).moneyInHand), "C", pi, game.currentmoneyinpot())
                    print

                else:
                    allInValue = game.player(1-playerIndex).moneyInHand + game.player(1-playerIndex).potMoney - game.player(playerIndex).potMoney
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2*game.player(1-playerIndex).lastBet)
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2)
                    print "Computer", playerIndex, "Raise Value", int(betValue)
                    game.player(playerIndex).bet(int(betValue), "R", pi, game.currentmoneyinpot())
                    print
            else:
                if 0.2*pi + np.random.uniform() < 0.6:
                    print "Computer", playerIndex, "Call Value", int(min(callValue, game.player(playerIndex).moneyInHand))
                    game.player(playerIndex).bet(min(callValue, game.player(playerIndex).moneyInHand), "C", pi, game.currentmoneyinpot())
                    print
                else:
                    betValue = (pi-0.2) * game.currentmoneyinpot()
                    allInValue = game.player(1-playerIndex).moneyInHand + game.player(1-playerIndex).potMoney - game.player(playerIndex).potMoney
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2*game.player(1-playerIndex).lastBet)
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2)

                    print "Computer", playerIndex, "Raise Value", int(betValue)
                    game.player(playerIndex).bet(int(betValue), "R", pi, game.currentmoneyinpot())
                    print

        # two players has the same money in pot, the opponent called
    # if this player is human, ask for input
    else:
        while True:
            action = raw_input("Enter your decision: input 'C' for Call or 'R' for Raise or 'F' for Fold:\n")
            if action == "F":
                print "You Fold......"
                return False, 1-playerIndex, tableIndex
            elif action == "C":
                callValue = abs(game.player(0).potMoney - game.player(1).potMoney)
                game.player(playerIndex).bet(callValue, "C", pi, game.currentmoneyinpot())
                print
                break
            elif action == "R":
                print "Your total money: ", game.player(playerIndex).moneyInHand
                betValue = math.ceil(game.player(1-playerIndex).lastBet * 2)
                if betValue >= game.player(playerIndex).moneyInHand:
                    betAmount = game.player(playerIndex).moneyInHand
                else:
                    #print "Debug..........", game.player(1-playerIndex).lastBet, betValue
                    betAmount = raw_input("Enter the amount you want to raise:\n")
                    while int(betAmount) < betValue or int(betAmount) > game.player(playerIndex).moneyInHand:
                        print "Your min and max raise values are", int(betValue), int(game.player(playerIndex).moneyInHand)
                        betAmount = raw_input("Enter the amount you want to raise:\n")
                game.player(playerIndex).bet(int(betAmount), "R", pi, game.currentmoneyinpot())
                print
                if betAmount > 0.2 * min(game.player(0).moneyInHand, game.player(1).moneyInHand):
                    tableIndex = 3
                else:
                    tableIndex = max(2, tableIndex)
                break
            else:
                print "Wrong input entered"

    return True, playerIndex, tableIndex

# Handle the game flow before flop stage
def preflop(game, alterDealer):
    '''
    game: an object of all imformation of the game
    alterDealer: the dealer of this stage
    '''
    # computer == player1
    # user == player0

    # print out human player's hole cards
    for i in xrange(game.numPlayer):
        if not game.player(i).isComputer:
            print "Your Cards: ", game.player(i).holdcards()
            print

    #print "Computer Cards: ", game.player(1).holdcards()

    # Big blind and small blind are bet automatically
    game.player(alterDealer).bet(2, "")
    game.player(1 - alterDealer).bet(1, "")

    game.increStageIndex()
    for i in xrange(game.numPlayer):
        if game.player(i).isComputer:
            print "Computer's money:", game.player(i).moneyInHand
        else:
            print "Your Money: ", game.player(i).moneyInHand
            print "Your Cards: ", game.player(i).holdcards()

    print "Total money on pot:", game.currentmoneyinpot()

    tableIndex = 1
    forward, winIndex, tableIndex = preflopMakeAction(game, 1 - alterDealer, tableIndex)
    # Test if game ends after the previous action
    if not forward:
        return False, winIndex
    forward, winIndex, tableIndex = preflopMakeAction(game, alterDealer, tableIndex)
    if not forward:
        return False, winIndex

    # All players make actions alternatively until one of the players stopped raise
    while game.player(0).potMoney != game.player(1).potMoney and game.player(0).moneyInHand != 0 and game.player(1).moneyInHand != 0:
        tableIndex = preflopMakeAction(game, 1 - alterDealer, tableIndex)
        if not forward:
            return False, 1 - alterDealer
        if game.player(0).potMoney == game.player(1).potMoney or game.player(0).moneyInHand == 0 or game.player(1).moneyInHand == 0:
            break
        tableIndex = preflopMakeAction(game, alterDealer, tableIndex)
        if not forward:
            return False, alterDealer

    # If one of the players has no money in hand, only the other player can take one more action.
    if game.player(0).moneyInHand == 0 and game.player(1).moneyInHand != 0:
        tableIndex = preflopMakeAction(game, 1, tableIndex + 1)
    elif game.player(1).moneyInHand == 0 and game.player(0).moneyInHand != 0:
        tableIndex = preflopMakeAction(game, 0, tableIndex + 1)

    for i in xrange(game.numPlayer):
        if game.player(i).isComputer:
            print "Computer's money:", game.player(i).moneyInHand
            print
        else:
            print "Your money:", game.player(i).moneyInHand
            print "Your Cards: ", game.player(i).holdcards()
            print

    print "Total money on pot:", game.currentmoneyinpot()

    winIndex = -1
    # Advance to the end of game when one of the players has no money in hand
    if game.player(0).moneyInHand == 0 or game.player(1).moneyInHand == 0:

        hand0 = game.player(0).holdcards() + game.publicCards
        hand1 = game.player(1).holdcards() + game.publicCards
        best0, strength0 = winningprob.bestfive(hand0)
        best1, strength1 = winningprob.bestfive(hand1)

        print "Your Best Five:", best0, "Original Cards in hand:", game.player(0).holdcards()
        print "Computer's Best Five:", best1, "Original Cards in hand:", game.player(1).holdcards()

        if hand0 == hand1:
            winIndex = -1
            print "Tie!!\n"
        elif hand0 > hand1:
            winIndex = 0
            print "You win!\n"
        else:
            winIndex = 1
            print "Computer wins!\n"
        return False, winIndex
    return True, -1



