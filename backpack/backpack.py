import random

class Item:
    def __init__(self, name, value, weight):
        self.name = name
        self.value = value
        self.weight = weight

def generate_random_items(num_items):
    items = []
    for i in range(num_items):
        items.append(Item(f"Item {i+1}", random.randint(1, 100), random.randint(1, 10)))
    return items

def fitness_function(solution, items, max_weight):
    total_value = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_value += items[i].value
            total_weight += items[i].weight
    if total_weight > max_weight:
        return 0
    else:
        return total_value

def generate_initial_population(population_size, num_items):
    population = []
    for _ in range(population_size):
        solution = [random.randint(0, 1) for _ in range(num_items)]
        population.append(solution)
    return population

def mutate(solution, mutation_rate):
    mutated_solution = solution[:]
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            mutated_solution[i] = 1 - mutated_solution[i]
    return mutated_solution

def select_parents(population, fitness_values):
    total_fitness = sum(fitness_values)
    selection_probs = [fitness / total_fitness for fitness in fitness_values]
    parent1_index = random.choices(range(len(population)), weights=selection_probs)[0]
    parent2_index = random.choices(range(len(population)), weights=selection_probs)[0]
    return parent1_index, parent2_index

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def genetic_algorithm(items, max_weight, population_size, mutation_rate, num_generations):
    population = generate_initial_population(population_size, len(items))
    for _ in range(num_generations):
        fitness_values = [fitness_function(solution, items, max_weight) for solution in population]
        sorted_population = [x for _, x in sorted(zip(fitness_values, population), reverse=True)]
        elite_count = int(0.1 * population_size)  # Select top 10% as elite
        next_generation = sorted_population[:elite_count]

        while len(next_generation) < population_size:
            parent1_index, parent2_index = select_parents(population, fitness_values)
            parent1 = population[parent1_index]
            parent2 = population[parent2_index]
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            next_generation.extend([child1, child2])

        population = next_generation

    best_solution = population[0]
    best_fitness = fitness_function(best_solution, items, max_weight)
    return best_solution, best_fitness


random.seed(42)
items = generate_random_items(20)
max_weight = 50
population_size = 100
mutation_rate = 0.1
num_generations = 100
best_solution, best_fitness = genetic_algorithm(items, max_weight, population_size, mutation_rate, num_generations)
print("best decision:", best_solution)
print("best value:", best_fitness)

