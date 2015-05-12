# AM207Final
AM207 Final Project
Texas hold 'em AI Poker Player Design
Yung-Jen Cheng
Peiheng Hu
Sail Wu
Xide Xia


Our code files are splitted to following 10 files.

Bluff_Bayesian_new.py
This file uses Bayesian to compute the bluff probability of the opponent.
Import this file and use fuction Bluff(Hist_Record) to compute this probability.
The input argument is the betting history of the opponent. The output is a probability between [0,1]

Strength_HMM.py
This file uses HMM to estimate the strength of opponent's hole cards.
Import this file and use HMM_state(Hist_Record) to estimate the strength state of opponent's hole cards.
The input argument is the betting history of the opponent. The outpur is a state of opponent's hole cards.
The possible states are 'Low', 'Medium','High', or 'No_State.' No_State is returned when there is no betting history to run HMM.

deal_compare.py
This file has functions to determine the type of five cards, compare two hands of five cards, and find out the largest five cards from seven cards (board cards + hole cards).
The following functions are used to determine the type of five cards:
flush(fivecards); straight(fivecards); straightflush(fivecards); fourkind(fivecards); fullhouse(fivecards); threekind(fivecards); twopairs(fivecards); onepair(fivecards)
The input is a list of five cards. The output will be a Boolean indicating whether these five cards belong to this kind, and the sorted cards to compare the same type of cards.
e.g. ['KS','TH', '3C', 'KD', '3S'] is five cards of two pairs. The output sorted list is [K, 3, T], which means the larger pair, the smaller pair and the rest high card.
This is used to compare two hands of five cards with the same type.
compare(fivecards1,fivecards2) takes input of two hands of five cards and output the larger one.
maxeach(boardcards,holecards) takes inputs of five board cards and two hole cards, and output the best five cards.

each_compare.py
gameflow.py
initial_52.py
postFlop.py
preflop.py
roundcontrol.py
winningprob.py