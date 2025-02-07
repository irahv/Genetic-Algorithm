import numpy as np
import random
import scipy.stats as ss
import math

def decimalToBinary(n:int)-> str:
    """
    Convert a decimal (base-10) number to its binary (base-2) representation.

    Parameters:
    n (int): A non-negative integer to be converted to binary.

    Returns:
    str: A string representing the binary equivalent of the input decimal number.
    
    Example:
    >>> decimalToBinary(10)
    '1010'
    >>> decimalToBinary(255)
    '11111111'
    """
    return bin(n).replace("0b", "")

def binaryToDecimal(n:str)->int:
    """
    Convert a binary (base-2) number (represented as a string) to its decimal (base-10) equivalent.

    Parameters:
    n (str): A string representing a binary number (only contains '0' and '1').

    Returns:
    int: The decimal equivalent of the binary number.

    Example:
    >>> binaryToDecimal('1010')
    10
    >>> binaryToDecimal('11111111')
    255
    """
    return int(n,2)


def cross_over(a: str,b: str,Pc:int) -> tuple[str, str]:
    """
    Perform a crossover operation between two strings `a` and `b` based on a given crossover probability.

    The function randomly chooses a crossover point in the two input strings. If a random value is less 
    than the given probability `Pc` (as a percentage), the two strings are modified by swapping portions 
    of them at a random point. If no crossover occurs, the original strings are returned.

    Parameters:
    a (str): The first string to be used in the crossover.
    b (str): The second string to be used in the crossover.
    Pc (int): The probability of performing the crossover (from 0 to 1).

    Returns:
    tuple: A tuple `(a1, b1)` containing the resulting strings after crossover. If no crossover occurs, 
           the output strings are the same as the input strings `a` and `b`.

    Example:
    >>> cross_over('111000', '000111', 0.70)
    ('111111', '000000')  # Output may vary depending on the random crossover point
    >>> cross_over('111000', '000111', 0.10)
    ('111000', '000111')  # Output will be the same as input if no crossover occurs
    """
    if Pc>float(np.random.uniform(0,1,1)):
        k = random.randint(0,len(a))
        a1 = a[0:k]+ b[k:len(a)]
        b1 = b[0:k] + a[k:len(a)]
    else:
        a1 =a
        b1 =b
    return a1,b1


def mutation(a:str,Pm:int)->str:
    """
    Perform a mutation on a binary string `a` based on a given mutation probability.

    The function randomly selects a position in the binary string and flips the bit (0 to 1 or 1 to 0) 
    with a probability of `Pm`. If no mutation occurs, the original string is returned unchanged.

    Parameters:
    a (str): A binary string (only contains '0' and '1') to be mutated.
    Pm (int): The probability of performing the mutation (from 0 to 1), representing the percentage chance 
              of flipping a bit in the string.

    Returns:
    str: The mutated binary string, or the original string if no mutation occurs.

    Example:
    >>> mutation('101010', 0.70)
    '101000'  # Output may vary based on random mutation point
    >>> mutation('101010', 0.10)
    '101010'  # Output will be the same as input if no mutation occurs
    """
    
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
def objective_func(D,decimal)->float:
    """
    Calculate the objective function value based on a binary input `D` and a scaling factor `decimal`.

    This function first converts the binary string `D` to its decimal equivalent, then normalizes it 
    by dividing by the `decimal` parameter. The normalized value is then used in an equation to 
    compute the objective function value, which is returned.

    Parameters:
    D (str): A binary string representing the input value, which will be converted to a decimal.
    decimal (int): A scaling factor used to normalize the decimal value of `D`.

    Returns:
    float: The result of the objective function, which is a floating-point value based on the 
           calculation involving the normalized value of `D`.

    Example:
    >>> objective_func('1010', 1000)
    655.1255397125103  # Example output based on the input parameters
    """
    D = binaryToDecimal(D)/decimal
    #a = math.sin(D)*math.exp(D)
    try:
        a = 800-62.83*(2*D+0.91*D**-0.2)
    except ZeroDivisionError:
        a = 800
    return a

def fitness_func(a)-> list:
    """
    Calculate the fitness of each individual in the population based on their rank.

    This function ranks the elements of the input list `a` and then normalizes the ranks to form a 
    probability distribution, where each element's rank is divided by the sum of all ranks. This 
    represents the relative fitness of each individual, where higher ranks get higher fitness values.

    Parameters:
    a (list): A list of numeric values representing the individuals in the population to be evaluated.

    Returns:
    list: A list of floats representing the normalized rank of each individual in `a`. The values 
          correspond to the fitness of the individuals, where higher fitness values represent higher 
          ranks.

    Example:
    >>> fitness_func([10, 20, 15, 5])
    [0.1, 0.4, 0.3, 0.2]  # Normalized ranks (fitness values)
    """
    b = ss.rankdata(a)
    b = [i/sum(b) for i in b]
    return b

def binary_fitness_dict(binary_seq,fitness,list_pop):
    """
    Create a dictionary mapping binary sequences to their corresponding fitness values.

    This function takes a list of binary sequences, a list of fitness values, and a population list, 
    and returns a dictionary where each binary sequence is mapped to its respective fitness value. 
    The dictionary is created by pairing elements from the `binary_seq` and `fitness` lists based on 
    their index positions.

    Parameters:
    binary_seq (list): A list of binary sequences (strings) representing the individuals in the population.
    fitness (list): A list of fitness values corresponding to each individual in the population.
    list_pop (list): A list of population individuals (not used directly in this function, but may be part of the overall process).

    Returns:
    dict: A dictionary where the keys are the binary sequences (from `binary_seq`) and the values are 
          the corresponding fitness values (from `fitness`).
    """
    binary_seq_fitness = {}
    for i in range(len(list_pop)):
        binary_seq_fitness.update({binary_seq[i]:fitness[i]})
    return binary_seq_fitness


def tournament(binary_seq,k,fitness,binary_seq_fitness,n)-> list:
    """
    Perform tournament selection to choose individuals from the population based on their fitness.

    This function selects individuals from the population using tournament selection, where a random 
    subset of individuals (of size `k`) is chosen, and the individual with the highest fitness in 
    that subset is selected. The process is repeated `n` times to produce a list of selected individuals.

    Parameters:
    binary_seq (list): A list of binary sequences (strings) representing the individuals in the population.
    k (int): The number of individuals to participate in each tournament (subset size).
    fitness (list): A list of fitness values corresponding to each individual in the population.
    binary_seq_fitness (dict): A dictionary mapping binary sequences to their fitness values.
    n (int): The number of selections (tournaments) to perform.

    Returns:
    list: A list of selected individuals (binary sequences) based on the tournament selection process.
    """
    binary_seq1 = []
    for i in range(n):
        ''' Tournament Selection'''
        K = np.random.choice(binary_seq,size=k,replace=False,p=fitness)
        K = [str(zz) for zz in K]
        K_seq_fitness = [binary_seq_fitness[i] for i in K]
        binary_seq1.append(K[K_seq_fitness.index(max(K_seq_fitness))])
    return binary_seq1



def optimize_function(gen,decimal,n,k,Pc,Pm) -> list:
    """
    Perform the optimization process using a genetic algorithm.

    This function implements a genetic algorithm to optimize a given function over a set number of generations.
    It evolves a population of individuals (represented by binary sequences) through selection, crossover, 
    and mutation operations. The function aims to maximize or minimize an objective function, depending on the 
    problem at hand.

    Parameters:
    gen (int): The number of generations the algorithm will run for.
    decimal (int): A scaling factor used for converting the binary sequences to decimal values.
    n (int): The size of the population (number of individuals).
    k (int): The number of individuals participating in each tournament selection.
    Pc (float): The probability of crossover between pairs of individuals.
    Pm (float): The probability of mutation applied to the population.

    Returns:
    list: A list of binary sequences representing the final population after the optimization process.

    Example:
    >>> result = optimize_function(gen=100, decimal=1024, n=50, k=5, Pc=0.9, Pm=0.05)
    >>> print(result)
    ['101010', '110101', '100101', ...]  # Final population after optimization

    Notes:
    - The function uses a tournament selection mechanism for parent selection.
    - Crossover is applied to pairs of individuals with a probability of `Pc`.
    - Mutation is applied to individuals with a probability of `Pm`.
    - The population evolves over `gen` generations, with each generation consisting of selection, crossover, mutation, 
      and evaluation of the objective function.
    """
    for generation in range(gen):
        if generation==0:
            list_pop = np.random.uniform(1.0, 63,n)
            for_binary_conv= [int(i*decimal) for i in list_pop]
            binary_seq = [decimalToBinary(i) for i  in for_binary_conv]
            len_binary_seq = [len(i) for i in binary_seq]
            binary_seq_clean= []
            
            for i in range(len(binary_seq)):
                binary_seq_clean.append(binary_seq[i].zfill(max(len_binary_seq)))
            
            binary_seq = binary_seq_clean
            objective_val = [objective_func(D,decimal=decimal) for D in binary_seq]
            fitness = fitness_func(objective_val)
            binary_seq_fitness = binary_fitness_dict(binary_seq,fitness,list_pop)
            binary_seq = tournament(binary_seq,k,fitness,binary_seq_fitness,n)
        else:
            
            index = [i for i in range(len(binary_seq)) if i%2==0 ]
            
            cross_seq = [cross_over(binary_seq[i],binary_seq[i+1],Pc) for i in index]
            cross_seq = [j for i in cross_seq for j in i]
            mutate_seq = [mutation(i,Pm) for i in cross_seq]
            binary_seq = mutate_seq
            
            objective_val = [objective_func(D,decimal=decimal) for D in binary_seq]
            fitness = fitness_func(objective_val)
            binary_seq_fitness = binary_fitness_dict(binary_seq,fitness,list_pop)
            binary_seq = tournament(binary_seq,k,fitness,binary_seq_fitness,n)
    return binary_seq