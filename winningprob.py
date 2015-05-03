#-------------------------------------------------------------------------------
# Name:        winningprob.py
# Purpose:
#
# Author:      Yj
#
# Created:     01/05/2015
# Copyright:   (c) Yj 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import deal_compare as dc
import each_compare as ec
import numpy as np
import itertools
import pandas as pd
import pickle
import initial_52

ALLCOMP = None
ALLCARDS = None
TYPEWIN = None
TYPELIST = [u'straightflush', u'fourkind', u'fullhouse', u'flush',
            u'straight', u'threekind', u'twopairs', u'onepair', u'highcard']

# find out the best five cards from the seven cards
def bestfive(sevencards):
    '''
    sevencards: list of seven cards. eg. ['6D', '7H', '2C', 'AD', 'AH', '2D', 'TC']
    return: best 5 cards, strength of the best 5 cards
    '''
    # list all combinations 5 out of 7
    permu = list(itertools.combinations(sevencards, 5))
    lind = 0
    lstr = ALLCOMP["".join(sorted(permu[lind]))]
    for i,five in enumerate(permu):
        key = "".join(sorted(five))
        cstr = ALLCOMP[key]
        if cstr > lstr:
            lind = i
            lstr = cstr
    return list(permu[lind]), lstr

def possiblecards(exclude, allcards=ALLCARDS):
    return [ c for c in allcards if c not in exclude ]

def determintype(fivecards):
    funclist = [dc.straightflush, dc.fourkind, dc.fullhouse, dc.flush, dc.straight, dc.threekind, dc.twopairs, dc.onepair]
    for i in xrange(len(funclist)):
        istype = funclist[i](fivecards)
        if istype[-1]:
            return TYPELIST[i]
    return TYPELIST[-1]


#==============================================================================#

def winc_river(boardcards, holecards, exclude=[]):
    assert( len(boardcards) == 5 ) #river has five boardcards
    myhighfive, mystrength = bestfive(boardcards + holecards)
    # the rest possible cards of opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude, ALLCARDS)
    opponentholecards = itertools.combinations(restcards, 2)
    wincount, tiecount, totalcount = 0,0,0
    for oneholecard in opponentholecards:
        totalcount += 1
        hishighfive, hisstrength = bestfive(boardcards + list(oneholecard))
        if mystrength > hisstrength:
            wincount += 1
        elif mystrength == hisstrength:
            tiecount += 1
    return wincount, tiecount, totalcount

def winp_river(boardcards, holecards, exclude=[]):
    wincount, tiecount, totalcount= winc_river(boardcards, holecards, exclude)
    return ( wincount + 0.5*tiecount ) / totalcount

#==============================================================================#

def winc_turn(boardcards, holecards, exclude=[]):
    assert( len(boardcards) == 4 ) #turn has four boardcards
    # the rest possible cards of one board card and opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude, ALLCARDS)
    restboardcard = itertools.combinations(restcards, 1)
    wincount, tiecount, totalcount = 0,0,0
    for oneboardcard in restboardcard:
        subwincount, subtiecount, subtotalcount = winc_river( boardcards+list(oneboardcard), holecards )
        wincount += subwincount
        tiecount += subtiecount
        totalcount += subtotalcount
    return wincount, tiecount, totalcount

def winp_turn(boardcards, holecards, exclude=[]):
    wincount, tiecount, totalcount= winc_turn(boardcards, holecards, exclude)
    return ( wincount + 0.5*tiecount ) / totalcount

#==============================================================================#

def winc_flop(boardcards, holecards, exclude=[]):
    assert( len(boardcards) == 3 ) #flop has three boardcards
    # the rest possible cards of one board card and opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude, ALLCARDS)
    restboardcard = itertools.combinations(restcards, 1)
    wincount, tiecount, totalcount = 0,0,0
    for oneboardcard in restboardcard:
        subwincount, subtiecount, subtotalcount = winc_turn( boardcards+list(oneboardcard), holecards )
        wincount += subwincount
        tiecount += subtiecount
        totalcount += subtotalcount
    return wincount, tiecount, totalcount

def winp_flop(boardcards, holecards, exclude=[]):
    wincount, tiecount, totalcount= winc_flop(boardcards, holecards, exclude)
    return ( wincount + 0.5*tiecount ) / totalcount

def winp_flop_appx(boardcards, holecards, exclude=[]):
    assert( len(boardcards) == 3 ) #flop has three boardcards
    # the rest possible cards of opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude, ALLCARDS)
    restboardcards = itertools.combinations(restcards, 2)
    typecount = dict(zip(TYPELIST, [0]*len(TYPELIST)))
    for twoboardcards in restboardcards:
        myhighfive, mystrength = bestfive(boardcards + list(twoboardcards))
        myhighfivetype = determintype(myhighfive)
        typecount[myhighfivetype] += 1
    weightedsum = float(0)
    totalcount = int(0)
    for onetype in TYPELIST:
        totalcount += typecount[onetype]
        weightedsum += typecount[onetype] * TYPEWIN[onetype]['P']
    return weightedsum / totalcount


#==============================================================================#

def opp_winp_river(boardcards, holecards, exclude=[]):
    assert( len(boardcards) == 5 ) #river has five boardcards
    # the rest possible cards of opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude, ALLCARDS)
    opponentholecards = itertools.combinations(restcards, 2)
    opp_winp = {}
    for oneholecard in opponentholecards:
        holecardlist = list(oneholecard)
        winrate = winp_river(boardcards, holecardlist)
        keyofholecard = "".join( sorted(holecardlist) )
        opp_winp[keyofholecard] = winrate
    return opp_winp

#==============================================================================#

def initialize():
    # initialize ALLCOMP
    global ALLCOMP
    filehandler = open("allCombDict_new.p","rb")
    ALLCOMP = pickle.load(filehandler)
    filehandler.close()
    # initialize ALLCARDS
    global ALLCARDS
    ALLCARDS = initial_52.cards_vec()
    # initialize TYPEWIN
    global TYPEWIN
    filehandler = open("TypeWin.pkl","rb")
    TYPEWIN = pickle.load(filehandler)
    filehandler.close()

if __name__ == 'winningprob':
   initialize()




