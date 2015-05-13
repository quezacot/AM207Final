#-------------------------------------------------------------------------------
# Name:        postFlop.py
# Purpose:     Controls the game of flop, turn, and river stage.
#              (three, four, five board cards are known respectively)
#-------------------------------------------------------------------------------

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

# Adjust pi given the state estimated from HMM
def adjustpibystate(pi, cardstate):
    '''
    pi: the original deterministic probability pi
    cardstate: the state estimated from HMM
    '''
    #states = ('Low', 'Medium','High', 'No_State')
    lowerpart = pi * 0.75
    if cardstate == 'Low':
        if pi <= 1.0/3.0:
            return pi*3 * 0.25 + lowerpart
        else: #pi > 1.0/3.0
            return 0.25 + lowerpart
    elif cardstate == 'Medium':
        if pi <= 1.0/3.0:
            return lowerpart
        elif pi > 1.0/3.0 and pi <= 2.0/3.0:
            return (pi - 1.0/3.0)*3 * 0.25 + lowerpart
        else: #pi > 2.0/3.0
            return 0.25 + lowerpart
    elif cardstate == 'High':
        if pi <= 2.0/3.0:
            return lowerpart
        else: #pi > 2.0/3.0
            return (pi - 2.0/3.0)*3 * 0.25 + lowerpart
    else: #No_State
        return pi

# Calculate the bet value that maximizes expections
def calcBetValue(pi, potSize):
    assert(pi < 0.5)
    return int(float(potSize)/(1/pi-2))

# Player makes the bet action.
def postflopMakeAction(game, playerIndex, pis):
    '''
    game: an object of all imformation of the game
    playerIndex: indicate which player is making action
    pis: the deterministic pi of each players.
    return: Falsed if the game is ended. Index of the winner player.
            True if the game is still on going. -1 means winner not determined yet.
    '''
    pi = pis[playerIndex]
    #print "bet history", game.player(1-playerIndex).betHistory
    card_state = hmm.HMM_state(game.player(1-playerIndex).betHistory)
    bluffprob = bluff.Bluff(game.player(1-playerIndex).betHistory)
##    print "playerIndex", playerIndex
##    print "pi", pi
##    print "card state", card_state
##    print "bluff?", bluffprob
    # estimated pi from HMM
    hmm_pi = adjustpibystate(pi, card_state)
    #print "hmm adjusted pi", hmm_pi
    # combine estimated pi from HMM and bluff
    bluff_pi = bluffprob*pi + (1-bluffprob)*hmm_pi
    #print "bluff adjusted pi", bluff_pi

    pi = bluff_pi

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
                    return False, 1-playerIndex

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
        else:
            # different strategies based on pi
            if pi < 0.5:
                if np.random.uniform() + pi*0.1 < 0.45:
                    print "Computer", playerIndex, "Check"
                    game.player(playerIndex).bet(0, "K", pi, game.currentmoneyinpot())
                    print
                else:
                    betValue = calcBetValue(pi, game.currentmoneyinpot())
                    betValue = min(betValue, game.player(playerIndex).moneyInHand, game.player(1-playerIndex).moneyInHand)
                    betValue = max(betValue, 2)
                    print "Computer", playerIndex, "Raise Value", int(betValue)
                    game.player(playerIndex).bet(betValue, "R", pi, game.currentmoneyinpot())
                    print
            else:
                if np.random.uniform() + pi*0.1 < 0.45:
                    print "Computer", playerIndex, "Check"
                    game.player(playerIndex).bet(0, "K", pi, game.currentmoneyinpot())
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
    # if player is human, ask for bet input
    else:
        while True:
            # next action when the other player raised.
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
                    return False, 1-playerIndex
                else:
                    print "Wrong input"
            # next action when the other player called.
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
                    return False, 1-playerIndex
                else:
                    print "Wrong input entered"
    return True, -1

# Control the game flow of flop, turn, and river stages.
def postFlop(game, alterDealer):
    '''
    game: an object of all imformation of the game
    alterDealer: the dealer of this stage
    return: Falsed if the game is ended. Index of the winner player.
            True if the game is still on going. -1 means winner not determined yet.
    '''
    #computer == player1
    #user == player0
    winpFuncs = [winningprob.winp_flop_appx, winningprob.winp_turn, winningprob.winp_river]
    stage = ["Flop", "Turn", "River"]
    print "################### Stage: ", stage[game.stageIndex-1], "###################"

    print "Here are the cards shown on the board: ", game.boardcard()
    print

    # Display every one's money in hand, pot size, and human player's hole cards.
    for i in xrange(game.numPlayer):
        if game.player(i).isComputer:
            print "Computer's money:", game.player(i).moneyInHand
        else:
            print "Your money:", game.player(i).moneyInHand
            print "Your Cards: ", game.player(i).holdcards()

    print "Total money on pot:", game.currentmoneyinpot()

    pi = []
    pi.append(winpFuncs[game.stageIndex-1](game.boardcard(), game.player(alterDealer).holdcards()))
    pi.append(winpFuncs[game.stageIndex-1](game.boardcard(), game.player(1-alterDealer).holdcards()))
    # At least one action after flop stage.
    forward, winIndex = postflopMakeAction(game, 1 - alterDealer, pi)
    # Test if game ends after the previous action
    if not forward:
        return False, winIndex
    forward, winIndex = postflopMakeAction(game, alterDealer, pi)
    if not forward:
        return False, winIndex
    ttt = 0 # count bet times for debug.
    # Bet is still on going if 1) players have different bet amount in pot. It means on of them raised.
    # 2) Both player still have money in hand. No one has been all in.
    while game.player(0).potMoney != game.player(1).potMoney and game.player(0).moneyInHand > 0 and game.player(1).moneyInHand > 0:
        forward, winIndex = postflopMakeAction(game, 1 - alterDealer, pi)
        # Return at anytime the game ends.
        if not forward:
            return False, 1 - alterDealer
        if game.player(0).potMoney == game.player(1).potMoney or game.player(0).moneyInHand <= 0 or game.player(1).moneyInHand <= 0:
            break
        forward, winIndex = postflopMakeAction(game, alterDealer, pi)
        if not forward:
            return False, alterDealer
        ttt += 1
        if ttt > 20:
            print "Not stoping ................................................................."
            break

    # One of the players is all-in
    if game.player(0).moneyInHand == 0 and game.player(1).moneyInHand != 0:
        forward, winIndex = postflopMakeAction(game, 1, pi)
        if not forward: # player 1 folded
            return False, 0
    elif game.player(1).moneyInHand == 0 and game.player(0).moneyInHand != 0:
        forward, winIndex = postflopMakeAction(game, 0, pi)
        if not forward: # player 0 folded
            return False, 1

    for i in xrange(game.numPlayer):
        if game.player(i).isComputer:
            print "Computer's money:", game.player(i).moneyInHand
        else:
            print "Your money:", game.player(i).moneyInHand
            print "Your Cards: ", game.player(i).holdcards()

    print "Total money on pot:", game.currentmoneyinpot()

    winIndex = -1
    # Game ended if it is in the river stage or one of the players has no money in hand.
    if game.stageIndex == 3 or game.player(1).moneyInHand == 0 or game.player(0).moneyInHand == 0:
        # determine the winner by cards.
        hand0 = game.player(0).holdcards() + game.publicCards
        hand1 = game.player(1).holdcards() + game.publicCards
        best0, strength0 = bestfive(hand0)
        best1, strength1 = bestfive(hand1)

        print "The public five cards are:", game.publicCards
        print "Your best five:", best0, winningprob.determintype(best0), "| Original cards in hand:", game.player(0).holdcards()
        print "Computer's best five:", best1, winningprob.determintype(best1), "| Original cards in hand:", game.player(1).holdcards()

        if strength0 == strength1:
            #winIndex = -1
            print "Tie!!\n"
        elif strength0 > strength1:
            winIndex = 0
            print "You win!\n"
        else:
            winIndex = 1
            print "Computer wins!\n"
        return False, winIndex
    return True, winIndex

# Game flow of flop, turn, and river stages
def afterPreFlop(game, alterDealer):
    alterDealer = 1 - alterDealer
    # loop through these three stages
    for i in xrange(3):
        game.increStageIndex()
        #print "Game Stage:", game.stageIndex, "###############################"
        forward, winIndex = postFlop(game, alterDealer)
        if not forward:
            #print "Flod???????????????????????????????????????????????????????????????????????????????????????"
            break
    return winIndex

# Game ended. Distribute the money in pot to the winner, or split it if it is a tie.
def distributeMoney(game, winIndex):
    if winIndex == -1:
        tie = (game.player(1).potMoney + game.player(0).potMoney)/2
        game.player(0).moneyInHand += tie
        game.player(1).moneyInHand += tie
        game.player(0).potMoney -= tie
        game.player(1).potMoney -= tie
    elif winIndex == 0 or winIndex == 1:
        total = game.player(0).potMoney + game.player(1).potMoney
        game.player(winIndex).moneyInHand += total
        game.player(0).potMoney = 0
        game.player(1).potMoney = 0
    else:
        print "Wrong index!"

    print "Distributing money..."
    print "Your money:", game.player(0).moneyInHand
    print "Computer's money:", game.player(1).moneyInHand
    print "Total money on pot:", game.currentmoneyinpot()
    print "################### Game Finished! ###################"
    print "################### -------------- ###################\n\n\n"
    return