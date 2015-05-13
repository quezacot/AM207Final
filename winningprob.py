#-------------------------------------------------------------------------------
# Name:        winningprob.py
# Purpose:     computes the deterministic winning probabilities in flop, turn,
#              and river stages.
#-------------------------------------------------------------------------------
import deal_compare as dc
import each_compare as ec
import numpy as np
import itertools
import pickle
import initial_52

ALLCOMP = None
ALLCARDS = None
TYPELIST = [u'straightflush', u'fourkind', u'fullhouse', u'flush',
            u'straight', u'threekind', u'twopairs', u'onepair', u'highcard']

# Find out the best five cards from the seven cards
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

# Return a card list of the 52 poker cards that excludes some cards.
def possiblecards(exclude):
    return [ c for c in ALLCARDS if c not in exclude ]

# Determine what type of the five cards is.
def determintype(fivecards):
    funclist = [dc.straightflush, dc.fourkind, dc.fullhouse, dc.flush, dc.straight, dc.threekind, dc.twopairs, dc.onepair]
    for i in xrange(len(funclist)):
        istype = funclist[i](fivecards)
        if istype[-1]:
            return TYPELIST[i]
    return TYPELIST[-1]


#==============================================================================#

# Compute the winning probability in river stage.
# Winc_river computes the counts and winp_river divides them to probability.
def winc_river(boardcards, holecards, exclude=[], samplerate=1.0, opponentholecards=None):
    '''
    boardcards: five board cards as a list. eg. ['KS','TH', '3C', 'KD', '3S']
    holecards: two hile cards as a list. eg. ['AC', '9D']
    exclude: some cards that eliminated from computing the winning probability.
    samplerate: sample part of possible opponent's hole cards to speed up this calculation.
    opponentholecards: a list of two cards of possible opponent's hole card. Leave it as None indicating all possibilities.
    return: wincount: wiin times in all permutations.
            tiecount: tie times in all permutations.
            totalcount: total permutations.
    '''
    assert( len(boardcards) == 5 ) #river has five boardcards
    myhighfive, mystrength = bestfive(boardcards + holecards)
    # the rest possible cards of opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude)
    if opponentholecards is None:
        opponentholecards = list(itertools.combinations(restcards, 2))
    sampleidx = np.arange(len(opponentholecards))
    if samplerate > 1: # only sample part of combinations
        numsamples = int(len(opponentholecards)/samplerate)
        sampleidx = np.random.choice(len(opponentholecards), numsamples, replace=False)

    wincount, tiecount, totalcount = 0,0,0
    for i in sampleidx:
    #for oneholecard in opponentholecards:
        oneholecard = opponentholecards[i]
        totalcount += 1
        hishighfive, hisstrength = bestfive(boardcards + list(oneholecard))
        if mystrength > hisstrength:
            wincount += 1
        elif mystrength == hisstrength:
            tiecount += 1
    return wincount, tiecount, totalcount

# Compute the winning probability in river stage.
def winp_river(boardcards, holecards, exclude=[], samplerate=1.0, opponentholecards=None):
    '''
    inputs are the same as winc_river
    return the winning probability.
    '''
    wincount, tiecount, totalcount= winc_river(boardcards, holecards, exclude, samplerate=samplerate, opponentholecards=opponentholecards)
    return ( wincount + 0.5*tiecount ) / totalcount

#==============================================================================#

# Compute the winning probability in turn stage.
# winc_turn computes the counts and winp_turn divides them to probability.
def winc_turn(boardcards, holecards, exclude=[]):
    '''
    boardcards: four board cards as a list. eg. ['KS','TH', '3C', 'KD']
    holecards: two hile cards as a list. eg. ['AC', '9D']
    exclude: some cards that eliminated from computing the winning probability.
    return: wincount: wiin times in all permutations.
            tiecount: tie times in all permutations.
            totalcount: total permutations.
    '''
    assert( len(boardcards) == 4 ) #turn has four boardcards
    # the rest possible cards of one board card and opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude)
    restboardcard = itertools.combinations(restcards, 1)
    wincount, tiecount, totalcount = 0,0,0
    for oneboardcard in restboardcard:
        subwincount, subtiecount, subtotalcount = winc_river( boardcards+list(oneboardcard), holecards )
        wincount += subwincount
        tiecount += subtiecount
        totalcount += subtotalcount
    return wincount, tiecount, totalcount

# Compute the winning probability in turn stage.
def winp_turn(boardcards, holecards, exclude=[]):
    '''
    inputs are the same as winc_turn
    return the winning probability.
    '''
    wincount, tiecount, totalcount= winc_turn(boardcards, holecards, exclude)
    return ( wincount + 0.5*tiecount ) / totalcount

#==============================================================================#

# Compute the winning probability in flop stage.
# winc_flop computes the counts and winp_flop divides them to probability.
def winc_flop(boardcards, holecards, exclude=[]):
    '''
    boardcards: three board cards as a list. eg. ['KS','TH', '3C']
    holecards: two hile cards as a list. eg. ['AC', '9D']
    exclude: some cards that eliminated from computing the winning probability.
    return: wincount: wiin times in all permutations.
            tiecount: tie times in all permutations.
            totalcount: total permutations.
    '''
    assert( len(boardcards) == 3 ) #flop has three boardcards
    # the rest possible cards of one board card and opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude)
    restboardcard = itertools.combinations(restcards, 1)
    wincount, tiecount, totalcount = 0,0,0
    for oneboardcard in restboardcard:
        subwincount, subtiecount, subtotalcount = winc_turn( boardcards+list(oneboardcard), holecards )
        wincount += subwincount
        tiecount += subtiecount
        totalcount += subtotalcount
    return wincount, tiecount, totalcount

def winp_flop(boardcards, holecards, exclude=[]):
    '''
    inputs are the same as winc_flop
    return the winning probability.
    '''
    wincount, tiecount, totalcount= winc_flop(boardcards, holecards, exclude)
    return ( wincount + 0.5*tiecount ) / totalcount

# Compute the approximated winning counts in flop stage by using samplerate=10 in winp_river.
# winc_flop_appx computes the counts and winp_flop_appx divides them to probability.
def winc_flop_appx(threeboardcards, holecards, exclude=[], samplerate=10.0):
    '''
    boardcards: three board cards as a list. eg. ['KS','TH', '3C']
    holecards: two hile cards as a list. eg. ['AC', '9D']
    exclude: some cards that eliminated from computing the winning probability.
    samplerate: sample part of possible opponent's hole cards to speed up this calculation.
    return: wincount: wiin times in all permutations.
            tiecount: tie times in all permutations.
            totalcount: total permutations.
    '''
    assert( len(threeboardcards) == 3 ) #flop has three boardcards
    # the rest possible cards of opponent's hole cards
    rest47cards = possiblecards(threeboardcards + holecards + exclude)
    restboardcards = itertools.combinations(rest47cards, 2)
    wincount, tiecount, totalcount = 0,0,0
    for twoboardcards in restboardcards:
        fiveboardcards = threeboardcards + list(twoboardcards)
        subwincount, subtiecount, subtotalcount = winc_river(fiveboardcards, holecards, samplerate=samplerate)
        wincount += subwincount
        tiecount += subtiecount
        totalcount += subtotalcount
    return wincount, tiecount, totalcount

# Compute the approximated winning probability in flop stage by using samplerate=10 in winp_river.
def winp_flop_appx(boardcards, holecards, exclude=[], samplerate=10.0):
    '''
    inputs are the same as winc_flop
    return the winning probability.
    '''
    wincount, tiecount, totalcount= winc_flop_appx(boardcards, holecards, exclude, samplerate=samplerate)
    return ( wincount + 0.5*tiecount ) / totalcount

#==============================================================================#

# Compute the winning probability of opponent
def opp_winp_river(boardcards, holecards, exclude=[]):
    '''
    boardcards: five board cards as a list. eg. ['KS','TH', '3C', 'KD', '3S']
    holecards: two hile cards as a list. eg. ['AC', '9D']
    exclude: some cards that eliminated from computing the winning probability.
    return: a dictionary of winning probability of oppoenet's all possible hole cards.
    '''
    assert( len(boardcards) == 5 ) #river has five boardcards
    # the rest possible cards of opponent's hole cards
    restcards = possiblecards(boardcards + holecards + exclude)
    opponentholecards = itertools.combinations(restcards, 2)
    opp_winp = {}
    for oneholecard in opponentholecards:
        holecardlist = list(oneholecard)
        winrate = winp_river(boardcards, holecardlist)
        keyofholecard = "".join( sorted(holecardlist) )
        opp_winp[keyofholecard] = winrate
    return opp_winp

#==============================================================================#

# Initialize the constants when imported
def initialize():
    # initialize ALLCOMP from loading allCombDict_new.p
    global ALLCOMP
    filehandler = open("allCombDict_new.p","rb")
    ALLCOMP = pickle.load(filehandler)
    filehandler.close()
    # initialize ALLCARDS from initial_52
    global ALLCARDS
    ALLCARDS = initial_52.cards_vec()

if __name__ == 'winningprob':
   initialize()




