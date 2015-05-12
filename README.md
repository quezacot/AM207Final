# AM207Final
AM207 Final Project
Texas hold 'em AI Poker Player Design
Yung-Jen Cheng
Peiheng Hu
Sail Wu
Xide Xia


Our code files are splitted to following 10 files.

deal_compare.py
This file has functions to determine the type of five cards, compare two hands of five cards, and find out the largest five cards from seven cards (board cards + hole cards).
The following functions are used to determine the type of five cards:
flush(fivecards); straight(fivecards); straightflush(fivecards); fourkind(fivecards); fullhouse(fivecards); threekind(fivecards); twopairs(fivecards); onepair(fivecards)
The input is a list of five cards. The output will be a Boolean indicating whether these five cards belong to this kind, and the sorted cards to compare the same type of cards.
e.g. ['KS','TH', '3C', 'KD', '3S'] is five cards of two pairs. The output sorted list is [K, 3, T], which means the larger pair, the smaller pair and the rest high card.
This is used to compare two hands of five cards with the same type.
compare(fivecards1,fivecards2) takes input of two hands of five cards and output the larger one.
maxeach(boardcards,holecards) takes inputs of five board cards and two hole cards, and output the best five cards.

createCompareDict.ipynb
This file generates a table of all possible five cards and sorts them in the order of cards' strength. The output is a pickle file allCombDict_new.p.
The strength is defined as a value that the larger five cards have larger strength. If two five cards are tie then they will have the same strength.

each_compare.py
This file has the same functions in deal_compare.py but eliminates the functions that do not need after the table allCombDict_new.p is generated.

initial_52.py
This file has convenient utilities that transfer numbers to cards, and generate a deck of all 52 cards.

winningprob.py
This file computes the deterministic winning probabilities in flop, turn, and river stages.
It has the following functions:
bestfive() takes input of seven cards and output the best five cards and its strength. This function uses the table allCombDict_new.p we generated.
winp_river() takes inputs of five board cards and two hole cards. Output is the probability to win.
When samplerate is set, this function only runs through part of the combinations of opponent's hole cards.
winp_turn(), winp_flop()takes inputs of four, three board cards respectively and two hole cards. Output is the probability to win.

Bluff_Bayesian_new.py
This file uses Bayesian to compute the bluff probability of the opponent.
Import this file and use fuction Bluff(Hist_Record) to compute this probability.
The input argument is the betting history of the opponent. The output is a probability between [0,1]

Strength_HMM.py
This file uses HMM to estimate the strength of opponent's hole cards.
Import this file and use HMM_state(Hist_Record) to estimate the strength state of opponent's hole cards.
The input argument is the betting history of the opponent. The outpur is a state of opponent's hole cards.
The possible states are 'Low', 'Medium', 'High', or 'No_State'. 'No_State' is returned when there is no betting history to run HMM.

roundcontrol.py
This file has two classes 'player' and 'roundcontrol.'
player class is to store all parameters and handle all actions related to a player, such as their hole cards, money in hand, bet history and betting action.
roundcontrol class is to store all parameters and handle all actions related to the table, such the money in pot, the board cards and to advance game stage.

preflop_table.py
This stores the winning probabilities when only two hole cards are known.
card_prob() takes input of two hole cards the an index to indicate the case whether the player is dealer.

preflop.py
This file controls the game of the preflop stage. (only two hole cards are known)
preflop() takes the input of roundcontrol that contains all information and an indicator of which player is the dealer.
preflopMakeAction() is to handle the bet action. 
The human player will be asked to input when it is his turn to bet.
The computer's will use its AI to determine the bet.

postFlop.py
This file controls the game of the flop, turn, and river stage. (three, four, five board cards are known respectively)
afterPreFlop() deals with the result of preflop(), stores the necessary changes and advances to flop stage.
postFlop() takes the input of roundcontrol that contains all information and an indicator of which player is the dealer.
postflopMakeAction() is to handle the bet action. 
The human player will be asked to input when it is his turn to bet.
The computer's will use its AI to determinge the bet.
adjustpibystate() uses the estimation that computes from Bluff_Bayesian_new.py and Strength_HMM.py

gameflow.py
This file combines preflop.py and postFlop.py to operatie the over all game flow.
It is also responsible to distribute the money to winner in the end of each game and restart the next game if the human player wants to.