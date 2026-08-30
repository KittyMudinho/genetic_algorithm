
import numpy as np
import random



QUOTE='GUSTAVO'
TAM_CROMO=len(QUOTE)
TAM_POP=TAM_CROMO*4


pop_init=np.zeros((TAM_POP,TAM_CROMO))

def init_pop():
    global pop_init
    global TAM_POP
    global TAM_CROMO
    for i in range(TAM_POP):
        pop_init[i]=np.random.randint(low=65,high=90,size=TAM_CROMO)

def cruza(dad1,dad2):
    global pop_init
    global TAM_CROMO
    pos_dad1=dad1
    pos_dad2=dad2
    dad1=pop_init[dad1]
    dad2=pop_init[dad2]
    son1=[0]*TAM_CROMO
    son2=[0]*TAM_CROMO
    son1[1]=dad1[1]
    son1[2]=dad1[2]
    son2[1]=dad2[1]
    son2[2]=dad2[2]
    pos=0
    for i in dad2:
        if i not in son1:
            son1[pos]=i
            pos=3
    pos=0
    for i in dad1:
        if i not in son2:
            son2[pos]=i
            pos=3
    pop_init[pos_dad1]=son1
    pop_init[pos_dad2]=son2

def no_rep(dad1,dad2):
    for i in dad1:
        if i in dad2:return False
    return True

def mk(val_quote):
    global pop_init
    dad1=0
    dad2=0
    while True:
        pos=random.sample(range(len(val_quote)),4)
        dad1 = pos[0] if val_quote[pos[0]] <= val_quote[pos[1]] else pos[1]
        dad2 = pos[2] if val_quote[pos[2]] <= val_quote[pos[3]] else pos[3]
        
        if dad1!=dad2 and no_rep(pop_init[dad1],pop_init[dad2])==True:break
    return dad1,dad2

def fitness():
    global pop_init, TAM_POP, TAM_CROMO, QUOTE
    val_quote = np.zeros(TAM_POP)
    for i in range(TAM_POP):
        for j in range(TAM_CROMO):
            val_quote[i] += (ord(QUOTE[j]) - pop_init[i][j])**2
    return val_quote

def mutacao(taxa=0.1):
    global pop_init, TAM_POP, TAM_CROMO
    for i in range(TAM_POP):
        for j in range(TAM_CROMO):
            if np.random.random() < taxa:
                pop_init[i][j] = np.random.randint(low=65, high=90)

def printar_pop():
    global pop_init
    print(pop_init)

def print_best(val_quote):
    global pop_init
    pos_min = np.argmin(val_quote)
    print('Best: ', end='')
    for i in pop_init[pos_min]:
        print(chr(int(i)), end='')
    print(f' | Erro: {val_quote[pos_min]}')

if __name__=='__main__':
    init_pop()
    ger=0
    while True:
        print(f'Geração: {ger}')
        val_quote=fitness()
        print_best(val_quote)
        if min(val_quote)==0:break
        dad1,dad2=mk(val_quote)
        cruza(dad1,dad2)
        mutacao(0.2)
        ger+=1
