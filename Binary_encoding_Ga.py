''' My code for genetic algorithm'''
'''maximize Y = 800- 62.83*[2D+0.91*D^-0.2] '''

''' Number of decimal places u wish in the answer'''
#%%

decimal = 10000000

'''Population in a generation '''
n = 100#int(decimal/10)

''' k-way tournament selection'''
''' Enter the value of k below'''
k = 10#int(decimal/100)

'''Number of Generations'''
gen = 50

'''Probability of Cross over '''
Pc = 0.85
''' Probability of Mutation'''
Pm = 0.5


import numpy as np
import random
import scipy.stats as ss
import math

def decimalToBinary(n):
    return bin(n).replace("0b", "")

def binaryToDecimal(n):
    return int(n,2)

''' Cross over'''
def cross_over(a,b,Pc):
    if Pc>float(np.random.uniform(0,1,1)):
        k = random.randint(0,len(a))
        a1 = a[0:k]+ b[k:len(a)]
        b1 = b[0:k] + a[k:len(a)]
    else:
        a1 =a
        b1 =b
    return a1,b1

''' Mutation'''
def mutation(a,Pm):
    if Pm>float(np.random.uniform(0,1,1)):
        a = list(a)
        k = random.randint(0,len(a)-1)
#        print(k)
        if a[k] =='1':
            a[k]='0'
        elif a[k]=='0':
            a[k]='1'
        a =''.join(a)
    else:
        a=a
    return a

''' Rank based fitness function'''
''' Question. WHy we are using rank based fitness ?'''
''' Ans. TO deal with negative fitness values'''
def objective_func(D):
    D = binaryToDecimal(D)/decimal
    #a = math.sin(D)*math.exp(D)
    a = 800-62.83*(2*D+0.91*D**-0.2)
    return a

def fitness_func(a):
    b = ss.rankdata(a)
    b = [i/sum(b) for i in b]
    return b

def binary_fitness_dict(binary_seq,fitness):
    binary_seq_fitness = {}
    for i in range(len(list_pop)):
        binary_seq_fitness.update({binary_seq[i]:fitness[i]})
    return binary_seq_fitness


def tournament(binary_seq,k,fitness,binary_seq_fitness):
    binary_seq1 = []
    for i in range(n):
        ''' Tournament Selection'''
        K = np.random.choice(binary_seq,size=k,replace=False,p=fitness)
        K = [str(zz) for zz in K]
        K_seq_fitness = [binary_seq_fitness[i] for i in K]
        binary_seq1.append(K[K_seq_fitness.index(max(K_seq_fitness))])
    return binary_seq1
   
#%%
for generation in range(gen):
    print(f'Generation {generation}')
    if generation==0:
        list_pop = np.random.uniform(1.0, 63,n)
        for_binary_conv= [int(i*decimal) for i in list_pop]
        binary_seq = [decimalToBinary(i) for i  in for_binary_conv]
        len_binary_seq = [len(i) for i in binary_seq]
        binary_seq_clean= []
        
        for i in range(len(binary_seq)):
            binary_seq_clean.append(binary_seq[i].zfill(max(len_binary_seq)))
        
        binary_seq = binary_seq_clean
        objective_val = [objective_func(D) for D in binary_seq]
        print(sum(objective_val)/len(objective_val))
        fitness = fitness_func(objective_val)
        binary_seq_fitness = binary_fitness_dict(binary_seq,fitness)
        binary_seq = tournament(binary_seq,k,fitness,binary_seq_fitness)
        #print(binary_seq)
    else:
        
        index = [i for i in range(len(binary_seq)) if i%2==0 ]
        
        cross_seq = [cross_over(binary_seq[i],binary_seq[i+1],Pc) for i in index]
        cross_seq = [j for i in cross_seq for j in i]
        mutate_seq = [mutation(i,Pm) for i in cross_seq]
        binary_seq = mutate_seq
        
        objective_val = [objective_func(D) for D in binary_seq]
        print(sum(objective_val)/len(objective_val))
        fitness = fitness_func(objective_val)
        binary_seq_fitness = binary_fitness_dict(binary_seq,fitness)
        binary_seq = tournament(binary_seq,k,fitness,binary_seq_fitness)
        #print(binary_seq)
#%%       
print(binaryToDecimal(binary_seq[1])/decimal)
#%%

