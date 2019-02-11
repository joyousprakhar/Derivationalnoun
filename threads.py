from itertools import islice
from multiprocessing import Process, Lock
import csv
glovewords={}
fck=0
with open('glove_word.txt', 'r') as document:
    glovewords = {}
    for line in document:
        line = line.split()
        if not line:  # empty line
            continue
        glovewords[line[0]] = []
def lcs1(X, Y, m, n): 
    L = [[0 for x in range(n+1)] for x in range(m+1)]   
    for i in range(m+1): 
        for j in range(n+1): 
            if i == 0 or j == 0: 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1] + 1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1])  
    index = L[m][n]  
    lcs = [""] * (index+1) 
    lcs[index] = "" 
    i = m 
    j = n 
    left=[]
    flag=1
    flag1=0
    right=[]
    while i > 0 and j > 0: 
        #print(X[i-1],' ',Y[j-1])
        if X[i-1] == Y[j-1]: 
            lcs[index-1] = X[i-1] 
            i-=1
            right.extend(Y[j-1])
            j-=1
            index-=1
            if i==0 :
                #print(',')
                left.extend(',')
            flag=0
            flag1=0
        elif L[i-1][j] > L[i][j-1]:
            if flag==0:
                left.extend(',')
                flag=1
            if flag1==0:
                right.extend(',')
                flag1=1
            i-=1
        else:
            if flag==0:
                #print(',')
                left.extend(',')
                flag=1
            if flag1==0:
                right.extend(',')
                flag1=1
            left.extend(Y[j-1])
            j-=1
    while i > 0:
        i-=1
    while j > 0:
        left.extend(Y[j-1])
        j-=1
    string="".join(left)
    string1=string[::-1]
    string5="".join(right)
    string6=string5[::-1]
#     print(string6)
    string2=[]
    i=0
    while i<(len(X)):
        if X[i]=='!':
            if i!=0:
                string2.extend(','+X[i]+X[i+1]+X[i+2])
            else:
                string2.extend(X[i]+X[i+1]+X[i+2])
            i+=3
        else:
            i+=1
    if(X[i-1])!='!':
        string2.extend(',')
    string3="".join(string2)
    return "".join(lcs),string1,string3,string6
def check(x,y):
    z,w,u,v=lcs1(x,y,len(x),len(y))
    u=u.split(',')
    w=w.split(',')
#     print(u)
#     print(w)
    if(len(w)!=len(u)):
        return -1
    t=[]
    t.append([])
    i=0
    j=0
    while i <len(x):
        if x[i]=='!':
            if(i!=0):
                t[j]="".join(t[j])
            i+=3
            j+=1
            t.append([])
        else:
            t[j].extend(x[i])
            i+=1
    t[j]="".join(t[j])
#     print(t)
    v=v.split(',')
#     print(v)
    i=0
    while i <len(t):
        try:
            if len(t[i])==0 and v[i]!='':
                return -1
            elif  len(t[i])!=0 and v[i]=='':
                return -1
            elif  len(t[i])==0 and v[i]=='':
                i+=1
                continue
            elif t[i]!=v[i]:
                return -1
        except IndexError:
            return -1
        i+=1
    
    i=0
    p=[]
    while i<len(w):
        if w[i]=='' and u[i]!='':
            return -1
        elif w[i]!='' and u[i]=='':
            return -1
        if w[i]=='' and u[i]=='':
            i+=1
            continue
        p.append(w[i])
        i+=1
    
    return p
def add(X,Y):
    i=0 
    j=0
    while i<(len(X)):
        if X[i]=='#':
            i+=3
            j+=1
        else:
            i+=1
    string2=[]
    for i in range(j+1) :
        string2.append([])
#     print(string2)
    i=j=0
    while i<(len(X)):
        if X[i]=='#':
            j+=1
            i+=3
        else:
            string2[j].extend(X[i])
            i+=1
#     print(j)
#     print(len(Y))
    if (j)!=(len(Y)):
        return -1
#     print(string2)
    z=[]
    i=0
    while i < j:
        z.extend(string2[i])
        z.extend(Y[i])
        i+=1
    z.extend(string2[i])
    return "".join(z)
def transform(x,y):
    X=x[0]
    Y=check(X,y)
    if(Y==-1):
        return -1
#     print(x[0])
#     print(Y)
    z=add(x[1],Y)
    return z

patterns={'!1!ly': {'#1#': {'-ly', '-y', '-ally'}, '#1#e': {'-ly'}, '#1#n': {'-ly'}, '#1#is': {'-ly'}}, '!1!ist': {'#1#': {'-ist'}, '#1#y': {'-ist'}, '#1#e': {'-ist'}, '#1#us': {'-ist'}, '#1#s': {'-ist'}, '#1#a': {'-ist'}, '#1#o': {'-ist'}, '#1#ous': {'-ist'}, '#1#es': {'-ist'}, '#1#um': {'-ist'}, '#1#ue': {'-ist'}, '#1#k': {'-ist'}, '#1#ah': {'-ist'}, '#1#as': {'-ist'}}, '!1!ian': {'#1#': {'-ian', '-an'}, '#1#e': {'East_Frisian', '-ian'}, '#1#a': {'-ian'}, '#1#y': {'-ian', '-an'}, '#1#o': {'-ian'}, '#1#us': {'-ian'}, '#1#ah': {'-ian'}, '#1#os': {'-ian'}, '#1#en': {'-ian'}, '#1#s': {'-ian'}, 'Tierra_del_#1#o': {'-ian'}, '#1#um': {'-ian'}, '#1#es': {'-ian'}, '#1#as': {'-ian'}, '#1#k': {'-ian'}, '#1#n': {'-ian'}, '#1#on': {'-ian'}, '#1#u': {'-ian'}, '#1#er': {'-ian'}, '#1#ae': {'-ian'}, '#1#ogen': {'-ian'}, '#1#enum': {'-ian'}}, '!1!like': {'#1#': {'-like'}}, '!1!able': {'#1#': {'-able'}, '#1#e': {'-able'}, '#1#er': {'-able'}, '#1#io': {'-able'}, '#1#y': {'-able'}, '#1#o': {'-able'}, '#1#ial': {'-able'}}, '!1!ily': {'#1#y': {'-ly'}, '#1#ey': {'-ly'}}, '!1!ship': {'#1#': {'relationship', '-ship'}, '#1#-cat': {'-ship'}, '#1#e': {'-ship'}}, '!1!ophyte': {'#1#a': {'-phyte'}, '#1#': {'-phyte'}, '#1#um': {'-phyte'}, '#1#us': {'-phyte'}, '#1#ic': {'-phyte'}}, '!1!ally': {'#1#': {'-ly', '-ally'}, '#1#e': {'-ally'}, '#1#y': {'-ally'}}, '!1!ling': {'#1#': {'-ing', '-ling'}, '#1#e': {'-ling'}}, '!1!y': {'#1#e': {'-ly', '-y'}, '#1#': {'-y', '-ly'}, '#1#ue': {'-y'}, '#1#atic': {'-y'}, '#1#ouac': {'-y'}, '#1#eth': {'-y'}, '#1#s': {'-y'}, '#1#ergarten': {'-y'}, '#1#an': {'-y'}, '#1#rum': {'-y'}, '#1#er': {'-y'}, '#1#ress': {'-y'}, '#1#roid': {'-y'}, '#1#idextrous': {'-y'}, 'a#1#': {'-y'}, '#1#ic': {'-y'}, '#1#in': {'-y'}, '#1#ron': {'-y'}, 'to#1#o': {'-y'}, '#1#red': {'-y'}, '#1#a': {'-y'}, '#1#hansa': {'-y'}, '#1#ile': {'-y'}, '#1#om': {'-y'}, '#1#ah': {'-y'}, '#1#on': {'-y'}, '#1#ependent': {'-y'}, '#1#ous': {'-y'}, '#1#enile': {'-y'}, '#1#igan': {'-y'}, '#1#nile': {'-y'}, '#1#ellous': {'-y'}, '#1#ington': {'-y'}, '#1#over': {'-y'}, '#1#pensive': {'-y'}, '#1#ival': {'-y'}}, '!1!al': {'#1#': {'-alis', '-al'}, '#1#o': {'-al'}, '#1#e': {'-cidal', '-al'}, '#1#us': {'-al'}, '#1#is': {'-al'}, '#1#s': {'-al'}, '#1#um': {'-al'}, '#1#on': {'-al'}, '#1#es': {'-al'}, '#1#y': {'-al'}, 'a#1#itas': {'-al'}, '#1#el': {'-al'}, '#1#os': {'-al'}, '#1#ous': {'-al'}}, '!1!ing': {'#1#e': {'-ing'}, '#1#': {'-ing'}, '#1#a': {'-ing'}, '#1#y': {'-ing'}, '#1#o': {'-ing'}, '#1#er': {'-ing'}, '#1#ent': {'-ing'}}, '!1!l': {'#1#': {'-el', '-al'}, '#1#d': {'-al'}, '#1#nt': {'-al'}, '#1#e': {'-al'}, '#1#_mater': {'-al'}}, '!1!ical': {'#1#y': {'-ical', '-ic'}, '#1#e': {'-ical'}, '#1#': {'-ical'}, '#1#ue': {'-ical'}, '#1#on': {'-ical'}, '#1#es': {'-ical'}, '#1#ne': {'-ical'}, '#1#os': {'-ical'}}, 'e!1!ous': {'E#1#ae': {'-ous'}, 'E#1#a': {'-ous'}}, '!1!osis': {'#1#e': {'-osis'}, '#1#': {'-osis'}, '#1#ic': {'-osis'}, '#1#um': {'-osis'}, '#1#i': {'-osis'}, '#1#a': {'-osis'}, '#1#us': {'-osis'}, '#1#es': {'-osis'}, '#1#in': {'-osis'}}, '!1!ic': {'#1#': {'-ic'}, '#1#y': {'-ic'}, '#1#a': {'purpura', '-ic'}, '#1#us': {'-ic'}, '#1#e': {'-ic'}, '#1#os': {'-ic'}, '#1#es': {'-ic'}, '-#1#e': {'-ic'}, '#1#ula': {'-ic'}, '#1#um': {'-ic'}, '#1#o': {'-ic'}, '#1#anda': {'-ic'}, '#1#ah': {'-ic'}, '#1#on': {'-ic'}, '#1#enum': {'-ic'}, '#1#or': {'-ic'}, '#1#ol': {'-ic'}, '#1#u': {'-ic'}, '#1#osis': {'-ic'}, '#1#ue': {'-ic'}, '#1#s': {'-ic'}, '#1#osol': {'-ic'}, '#1#ese': {'-ic'}, '#1#ea': {'-ic'}, '#1#ene': {'-ic'}, '#1#en': {'-ic'}, '#1#er': {'-ic'}}, '!1!c': {'#1#s': {'-ic'}, '#1#a': {'-ic'}, '#1#um': {'-ic'}, '#1#': {'-ac', '-ic'}, '#1#ne': {'-ic'}, '#1#n': {'-ic'}, '#1#de': {'-ic'}, '#1#ty': {'-ic'}, '#1#sm': {'-ic'}, '#1#an': {'-ic'}, '#1#ze': {'-ic'}}, '!1!n': {'#1#': {'-an', 'deflagrare', '-n', '-ian', 'Italia'}, '#1#s': {'-ian', '-an'}, '#1#e': {'-an'}, '#1#h': {'-an'}, 'fur#1#l': {'-an'}}, 'e!1!osis': {'E#1#a': {'-osis'}, 'E#1#': {'-osis'}}, '!1!d': {'#1#': {'-oid', '-ed'}, '#1#ve': {'-ed'}, '#1#a': {'-oid'}, '#1#s': {'-ed'}}, '!1!ability': {'#1#': {'-ability'}, '#1#e': {'-ability'}}, '!1!kish': {'#1#': {'-ish'}}, '!1!tic': {'#1#sis': {'-otic', '-ic'}, '#1#s': {'-otic', '-ic'}, '#1#': {'-ic'}, '#1#m': {'-ic'}, '#1#cy': {'-ic'}, '#1#n': {'-ic'}, '#1#agus': {'-ic'}, '#1#sity': {'-ic'}, '#1#sy': {'-ic'}}, '!1!bie': {'#1#': {'-ie'}, '#1#orah': {'-ie'}}, '!1!ed': {'#1#': {'-ed'}, '#1#a': {'-ed'}, '#1#s': {'-ed'}, '#1#us': {'-ed'}, '#1#is': {'-ed'}, '#1#ion': {'-ed'}, '#1#ing': {'-ed'}, '#1#y': {'-ed'}}, '!1!izette': {'#1#y': {'-ette'}}, '!1!dom': {'#1#': {'-dom'}, '#1#ale': {'-dom'}}, '!1!st': {'#1#a': {'-ist'}, '#1#': {'-ist'}, '#1#cs': {'-ist'}, '#1#ve': {'-ist'}, '#1#c': {'-ist'}, '#1#e': {'-ist'}, '#1#ze': {'-ist', 'catechista'}, '#1#ty': {'-ist'}, '#1#on': {'-ist'}}, '!1!ation': {'#1#e': {'-ation'}, '#1#': {'-ation'}, '#1#um': {'-ation'}, '#1#o': {'-ation'}, '#1#us': {'-ation'}}, '!1!by': {'#1#': {'-y'}, '#1#ant': {'-y'}, '#1#orah': {'-y'}, '#1#son': {'-y'}}, '!1!oid': {'#1#': {'-oid'}, '#1#a': {'-oid'}, '#1#e': {'-oid'}, '#1#in': {'-oid'}, '#1#ix': {'-oid'}, '#1#ite': {'-oid'}, '#1#us': {'-oid'}, '#1#um': {'-oid'}, '#1#ic': {'-oid'}, '#1#er': {'-oid'}, '#1#y': {'-oid'}, '#1#ate': {'-oid'}, '#1#as': {'-oid'}, '#1#al': {'-oid'}, '#1#ical': {'-oid'}, '#1#ian': {'-oid'}, '#1#ion': {'-oid'}, '#1#ence': {'-oid'}, '#1#ium': {'-oid'}, '#1#i': {'-oid'}, '#1#im': {'-oid'}, '#1#ia': {'-oid'}, '#1#is': {'-oid'}, '#1#u': {'-oid'}, '#1#ene': {'-oid'}, '#1#ile': {'-oid'}, '#1#eus': {'-oid'}, '#1#ee': {'-oid'}}, '!1!ish': {'#1#': {'-ish'}, '#1#e': {'-ish'}, '#1#y': {'-ish'}, '#1#head': {'-ish'}, '#1#s': {'-ish'}, '#1#a': {'-ish'}, '#1#wall': {'-ish'}, '#1#ous': {'-ish'}, '#1#w': {'-ish'}}, '!1!vian': {'#1#ughs': {'-ian'}, '#1#uv': {'-ian'}, '#1#': {'-ian'}, '#1#w': {'-ian'}}, '!1!ette': {'#1#': {'-ette'}, '#1#ie': {'-ette'}, '#1#a': {'-ette'}, '#1#o': {'-ette'}, '#1#ine': {'-ette'}, '#1#ance': {'-ette'}, '#1#in': {'-ette'}, '#1#it': {'-ette'}, '#1#y': {'-ette'}, '#1#oline': {'-ette'}}, '!1!ie': {'#1#': {'-y', '-ie'}, '#1#e': {'-ie'}, '#1#ellunge': {'-ie'}, '#1#emia': {'-ie'}, '#1#er': {'-ie'}, '#1#onen': {'-ie'}, '#1#er_machine': {'-ie'}, '#1#ela': {'-ie'}, '#1#nance': {'-ie'}, '#1#elette': {'-ie'}, '#1#oundlander': {'-ie'}, '#1#raham': {'-ie'}, '#1#et': {'-ie'}, '#1#lahoma': {'-ie'}, '#1#a-percha': {'-ie'}, '#1#el': {'-ie'}, '#1#amin': {'-ie'}, '#1#ane': {'-ie'}, '#1#est': {'-ie'}, '#1#weiler': {'-ie'}, '#1#anent': {'-ie'}, '#1#ence': {'-ie'}, '#1#oline': {'-ie'}, '#1#entinian': {'-ie'}, '#1#ard': {'-ie'}, '#1#rich': {'-ie'}, '#1#ecue': {'-ie'}, '#1#enile': {'-ie'}, '#1#eth': {'-ie'}, '#1#ribution': {'-ie'}, '#1#keeper': {'-ie'}, '#1#maker': {'-ie'}, '#1#asa': {'-ie'}, '#1#ustus': {'-ie'}, '#1#al': {'-ie'}, '#1#ara': {'-ie'}, '#1#sgefangener': {'-ie'}, '#1#omer': {'-ie'}, '#1#on': {'-ie'}, '#1#an': {'-ie'}, '#1#eboy': {'-ie'}, '#1#ert': {'-ie'}}, '!1!ny': {'#1#': {'-y'}, '#1#cent': {'-y'}, '#1#itor': {'-y'}, '#1#ald': {'-y'}}, '!1!ial': {'#1#y': {'-al'}, '#1#es': {'-al'}}, 'omni!1!': {'-#1#': {'omni-'}}, '!1!i': {'#1#us': {'-i'}, '#1#': {'-i'}}, 'cry!1!': {'-#1#': {'cryo-'}}, '!1!py': {'#1#': {'-y'}, '#1#ileptic': {'-y'}, '#1#sy': {'-y'}}, '!1!-!2!ish': {'#1#_#2#': {'-ish'}}, '!1!an': {'#1#s': {'-ian', '-an'}, '#1#': {'-ian', '-an'}, '#1#e': {'-ian', '-an'}, '#1#us': {'-ian', '-an'}, '#1#um': {'-ian', '-an'}, '#1#o': {'-ian', '-an'}, '#1#u': {'-an'}, '#1#on': {'-an'}, '#1#i': {'-an'}, '#1#ne': {'-ian'}, '#1#os': {'-an'}, '#1#n': {'-an'}, '#1#c': {'-ian'}, '#1#ia': {'-an'}}, 'phot!1!': {'-#1#': {'photo-'}}, '!1!ble': {'#1#te': {'-able'}, '#1#re': {'-able'}, '#1#': {'-able'}}, '!1!ic_acid': {'#1#': {'-ic'}, '#1#e': {'-ic'}, '#1#y': {'-ic'}, '#1#o': {'-ic'}, '#1#um': {'-ic'}, '#1#a': {'-ic'}}, '!1!ous': {'#1#': {'-ous'}, '#1#a': {'-ous'}, '#1#e': {'-ous'}, '#1#y': {'-ous'}, '#1#um': {'-ous'}, '#1#ic': {'-ous'}, '#1#ty': {'-ous'}, '#1#ium': {'-ous'}, '#1#is': {'-ous'}, '#1#enum': {'-ous'}, '#1#es': {'-ous'}, '#1#ine': {'-ous'}, '#1#ie': {'-ous'}, '#1#s': {'-ous'}, '#1#ese': {'-ous'}, '#1#etic': {'-ous'}}, '!1!ely': {'#1#le': {'-ly'}}, '!1!age': {'#1#': {'-age'}, '#1#e': {'-age'}}, '!1!e': {'#1#t': {'-ie'}, '#1#mo': {'-ie'}, '#1#osis': {'-ie'}, '#1#ng_picture': {'-ie'}, '#1#navian': {'-ie'}, '#1#gan': {'-ie'}, '#1#nese': {'-ie'}, '#1#val': {'-ie'}}, '!1!pable': {'#1#': {'-able'}}, '!1!s': {'#1#': {'-s'}, '#1#d': {'-s'}, '#1#_Four': {'-s'}, '#1#in': {'-s'}, '#1#er': {'-s'}, '#1#man': {'-s'}}, '!1!tical': {'#1#cy': {'-ical'}, '#1#': {'-ical'}}, 'apo!1!': {'-#1#': {'apo-'}}, '!1!nish': {'#1#': {'-ish'}}, '!1!dable': {'#1#': {'-able'}}, '!1!us': {'#1#n': {'-ous'}, '#1#se': {'-ous'}, '#1#': {'-ous'}, '#1#s': {'-ous'}}, '!1!ied': {'#1#y': {'-ed'}}, '!1!t': {'#1#': {'-ist'}, '#1#m': {'-ist', 'Sade'}, '#1#is': {'-ist'}, '#1#e': {'-ist'}}, '!1!aholic': {'#1#': {'-aholic'}, '#1#y': {'-aholic'}}, '!1!dy': {'#1#': {'-y'}, '#1#red': {'-y'}, '#1#pole': {'-y'}, '#1#eleine': {'-y'}, '#1#eo': {'-y'}, '#1#illac': {'-y'}, '#1#ka': {'-y'}, '#1#wig': {'-y'}}, 'auto!1!': {'-#1#': {'auto-'}, '#1#': {'auto-'}}, '!1!nic': {'#1#se': {'-ic'}, '#1#': {'-ic'}}, '!1!ted': {'#1#': {'-ed'}, '#1#sion': {'-ed'}}, '!1!erly': {'#1#': {'-ly'}}, 'andro!1!': {'-#1#': {'andro-'}}, 'lith!1!': {'-#1#': {'lith-'}}, '!1!om': {'#1#': {'-dom'}}, '!1!-like': {'#1#': {'-like'}}, 'archaeo!1!': {'-#1#': {'archaeo-'}}, '!1!iable': {'#1#y': {'-able'}, '#1#e': {'-able'}}, 'a!1!ous': {'A#1#ae': {'-ous'}, 'A#1#a': {'-ous'}}, '!1!id': {'#1#se': {'-oid'}, '#1#s': {'-oid'}, '#1#ne': {'-oid'}, '#1#': {'-oid'}, '#1#n': {'-oid'}, '#1#o': {'-oid'}, '#1#t': {'-oid'}, '#1#us': {'-oid'}, '#1#de': {'-oid'}, '#1#l': {'-oid'}, '#1#w': {'-oid'}}, '!1!gy': {'#1#': {'-y'}, '#1#nature': {'-y'}, '#1#nore': {'-y'}, '#1#ness': {'-y'}, '#1#nant': {'-y'}}, '!1!gish': {'#1#': {'-ish'}}, '!1!my': {'#1#': {'-y'}, '#1#aha': {'-y'}, '#1#b': {'-y'}, '#1#in_de_fer': {'-y'}, '#1#entine': {'-y'}}, 'r!1!ous': {'R#1#ae': {'-ous'}, 'R#1#a': {'-ous'}}, 'noso!1!': {'-#1#': {'noso-'}}, 'm!1!n': {'M#1#e': {'-an'}, 'M#1#': {'-ian', '-an'}}, '!1!led': {'#1#': {'-ed'}}, '!1!nable': {'#1#': {'-able'}}, 'ge!1!': {'-#1#': {'geo-'}}, '!1!tion': {'#1#': {'-ation'}, '#1#ry': {'-ation'}, '#1#l': {'-ation'}, '#1#re': {'-ation'}}, 'S!1!po': {'s#1#tic_tank': {'-o'}}, '!1!gable': {'#1#': {'-able'}}, '!1!pie': {'#1#': {'-ie'}}, '!1!enish': {'#1#ine': {'-ish'}}, '!1!itude': {'#1#': {'-itude'}, '#1#e': {'-itude'}}, 'R!1!y': {'T._r#1#': {'-y'}}, 'p!1!n': {'P#1#': {'-ian', '-an'}, 'P#1#e': {'-an'}}, '!1!vy': {'#1#ouac': {'-y'}, '#1#erage': {'-y'}, '#1#': {'-y'}, '#1#idend': {'-y'}, '#1#ilian': {'-y'}}, '!1!lic': {'#1#': {'-ic'}}, 'c!1!n': {'C#1#': {'-ian', '-an'}, 'C#1#e': {'-an'}}, '!1!inal': {'#1#en': {'-al'}, '#1#e': {'-al'}, '#1#o': {'-al'}}, 'a!1!cal': {'A#1#a': {'-ical'}}, 'are!1!': {'-#1#': {'areo-'}}, '!1!loid': {'#1#': {'-oid'}}, '!1!o!2!': {'#1##2#': {'-oid', '-ous'}, '#1##2#e': {'-oid'}}, '!1!ged': {'#1#': {'-ed'}}, 'A!1!ship': {'a#1#': {'-ship'}}, 'K!1!ist': {'k#1#': {'-ist'}}, '!1!bing': {'#1#': {'-ing'}}, '!1!potts': {'#1#ip': {'-s'}}, 'demi!1!': {'-#1#': {'demi-'}}, 's!1!ic': {'S#1#es': {'-ic'}}, '!1!ably': {'#1#e': {'-ably'}, '#1#': {'-able', '-ably'}}, 'necro!1!': {'-#1#': {'necro-'}}, 'm!1!ous': {'M#1#ae': {'-ous'}, 'M#1#i': {'-ous'}, 'M#1#a': {'-ous'}, 'M#1#es': {'-ous'}}, '!1!lable': {'#1#': {'-able'}}, 'b!1!l': {'B#1#': {'-al'}}, 'philo!1!': {'-#1#': {'philo-'}, '#1#': {'philo-'}}, 'b!1!an': {'B#1#s': {'-an'}}, '!1!y_pie': {'#1#e': {'-y'}}, '!1!ious': {'#1#y': {'-ous'}, '#1#': {'-ous'}, '#1#e': {'-ous'}}, '!1!rous': {'#1#er': {'-ous'}, '#1#ur': {'-ous'}, '#1#or': {'-ous'}}, '!1!h': {'#1#': {'-th'}}, '!1!bish': {'#1#': {'-ish'}}, 'o!1!otic': {'O#1#a': {'-ic'}}, '!1!cranterian': {'#1#': {'-ian'}}, '!1!tist': {'#1#': {'-ist'}, '#1#ce': {'-ist'}}, 'A!1!n': {'a#1#': {'-an'}}, 'Ions': {'John': {'-s'}}, '!1!ky': {'#1#': {'-y'}, '#1#can': {'-y'}, '#1#stasy': {'-y'}, '#1#castic': {'-y'}}, '!1!tosis': {'#1#': {'-osis'}}, '!1!idic': {'#1#us': {'-ic'}}, '!1!tte': {'#1#': {'-ette'}, '#1#e': {'-ette'}, '#1#r': {'-ette'}}, '!1!sy': {'#1#phorus': {'-y'}, '#1#': {'-y'}, '#1#tic': {'-y'}, '#1#cilla': {'-y'}}, 'Ozz!1!': {'-#1#': {'-ie'}}, '!1!ped': {'#1#': {'-ed'}}, 'd!1!ous': {'D#1#ae': {'-ous'}, 'D#1#a': {'-ous'}}, 'T!2!!1!an': {'t#2#-#1#us': {'-ian'}}, '!1!-!2!ed': {'#1#_#2#': {'-ed'}}, 'h!1!e': {'H#1#mer': {'-ie'}}, '!1!table': {'#1#': {'-able'}, '#1#ful': {'-able'}}, 'p!1!ous': {'P#1#ae': {'-ous'}, 'P#1#es': {'-ous'}, 'P#1#a': {'-ous'}}, 'li!1!ey': {'lu#1#': {'-y'}}, '!1!amic': {'#1#ome': {'-ic'}}, '!1!!2!ical': {'#1#_#2#e': {'-ical'}}, 'chalc!1!': {'-#1#': {'chalco-'}}, 'para!1!': {'-#1#': {'para-'}}, 'syncranter!1!': {'-#1#': {'syn-'}}, '!1!bility': {'#1#te': {'-ability'}}, '!1!!2!ing': {'#1#_#2#': {'-ing'}, '#1#_#2#e': {'-ing'}, '#1#_#2#es': {'-ing'}}, '!1!als': {'#1#': {'-al'}}, 'spermato!1!': {'-#1#': {'spermato-'}}, '!1!ilist': {'#1#le': {'-ist'}}, '!1!a!2!': {'#1#u#2#': {'-able'}, '#1#o#2#': {'-th'}}, '!1!ty': {'#1#': {'-y'}, '#1#itia': {'-y'}, '#1#esque': {'-y'}, '#1#ural': {'-y'}}, '!1!ding': {'#1#': {'-ing'}}, 'e!1!n': {'E#1#': {'-ian', '-an'}}, 'bacill!1!': {'-#1#': {'bacillo-'}}, '!1!ey': {'#1#art': {'-y'}, '#1#': {'-y'}}, '!1!inous': {'#1#o': {'-ous'}, '#1#e': {'-ous'}, '#1#en': {'-ous'}}, 'f!1!osis': {'F#1#um': {'-osis'}, 'F#1#a': {'-osis'}}, '!1!inoid': {'#1#e': {'-oid'}, '#1#en': {'-oid'}}, 'haem!1!': {'-#1#': {'haemo-'}}, '!1!o': {'#1#': {'-o'}, '#1#man': {'-o'}, '#1#red': {'-o'}, '#1#anese': {'-o'}, '#1#ledon': {'-o'}, '#1#wich': {'-o'}, '#1#ersation': {'-o'}, '#1#er': {'-o'}, '#1#ins': {'-o'}, '#1#regationalist': {'-o'}, 'tri#1#e': {'-o'}, '#1#e': {'-o'}, '#1#entation': {'-o'}, '#1#iration': {'-o'}, '#1#ician': {'-o'}, '#1#y': {'-o'}, '#1#ative': {'-o'}, '#1#ing_club': {'-o'}, '#1#esan': {'-o'}, '#1#mantle': {'-o'}, '#1#umentary': {'-o'}, '#1#el': {'-o'}, '#1#abwean': {'-o'}, '#1#feast': {'-o'}, '#1#ibution': {'-o'}, '#1#ering': {'-o'}, '#1#iant': {'-o'}, '#1#age': {'-o'}, '#1#enson': {'-o'}, '#1#ylated_spirits': {'-o'}, '#1#avation': {'-o'}, '#1#itality': {'-o'}, '#1#ington': {'-o'}, '#1#ian': {'-o'}, '#1#ified': {'-o'}, '#1#alist': {'-o'}}, 'North_!1!ian': {'#1#a': {'-ian'}}, '!1!th': {'#1#': {'-th'}, '#1#e': {'-th'}, '#1#ng': {'-th'}, '#1#l': {'-th'}, '#1#w': {'-th'}}, 'Hellen!1!': {'-#1#': {'Helleno-'}}, '!1!ping': {'#1#': {'-ing'}}, 'g!1!able': {'G#1#e': {'-able'}}, '!1!iage': {'#1#y': {'-age'}}, '!1!gie': {'#1#': {'-y', '-ie'}, '#1#nant': {'-ie'}, '#1#uana': {'-y'}}, '!1!bed': {'#1#': {'-ed'}}, 'b!1!ous': {'B#1#ae': {'-ous'}}, 'n!1!dy': {'N#1#': {'-y'}}, 'aerohydr!1!': {'-#1#': {'aero-'}}, '!1!aian': {'#1#y': {'-ian'}}, '!1!nian': {'#1#': {'-ian'}}, 'micro!1!': {'#1#': {'micro-'}, '-#1#': {'micro-'}}, '!1!iability': {'#1#y': {'-ability'}}, '!2!-!1!ish': {'#2#_#1#': {'-ish'}}, 'C!1!y': {'c#1#': {'-y'}}, 'nepion!1!': {'-#1#': {'-n-'}}, 'Sino-Xen!1!': {'-#1#': {'Sino-'}}, '!1!ral': {'#1#': {'-al'}, '#1#er': {'-al'}}, 'h!1!ous': {'H#1#ae': {'-ous'}, 'H#1#a': {'-ous'}}, '!2!!1!ed': {'#2#-#1#': {'-ed'}}, 'a!1!n': {'A#1#': {'-n', '-ian', '-an'}}, '!1!roid': {'#1#er': {'-oid'}}, 's!1!ous': {'S#1#a': {'-ous'}, 'S#1#ae': {'-ous'}}, 'b!1!n': {'B#1#': {'-n', '-an'}}, '!1!pish': {'#1#': {'-ish'}}, 'j!1!oid': {'J#1#a': {'-oid'}}, '!1!-ish': {'#1#': {'-ish'}}, '!1!lability': {'#1#': {'-ability'}}, 'cruci!1!ist': {'#1#': {'-ist'}}, '!1!dish': {'#1#': {'-ish'}}, 'k!1!osis': {'K#1#a': {'-osis'}}, 'n!1!ous': {'N#1#ae': {'-ous'}}, '!1!to': {'#1#istician': {'-o'}, '#1#': {'-o'}}, '!1!elps': {'#1#ilip': {'-s'}}, 'G!1!ie': {'g#1#': {'-ie'}}, 'h!1!an': {'H#1#s': {'-an'}, 'H#1#i': {'-an'}}, 'l!1!ous': {'L#1#ae': {'-ous'}, 'L#1#a': {'-ous'}}, '!1!j!2!ist': {'#1#i#2#': {'-ist'}}, '!1!ual': {'#1#': {'-al'}}, '!1!coid': {'#1#x': {'-oid'}}, 's!1!oid': {'S#1#ia': {'-oid'}, 'S#1#us': {'-oid'}, 'S#1#es': {'-oid'}, 'S#1#a': {'-oid'}, 'S#1#um': {'-oid'}}, '!1!tly': {'#1#s': {'-ly'}}, '!1!ggens': {'#1#ck': {'-s'}}, 'p!1!ic': {'P#1#a': {'-ic'}, 'P#1#as': {'-ic'}, 'P#1#um': {'-ic'}, 'P#1#': {'-ic'}, 'P#1#us': {'-ic'}}, 'O!1!ish': {'o#1#': {'-ish'}}, 'e!1!ed': {'E#1#': {'-ed'}}, 'j!1!nish': {'J#1#': {'-ish'}}, '!1!zy': {'#1#': {'-y'}, '#1#ophrenic': {'-y'}}, '!1!ded': {'#1#': {'-ed'}}, 'a!1!o!2!osis': {'A#1#a#2#a': {'-osis'}}, '!1!sie': {'#1#ition': {'-ie'}, '#1#bane': {'-ie'}, '#1#tralia': {'-ie'}, '#1#ther': {'-ie'}, '#1#ent': {'-ie'}, '#1#tume': {'-ie'}, '#1#erve': {'-ie'}}, 't!1!ous': {'T#1#a': {'-ous'}, 'T#1#ae': {'-ous'}}, 'b!1!ie': {'B#1#evik': {'-ie'}}, '!1!tie': {'#1#': {'-ie'}}, 'l!1!oid': {'L#1#ia': {'-oid'}, 'L#1#us': {'-oid'}}, '!1!ned': {'#1#': {'-ed'}}, 'H!1!ist': {'h#1#y': {'-ist'}}, '!1!!2!d': {'#1#b#2#': {'-ed'}, '#1#us#2#': {'-ed'}, '#1#y#2#': {'-ed'}}, '!1!ming': {'#1#': {'-ing'}}, '!1!-!2!y': {'#1#_#2#': {'-y'}, '#1#_#2#e': {'-y'}}, '!1!iologist': {'#1#y': {'-ist'}}, '!1!ly_imbalanced': {'#1#': {'-ly'}}, 'c!1!ous': {'C#1#ae': {'-ous'}, 'C#1#a': {'-ous'}}, '!1!ian_warbler': {'#1#e': {'-ian'}}, 'Jeynes': {'John': {'-s'}}, 's!1!ally': {'S#1#': {'-ally'}}, 'c!1!oid': {'C#1#a': {'-oid'}, 'C#1#us': {'-oid'}, 'C#1#': {'-oid'}}, '!2!-!1!ed': {'#2#_#1#': {'-ed'}}, 'e!1!ic': {'E#1#a': {'-ic'}, 'E#1#': {'-ic'}}, 'anthrac!1!': {'-#1#': {'anthraco-'}}, 'lip!1!': {'-#1#': {'lip-'}}, '!1!tal': {'#1#': {'-al'}}, 'hapl!1!': {'-#1#': {'haplo-'}}, '!1!tous': {'#1#': {'-ous'}}, '!1!ei!2!y': {'#1#y#2#er': {'-y'}}, '!1!red': {'#1#': {'-ed'}}, '!1!bearing': {'#1#': {'bearing'}}, 's!1!al': {'S#1#us': {'-al'}}, '!1!ian_gland': {'#1#': {'-ian'}}, '!1!!2!ian': {'#1#h#2#': {'-ian'}}, '!1!sho': {'#1#tional_service': {'-o'}}, '!1!adic': {'#1#': {'-adic'}}, 'enter!1!': {'-#1#': {'entero-'}}, '!1!ging': {'#1#': {'-ing'}}, 'l!1!n': {'L#1#': {'-ian', '-an'}}, '!1!king': {'#1#': {'-ing'}}, '!1!lation': {'#1#': {'-ation'}}, 'a!1!l': {'A#1#': {'-al'}}, '!1!tability': {'#1#': {'-ability'}}, 'Piarist': {'pius': {'-ist'}}, 'metallo!1!': {'-#1#': {'metallo-'}}, 'L!1!vy': {'Ol#1#ia': {'-y'}}, 'homophyly': {'-y': {'homo-'}}, 'fibr!1!': {'-#1#': {'fibro-'}}, '!1!-ly': {'#1#': {'-ly'}}, 's!1!ian': {'S#1#': {'-ian'}}, 'b!1!e': {'B#1#a': {'-phyte'}}, 'G!1!ist': {'g#1#': {'-ist'}}, 'dips!1!': {'-#1#': {'dipso-'}}, '!1!cidal': {'#1#': {'-cidal'}, '#1#a': {'-cidal'}}, 'limn!1!': {'-#1#': {'limno-'}}, '!1!kable': {'#1#': {'-able'}}, 'spermat!1!': {'-#1#': {'spermato-'}}, '!1!nage': {'#1#': {'-age'}}, 'p!1!cidal': {'P#1#s': {'-cidal'}}, 'homoe!1!': {'-#1#': {'homoe-'}}, 't!1!n': {'T#1#': {'-an'}, 'T#1#e': {'-an'}}, 'Eyetie': {'Italian': {'-ie'}}, 'o!1!ous': {'O#1#ae': {'-ous'}, 'O#1#a': {'-ous'}}, '!1!!2!able': {'#1#_#2#': {'-able'}, '#1#-#2#': {'-able'}}, 'angi!1!': {'-#1#': {'angio-'}}, '!1!pability': {'#1#': {'-ability'}}, '!1!ting': {'#1#': {'-ing'}}, 'apter!1!': {'-#1#': {'a-'}}, '!1!po': {'#1#': {'-o'}, '#1#ical': {'-o'}}, 'oligo!1!': {'-#1#': {'oligo-'}}, '!1!iation': {'#1#e': {'-ation'}, '#1#y': {'-ation'}}, 'm!1!lic': {'M#1#ceae': {'-ic'}}, 'xeno!1!': {'-#1#': {'xeno-'}}, 'a!1!': {'-#1#': {'a-'}}, 'nucle!1!': {'-#1#': {'nucleo-'}}, '!1!le': {'#1#ilis': {'-able'}}, 'U!1!ist': {'u#1#': {'-ist'}}, '!1!eal': {'#1#is': {'-al'}, '#1#aeus': {'-al'}}, 'M!1!ist': {'m#1#': {'-ist'}}, 'malac!1!': {'-#1#': {'malaco-'}}, 'e!1!oid': {'E#1#a': {'-oid'}}, '!1!oidal': {'#1#': {'-oid'}, '#1#us': {'-oid'}, '#1#a': {'-oid'}}, 'hipp!1!': {'-#1#': {'hipp-', 'hippo-'}}, '!1!ility': {'#1#le': {'-ability'}}, '!1!ning': {'#1#': {'-ing'}, '#1#en': {'-ing'}}, 'A!1!al': {'a#1#e': {'-al'}}, 'h!1!n': {'H#1#': {'-an'}}, '!1!ntian': {'#1#s': {'-ian'}}, 'n!1!l': {'N#1#': {'-al'}}, 'athero!1!': {'#1#': {'athero-'}}, 'R!1!ette': {'r#1#': {'-ette'}}, '!1!ro': {'#1#elict': {'-o'}, '#1#alytic': {'-o'}}, '!1!rable': {'#1#': {'-able'}, '#1#er': {'-able'}}, 'p!1!oid': {'P#1#': {'-oid'}}, '!1!list': {'#1#': {'-ist'}}, 'endo!1!': {'-#1#': {'endo-'}}, '!1!icism': {'#1#e': {'-ic'}}, 'orthoclast!1!': {'-#1#': {'ortho-'}}, '!1!vish': {'#1#': {'-ish'}}, 'kerat!1!': {'-#1#': {'kerat-', 'kerato-'}}, '!1!-!2!d': {'#1#_#2#': {'-ed'}}, '!1!tish': {'#1#': {'-ish'}, '#1#e': {'-ish'}}, 'p!1!l': {'P#1#': {'-al'}}, 'rhod!1!': {'-#1#': {'rhodo-'}}, 'oro!1!': {'-#1#': {'oro-'}}, 'fungi!1!': {'-#1#': {'fungi-'}}, 'f!1!ic': {'F#1#y': {'-ic'}, 'F#1#ay': {'-ic'}}, '!1!-grazing': {'#1#': {'grazing'}}, 'm!1!oid': {'M#1#a': {'-oid'}, 'M#1#ium': {'-oid'}, 'M#1#us': {'-oid'}, 'M#1#e': {'-oid'}, 'M#1#': {'-oid'}}, 'd!1!ie': {'D#1#': {'-ie'}}, '!1!lings': {'#1#': {'-ling'}}, 'Nehruv!1!': {'-#1#': {'-v-'}}, '!1!bability': {'#1#': {'-ability'}}, 'P!1!ie': {'Hartlep#1#': {'-ie'}}, '!1!ion': {'#1#e': {'-ation'}}, 'fafiation': {'FAFIA': {'-ation'}}, 'ptero!1!': {'-#1#': {'ptero-'}}, 'ento!1!': {'-#1#': {'ento-'}}, '!1!!2!t': {'#1#es#2#': {'-ist'}}, 'dermat!1!': {'-#1#': {'dermato-'}}, 'l!1!ic_acid': {'L#1#a': {'-ic'}}, '!1!!2!ed': {'#1#_#2#': {'-ed'}, '#1#_#2#s': {'-ed'}}, '!1!bo': {'#1#': {'-o'}}, 'f!1!n': {'F#1#e': {'-an'}}, 'P!1!ist': {'p#1#': {'-ist'}}, 'gnath!1!': {'-#1#': {'gnatho-'}}, 'anthropo!1!': {'-#1#': {'anthropo-'}}, '!1!x': {'#1#ck': {'-s'}}, '!2!!1!ation': {'#2#b#1#': {'-ation'}}, '!1!!2!y': {'#1#_#2#': {'-y'}}, '!1!ade': {'#1#': {'-ade'}}, 'l!1!id': {'L#1#n': {'-oid'}}, 'antibrom!1!': {'-#1#': {'anti-'}}, 'h!1!oid': {'H#1#is': {'-oid'}, 'H#1#a': {'-oid'}}, 'muzzie': {'Muslim': {'-ie'}}, 'Transpond!1!': {'-#1#': {'trans-'}}, '!1!sexual': {'#1#': {'-sexual'}}, 'j!1!ation': {'i#1#um': {'-ation'}}, 'a!1!ian': {'A#1#': {'-ian'}, 'A#1#us': {'-ian'}, 'A#1#ea': {'-ian'}, 'A#1#a': {'-ian'}}, 'e!1!l': {'E#1#': {'-al'}}, 'C!1!ie': {'c#1#': {'-ie'}}, '!1!cious': {'#1#ty': {'-ous'}, '#1#x': {'-ous'}}, '!1!an_system': {'#1#us': {'-an'}}, '!1!toid': {'#1#brity': {'-oid'}, '#1#': {'-oid'}, '#1#s': {'-oid'}}, '!1!nie': {'#1#': {'-ie'}}, 's!1!n': {'S#1#': {'-ian', '-an'}}, '!1!steading': {'#1#': {'homesteading'}}, 'j!1!ous': {'J#1#ae': {'-ous'}}, 'b!1!osis': {'B#1#a': {'-osis'}}, 'arterio!1!': {'#1#': {'arterio-'}}, '!1!eian': {'#1#y': {'-an'}}, 'hystero!1!': {'-#1#': {'hystero-'}}, '!1!bable': {'#1#': {'-able'}}, '!1!matist': {'#1#': {'-ist'}}, '!1!bist': {'#1#': {'-ist'}}, 'g!1!ic': {'G#1#us': {'-ic'}, 'G#1#': {'-ic'}}, 'nepheli!1!ous': {'-#1#': {'-ous'}}, '!1!ins': {'#1#e': {'-ing'}, '#1#': {'-s'}}, 'M!1!tte': {'m#1#': {'-ette'}}, 'arthro!1!': {'-#1#': {'arthro-'}}, 'P!1!n': {'p#1#': {'-an'}}, '!1!med': {'#1#': {'-ed'}}, 'misocapn!1!': {'-#1#': {'miso-'}}, 'dendr!1!': {'-#1#': {'dendr-'}}, 'dec!1!': {'-#1#': {'deca-'}}, '!1!go': {'#1#': {'-o'}, '#1#ly': {'-o'}, '#1#nant': {'-o'}, '#1#etarian': {'-o'}}, '!1!cy': {'#1#topus': {'-y'}, '#1#': {'-y'}}, 'odont!1!': {'-#1#': {'odonto-'}}, 'geot!1!': {'-#1#': {'geo-'}}, 'h!1!l': {'H#1#': {'-al'}}, 'kerato!1!': {'-#1#': {'kerato-'}}, 'C!1!ian': {'c#1#y': {'-ian'}, 'c#1#e': {'-ian'}}, '!1!ies': {'#1#y': {'-ie', '-s'}, '#1#ey': {'-s'}, '#1#': {'-ie'}}, 'h!1!ic': {'H#1#a': {'-ic'}}, '!1!ration': {'#1#': {'-ation'}}, 'calci!1!': {'-#1#': {'calci-'}}, '!1!ps': {'#1#ip': {'-s'}, '#1#': {'-s'}}, '!1!mable': {'#1#': {'-able'}}, '!1!ean': {'#1#a': {'-an'}, '#1#': {'-an'}, '#1#i': {'-an'}}, '!1!mic': {'#1#': {'-ic'}}, 'fluor!1!': {'-#1#': {'fluor-', 'fluoro-'}}, 'chlor!1!': {'-#1#': {'chloro-', 'chlor-'}}, 'bili!1!': {'-#1#': {'bili-'}}, '!1!sh': {'#1#an': {'-ish'}, '#1#a': {'-ish'}}, 'pyg!1!': {'-#1#': {'pygo-'}}, '!1!sable': {'#1#': {'-able'}}, '!1!ggs': {'#1#ck': {'-s'}}, '!1!icidal': {'#1#': {'-cidal'}, '#1#y': {'-cidal'}, '#1#e': {'-cidal'}}, '!1!otic': {'#1#': {'-otic'}}, 'hepat!1!': {'-#1#': {'hepato-'}}, 'carpo!1!': {'-#1#': {'carpo-'}}, 'm!1!ish': {'M#1#': {'-ish'}}, 'q!1!ic': {'Q#1#e': {'-ic'}}, 'n!1!n': {'N#1#': {'-an'}}, 'L!1!able': {'l#1#': {'-able'}}, 'm!1!ling': {'M#1#': {'-ling'}}, '!1!eous': {'#1#y': {'-ous'}}, 'miso!1!': {'-#1#': {'miso-'}}, '!1!fied': {'#1#sfy': {'-ed'}}, '!1!iosis': {'#1#': {'-osis'}}, '!1!-seeking': {'#1#': {'seeking'}}, 'cyt!1!': {'-#1#': {'cyto-'}}, 'hypn!1!': {'-#1#': {'hypno-'}}, 'pentadelph!1!': {'-#1#': {'penta-'}}, '!1!mo': {'#1#': {'-o'}}, 'n!1!ic': {'N#1#e': {'-ic'}}, 's!1!toid': {'S#1#': {'-oid'}}, 'mon!1!': {'-#1#': {'mono-'}}, '!1!-!2!by': {'#1#_#2#': {'-y'}}, 'm!1!al': {'M#1#e': {'-al'}}, '!1!te': {'#1#': {'-ette'}}, 'i!1!ic': {'I#1#es': {'-ic'}}, '!1!do': {'#1#': {'-o'}}, '!1!mish': {'#1#': {'-ish'}}, '!1!ah!2!ic': {'#1##2#ate': {'-aholic'}}, 'ecto!1!': {'-#1#': {'ecto-'}}, '!1!is': {'#1#': {'-osis'}}, '!1!zzy': {'#1#sition': {'-y'}, '#1#st': {'-y'}}, 'ith': {'i': {'-th'}}, '!1!ggins': {'#1#ck': {'-s'}}, 'c!1!': {'co#1#le': {'cupa'}}, 'tauri!1!ous': {'#1#u': {'-ous'}}, '!1!ian_telescope': {'#1#': {'-ian'}}, '!1!enian': {'#1#ine': {'-ian'}}, 'g!1!ian': {'G#1#': {'-ian'}}, '!1!-auntish': {'#1#': {'-ish'}}, '!1!titude': {'#1#': {'-itude'}}, 'a!1!st': {'a_#1#': {'-ist'}}, '!1!dability': {'#1#': {'-ability'}}, '!1!ication': {'#1#y': {'-ation'}, '#1#e': {'-ic'}}, 'a!1!ic': {'A#1#a': {'-ic'}}, 'poly!1!': {'-#1#': {'poly-'}}, '!1!lie': {'#1#': {'-ly', '-ie'}, '#1#marnock': {'-ie'}, '#1#itician': {'-ie'}, '#1#and': {'-ie'}}, '!1!-o': {'#1#': {'-o'}}, 'nemato!1!': {'-#1#': {'nemato-'}}, 'p!1!ian': {'P#1#': {'-ian'}, 'P#1#ea': {'-ian'}}, '!1!_!2!-like': {'#1#-#2#': {'-like'}}, '!1!mie': {'#1#': {'-ie'}, '#1#inist': {'-ie'}, '#1#_sim': {'-ie'}, '#1#itation': {'-ie'}}, 'P!1!ian': {'p#1#us': {'-ian'}}, 'o!1!n': {'O#1#': {'-an'}}, '!1!cal': {'#1#s': {'-ical'}}, 'd!1!n': {'D#1#': {'-an'}}, 'arvo': {'afternoon': {'-o'}}, '!1!ism': {'#1#': {'-ian'}}, '!1!mist': {'#1#': {'-ist'}}, 'loo!1!': {'l#1#utenant': {'-ie'}}, 'g!1!n': {'G#1#': {'-ian', '-an'}}, '!1!nal': {'#1#': {'obsidere', '-al'}}, 'p!1!c': {'P#1#um': {'-ic'}}, 'm!1!ic': {'M#1#a': {'-ic'}, 'M#1#': {'-ic'}}, 'ptilopaed!1!': {'-#1#': {'ptilo-'}}, 'e!1!ade': {'E#1#': {'-ade'}}, 'tropho!1!': {'-#1#': {'tropho-'}}, 'tying': {'tie': {'-ing'}}, 'p!1!an': {'P#1#': {'-an'}, 'P#1#s': {'-an'}}, 'p!1!eous': {'P#1#aceae': {'-ous'}}, 'e!1!agic': {'ga#1#e': {'-ic'}}, 'oste!1!': {'-#1#': {'osteo-'}}, '!1!y-housey': {'#1#': {'-y'}}, 'g!1!ous': {'G#1#ae': {'-ous'}}, 'pteryg!1!': {'-#1#': {'pterygo-'}}, '!1!dist': {'#1#': {'-ist'}}, '!1!e!2!d': {'#1##2#': {'-ed'}}, 'un!1!': {'#1#': {'un-'}}, '!1!sis': {'#1#tic': {'-osis'}, '#1#': {'-osis'}}, 'mast!1!': {'-#1#': {'-oid'}}, '!1!onian': {'#1#ah': {'-ian'}}, '!1!agn!2!able': {'#1#sp#2#e': {'-able'}}, 'cyan!1!': {'-#1#': {'cyano-'}}, 'q!1!oid': {'Q#1#us': {'-oid'}}, 'hydr!1!': {'-#1#': {'hydro-'}}, 'S!1!y': {'s#1#r': {'-y'}, 's#1#': {'-y'}}, 'entomo!1!': {'-#1#': {'entomo-'}}, 'astr!1!': {'-#1#': {'astro-'}}, 'ichthy!1!': {'-#1#': {'ichthyo-'}}, 'chondr!1!': {'-#1#': {'chondro-'}}, '!1!vo': {'#1#erty': {'-o'}}, 'irid!1!': {'-#1#': {'irid-'}}, 's!1!ist': {'S#1#': {'-ist'}}, 'dys!1!': {'#1#': {'dys-'}}, '!1!ric': {'#1#er': {'-ic'}}, '!1!nist': {'#1#': {'-ist'}}, 'E!1!ian': {'e#1#': {'-ian'}}, '!2!-!1!y': {'#2#_#1#': {'-y'}}, 'myrmec!1!': {'-#1#': {'myrmeco-'}}, '!1!d!2!ist': {'#1#_D#2#': {'-ist'}}, '!1!w!2!s': {'#1##2#': {'-s'}}, 'anth!1!': {'-#1#': {'antho-'}}, '!1!fy': {'#1#': {'-y'}}, '!1!': {'#1#rghini': {'-o'}, '#1#m': {'-o'}, '#1#a': {'-an', '-ic'}, '#1#': {'-ed', '-al', 'nervosus'}, '#1#e': {'oculus'}, '#1#rite': {'-o'}}, '!1!lette': {'#1#': {'-ette'}}, '!1!uous': {'#1#': {'-ous'}}, 'c!1!l': {'C#1#': {'-al'}}, 'potam!1!': {'-#1#': {'potam-'}}, 'xeri!1!': {'-#1#': {'xeri-'}}, '!1!gies': {'#1#atoni': {'-ie'}}, '!1!phyte': {'#1#s': {'-phyte'}, '#1#': {'-phyte'}}, 'epi!1!': {'-#1#': {'epi-'}}, '!2!!1!ing': {'#2#_#1#': {'-ing'}}, 'p!1!al': {'P#1#': {'-al'}, 'P#1#us': {'-al'}}, '!1!-!2!ing': {'#1#_#2#': {'-ing'}}, 'hemat!1!': {'-#1#': {'hemato-'}}, 'aqu!1!': {'-#1#': {'aqua-'}}, '!1!ude': {'#1#e': {'-itude'}}, 'uran!1!': {'-#1#': {'uran-'}}, 'encephal!1!': {'-#1#': {'encephalo-'}}, 'ket!1!': {'-#1#': {'keto-'}}, 'meso!1!': {'-#1#': {'meso-'}}, 'hol!1!': {'-#1#': {'holo-'}}, '!1!zzo': {'#1#sbian': {'-o'}}, 'A!1!ies': {'a#1#y': {'-s'}}, '!2!!1!ous': {'#2#_#1#ur': {'-ous'}}, 'acanth!1!': {'-#1#': {'acanth-'}}, '!1!t!2!ic': {'#1##2#': {'-ic'}}, '!1!dal': {'#1#s': {'-al'}, '#1#': {'-al'}}, 'Kachruv!1!': {'-#1#': {'-v-'}}, 'B!1!os': {'b#1#aneer': {'-o'}}, '!1!ry': {'#1#er': {'-y'}, '#1#': {'-y'}}, 'cudgel': {'cog': {'-el'}}, 'achrom!1!': {'-#1#': {'a-'}}, 'fobby': {'FOB': {'-y'}}, 'autac!1!': {'-#1#': {'aut-'}}, '!1!r!2!an': {'#1##2#pa': {'-an'}}, '!1!lage': {'#1#': {'-age'}}, '!1!ed_up': {'#1#': {'-ed'}}, 'p!1!id': {'P#1#': {'-oid'}}, 'r!1!n': {'R#1#': {'-an'}}, 'A!1!ian': {'a#1#y': {'-an'}}, 'w!1!sy': {'#1#ze': {'-y'}}, 'a!1!osis': {'A#1#us': {'-osis'}, 'A#1#es': {'-osis'}, 'A#1#a': {'-osis'}}, 'robo!1!': {'-#1#': {'robo-'}}, '!1!!2!gy': {'#1#_#2#': {'-y'}}, 'erythr!1!': {'-#1#': {'erythro-'}}, 'm!1!ropinocytic': {'-#1#': {'micro-'}}, 'ab!1!ie': {'#1#al': {'-ie'}}, '!1!iac': {'#1#y': {'-ac'}}, 'di!1!': {'-#1#': {'di-'}}, 'he!1!th': {'h#1#': {'-th'}}, 'u!1!st': {'U#1#a': {'-ist'}}, '!1!gability': {'#1#': {'-ability'}}, 'cupro!1!': {'-#1#': {'cupro-'}}, 'zymo!1!': {'-#1#': {'zymo-'}}, 'heter!1!': {'-#1#': {'hetero-'}}, 'omn!1!': {'-#1#': {'omni-'}}, 'b!1!ic': {'B#1#s': {'-ic'}}, '!1!!2!ist': {'en_#1#_#2#': {'-ist'}, '#1#-#2#e': {'-ist'}}, 'hyster!1!': {'-#1#': {'hystero-'}}, 'primi!1!ial': {'#1#erare': {'-al'}}, 'b!1!ian': {'B#1#': {'-ian'}}, 'l!1!al': {'L#1#us': {'-al'}}, 'c!1!icosis': {'C#1#ex': {'-osis'}}, '!1!no': {'#1#': {'-o'}}, '!1!les': {'#1#ell': {'-s'}}, 'S!1!ist': {'s#1#': {'-ist'}}, 'phyll!1!': {'-#1#': {'phyllo-'}}, '!2!y-!1!y': {'#2#_and_#1#': {'-y'}}, '!1!zo': {'#1#': {'-o'}}, '!1!zie': {'#1#': {'-ie'}}, 'spheno!1!': {'-#1#': {'spheno-'}}, 'H!1!bins': {'R#1#ert': {'-s'}}, 'acr!1!': {'-#1#': {'acro-'}}, '!1!!2!ged': {'#1#_#2#': {'-ed'}}, 'embryo!1!': {'-#1#': {'embryo-'}}, '!1!-!2!ist': {'#1#_#2#': {'-ist'}, '#1#_#2#e': {'-ist'}, '#1#_#2#s': {'-ist'}}, '!2!-!3!-!1!ish': {'#2#_#3#_#1#': {'-ish'}}, 'B!1!y': {'b#1#': {'-y'}}, '!1!tage': {'#1#': {'-age'}}, 'ferro!1!': {'-#1#': {'ferro-'}}, 'gyr!1!': {'-#1#': {'gyro-'}}, 'f!1!c': {'F#1#um': {'-ic'}}, '!1!mage': {'#1#': {'-age'}}, 'aur!1!': {'-#1#': {'auro-'}}, 'S!1!nie': {'Wis#1#sin': {'-ie'}}, 'R!1!ation': {'r#1#e': {'-ation'}}, '!1!e!2!ed': {'#1#a#2#': {'-ed'}}, 'cholecyst!1!': {'-#1#': {'cholecysto-'}}, 'i!1!able': {'I#1#': {'-able'}}, '!1!mbo': {'#1#ndwich': {'-o'}}, '!1!-!2!ped': {'#1#_#2#': {'-ed'}}, '!1!ator': {'#1#e': {'-ator'}, '#1#': {'-ator'}}, '!2!s!1!ian': {'#2#_S#1#e': {'-ian'}}, 'aero!1!': {'-#1#': {'aero-'}}, '!2!!1!ist': {'#2#i#1#': {'-ist'}}, '!1!gity': {'#1#': {'-y'}}, 'omphal!1!': {'-#1#': {'omphalo-'}}, 'D!1!ian': {'d#1#': {'-ian'}, 'd#1#e': {'-ian'}}, 'pe!1!e': {'p#1#s': {'-ie'}}, 'diplo!1!': {'-#1#': {'diplo-'}}, 'acro!1!': {'-#1#': {'acro-'}}, 'l!1!osis': {'L#1#a': {'-osis'}, 'L#1#us': {'-osis'}}, 'my!1!': {'-#1#': {'myo-'}}, 'oct!1!': {'-#1#': {'oct-'}}, '!1!ked': {'#1#': {'-ed'}}, 'alexithym!1!': {'-#1#': {'a-'}}, '!1!pist': {'#1#': {'-ist'}}, 'scler!1!': {'-#1#': {'sclero-'}}, '!2!!1!ship': {'#2#_#1#': {'-ship'}}, 'melan!1!': {'-#1#': {'melano-'}}, 'antalg!1!': {'-#1#': {'anti-'}}, 'he!1!ie': {'h#1#d': {'-ie'}}, '!1!rian': {'#1#er': {'-ian'}, '#1#': {'-ian'}, '#1#s': {'-ian'}}, '!1!eight': {'#1#ay': {'-th'}}, '!1!ctic': {'#1#x': {'-ic'}}, 'voicen!1!': {'-#1#': {'-ing'}}, 'g!1!ish': {'G#1#': {'-ish'}}, 'd!1!hromatic': {'-#1#': {'di-'}}, 'isonom!1!': {'-#1#': {'iso-'}}, 'f!1!hoid': {'F#1#': {'-oid'}}, 'apan': {'APA': {'-n'}}, 'twoccing': {'TWOC': {'-ing'}}, '!1!osis_nigricans': {'#1#us': {'-osis'}}, '!2!!1!edness': {'#2#_#1#': {'-ed'}}, '!1!el': {'#1#': {'-el'}}, 'polyadelph!1!': {'-#1#': {'poly-'}}, 'q!1!l': {'Q#1#': {'-al'}}, 'b!1!cidal': {'B#1#': {'-cidal'}}, 'otoconi!1!': {'-#1#': {'-al'}}, 'selen!1!': {'-#1#': {'seleno-'}}, 'a!1!ie': {'A#1#erger': {'-ie'}}, 'N!1!ic': {'n#1#he': {'-ic'}, 'n#1#': {'-ic'}}, 'o!1!c': {'O#1#a': {'-ic'}}, '!1!mosis': {'#1#': {'-osis'}}, '!1!cable': {'#1#ke': {'-able'}, '#1#quer': {'-able'}}, 'T!1!ian': {'t#1#y': {'-an'}}, 'Uckew!1!t': {'W#1#': {'-ist'}}, '!1!zzie': {'#1#sbian': {'-ie'}}, '!1!die': {'#1#': {'-ie'}, '#1#rella': {'-ie'}, '#1#ge': {'-ie'}}, 'digi!1!': {'-#1#': {'digi-'}}, '!1!gage': {'#1#': {'-age'}}, 'a!1!an': {'A#1#i': {'-ian', '-an'}, 'A#1#s': {'-an'}}, 'D!1!ist': {'d#1#': {'-ist'}}, 'j!1!ic': {'J#1#a': {'-ic'}}, '!2!a!1!al': {'#2##1#': {'-al'}}, 'sapro!1!': {'-#1#': {'sapro-'}}, '!1!rish': {'#1#': {'-ish'}}, 'cycl!1!': {'-#1#': {'cyclo-'}}, '!1!so': {'#1#tenance': {'-o'}}, 't!1!ed': {'T#1#': {'-ed'}}, '!1!!2!ish': {'#1#-#2#': {'-ish'}, '#1#_#2#': {'-ish'}}, '!1!zoid': {'#1#s': {'-oid'}}, '!1!zable': {'#1#': {'-able'}}, '!1!a!2!s': {'#1##2#': {'-s'}, '#1#e#2#': {'-s'}}, '!1!-!2!-able': {'#1#_#2#': {'-able'}}, '!1!page': {'#1#': {'-age'}}, 'Tardis-like': {'TARDIS': {'-like'}}, 'l!1!doid': {'L#1#s': {'-oid'}}, 'anhydr!1!': {'-#1#': {'an-'}}, 'f!1!hic': {'F#1#': {'-ic'}}, '!1!sic': {'#1#': {'-ic'}, '#1#us': {'-ic'}}, 'gafiation': {'GAFIA': {'-ation'}}, 'i!1!y': {'I#1#': {'-y'}}, '!1!cional': {'#1#x': {'-al'}}, '!1!kian': {'#1#': {'-ian'}}, '!1!ings': {'#1#e': {'-ing'}, '#1#': {'-ing', '-s'}}, 'copro!1!': {'-#1#': {'copro-'}}, 'a!1!lous': {'#1#': {'-ous'}}, '!1!ously': {'#1#e': {'-ous'}}, 'L!1!an': {'l#1#s': {'-ian'}}, '!1!ian_body': {'#1#': {'-ian'}}, 'chrom!1!': {'-#1#': {'chromo-'}}, 'dermo!1!': {'-#1#': {'dermo-'}}, 'd!1!ean': {'D#1#ae': {'-an'}}, '!1!!2!ous': {'#1#o#2#e': {'-ous'}}, 'anto!1!': {'-#1#': {'anto-'}}, 'G!1!ic': {'g#1#a': {'-ic'}}, 'rhiz!1!': {'-#1#': {'rhizo-'}}, '!1!!2!ied': {'#1#y#2#y': {'-ed'}}, '!1!tian': {'#1#ce': {'-ian'}}, 'exo!1!': {'-#1#': {'exo-'}}, 'leaky': {'-y': {'-y'}}, 'd!1!oid': {'D#1#es': {'-oid'}}, '!1!vable': {'#1#': {'-able'}}, 'hygr!1!': {'-#1#': {'hygro-'}}, 'durgy': {'dwarf': {'-y'}}, '!1!ggles': {'#1#ck': {'-s'}}, '!1!!2!te': {'#1#mark#2#': {'-ette'}}, 'dy!1!': {'-#1#': {'di-'}}, 'acro!1!al': {'#1#o': {'-al'}}, '!1!kie': {'#1#coholic': {'-ie'}, '#1#_Kong': {'-ie'}}, '!1!coming': {'#1#': {'coming'}}, 'Z!1!ette': {'z#1#': {'-ette'}}, 'ef!1!d': {'ex#1#': {'-ed'}}, 'antiscol!1!': {'-#1#': {'anti-'}}, 'orthodrom!1!': {'-#1#': {'ortho-'}}, 'g!1!oid': {'G#1#': {'-oid'}}, 'dirhin!1!': {'-#1#': {'di-'}}, '!1!zed': {'#1#': {'-ed'}}, 'c!1!ic': {'C#1#': {'-ic'}}, 'cardi!1!': {'-#1#': {'cardio-'}}, '!1!jorat!2!n': {'#1##2#r': {'-ation'}}, 'zygo!1!': {'-#1#': {'zygo-'}}, 'sporo!1!': {'-#1#': {'sporo-'}}, 'o!1!an': {'O#1#es': {'-an'}, 'O#1#': {'-an'}}, '!1!tude': {'#1#e': {'-itude'}}, '!1!icoid': {'#1#ex': {'-oid'}}, 'antho!1!': {'-#1#': {'antho-'}}, 'KBs': {'kine_bud': {'-s'}}, 'c!1!cidal': {'C#1#': {'-cidal'}}, '!1!rator': {'#1#er': {'-ator'}}, 'iod!1!': {'-#1#': {'iodo-'}}, '!2!i!1!y': {'#2#e#1#e': {'-y'}}, 'nulli!1!ian': {'#1#es': {'-ian'}}, '!1!can': {'#1#que': {'-an'}}, 'retin!1!': {'-#1#': {'-oid'}}, 'B!1!': {'b#1#e': {'-ist'}, 'b#1#a': {'Baptist'}}, 'bathy!1!': {'-#1#': {'bathy-'}}, 'leuc!1!': {'-#1#': {'leuco-'}}, 'S!1!gy': {'s#1#osaurus': {'-y'}}, '!2!!1!ly': {'#2#_#1#': {'-ly'}}, 'c!1!an': {'C#1#s': {'-an'}}, 'a!1!oid': {'A#1#ae': {'-oid'}, 'A#1#us': {'-oid'}, 'A#1#a': {'-oid'}}, 'osteo!1!': {'-#1#': {'osteo-'}}, 'Pigouv!1!': {'-#1#': {'-v-'}}, 'natting': {'NAT': {'-ing'}}, 'teleo!1!': {'-#1#': {'teleo-'}}, 'xantho!1!': {'-#1#': {'xantho-'}}, 'b!1!ist': {'B#1#e': {'-ist'}}, '!1!ulist': {'#1#le': {'-ist'}}, 'anemo!1!': {'-#1#': {'anemo-'}}, 'halo!1!': {'-#1#': {'halo-'}}, '!1!b!2!s': {'#1##2#': {'-s'}}, '!1!_foodist': {'#1#': {'-ist'}}, 'stann!1!': {'-#1#': {'stanno-'}}, 'f!1!ous': {'F#1#ae': {'-ous'}}, 'ophthalm!1!': {'-#1#': {'ophthalmo-'}}, 'heterotopy': {'-y': {'hetero-'}}, 'anthropon!1!': {'-#1#': {'anthropo-'}}, '!1!iette': {'#1#y': {'-ette'}}, '!1!vie': {'#1#ilian': {'-ie'}}, '!1!!2!ability': {'#1#_#2#': {'-ability'}}, 'R!1!ic': {'r#1#e': {'-ic'}}, 'bi!1!': {'-#1#': {'bi-'}}, 'hygro!1!': {'-#1#': {'hygro-'}}, 'g!1!zo': {'Gu#1#ea': {'-o'}}, '!1!iness': {'#1#e': {'-y'}}, 'M!1!ian': {'m#1#': {'-ian'}}, 'A!1!ly': {'a#1#': {'-ly'}}, '!1!blowing': {'#1#': {'blowing'}}, '!1!-ship': {'#1#': {'-ship'}}, 'C!1!nian': {'c#1#': {'-ian'}}, '!1!-!2!ly': {'#1#_#2#': {'-ly'}}, '!1!vely': {'#1#fe': {'-ly'}, '#1#of': {'-ly'}}, 'b!1!oid': {'B#1#s': {'-oid'}}, 'm!1!ian': {'M#1#a': {'-ian'}, 'M#1#us': {'-ian'}}, '!1!osexual': {'#1#ens': {'-sexual'}}, '!1!ovian': {'#1#ue': {'-ian'}}, 'S!1!ies': {'s#1#y': {'-s'}}, 'afterwards': {'-s': {'-s'}}, '!1!os': {'#1#ation_Army': {'-o'}}, '!1!edness': {'#1#': {'-ed'}}, 'limno!1!': {'-#1#': {'limno-'}}, '!1!sian': {'#1#': {'-ian'}}, '!2!-!1!ling': {'#2#_#1#': {'-ing'}}, '!1!achingly': {'#1#': {'-ly'}}, 'p!1!aic': {'P#1#ee': {'-ic'}}, '!1!ring': {'#1#': {'-ing'}}, 'early': {'ere': {'-ly'}}, '!1!-!2!like': {'#1#_#2#': {'-like'}}, '!1!t!2!erous': {'#1##2#': {'-ous'}}, '!2!!1!ping': {'#2#_#1#': {'-ing'}}, 'onomat!1!': {'-#1#': {'onomato-'}}, 'l!1!ic': {'L#1#a': {'-ic'}}, 'cupr!1!': {'-#1#': {'cupr-'}}, '!1!ulous': {'#1#le': {'-ous'}}, '!1!rability': {'#1#': {'-ability'}}, 'd!1!l': {'D#1#': {'-al'}}, '!1!y_challenged': {'#1#e': {'-ly'}}, 'Pol!1!s': {'Pau#1#': {'-s'}}, 'oneir!1!': {'-#1#': {'oneir-', 'oneiro-'}}, 'oo!1!': {'-#1#': {'oo-'}}, 'q!1!ist': {'Q#1#y': {'-ist'}}, '!1!ce': {'#1#n': {'-s'}}, '!1!dic': {'#1#s': {'-ic'}, '#1#ble': {'-adic'}}, 'meta!1!': {'-#1#': {'meta-'}}, '!1!tan': {'#1#s': {'-an'}}, '!1!rical': {'#1#er': {'-ical'}, '#1#ar': {'-ical'}}, '!1!dly': {'#1#': {'-ly'}}, 'u!1!ian': {'U#1#a': {'-ian'}}, 'U!1!ian': {'u#1#': {'-ian'}}, 'c!1!c_acid': {'C#1#um': {'-ic'}}, 'jth': {'j': {'-th'}}, 's!1!an': {'S#1#i': {'-ian'}}, '!1!y_pants': {'#1#': {'-y'}}, '!1!bens': {'#1#in': {'-s'}}, 'dendro!1!': {'-#1#': {'dendro-'}}, 'sphygm!1!': {'-#1#': {'sphygmo-'}}, 'chem!1!': {'-#1#': {'chemo-'}}, 'm!1!an': {'M#1#s': {'-an'}, 'M#1#i': {'-an'}}, '!1!cic': {'#1#x': {'-ic'}}, 'rhin!1!': {'-#1#': {'rhino-', 'rhin-'}}, 'zoo!1!': {'-#1#': {'zoo-'}}, '!1!fth': {'#1#ve': {'-th'}}, 't!1!!2!l': {'T#1#a#2#': {'-al'}}, 'glyco!1!': {'-#1#': {'glyco-'}}, 'cyano!1!': {'-#1#': {'cyano-'}}, 'm!1!ed': {'M#1#': {'-ed'}}, '!1!y-!2!y': {'#1#_#2#': {'-y'}}, '!1!-!3!-!2!ian': {'#1#_#3#_#2#': {'-ian'}}, 'h!1!ic_acid': {'H#1#a': {'-ic'}}, 'kth': {'k': {'-th'}}, 'acanthoclad!1!': {'-#1#': {'acantho-'}}, '!1!!2!ic': {'#1#_#2#': {'-ic'}}, 'pneumo!1!': {'-#1#': {'pneumo-'}}, 'nephr!1!': {'-#1#': {'nephro-'}}, '!1!pheno!2!ing': {'#1##2#e': {'-ing'}}, 'rheo!1!': {'-#1#': {'rheo-'}}, 'heli!1!': {'-#1#': {'helio-'}}, 'cten!1!': {'-#1#': {'cteno-'}}, 'helio!1!': {'-#1#': {'helio-'}}, 'sarc!1!': {'-#1#': {'sarco-'}}, 'C!1!ist': {'c#1#': {'-ist'}}, 'anti!1!ist': {'#1#': {'-ist'}}, '!1!tial': {'#1#ce': {'-al'}}, '!1!pots': {'#1#ip': {'-s'}}, 'p!1!ish': {'P#1#': {'-ish'}}, 'a!1!ally': {'A#1#': {'-ally'}}, 't!1!ic': {'T#1#a': {'-ic'}}, 'g!1!dist': {'G#1#': {'-ist'}}, 'r!1!o!2!': {'R#1##2#': {'-ous'}}, 'atl!1!': {'-#1#': {'atlo-'}}, 'myel!1!': {'-#1#': {'myelo-'}}, 'cerato!1!': {'-#1#': {'cerato-'}}, 'i!1!n': {'I#1#': {'-an'}, 'I#1#e': {'-an'}}, 'M!1!ie': {'m#1#e': {'-ie'}}, 'carcin!1!': {'-#1#': {'carcino-'}}, '!1!lian': {'#1#': {'-ian'}}, 'chron!1!': {'-#1#': {'chrono-'}}, 'proto!1!': {'-#1#': {'proto-'}}, 'n-adic': {'n': {'-adic'}}, 'hetero!1!': {'-#1#': {'hetero-'}}, '!2!-!1!al': {'#2#_#1#': {'-al'}, '#2#_#1#um': {'-al'}}, '!1!iship': {'#1#y': {'-ship'}}, 'hapto!1!': {'-#1#': {'hapto-'}}, 'giddy': {'god': {'-y'}}, '!1!iteal': {'#1#es': {'-al'}}, 'L!1!ist': {'l#1#e': {'-ist'}}, 'hal!1!': {'-#1#': {'halo-'}}, 'tetrasem!1!': {'-#1#': {'tetra-'}}, '!1!wering': {'#1#ur': {'-ing'}}, 'schizo!1!': {'-#1#': {'schizo-'}}, '!1!ibility': {'#1#able': {'-ability'}}, 'pyro!1!': {'-#1#': {'pyro-'}}, '!1!ingly': {'#1#ere': {'-ing'}}, '!1!fo': {'#1#ugee': {'-o'}}, 'kinet!1!': {'-#1#': {'kineto-'}}, 'E!1!ie': {'e#1#': {'-ie'}}, '!1!etic': {'#1#ite': {'-ic'}}, 'r!1!l': {'R#1#': {'-al'}}, '!1!gnable': {'#1#ndre': {'-able'}}, '!1!rth': {'#1#ar': {'-th'}}, 'not!1!': {'-#1#': {'noto-'}}, 'rhodo!1!': {'-#1#': {'rhodo-'}}, 'py!1!': {'-#1#': {'pyo-'}}, 'm!1!l': {'M#1#': {'-al'}}, 'xero!1!': {'-#1#': {'xero-'}}, 'e!1!an': {'E#1#s': {'-an'}}, 'o!1!ic': {'O#1#': {'-ic'}}, '!1!u!2!s': {'#1##2#': {'-s'}}, '!1!ens': {'#1#': {'-s'}}, 'myrmeco!1!': {'-#1#': {'myrmeco-'}}, 'paleo!1!': {'-#1#': {'paleo-'}}, 'oxylo!1!': {'-#1#': {'oxy-'}}, '!1!ved': {'#1#f': {'-ed'}}, '!1!linger': {'#1#': {'-ling'}}, 'chromo!1!': {'-#1#': {'chromo-'}}, 'diadelph!1!': {'-#1#': {'di-'}}, 'd!1!icosis': {'D#1#ex': {'-osis'}}, 'adip!1!': {'-#1#': {'adipo-'}}, 'derm!1!': {'-#1#': {'derm-'}}, 'T!1!y': {'Gert#1#e': {'-y'}}, '!1!nation': {'#1#': {'-ation'}}, 'e!1!c': {'E#1#a': {'-ic'}}, '!1!et!2!': {'#1#a#2#': {'-ette'}}, '!1!rist': {'#1#er': {'-ist'}}, 's!1!ical': {'S#1#': {'-ical'}}, 'anthr!1!': {'-#1#': {'anthro-'}}, '!1!es': {'#1#': {'-s'}}, '!1!e!2!y': {'#1#a#2#e': {'-y'}}, 'zyo!1!': {'-#1#': {'zygo-'}}, 'sacchar!1!': {'-#1#': {'saccharo-'}}, 'capn!1!': {'-#1#': {'capno-'}}, 'bio!1!': {'-#1#': {'bio-'}}, 'octo!1!': {'-#1#': {'octo-'}}, '!1!!2!e': {'#1#i#2#a': {'-ie'}}, '!1!mpy': {'#1#ndpa': {'-y'}}, 'parodical': {'satire': {'-ical'}}, 'crypto!1!': {'-#1#': {'crypto-'}}, 'Noach!1!': {'-#1#': {'-ian'}}, 'R!1!ian': {'r#1#y': {'-an'}}, 'l!1!e': {'L#1#a': {'-phyte'}}, 'phyt!1!': {'-#1#': {'phyto-'}}, '!1!-making': {'make_a_#1#': {'-ing'}}, '!1!zical': {'#1#': {'-ical'}}, 'agalact!1!': {'-#1#': {'a-'}}, 'pyrg!1!al': {'-#1#': {'-al'}}, '!1!-!2!able': {'#1#_#2#': {'-able'}}, 'cephal!1!': {'-#1#': {'cephalo-'}}, 's!1!c': {'S#1#a': {'-ic'}}, 'ent!1!': {'-#1#': {'ent-'}}, 'arthr!1!': {'-#1#': {'arthr-'}}, 'neur!1!': {'-#1#': {'neuro-'}}, 'chyl!1!': {'-#1#': {'chylo-'}}, '!1!cial': {'#1#x': {'-al'}}, 'g!1!l': {'G#1#': {'-al'}}, 't!1!ic_acid': {'T#1#a': {'-ic'}}, '!1!hthyic': {'-#1#': {'ichthy-'}}, 'Ripua!1!an': {'#1#pa': {'-an'}}, 'transpond!1!': {'-#1#': {'trans-'}}, '!1!oplasty': {'#1#a': {'-o'}}, '!1!!2!al': {'#1#cula#2#ere': {'-al'}}, '!1!m!2!ing': {'#1#w#2#': {'-ing'}}, 'sphen!1!': {'-#1#': {'spheno-'}}, '!1!-scratching': {'#1#': {'scratching'}}, '!1!-!2!py': {'#1#_#2#': {'-y'}}, '!2!!1!d': {'#2#_#1#': {'-ed'}}, 'tropo!1!': {'-#1#': {'tropo-'}}, 'photo!1!': {'-#1#': {'photo-'}}, '!1!olitan': {'#1#le': {'-an'}}, 'im!1!ed': {'in#1#': {'-ed'}}, 'i!1!ous': {'I#1#ae': {'-ous'}}, '!1!ional': {'#1#ere': {'-al'}}, '!1!itic': {'#1#e': {'-ic'}}, 'acheil!1!': {'-#1#': {'a-'}}, 'mono!1!': {'-#1#': {'mono-'}}, 'ferr!1!': {'-#1#': {'ferr-'}}, 'telotroch!1!': {'-#1#': {'telo-'}}, 't!1!ian': {'T#1#a': {'-ian'}, 'T#1#': {'-ian'}}, 'nitro!1!': {'-#1#': {'nitro-'}}, '!1!-ian': {'#1#': {'-ian'}}, 'entom!1!': {'-#1#': {'entomo-'}}, 'chrono!1!': {'-#1#': {'chrono-'}}, '!2!-!1!d': {'#2#_#1#': {'-ed'}}, 'd!1!osis': {'D#1#us': {'-osis'}, 'D#1#': {'-osis'}}, 'paraglenal': {'-oid': {'para-'}}, '!1!!2!ly': {'#1#a#2#': {'-ly'}, '#1#i#2#': {'-ly'}}, 'diacranter!1!': {'-#1#': {'dia-'}}, '!1!boid': {'#1#p': {'-oid'}}, 'argyr!1!': {'-#1#': {'argyr-'}}, 'thalassio!1!': {'-#1#': {'thalasso-'}}, 'S!1!-Simonianism': {'s#1#': {'-ian'}}, 'un!1!d': {'#1#': {'-ed'}}, 'paraphylet!1!': {'-#1#': {'para-'}}, '!1!irous': {'#1#re': {'-ous'}}, '!1!hip': {'#1#': {'-ship'}}, '!1!-dom': {'#1#': {'-dom'}}, 'B!1!ist': {'b#1#': {'-ist'}}, '!1!lt': {'#1#el': {'-ed'}}, 'D!1!ianism': {'d#1#': {'-ian'}}, 'Mossie': {'Maurice': {'-ie'}}, 'icter!1!': {'-#1#': {'ictero-'}}, '!1!gges': {'#1#ck': {'-s'}}, '!1!an_telescope': {'#1#o': {'-an'}}, 'cryo!1!': {'-#1#': {'cryo-'}}, '!1!vic': {'#1#f': {'-ic'}}, '!1!geal': {'#1#x': {'-al'}}, '!1!sed': {'#1#': {'-ed'}}, 'aden!1!': {'-#1#': {'adeno-'}}, 'r!2!g!1!ian': {'R#2#_G#1#': {'-ian'}}, 'ect!1!': {'-#1#': {'ecto-'}}, '!1!y-cat': {'#1#': {'-y'}}, '!1!ello!2!': {'#1##2#': {'-ous'}}, '!2!!1!t': {'#2#_#1#': {'-ist'}}, '!1!emie': {'#1#mature': {'-ie'}}, '!1!udlian': {'#1#ool': {'puddle'}}, 'therm!1!': {'-#1#': {'therm-'}}, '!1!xie': {'#1#sidential': {'-ie'}}, 'b!1!c_acid': {'B#1#a': {'-ic'}}, '!1!or': {'#1#e': {'-ator'}}, 'lth': {'l': {'-th'}}, 'w!1!y': {'W#1#ington_boot': {'-y'}}, 'chromat!1!': {'-#1#': {'chromato-'}}, 'ir!1!table': {'in#1#': {'-able'}}, 'mero!1!': {'-#1#': {'mero-'}}, '!1!ticidal': {'#1#s': {'-cidal'}}, '!1!brel': {'#1#per': {'-el'}}, 'litho!1!': {'-#1#': {'litho-'}}, 'D!1!id': {'d#1#': {'-oid'}}, 'holo!1!': {'-#1#': {'holo-'}}, 'dipl!1!': {'-#1#': {'diplo-'}}, 'd!1!ic': {'D#1#ae': {'-ic'}}, '!2!!1!nal': {'#2#a#1#': {'-al'}}, 'anthrop!1!': {'-#1#': {'anthropo-'}}, 'chloro!1!': {'-#1#': {'chloro-'}}, '!1!anic': {'#1#in': {'-ic'}}, 'P!1!y': {'p#1#': {'-y'}}, '!1!bean': {'#1#e': {'-an'}}, 'gamo!1!': {'-#1#': {'gamo-'}}, '!1!elike': {'#1#': {'-like'}}, '!1!ian_link': {'#1#': {'-ian'}}, 'dermato!1!': {'-#1#': {'dermato-'}}, 'd!1!an': {'D#1#i': {'-an'}}, 'pithec!1!': {'-#1#': {'pithec-'}}, 'cheil!1!': {'-#1#': {'cheilo-'}}, '!1!knuckling': {'#1#': {'-ing'}}, 'l!1!an': {'L#1#s': {'-an'}}, 'plumb!1!': {'-#1#': {'plumb-'}}, 'rhabd!1!': {'-#1#': {'rhabdo-'}}, 'blast!1!': {'-#1#': {'blasto-'}}, 'Jeanes': {'John': {'-s'}}, 'bread!1!': {'-#1#': {'-th'}}, 'Scadian': {'SCA': {'-ian'}}, '!1!pity': {'#1#': {'-y'}}, '!1!mal': {'#1#': {'-al'}}, 'e!1!c_acid': {'E#1#a': {'-ic'}}, 'peristero!1!ous': {'-#1#': {'-ous'}}, 'l!1!otic': {'L#1#a': {'-otic'}}, 'T!1!ly': {'Mat#1#da': {'-y'}}, '!1!lpots': {'#1#ip': {'-s'}}, 'phyllo!1!': {'-#1#': {'phyllo-'}}, 'commo': {'-o': {'-o'}}, 'R!1!an': {'r#1#en': {'-ian'}}, '!1!-!2!ding': {'#1#_#2#e': {'-ing'}}, 'phyco!1!': {'-#1#': {'phyco-'}}, '!1!t!2!ical': {'#1#c#2#y': {'-ical'}}, 't!1!an': {'T#1#i': {'-an'}}, '!1!tor': {'#1#': {'-ator'}}, '-!1!us': {'#1#': {'-ous'}}, 'o!1!oid': {'O#1#a': {'-oid'}}, 'nan!1!': {'-#1#': {'nano-'}}, 'im!1!able': {'in#1#': {'-able'}}, 'm!1!ist': {'M#1#': {'-ist'}}, 'agro!1!': {'-#1#': {'agro-'}}, 'hydro!1!': {'-#1#': {'hydro-'}}, 'aren!1!': {'-#1#': {'areno-'}}, 'chondro!1!': {'-#1#': {'chondro-'}}, '!1!g!2!': {'#1#p#2#': {'-ie'}}, 'phall!1!': {'-#1#': {'phallo-'}}, 'b!1!y': {'bo#1#': {'-y'}}, '!1!fian': {'#1#': {'-ian'}}, 'd!1!ist': {'D#1#a': {'-ist'}}, 'pterido!1!': {'-#1#': {'pterido-'}}, 'phyto!1!': {'-#1#': {'phyto-'}}, 'somat!1!': {'-#1#': {'somato-'}}, '!1!o!2!y': {'um#1#e#2#a': {'-y'}}, '!2!r!1!': {'#2##1#': {'-ing'}}, 'cyto!1!': {'-#1#': {'cyto-'}}, 'Palladi!1!': {'-#1#': {'-an'}}, 'preter!1!': {'-#1#': {'preter-'}}, '!1!t!2!!3!al': {'#1##2#t#3#': {'-al'}}, '!1!-gooding': {'#1#': {'-ing'}}, 'mega!1!': {'-#1#': {'mega-'}}, 'gameto!1!': {'-#1#': {'gameto-'}}, 'c!1!osis': {'C#1#a': {'-osis'}}, 'tetradelph!1!': {'-#1#': {'tetra-'}}, '!1!ed_out': {'#1#': {'-ed'}}, 'amphi!1!': {'-#1#': {'amphi-'}}, '!1!ioid': {'#1#y': {'-oid'}}, 'ornith!1!': {'-#1#': {'ornitho-'}}, '!1!!2!-like': {'#1#-#2#': {'-like'}}, '!1!os!2!ian': {'#1#-o-S#2#': {'-ian'}}, '!1!ffy': {'#1#venger': {'-y'}}, '!1!gian': {'#1#x': {'-ian'}}, '!1!nability': {'#1#': {'-ability'}}, 'tricho!1!': {'-#1#': {'tricho-'}}, 'thalasso!1!': {'-#1#': {'thalasso-'}}, 'socio!1!': {'-#1#': {'socio-'}}, '!2!w!1!n': {'#2#v#1#': {'-ian'}}, '!1!ulosis': {'#1#le': {'-osis'}}, '!1!lpotts': {'#1#ip': {'-s'}}, 'haplo!1!': {'-#1#': {'haplo-'}}, '!2!-!1!ly': {'#2#_#1#': {'-ly'}}, 'geo!1!': {'-#1#': {'geo-'}}, 'pan!1!': {'-#1#': {'pan-'}}, 'anem!1!': {'-#1#': {'anemo-'}}, 'isolecith!1!': {'-#1#': {'iso-'}}, 'I-ship': {'I': {'-ship'}}, 'ligne!1!': {'-#1#': {'lign-'}}, '!1!ofy': {'#1#u-frou': {'-y'}}, 'lign!1!': {'-#1#': {'lign-'}}, '-!1!c': {'#1#a': {'-ic'}}, 'psychro!1!': {'-#1#': {'psychro-'}}, 'astomat!1!': {'-#1#': {'a-'}}, 'hist!1!': {'-#1#': {'histo-'}}, 'Liddy': {'Lydia': {'-y'}}, '!1!c_acid': {'#1#on': {'-ic'}}, 'strepto!1!': {'-#1#': {'strepto-'}}, 'cyber!1!': {'-#1#': {'cyber-'}}, '!1!fing': {'#1#': {'-ing'}}, 'flimsy': {'film': {'-s'}}, 'Q!1!ie': {'q#1#': {'-ie'}}}
print(len(patterns))

def func(patter,ctr,lock):
        file_path='falsepa_sumeghrc'+str(ctr)+'.csv'
        i=0
        
#     print(type(patter))
#     print(len(patter))
    #with open(file_path, 'w') as outcsv:   
        #
        #writer.writerow(['Affix', 'Source_word', 'Derived_word','sourceSkeleton','targetSkeleton'])
        for p, value in patter.items():
    #         if(i==40):
    #             break
            for q, affixset in value.items():
                pat=[p,q]
                i=0
                print('\n\n')
                print(pat[0])
                print(pat[1])
                print('\n\n')
                for der in glovewords:
                    if(i>2000):
                        break
            #         print(der,end='\t')
                    a=transform(pat,der)
            #         print(a)
                    if a==-1:
                        continue
                    try:
                        i=i+1
                        glovewords[a]
                        for val in affixset: 
                            #writer.writerow([val[1:],a,der,pat[1],pat[0]])
                            #fck=fck+1
                            lock.acquire()
                            outcsv= open(file_path,'a')   #append mode- 'a'
                            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                            writer.writerow([val[1:],a,der,pat[1],pat[0]])
                            
#                             wr.write(str(val[1:]))
#                             wr.write(",")
#                             wr.write(str(a))
#                             wr.write(",")
#                             wr.write(str(der))
#                             wr.write(",")
#                             wr.write(str(pat[1]))
#                             wr.write(",")
#                             wr.write(str(pat[0]))
#                             wr.write("\n")
                            outcsv.close()
                            
                            print(val,end='\t')
                            print(a,end='\t')
                            print(der,end='\t')
                            print(pat[1],end='\t')
                            print(pat[0])
                            lock.release()
                    except KeyError:
                        pass
        #wr.close()            
pats=[]
                    
def chunks(data, SIZE=25):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}
if __name__=='__main__':
    ctr=0
    l=Lock()
    fck=0
    procs=[]
    for item in chunks(patterns,25):
        ctr+=1
        itt={}
        itt.update(item)
        #print('\n\n\n\n\n\n\n\n')
        Process(target=func,args=(itt,ctr,l)).start()
    #procs.append(proc)
    #proc.start()
# for ps in procs:
#     ps.join()
    
#     pats.append(item)                    

#    chunk
    
#  for pp in range(0,43):
#     inps={}
#     inps.update(pats[pp])
#     Process(target=func,args=(inps)).start()

    

