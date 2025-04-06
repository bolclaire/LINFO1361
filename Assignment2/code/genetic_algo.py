import random
from game_manager import *
from alphabeta2 import AlphaBetaAgent

# Parameters
POP_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 25
CRITERION_NUMBER = 10
Win_Table = {}

def list_to_namedtuple(l):
    #TODO
    return

def base_value() -> float:
    return 2*random.random()-1

# Generate a random string
def random_individual(length):
    return [base_value() for _ in range(length)]

# Fitness: number of characters that match the target
def fitness(individual):
    return Win_Table[tuple(individual)]

# Selection: pick 2 individuals via tournament
def select(population):
    return max(random.sample(population, 3), key=fitness)

# Crossover: mix two parents
def crossover(parent1, parent2):
    point = random.randint(0, CRITERION_NUMBER-1)
    return parent1[:point] + parent2[point:]

# Mutation: randomly change some characters
def mutate(individual):
    return [
        c if random.random() > MUTATION_RATE else base_value()
        for c in individual
    ]

def get_new_table(population):
    result = {}
    for i in range(GENERATIONS):
        for j in range(i+1, GENERATIONS):
            #TODO
            win_p1, win_p2 = TextGameManager(agent_1=AlphaBetaAgent(-1), agent_2=AlphaBetaAgent(-1)).play()[0]
            if win_p1 == 1:
                result[tuple(population[i])] += 1
            elif win_p2 == 1:
                result[tuple(population[j])] += 1

            #TODO
            win_p1, win_p2 = TextGameManager(agent_1=AlphaBetaAgent(-1), agent_2=AlphaBetaAgent(-1)).play()[0]
            if win_p1 == 1:
                result[tuple(population[j])] += 1
            elif win_p2 == 1:
                result[tuple(population[i])] += 1
    
    return result

# Main loop
def genetic_algorithm():
    population = [random_individual(CRITERION_NUMBER) for _ in range(POP_SIZE)]
    for generation in range(GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        best = population[0]
        print(f"Gen {generation}: {best} | Fitness: {fitness(best)}")

        with open("test.txt", "a") as file:
            file.write(str(best) + "\n")

        next_gen = []
        for _ in range(POP_SIZE):
            parent1 = select(population)
            parent2 = select(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_gen.append(child)
        population = next_gen

# Run it!
genetic_algorithm()