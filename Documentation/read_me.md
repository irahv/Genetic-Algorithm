```
# Assumptions for the Genetic Algorithm:

1. **Equal Population Across Generations**: 
   - It is assumed that the population size remains constant across all generations. Each generation will contain an equal number of individuals, ensuring consistency in the evolutionary process.


2. **Crossover and Mutation Based on Hyperparameters**: 
   - The rates of crossover (Pc) and mutation (Pm) are determined by the respective hyperparameters. These values control the probability of these operations being applied during the evolutionary process:
     - **Crossover (Pc)**: This defines the probability that two parent individuals will undergo crossover to create offspring.
     - **Mutation (Pm)**: This defines the probability of introducing random mutations to an individual during the evolution.


3. **Tournament Selection for Parent Selection**: 
   - A tournament selection method is employed, where a fixed number of individuals (k) are randomly selected from the population. The best individual from this subset, based on fitness, is chosen as a parent for the next generation's reproduction process. This selection strategy introduces competition and diversity into the population.

4. **Termination Condition Based on Generation Limit**: 
   - The algorithm will terminate once the predefined generation limit is reached, signaling that the evolutionary process has concluded. This limit acts as a stopping criterion, preventing the algorithm from running indefinitely and ensuring that the search for optimal solutions remains finite and manageable.

5. **Optimization Goal**:
   - The algorithm aims to optimize the objective function within the given number of generations. Although the focus is on generating better solutions with each generation, the process is bound by the specified generation count.
```