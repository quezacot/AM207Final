
# coding: utf-8

# In[15]:

import random

def transfer(n):
    '''
    input is a number
    return a string in a card
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

def cards_vec():
    '''
    return a vector of 52 cards in poker
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

