import numpy as np
import pickle
import roundcontrol
import preflop_table
from preflop_table import card_prob
import math
import winningprob
from winningprob import bestfive
from preflop import preflop

import Bluff_Bayesian_new as bluff
import Strength_HMM as hmm


def calcBetValue(pi, potSize):
    assert(pi < 0.5)
    return int(float(potSize)/(1/pi-2))


def postflopMakeAction(game, playerIndex, pis):
    pi = pis[playerIndex]
    print "bet history", game.player(1-playerIndex).betHistory
    card_state = hmm.HMM_state(game.player(1-playerIndex).betHistory)
    bluffprob = bluff.Bluff(game.player(1-playerIndex).betHistory)
    print "playerIndex", playerIndex
    print "pi", pi
    print "card state", card_state
    print "bluff?", bluffprob

    if game.player(playerIndex).isComputer:
        if abs(game.player(0).potMoney - game.player(1).potMoney) != 0:
            callValue = abs(game.player(0).potMoney - game.player(1).potMoney)
            if pi < 0.5:
                # Opponent Raised
                betValue = calcBetValue(pi, game.currentmoneyinpot())

                if betValue < callValue:
                    print "Player", playerIndex, "Fold......"
                    game.player(playerIndex).bet(0, "F", pi, game.currentmoneyinpot())
                    print
                    return False, playerIndex

                if betValue <= 2*callValue:
                    print "Player", playerIndex, "Call Value", int(min(callValue, game.player(playerIndex).moneyInHand))
                    game.player(playerIndex).bet(min(callValue, game.player(playerIndex).moneyInHand), "C", pi, game.currentmoneyinpot())
                    print

                else:
                    allInValue = game.player(1-playerIndex).moneyInHand + game.player(1-playerIndex).potMoney - game.player(playerIndex).potMoney
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2*game.player(1-playerIndex).lastBet)
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2)
                    print "Player", playerIndex, "Raise Value", int(betValue)
                    game.player(playerIndex).bet(int(betValue), "R", pi, game.currentmoneyinpot())
                    print

            else:
                if 0.2*pi + np.random.uniform() < 0.6:
                    print "Player", playerIndex, "Call Value", int(min(callValue, game.player(playerIndex).moneyInHand))
                    game.player(playerIndex).bet(min(callValue, game.player(playerIndex).moneyInHand), "C", pi, game.currentmoneyinpot())
                    print
                else:
                    betValue = (pi-0.2) * game.currentmoneyinpot()
                    allInValue = game.player(1-playerIndex).moneyInHand + game.player(1-playerIndex).potMoney - game.player(playerIndex).potMoney
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2*game.player(1-playerIndex).lastBet)
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2)
                    print "Player", playerIndex, "Raise Value", int(betValue)
                    game.player(playerIndex).bet(int(betValue), "R", pi, game.currentmoneyinpot())
                    print

        else:
            # Opponent Called
            if pi < 0.5:
                if np.random.uniform() + pi*0.1 < 0.45:
                    print "Player", playerIndex, "Check"
                    game.player(playerIndex).bet(0, "K", pi, game.currentmoneyinpot())
                    print
                else:
                    betValue = calcBetValue(pi, game.currentmoneyinpot())
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, game.player(1-playerIndex).moneyInHand)
                    betValue = max(betValue, 2)
                    print "Player", playerIndex, "Raise Value", int(betValue)
                    game.player(playerIndex).bet(betValue, "R", pi, game.currentmoneyinpot())
                    print
            else:
                if np.random.uniform() + pi*0.1 < 0.45:
                    print "Player", playerIndex, "Check"
                    game.player(playerIndex).bet(0, "K", pi, game.currentmoneyinpot())
                    print
                else:
                    betValue = (pi-0.2) * game.currentmoneyinpot()
                    allInValue = game.player(1-playerIndex).moneyInHand + game.player(1-playerIndex).potMoney - game.player(playerIndex).potMoney
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2*game.player(1-playerIndex).lastBet)
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, allInValue)
                    betValue = max(betValue, 2)
                    print "Player", playerIndex, "Raise Value", int(betValue)
                    game.player(playerIndex).bet(int(betValue), "R", pi, game.currentmoneyinpot())
                    print
    else:
        while True:
            if abs(game.player(0).potMoney - game.player(1).potMoney) != 0:
                action = raw_input("Enter your decision: input 'C' for Call or 'R' for Raise or 'F' for Fold:\n")

                if action == "C":
                    callValue = abs(game.player(0).potMoney - game.player(1).potMoney)
                    print "You Call", int(min(callValue, game.player(playerIndex).moneyInHand))
                    game.player(playerIndex).bet(min(callValue, game.player(playerIndex).moneyInHand), "C", pi, game.currentmoneyinpot())

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
                        while int(betAmount) < betValue or int(betAmount) > min(game.player(playerIndex).moneyInHand, game.player(1-playerIndex).moneyInHand):
                            print "Your min and max raise values are", int(betValue), min(game.player(playerIndex).moneyInHand, game.player(1-playerIndex).moneyInHand)
                            betAmount = raw_input("Enter the amount you want to raise:\n")
                    print "You Raise", int(betAmount)
                    game.player(playerIndex).bet(int(betAmount), "R", pi, game.currentmoneyinpot())

                    print
                    break

                elif action == "F":
                    print "You Fold......"
                    game.player(playerIndex).bet(0, "F", pi, game.currentmoneyinpot())
                    #game.player(0).hist
                    return False, playerIndex
                else:
                    print "Wrong input"

            else:
                action = raw_input("Enter your decision: input 'K' for Check or 'R' for Raise or 'F' for Fold:\n")

                if action == "K":
                    game.player(playerIndex).bet(0, "K", pi, game.currentmoneyinpot())
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
                        while int(betAmount) < betValue or int(betAmount) > min(game.player(playerIndex).moneyInHand, game.player(1-playerIndex).moneyInHand):
                            print "Your min and max raise values are", int(betValue), min(game.player(playerIndex).moneyInHand, game.player(1-playerIndex).moneyInHand)
                            betAmount = raw_input("Enter the amount you want to raise:\n")
                    game.player(playerIndex).bet(int(betAmount), "R", pi, game.currentmoneyinpot())
                    print
                    break

                elif action == "F":
                    game.player(playerIndex).bet(0, "F", pi, game.currentmoneyinpot())
                    return False, playerIndex
                else:
                    print "Wrong input entered"
    return True, -1


def postFlop(game, alterDealer):
    '''
    computer == player1
    user == player0
    '''
    winpFuncs = [winningprob.winp_flop_appx, winningprob.winp_turn, winningprob.winp_river]
    stage = ["Flop", "Turn", "River"]
    print "################### Stage: ", stage[game.stageIndex-1], "###################"

    print "Here are the cards shown on the board: ", game.boardcard()
    print

    # start with big and move first

    print "Player 0 money:", game.player(0).moneyInHand
    print "Player 1 money:", game.player(1).moneyInHand
    print "Total money on pot:", game.currentmoneyinpot()
    print

    pi = []
    pi.append(winpFuncs[game.stageIndex-1](game.boardcard(), game.player(alterDealer).holdcards()))
    pi.append(winpFuncs[game.stageIndex-1](game.boardcard(), game.player(1-alterDealer).holdcards()))

    forward, winIndex = postflopMakeAction(game, 1 - alterDealer, pi)
    if not forward:
        return False, 1 - alterDealer
    forward, winIndex = postflopMakeAction(game, alterDealer, pi)
    if not forward:
        return False, alterDealer
    ttt = 0
    while game.player(0).potMoney != game.player(1).potMoney and game.player(0).moneyInHand != 0 and game.player(1).moneyInHand != 0:
        forward, winIndex = postflopMakeAction(game, 1 - alterDealer, pi)
        if not forward:
            return False, 1 - alterDealer
        if game.player(0).potMoney == game.player(1).potMoney or game.player(0).moneyInHand == 0 or game.player(1).moneyInHand == 0:
            break
        forward, winIndex = postflopMakeAction(game, alterDealer, pi)
        if not forward:
            return False, alterDealer
        ttt += 1
        if ttt > 20:
            print "Not stoping ................................................................."
            break

    if game.player(0).moneyInHand == 0 and game.player(1).moneyInHand != 0:
        forward, winIndex = postflopMakeAction(game, 1, pi)
        if not forward:
            return False, 1
    elif game.player(1).moneyInHand == 0 and game.player(0).moneyInHand != 0:
        forward, winIndex = postflopMakeAction(game, 0, pi)
        if not forward:
            return False, 0

    print "Player 0 money:", game.player(0).moneyInHand
    print "Player 1 money:", game.player(1).moneyInHand
    print "Total money on pot:", game.currentmoneyinpot()
    print

    winIndex = -1
    if game.stageIndex == 3 or (game.player(1).moneyInHand == 0 and game.player(0).moneyInHand == 0):
        hand0 = game.player(0).holdcards() + game.publicCards
        hand1 = game.player(1).holdcards() + game.publicCards
        best0, strength0 = bestfive(hand0)
        best1, strength1 = bestfive(hand1)

        print "The public five cards are:", game.publicCards
        print "Player 0 best five:", best0, "| Original cards in hand:", game.player(0).holdcards()
        print "Player 1 best five:", best1, "| Original cards in hand:", game.player(1).holdcards()

        if strength0 == strength1:
            winIndex = 2
            print "Tie!!\n"
        elif strength0 > strength1:
            winIndex = 0
            print "Player 0 wins!\n"
        else:
            winIndex = 1
            print "Player 1 wins!\n"
        return False, 1-winIndex
    return True, winIndex


def afterPreFlop(game, alterDealer):
    alterDealer = 1 - alterDealer
    for i in xrange(3):
        game.increStageIndex()
        #print "Game Stage:", game.stageIndex, "###############################"
        forward, winIndex = postFlop(game, alterDealer)
        if not forward:
            #print "Flod???????????????????????????????????????????????????????????????????????????????????????"
            break
    return winIndex


def distributeMoney(game, winIndex):
    if winIndex == -1:
        tie = (game.player(1).potMoney + game.player(0).potMoney)/2
        game.player(0).moneyInHand += tie
        game.player(1).moneyInHand += tie
        game.player(0).potMoney -= tie
        game.player(1).potMoney -= tie
    elif winIndex == 0 or winIndex == 1:
        total = game.player(0).potMoney + game.player(1).potMoney
        game.player(1-winIndex).moneyInHand += total
        game.player(0).potMoney = 0
        game.player(1).potMoney = 0
    else:
        print "Wrong index!"

    print "Distributing money..."
    print "Player 0 money:", game.player(0).moneyInHand
    print "Player 1 money:", game.player(1).moneyInHand
    print "Total money on pot:", game.currentmoneyinpot()
    print "################### Game Finished! ###################"
    print "################### -------------- ###################\n\n\n"
    return