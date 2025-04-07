import random
from game_manager import *
from alphabeta import *

# Parameters
POP_SIZE = 25
MUTATION_RATE = 0.01
GENERATIONS = 10000
CRITERION_NUMBER = 8
Win_Table = {}

def list_to_namedtuple(l: list[float]) -> HeuristicCoeffs:
    base_tuple = init_coeffs()
    modif = {}
    modif['has_king']           = Coeff(l[0], 1)
    modif['has_king_adv']       = Coeff(l[1],-1)
    modif['has_general']        = Coeff(l[2], 1)
    modif['has_general_adv']    = Coeff(l[3],-1)
    modif['has_soldier']        = Coeff(l[4], 1)
    modif['has_soldier_adv']    = Coeff(l[5],-1)
    modif['has_token']          = Coeff(l[6], 1)
    modif['has_token_adv']      = Coeff(l[7],-1)

    return mod_coeffs(base_tuple, modif)

def base_value() -> float:
    return 100*random.random()

# Generate a random string
def random_individual():
    return [base_value() for _ in range(8)]

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
    

# Run it!
population = [random_individual() for _ in range(POP_SIZE)]
for generation in range(GENERATIONS):

    Win_Table = {tuple(individual): 0 for individual in population}
    p1_agents = [AlphaBetaAgent(1, list_to_namedtuple(population[i])) for i in range(POP_SIZE)]
    p2_agents = [AlphaBetaAgent(1, list_to_namedtuple(population[i])) for i in range(POP_SIZE)]
    for i in range(POP_SIZE):
        for j in range(i+1, POP_SIZE):
            win_p1, win_p2 = TextGameManager(agent_1=p1_agents[i], agent_2=p2_agents[j], display=False).play()
            if win_p1 == 1:
                Win_Table[tuple(population[i])] += 1
            elif win_p2 == 1:
                Win_Table[tuple(population[j])] += 1

            win_p1, win_p2 = TextGameManager(agent_1=p1_agents[j], agent_2=p2_agents[i], display=False).play()
            if win_p1 == 1:
                Win_Table[tuple(population[j])] += 1
            elif win_p2 == 1:
                Win_Table[tuple(population[i])] += 1
    
    population = sorted(population, key=fitness, reverse=True)
    best = population[0]
    print(f"Gen {generation}: {best} | Fitness: {fitness(best)}")

    with open("best_individual.txt", "a") as file:
        file.write(str(best) + "\n")

    next_gen = []
    for _ in range(POP_SIZE):
        parent1 = select(population)
        parent2 = select(population)
        child = crossover(parent1, parent2)
        child = mutate(child)
        next_gen.append(child)
    population = next_gen

with open("best_individual.txt", "a") as file:
    file.write("\n")