from typing import Tuple
import numpy as np
import pandas as pd
from tqdm import tqdm


class Evolver:

    def __init__(self):
        pass

    def generate_initial_population(self, n: int, k: int) -> np.ndarray:
        return np.random.choice([0, 1], size=(n, k))

    def fitness_function(self, chromosome: np.ndarray, S: np.ndarray) -> int:
        return np.sum(S * chromosome)

    def is_viable(self, chromosome: np.ndarray, S: np.ndarray, T: int) -> bool:
        return self.fitness_function(chromosome, S) <= T

    def evaluate_cost(self, chromosome: np.ndarray, S: np.ndarray, T: int) -> int:
        feasible = int(self.is_viable(chromosome, S, T))
        fitness = self.fitness_function(chromosome, S)
        return feasible * (T - fitness) + (1 - feasible) * fitness

    def select_parents(self, population: np.ndarray, S: np.ndarray, T: int) -> Tuple[np.ndarray, np.ndarray]:
        indices = np.random.randint(low=0, high=len(population), size=4)
        selected_chromosomes = population[indices, :]
        selected_costs = [self.evaluate_cost(chromosome, S, T) for chromosome in selected_chromosomes]
        parent1 = selected_chromosomes[np.argmin(selected_costs[:2])]
        parent2 = selected_chromosomes[np.argmin(selected_costs[2:]) + 2]
        return parent1, parent2

    def perform_crossover(self, parent1: np.ndarray, parent2: np.ndarray, S: np.ndarray, prob: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
        r = np.random.random()
        if r <= prob:
            index = np.random.randint(len(S))
            child1 = np.concatenate((parent1[:index + 1], parent2[index + 1:]))
            child2 = np.concatenate((parent2[:index + 1], parent1[index + 1:]))
            return child1, child2
        else:
            return parent1, parent2

    def apply_mutation(self, child1: np.ndarray, child2: np.ndarray, prob: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
        r = np.random.random()
        if r <= prob:
            index_1 = np.random.randint(len(child1))
            index_2 = np.random.randint(len(child2))
            child1[index_1] = 1 - child1[index_1]
            child2[index_2] = 1 - child2[index_2]
        return child1, child2

    def evolve(self, S: np.ndarray, T: int, crossover_probability: float = 0.5, mutation_probability: float = 0.1, population_size: int = 100, num_generations: int = 100):
        best_cost = np.Inf
        best_solution = None
        records = []

        population = self.generate_initial_population(population_size, len(S))
        cost_list = [self.evaluate_cost(chromosome, S, T) for chromosome in population]

        for i in tqdm(range(num_generations)):
            new_population = []
            while len(new_population) < population_size:
                parent1, parent2 = self.select_parents(population, S, T)
                child1, child2 = self.perform_crossover(parent1, parent2, S, crossover_probability)
                child1, child2 = self.apply_mutation(child1, child2, mutation_probability)
                child1_cost = self.evaluate_cost(child1, S, T)
                child2_cost = self.evaluate_cost(child2, S, T)
                if child1_cost < self.evaluate_cost(parent1, S, T):
                    new_population.append(child1)
                else:
                    new_population.append(parent1)
                if child2_cost < self.evaluate_cost(parent2, S, T):
                    new_population.append(child2)
                else:
                    new_population.append(parent2)
            cost_list = [self.evaluate_cost(chromosome, S, T) for chromosome in new_population]
            temp_cost = min(cost_list)
            temp_solution = population[cost_list.index(temp_cost)]
            if temp_cost < best_cost or best_solution is None:
                best_solution = temp_solution
                best_cost = temp_cost
            population = np.array(new_population)
            records.append({'iteration': i, 'best_cost': best_cost, 'best_solution': best_solution})
        
        records = pd.DataFrame(records)
        
        return best_cost, best_solution, records