#-------------------------------------------------------------------------------
# Name:        each_compare.py
# Purpose:     This file has the same functions in deal_compare.py but eliminates
#              the functions that do not need after the table allCombDict_new.p is generated.
#-------------------------------------------------------------------------------

# These functions are the same as in deal_compare.py
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


# In[1]:

def compare(a,b):
    sfva,sfba=straightflush(a)
    sfvb,sfbb=straightflush(b)
    if sfva or sfbb:
        if sfva>sfvb:
            return a,'straightflush',0
        elif sfva==sfvb:
            return a,'straightflush',1
        else:
            return b,'straightflush',0

    fourv4a,fourv1a,fourba=fourkind(a)
    fourv4b,fourv1b,fourbb=fourkind(b)
    if fourba and (not fourbb):
        return a,'four-of-a-kind',0
    elif (not fourba) and fourbb:
        return b,'four-of-a-kind',0
    elif fourba and fourbb:
        if fourv4a>fourv4b:
            return a,'four-of-a-kind',0
        elif fourv4a<fourv4b:
            return b,'four-of-a-kind',0
        elif fourv4a==fourv4b:
            if fourv1a>fourv1b:
                return a,'four-of-a-kind',0
            elif fourv1a==fourv1b:
                return a,'four-of-a-kind',1
            else:
                return b,'four-of-a-kind',0

    fhousev4a,fhousev1a,fhouseba=fullhouse(a)
    fhousev4b,fhousev1b,fhousebb=fullhouse(b)
    if fhouseba and (not fhousebb):
        return a,'full-house',0
    elif (not fhouseba) and fhousebb:
        return b,'full-house',0
    elif fhouseba and fhousebb:
        if fhousev4a>fhousev4b:
            return a,'full-house',0
        elif fhousev4a<fhousev4b:
            return b,'full-house',0
        elif fhousev4a==fhousev4b:
            if fhousev1a>fhousev1b:
                return a,'full-house',0
            elif fhousev1a==fhousev1b:
                return a,'full-house',1
            else:
                return b,'full-house',0

    fva,fba=flush(a)
    fvb,fbb=flush(b)
    if fba or fbb:
        if fva>fvb:
            return a,'flush',0
        elif fva==fvb:
            return a,'flush',1
        else:
            return b,'flush',0

    sva,sba=straight(a)
    svb,sbb=straight(b)
    if sba or sbb:
        if sva>svb:
            return a,'straight',0
        elif sva==svb:
            return a,'straight',1
        else:
            return b,'straight',0

    tv3a,tvra,tba=threekind(a)
    tv3b,tvrb,tbb=threekind(b)
    if tba and (not tbb):
        return a,'three-of-a-kind',0
    elif (not tba) and tbb:
        return b,'three-of-a-kind',0
    elif tba and tbb:
        if tv3a>tv3b:
            return a,'three-of-a-kind',0
        elif tv3a<tv3b:
            return b,'three-of-a-kind',0
        elif tv3a==tv3b:
            if tvra>tvrb:
                return a,'three-of-a-kind',0
            elif tvra==tvrb:
                return a,'three-of-a-kind',1
            else:
                return b,'three-of-a-kind',0

    tuv2a,tuvra,tuba=twopairs(a)
    tuv2b,tuvrb,tubb=twopairs(b)
    if tuba and (not tubb):
        return a,'two-pairs',0
    elif (not tuba) and tubb:
        return b,'two-pairs',0
    elif tuba and tubb:
        if tuv2a>tuv2b:
            return a,'two-pairs',0
        elif tuv2a<tuv2b:
            return b,'two-pairs',0
        elif tuv2a==tuv2b:
            if tuvra>tuvrb:
                return a,'two-pairs',0
            elif tuvra==tuvrb:
                return a,'two-pairs',1
            else:
                return b,'two-pairs',0

    onev1a,onevra,oneba=onepair(a)
    onev1b,onevrb,onebb=onepair(b)
    if oneba and (not onebb):
        return a,'one-pair',0
    elif (not oneba) and onebb:
        return b,'one-pair',0
    elif oneba and onebb:
        if onev1a>onev1b:
            return a,'one-pair',0
        elif onev1a<onev1b:
            return b,'one-pair',0
        elif onev1a==onev1b:
            if onevra>onevrb:
                return a,'one-pair',0
            elif onevra==onevrb:
                return a,'one-pair',1
            else:
                return b,'one-pair',0

    va=highcard(a)
    vb=highcard(b)
    if va>vb:
        return a,'high-card',0
    elif va==vb:
        return a,'high-card',1
    else:
        return b,'high-card',0

