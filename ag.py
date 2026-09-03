import numpy as np
import random
import matplotlib.pyplot as plt

errors_best=[]
errors_worst=[]
errors_med=[]
QUOTE='GUSTAVO'
TAM_CROMO=len(QUOTE)
TAM_POP=TAM_CROMO*8
taxa_melhor=int(TAM_POP*0.10)

pop_init=np.zeros((TAM_POP,TAM_CROMO))

def init_pop():
    global pop_init, TAM_POP, TAM_CROMO
    for i in range(TAM_POP):
        pop_init[i]=np.random.randint(low=65,high=90,size=TAM_CROMO)

def cruza(dad1,dad2):
    global pop_init, TAM_CROMO
    pos_dad1=dad1
    pos_dad2=dad2
    dad1=pop_init[dad1]
    dad2=pop_init[dad2]
    son1=[0]*TAM_CROMO
    son2=[0]*TAM_CROMO
    random_pos=random.sample(range(1,TAM_CROMO),1)[0]
    for i in range(TAM_CROMO):
        if i in range(random_pos,TAM_CROMO):
            son1[i]=dad1[i]
            son2[i]=dad2[i]
        else:
            son1[i]=dad2[i]
            son2[i]=dad1[i]
    pop_init[pos_dad1]=son1
    pop_init[pos_dad2]=son2

def mk(val_quote,latest_dads):
    global pop_init, TAM_CROMO
    dad1=0
    dad2=0
    aval_dads=[]
    for i in range(TAM_POP):
        if i not in latest_dads:aval_dads.append(i)
    if len(aval_dads)==2:
        return aval_dads[0],aval_dads[1]
    pos=random.sample(aval_dads,4)
    dad1 = pos[0] if val_quote[pos[0]] <= val_quote[pos[1]] else pos[1]
    dad2 = pos[2] if val_quote[pos[2]] <= val_quote[pos[3]] else pos[3]
    return dad1,dad2

def fitness():
    global pop_init, TAM_POP, TAM_CROMO, QUOTE
    val_quote = np.zeros(TAM_POP)
    for i in range(TAM_POP):
        for j in range(TAM_CROMO):
            val_quote[i] += (ord(QUOTE[j]) - pop_init[i][j])**2
    return val_quote

def best_elements(val_quote):
    global pop_init,taxa_melhor
    best=[]
    for i in range(len(pop_init)):
        if i in np.argsort(val_quote)[:taxa_melhor]:best.append(pop_init[i])
    return best

def elitismo(val_quote,best):
    global pop_init,taxa_melhor
    piores=np.argsort(val_quote)[len(val_quote)-taxa_melhor:len(val_quote)]
    pos=0
    idx_eli=[]
    for i in range(len(pop_init)):
        if i in piores:
            pop_init[i]=best[pos]
            idx_eli.append(i)
            pos+=1
    return idx_eli

def mutacao(idx_eli,taxa=0.03):
    global pop_init, TAM_POP, TAM_CROMO
    for i in range(TAM_POP):
        if i in idx_eli:continue
        for j in range(TAM_CROMO):
            if np.random.random() < taxa:
                pop_init[i][j] = np.random.randint(low=65, high=90)

def printar_pop():
    global pop_init
    print(pop_init)

def print_best(val_quote):
    global pop_init,errors_best,errors_worst
    pos_min = np.argmin(val_quote)
    pos_max=np.argmax(val_quote)
    print('Best: ', end='')
    for i in pop_init[pos_min]:
        print(chr(int(i)), end='')
    print(f' | Erro: {val_quote[pos_min]}')
    errors_best.append(val_quote[pos_min])
    errors_worst.append(val_quote[pos_max])
    errors_med.append(np.mean(val_quote))

if __name__=='__main__':
    init_pop()
    ger=0
    latest_dads=[]
    while True:
        latest_dads=[]
        print(f'Geração: {ger}')
        val_quote=fitness()
        print_best(val_quote)
        best=best_elements(val_quote)
        if min(val_quote)==0:break
        while len(latest_dads)!=TAM_POP:
            dad1,dad2=mk(val_quote,latest_dads)
            latest_dads.append(dad1)
            latest_dads.append(dad2)
            cruza(dad1,dad2)
        val_quote=fitness()
        idx_eli=elitismo(val_quote,best)
        mutacao(idx_eli)
        ger+=1

    plt.plot(errors_best,color='green',label='MELHOR')
    plt.plot(errors_med,color='blue',label='MÉDIO')
    plt.plot(errors_worst,color='red',label='PIOR')
    plt.xlabel('Geração')
    plt.ylabel('Erro')
    plt.title('Erro por geração')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()
