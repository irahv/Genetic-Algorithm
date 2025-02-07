import os
from src import function_optimize as fo

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

optimal_values = fo.optimize_function(gen=gen,decimal=decimal,n=n,k=k,Pc=Pc,Pm=Pm)
print(int(optimal_values[1],2)/decimal)