#-------------------------------------------------------------------------------
# Name:        initial_52.py
# Purpose:     This file has convenient utilities that transfer numbers to cards,
#              and generate a deck of all 52 cards.
#-------------------------------------------------------------------------------
import random

# Transfer card representation from an int to a string.
def transfer(n):
    '''
    n: an int from [0, 12]
    return: a string of a card
    '''
    if n>0 and n<9:
        return str(n+1)
    elif n==0:
        return str('A')
    elif n==9:
        return str('T')
    elif n==10:
        return str('J')
    elif n==11:
        return str('Q')
    else:
        return str('K')

# Return a card list of 52 poker cards.
# Use 2 characters to represent one card: e.g. AS is spade A, TC is club ten, 2D is diamond two, and JH is heart J
def cards_vec():
    '''
    return a list of 52 cards in poker
    '''
    origina_num=range(52)
    table=[]
    for cardt in origina_num:
        if cardt%4==0:
            table.append(transfer(cardt//4)+'S')
        elif cardt%4==1:
            table.append(transfer(cardt//4)+'H')
        elif cardt%4==2:
            table.append(transfer(cardt//4)+'D')
        else:
            table.append(transfer(cardt//4)+'C')
    return table

