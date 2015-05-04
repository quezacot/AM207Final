
# coding: utf-8

# In[23]:

import numpy as np
import random
import copy


# In[22]:

states = ('Low', 'Medium','High')
observations = ('call,L', 'call,M', 'call,H','Raise,L','Raise,M','Raise,H')
start_probability = {'Low': 1.0/3, 'Medium':1.0/3,'High':1.0/3 }

transition_probability = {
   'Low' : {'Low': 0.5, 'Medium':1.0/3,'High':1.0/6},
   'Medium' : {'Low': 1.0/3, 'Medium': 1.0/3,'High':1.0/3},
    'High':{'Low': 1.0/6, 'Medium':1.0/3,'High':0.5}    
   }

emission_probability_base = {
   'Low' : {'call,L':50, 'call,M':12, 'call,H':8,'Raise,L':15,'Raise,M':10,'Raise,H':5},
   'Medium' : {'call,L':15, 'call,M':20, 'call,H':15,'Raise,L':15,'Raise,M':20,'Raise,H':25},
    'High':{'call,L':5, 'call,M':10, 'call,H':15,'Raise,L':15,'Raise,M':30,'Raise,H':25}    
   }

emission_probability = {
   'Low' : {'call,L':0.50, 'call,M':0.12, 'call,H':0.08,'Raise,L':0.15,'Raise,M':0.10,'Raise,H':0.05},
   'Medium' : {'call,L':0.15, 'call,M':0.20, 'call,H':0.15,'Raise,L':0.15,'Raise,M':0.20,'Raise,H':0.25},
    'High':{'call,L':0.05, 'call,M':0.10, 'call,H':0.15,'Raise,L':0.15,'Raise,M':0.30,'Raise,H':0.25}    
   }


# In[12]:

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
 
    # Run Viterbi for t > 0
    t=0
    
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
     
    #print_dptable(V)
    (prob, state) = max((V[t][y], y) for y in states)
    return (prob, path[state])


# In[24]:

def update_emission_prob(Hist_Record,ebase=copy.deepcopy(emission_probability_base),e_prob=emission_probability):
    if len(Hist_Record)==1:
        return emission_probability
    
    for i in range(len(Hist_Record)-1):
        if Hist_Record[i]==[]:
            continue
        for j in range(len(Hist_Record[i])):
            
            if Hist_Record[i][j]==[]:
                continue
            
            for each_record in Hist_Record[i][j]:
                if each_record[0]=='K':
                    if each_record[1]<1.0/3:
                        ebase['Low']['call,L']+=1
                    elif each_record[1]<2.0/3:
                        ebase['Medium']['call,L']+=1
                    else:
                        ebase['High']['call,L']+=1
            
                elif each_record[0]=='C':
                    if each_record[1]<1.0/3:
                        if each_record[2]<1.0/3:                            
                            ebase['Low']['call,L']+=1
                        elif each_record[2]<2.0/3:
                            ebase['Low']['call,M']+=1
                        else:
                            ebase['Low']['call,H']+=1
                    elif each_record[1]<2.0/3:
                        if each_record[2]<1.0/3:                            
                            ebase['Medium']['call,L']+=1
                        elif each_record[2]<2.0/3:
                            ebase['Medium']['call,M']+=1
                        else:
                            ebase['Medium']['call,H']+=1
                    else:
                        if each_record[2]<1.0/3:                            
                            ebase['High']['call,L']+=1
                        elif each_record[2]<2.0/3:
                            ebase['High']['call,M']+=1
                        else:
                            ebase['High']['call,H']+=1
                    
                elif each_record[0]=='R':
                    if each_record[1]<1.0/3:
                        if each_record[2]<1.0/3:                            
                            ebase['Low']['Raise,L']+=1
                        elif each_record[2]<2.0/3:
                            ebase['Low']['Raise,M']+=1
                        else:
                            ebase['Low']['Raise,H']+=1
                    elif each_record[1]<2.0/3:
                        if each_record[2]<1.0/3:                            
                            ebase['Medium']['Raise,L']+=1
                        elif each_record[2]<2.0/3:
                            ebase['Medium']['Raise,M']+=1
                        else:
                            ebase['Medium']['Raise,H']+=1
                    else:
                        if each_record[2]<1.0/3:                            
                            ebase['High']['Raise,L']+=1
                        elif each_record[2]<2.0/3:
                            ebase['High']['Raise,M']+=1
                        else:
                            ebase['High']['Raise,H']+=1
    
    low_total=sum(ebase['Low'].values())
    medium_total=sum(ebase['Medium'].values())
    high_total=sum(ebase['High'].values())
    
    emission_probability_new = {
   'Low' : {'call,L': float(ebase['Low']['call,L'])/low_total, 
            'call,M':float(ebase['Low']['call,M'])/low_total, 
            'call,H':float(ebase['Low']['call,H'])/low_total,
            'Raise,L':float(ebase['Low']['Raise,L'])/low_total, 
            'Raise,M':float(ebase['Low']['Raise,M'])/low_total,
            'Raise,H':float(ebase['Low']['Raise,H'])/low_total},
   'Medium' : {'call,L': float(ebase['Medium']['call,L'])/medium_total, 
            'call,M':float(ebase['Medium']['call,M'])/medium_total, 
            'call,H':float(ebase['Medium']['call,H'])/medium_total,
            'Raise,L':float(ebase['Medium']['Raise,L'])/medium_total, 
            'Raise,M':float(ebase['Medium']['Raise,M'])/medium_total,
            'Raise,H':float(ebase['Medium']['Raise,H'])/medium_total},
   'High' : {'call,L': float(ebase['Medium']['call,L'])/high_total, 
            'call,M':float(ebase['High']['call,M'])/high_total, 
            'call,H':float(ebase['High']['call,H'])/high_total,
            'Raise,L':float(ebase['High']['Raise,L'])/high_total, 
            'Raise,M':float(ebase['High']['Raise,M'])/high_total,
            'Raise,H':float(ebase['High']['Raise,H'])/high_total}}    
   
    return  emission_probability_new


# In[25]:

def current_obs(Hist_Record):
    cur_obs=[]
    current_record=Hist_Record[-1]
    for j in range(len(current_record)):
        if current_record[j]==[]:
            return cur_obs
        
        item=current_record[j][-1]
        
        if item[0]=='K':            
            cur_obs.append('call,L')
        
        elif item[0]=='C':
            if item[2]<1.0/3:
                cur_obs.append('call,L')
            elif item[2]<2.0/3:
                cur_obs.append('call,M')
            else:
                cur_obs.append('call,H')
        
        elif item[0]=='R':
            if item[2]<1.0/3:
                cur_obs.append('Raise,L')
            elif item[2]<2.0/3:
                cur_obs.append('Raise,M')
            else:
                cur_obs.append('Raise,H')
    return cur_obs


# In[28]:

def HMM_state(Hist_Record):
    
    cur_obs=current_obs(Hist_Record)
    
    if cur_obs==[]:
        return 'No_State'
    
    emission_prob_new=update_emission_prob(Hist_Record,ebase=copy.deepcopy(emission_probability_base),e_prob=emission_probability)
    
    results=viterbi(cur_obs, states, start_probability, transition_probability, emit_p=emission_prob_new)
        
    return results[1][-1]

