
# coding: utf-8

# In[1]:

import random

def transfer(n):
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

def texassim(p):
    cards_d=random.sample(range(52),5+p*2)
    #S:%4==0; H:%4==1; D:%4==2; C:%4==3
    table=[]
    for i in range(5):
        cardt=cards_d.pop(0)
        if cardt%4==0:
            table.append(transfer(cardt//4)+'S')
        elif cardt%4==1:
            table.append(transfer(cardt//4)+'H')        
        elif cardt%4==2:
            table.append(transfer(cardt//4)+'D')
        else:
            table.append(transfer(cardt//4)+'C')   
    
    players=[]
    
    for i in range(p):
        players.append([])
        for j in range(2):
            cardt=cards_d.pop(0)
            if cardt%4==0:
                players[i].append(transfer(cardt//4)+'S')
            elif cardt%4==1:
                players[i].append(transfer(cardt//4)+'H')        
            elif cardt%4==2:
                players[i].append(transfer(cardt//4)+'D')
            else:
                players[i].append(transfer(cardt//4)+'C') 
    
    return table,players


# In[2]:

def highcard(a):
    al=sorted([a[0][0]]+[a[1][0]]+[a[2][0]]+[a[3][0]]+[a[4][0]])   
    dic={'2':0,'3':1,'4':2,'5':4,'6':8,'7':16,'8':32,'9':64,'T':128,'J':256,'Q':512,'K':1024,'A':2048}
    tot=0
    for i in range(5):
        tot+=dic[al[i]]
    return tot

def flush(a):
    if a[0][1]==a[1][1]==a[2][1]==a[3][1]==a[4][1]:
        val=highcard(a)
        return val,True
    else:
        return 0,False

def straight(a):
    al=sorted([a[0][0]]+[a[1][0]]+[a[2][0]]+[a[3][0]]+[a[4][0]])
    if al==['2','3','4','5','A']:
        return 1,True
    elif al==['2','3','4','5','6']:
        return 2,True
    elif al==['3','4','5','6','7']:
        return 3,True
    elif al==['4','5','6','7','8']:
        return 4,True
    elif al==['5','6','7','8','9']:
        return 5,True
    elif al==['6','7','8','9','T']:
        return 6,True
    elif al==['7','8','9','J','T']:
        return 7,True
    elif al==['8','9','J','Q','T']:
        return 8,True
    elif al==['9','J','K','Q','T']:
        return 9,True
    elif al==['A','J','K','Q','T']:
        return 10,True
    else:
        return 0,False
    
def straightflush(a):
    fv,fb=flush(a)
    sv,sb=straight(a)
    if fb and sb:
        return sv,True
    else:
        return 0,False

def fourkind(a):
    dic={'2':0,'3':1,'4':2,'5':4,'6':8,'7':16,'8':32,'9':64,'T':128,'J':256,'Q':512,'K':1024,'A':2048}
    al=sorted([a[0][0]]+[a[1][0]]+[a[2][0]]+[a[3][0]]+[a[4][0]])
    if al[0]==al[1]==al[2]==al[3]:
        return dic[al[0]],dic[al[4]],True
    elif al[1]==al[2]==al[3]==al[4]:
        return dic[al[1]],dic[al[0]],True
    else:
        return 0,0,False

def fullhouse(a):
    dic={'2':0,'3':1,'4':2,'5':4,'6':8,'7':16,'8':32,'9':64,'T':128,'J':256,'Q':512,'K':1024,'A':2048}
    al=sorted([a[0][0]]+[a[1][0]]+[a[2][0]]+[a[3][0]]+[a[4][0]])
    if al[0]==al[1]==al[2] and al[3]==al[4]:
        return dic[al[0]],dic[al[3]],True
    elif al[0]==al[1] and al[2]==al[3]==al[4]:
        return dic[al[2]],dic[al[0]],True
    else:
        return 0,0,False

def threekind(a):
    dic={'2':0,'3':1,'4':2,'5':4,'6':8,'7':16,'8':32,'9':64,'T':128,'J':256,'Q':512,'K':1024,'A':2048}
    al=sorted([a[0][0]]+[a[1][0]]+[a[2][0]]+[a[3][0]]+[a[4][0]])
    if al[0]==al[1]==al[2]:
        return dic[al[0]],dic[al[3]]+dic[al[4]],True
    elif al[1]==al[2]==al[3]:
        return dic[al[1]],dic[al[0]]+dic[al[4]],True
    elif al[2]==al[3]==al[4]:
        return dic[al[2]],dic[al[0]]+dic[al[1]],True
    else:
        return 0,0,False

def twopairs(a):
    dic={'2':0,'3':1,'4':2,'5':4,'6':8,'7':16,'8':32,'9':64,'T':128,'J':256,'Q':512,'K':1024,'A':2048}
    al=sorted([a[0][0]]+[a[1][0]]+[a[2][0]]+[a[3][0]]+[a[4][0]])
    if al[0]==al[1] and al[2]==al[3]:
        return dic[al[0]]+dic[al[2]],dic[al[4]],True
    elif al[0]==al[1] and al[3]==al[4]:
        return dic[al[0]]+dic[al[3]],dic[al[2]],True
    elif al[1]==al[2] and al[3]==al[4]:
        return dic[al[1]]+dic[al[3]],dic[al[0]],True
    else:
        return 0,0,False

def onepair(a):
    dic={'2':0,'3':1,'4':2,'5':4,'6':8,'7':16,'8':32,'9':64,'T':128,'J':256,'Q':512,'K':1024,'A':2048}
    al=sorted([a[0][0]]+[a[1][0]]+[a[2][0]]+[a[3][0]]+[a[4][0]])
    if al[0]==al[1]:
        return dic[al[0]],dic[al[2]]+dic[al[3]]+dic[al[4]],True
    elif al[1]==al[2]:
        return dic[al[1]],dic[al[0]]+dic[al[3]]+dic[al[4]],True
    elif al[2]==al[3]:
        return dic[al[2]],dic[al[0]]+dic[al[1]]+dic[al[4]],True
    elif al[3]==al[4]:
        return dic[al[3]],dic[al[0]]+dic[al[1]]+dic[al[2]],True
    else:
        return 0,0,False


# In[3]:

def compare(a,b):
    sfva,sfba=straightflush(a)
    sfvb,sfbb=straightflush(b)
    if sfva or sfbb:
        if sfva>=sfvb:
            return a,'straightflush'
        else:
            return b,'straightflush'
    
    fourv4a,fourv1a,fourba=fourkind(a)
    fourv4b,fourv1b,fourbb=fourkind(b)
    if fourba and (not fourbb):
        return a,'four-of-a-kind'
    elif (not fourba) and fourbb:
        return b,'four-of-a-kind'
    elif fourba and fourbb:
        if fourv4a>fourv4b:
            return a,'four-of-a-kind'
        elif fourv4a<fourv4b:
            return b,'four-of-a-kind'
        elif fourv4a==fourv4b:
            if fourv1a>=fourv1b:
                return a,'four-of-a-kind'
            else:
                return b,'four-of-a-kind'
 
    fhousev4a,fhousev1a,fhouseba=fullhouse(a)
    fhousev4b,fhousev1b,fhousebb=fullhouse(b)
    if fhouseba and (not fhousebb):
        return a,'full-house'
    elif (not fhouseba) and fhousebb:
        return b,'full-house'
    elif fhouseba and fhousebb:
        if fhousev4a>fhousev4b:
            return a,'full-house'
        elif fhousev4a<fhousev4b:
            return b,'full-house'
        elif fhousev4a==fhousev4b:
            if fhousev1a>=fhousev1b:
                return a,'full-house'
            else:
                return b,'full-house'    
            
    fva,fba=flush(a)
    fvb,fbb=flush(b)
    if fba or fbb:
        if fva>=fvb:
            return a,'flush'
        else:
            return b,'flush'
    
    sva,sba=straight(a)
    svb,sbb=straight(b)
    if sba or sbb:
        if sva>=svb:
            return a,'straight'
        else:
            return b,'straight'    
    
    tv3a,tvra,tba=threekind(a)
    tv3b,tvrb,tbb=threekind(b)
    if tba and (not tbb):
        return a,'three-of-a-kind'
    elif (not tba) and tbb:
        return b,'three-of-a-kind'
    elif tba and tbb:
        if tv3a>tv3b:
            return a,'three-of-a-kind'
        elif tv3a<tv3b:
            return b,'three-of-a-kind'
        elif tv3a==tv3b:
            if tvra>=tvrb:
                return a,'three-of-a-kind'
            else:
                return b,'three-of-a-kind' 
    
    tuv2a,tuvra,tuba=twopairs(a)
    tuv2b,tuvrb,tubb=twopairs(b)
    if tuba and (not tubb):
        return a,'two-pairs'
    elif (not tuba) and tubb:
        return b,'two-pairs'
    elif tuba and tubb:
        if tuv2a>tuv2b:
            return a,'two-pairs'
        elif tuv2a<tuv2b:
            return b,'two-pairs'
        elif tuv2a==tuv2b:
            if tuvra>=tuvrb:
                return a,'two-pairs'
            else:
                return b,'two-pairs'
    
    onev1a,onevra,oneba=onepair(a)
    onev1b,onevrb,onebb=onepair(b)
    if oneba and (not onebb):
        return a,'one-pair'
    elif (not oneba) and onebb:
        return b,'one-pair'
    elif oneba and onebb:
        if onev1a>onev1b:
            return a,'one-pair'
        elif onev1a<onev1b:
            return b,'one-pair'
        elif onev1a==onev1b:
            if onevra>=onevrb:
                return a,'one-pair'
            else:
                return b,'one-pair'
    
    va=highcard(a)
    vb=highcard(b)
    if va>=vb:
        return a,'high-card'
    else:
        return b,'high-card'  


# In[4]:

def maxeach(table,each):
    combine=table+each
    sol=combine[:5]
    for i in range(3):
        for j in range(i+1,4):
            for k in range(j+1,5):
                for l in range(k+1,6):
                    for m in range(l+1,7):
                        each_set=[combine[i]]+[combine[j]]+[combine[k]]+[combine[l]]+[combine[m]]
                        sol,win_type=compare(sol,each_set)
    return sol,win_type


# In[5]:

def maxall(table,allhand):
    eachhand=[]
    for i in range(len(allhand)):
        eachhand.append(maxeach(table,allhand[i]))
    
#     print eachhand
    
    sol={}
    for j in range(len(eachhand)):
        sol_j,w_t=eachhand[j]
        sol_index=j
        for jj in range(len(eachhand)):
            sol_jj,w_tjj=eachhand[jj]
            sol_j,w_t=compare(sol_j,sol_jj)
            if sol_j==sol_jj:
                sol_index=jj
        sol[str(sol_index)]=sol_j,w_t
#     print sol_j
    return sol

