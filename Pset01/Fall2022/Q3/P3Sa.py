import numpy as np
import pandas as pd
from tqdm import tqdm


class GeneticAlgorithm:

    def __init__(self):
        pass

    def random_chromosome_generator(self, n: int) -> np.ndarray:
        return np.random.choice([0, 1], size=n)

    def is_valid_solution(self, chromosome: np.ndarray, S: np.ndarray, T: int) -> bool:
        return np.dot(S, chromosome) <= T

    def mutate_chromosome(self, chromosome: np.ndarray, S: np.ndarray, T: int, mutation_prob: float = 0.5) -> np.ndarray:
        while True:
            mutated_chromosome = chromosome.copy()
            index_1 = np.random.randint(len(mutated_chromosome))
            mutated_chromosome[index_1] = 1 - mutated_chromosome[index_1]
            r = np.random.random()
            if r <= mutation_prob:
                index_2 = np.random.randint(len(mutated_chromosome))
                mutated_chromosome[index_2] = 1 - mutated_chromosome[index_2]
            if self.is_valid_solution(mutated_chromosome, S, T):
                break
        return mutated_chromosome

    def fitness_function(self, chromosome: np.ndarray, S: np.ndarray, T: int) -> int:
        return abs(T - np.dot(S, chromosome))

    def probability_select(self, fitness: int, temperature: float) -> float:
        return np.exp(-fitness / temperature)

    def run_algorithm(self, S: np.ndarray, T: int, mutation_prob: float = 0.5, generations: int = 3000, temperature: float = 30):
        best_cost = np.Inf
        best_solution = None
        records = []

        current_chromosome = self.random_chromosome_generator(len(S))
        best_cost = self.fitness_function(current_chromosome, S, T)
        best_solution = current_chromosome
        temp_decay = temperature / generations

        for i in tqdm(range(generations)):
            mutated_chromosome = self.mutate_chromosome(
                current_chromosome, S, T, mutation_prob)
            current_chromosome_fitness = self.fitness_function(
                current_chromosome, S, T)
            mutated_chromosome_fitness = self.fitness_function(
                mutated_chromosome, S, T)

            if current_chromosome_fitness > mutated_chromosome_fitness:
                current_chromosome = mutated_chromosome
                best_solution = current_chromosome
                best_cost = mutated_chromosome_fitness
            elif np.random.random() <= self.probability_select(current_chromosome_fitness, temperature):
                current_chromosome = mutated_chromosome
                best_solution = current_chromosome
                best_cost = mutated_chromosome_fitness

            temperature -= temp_decay
            records.append({'generation': i, 'best_cost': best_cost,
                            'best_solution': best_solution})

        records_df = pd.DataFrame(records)
        return best_cost, best_solution, records_df


if __name__ == "__main__":
    S = np.array([10, 20, 30, 40, 50])
    T = 100
    mutation_probability = 0.3
    generations = 5000
    initial_temperature = 50

    genetic_algorithm = GeneticAlgorithm()
    best_cost, best_solution, records = genetic_algorithm.run_algorithm(
        S, T, mutation_prob=mutation_probability, generations=generations, temperature=initial_temperature)

    print("Best Cost:", best_cost)
    print("Best Solution:", best_solution)
    print(records)