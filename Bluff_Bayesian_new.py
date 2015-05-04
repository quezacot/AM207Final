
# coding: utf-8

# In[57]:

import numpy as np


# In[ ]:

def Two_records(Hist_Record):
    PS=[]
    BL=[]
    if len(Hist_Record)==1:
        return np.asarray(PS),np.asarray(BL)
    
    for i in range(len(Hist_Record)-1):
        each_record=Hist_Record[i]
        if each_record==[]:
            continue
        for j in range(len(each_record)):
            if each_record[j]==[]:
                continue
            for item in each_record[j]:
                PS.append(item[2])
                BL.append(int(item[1]<0.5))
            
            
    return np.asarray(PS),np.asarray(BL)


# In[1]:

def current_PS(Hist_Record):
    cur_record=Hist_Record[-1]
    cur_ps=None
    for item in cur_record:
        if item==[]:
            return cur_ps
        else:
            cur_ps=item[-1][2]
    return cur_ps


# In[56]:

def estimate_bluff(PS_percent_list,Bluff_list,current_PS,sig1=10,sig2=10,N=1000,K=100):
    
    # the bluff function
    def f(theta1, theta2, t):
        return 1.0 / (1 + np.exp(-theta1 -theta2*t))
    # the posterior distribution
    def posterior(theta1, theta2, T=PS_percent_list,I=Bluff_list,sig1=sig1,sig2=sig2):

        # calculate prior based on thetas
        prior = np.exp(-theta1**2 / sig1**2 - theta2**2 / 2/sig2**2)

        # the likelihood function for one datapoint
        def likely(t,i):
            fail = f(theta1, theta2, t)
            failnot = 1 - fail
            #fail**(i)*failnot**(1-i)==fail*i+failnot*(1-i), using addition is simpler than multiplication
            return fail * i + failnot * (1-i)

        # likelihood for each datapoint and stor in the np array
        likelihood = likely(T,I)

        # posterior = prior * likelihood for each given prior
        return prior * np.prod(likelihood)  
    
    Posterior=np.vectorize(posterior)
    
    result=np.zeros(K)
    
    for i in range(K):
        ath1 = np.random.uniform(low=-30, high=30, size=N)

        ath2 = np.random.uniform(low=-30, high=30, size=N)

        ptr=Posterior(ath1,ath2) 

        ysp =  np.random.uniform(low=0, high=np.max(ptr), size=N)

        idx = (ysp<ptr)
        
        result[i]=np.mean(f(ath1[idx], ath2[idx],current_PS))
    return np.mean(result)


# In[ ]:

def Bluff(Hist_Record):
    cur_ps=current_PS(Hist_Record)
    
    PS,BL=Two_records(Hist_Record)
    
    if cur_ps==None:
        return 0.5
    
    if len(PS)==0:
        return 0.5
    
    return estimate_bluff(PS,BL,cur_ps,sig1=10,sig2=10,N=1000,K=100)

