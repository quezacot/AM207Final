#-------------------------------------------------------------------------------
# Name:        Bluff_Bayesian_new.py
# Purpose:     Uses Bayesian to compute the bluff probability of the opponent.
#-------------------------------------------------------------------------------
import numpy as np

# Extract bet amount history and bluff history of previous games from total bet history record
def Two_records(Hist_Record):
    '''
    Hist_Record: player's bet history
    return: the lists of bet value history and bluff history
    '''
    PS=[] # the list of bet amount in proportion of pot size
    BL=[] # the list of bluff history. 1 bluffed, 0 not
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


# Extract the bet amount of current game. There is bluff state of current game.
def current_PS(Hist_Record):
    '''
    Hist_Record: player's bet history
    return: current bet amount in proportion to pot size
    '''
    cur_record=Hist_Record[-1]
    cur_ps=None
    for item in cur_record:
        if item==[]:
            return cur_ps
        else:
            cur_ps=item[-1][2]
    return cur_ps


# estimate the bluff probability using Bayesian
def estimate_bluff(PS_percent_list,Bluff_list,current_PS,sig1=10,sig2=10,N=1000,K=100):
    '''
    PS_percent_list: the list of bet amount in proportion of pot size
    Bluff_list: the list of bluff history. 1 bluffed, 0 not
    current_PS: current bet amount in proportion to pot size
    sig1, sig2: the parameters of Normal distribution used in the Bayesian model.
    N: MCMC number of samples.
    K: MCMC number of iterations.
    '''
    # the bluff probability density function
    def f(theta1, theta2, t):
        '''
        theta1, theta2: parameters used in the Normal distribution
        t: bet amount in proportion to pot size
        return the pdf based on these parameters
        '''
        return 1.0 / (1 + np.exp(-theta1 -theta2*t))

    # the posterior distribution. The input arguments are the same as estimate_bluff()
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

    # MCMC sampling
    for i in range(K):
        ath1 = np.random.uniform(low=-30, high=30, size=N)
        ath2 = np.random.uniform(low=-30, high=30, size=N)
        ptr=Posterior(ath1,ath2)
        ysp =  np.random.uniform(low=0, high=np.max(ptr), size=N)
        idx = (ysp<ptr)
        result[i]=np.mean(f(ath1[idx], ath2[idx],current_PS))
    return np.mean(result)


# Determine the probability that the opponent bluffed.
def Bluff(Hist_Record):
    '''
    Hist_Record: the bet history of the opponent.
    return: a probability
    '''
    cur_ps=current_PS(Hist_Record)
    PS,BL=Two_records(Hist_Record)

    # return 0.5 if we have no bet history
    if cur_ps==None:
        return 0.5

    if len(PS)==0:
        return 0.5

    return estimate_bluff(PS,BL,cur_ps,sig1=10,sig2=10,N=1000,K=100)

