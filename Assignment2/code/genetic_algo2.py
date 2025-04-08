import random
from game_manager import *
from alphabeta import *
from mcts_agent import MCTS

# Parameters
POP_SIZE = 50
MUTATION_RATE = 0.01
GENERATIONS = 10000
COEFFS_NUMBER = 24
ACTION_NUMBER = 5
FIGHT_NUMBER = 5
MCTS_AGENT = MCTS(1, 1.4142)

def base_coeff() -> float:
    return 100*random.random()

def random_individual():
    l = [Coeff(l[i]) for i in range(COEFFS_NUMBER)]
    base_tuple = HeuristicCoeffs(*l)

def update_table(population, table: list[int]):
    Win_Table = {tuple(individual): 0 for individual in population}
    p1_agents = [AlphaBetaAgent(1, population[i][0], population[i][1]) for i in range(POP_SIZE)]
    p2_agents = [AlphaBetaAgent(-1, population[i][0], population[i][1]) for i in range(POP_SIZE)]
    for i in range(POP_SIZE):

            for _ in range(FIGHT_NUMBER):
                j = random.randint(0, POP_SIZE-1)
                while i == j:
                    j = random.randint(0, POP_SIZE-1)

                win_p1, win_p2 = TextGameManager(agent_1=p1_agents[i], agent_2=p2_agents[j], display=False).play()
                if win_p1 == 1:
                    Win_Table[tuple(population[i])] += 1

                win_p1, win_p2 = TextGameManager(agent_1=p1_agents[j], agent_2=p2_agents[i], display=False).play()
                if win_p2 == 1:
                    Win_Table[tuple(population[i])] += 1
            
            # for _ in range(3):
            #     win_p1, win_p2 = TextGameManager(agent_1=MCTS_AGENT, agent_2=p2_agents[i], display=False).play()
            #     if win_p2 == 1:
            #         Win_Table[tuple(population[i])] += 3

def update_population(population, table: list[int]):
    population = sorted(population, key=fitness, reverse=True)
    best = population[0]
    print(f"Gen {generation}: {best} | Fitness: {fitness(best)}")
    with open("best_individual.txt", "a") as file:
        file.write(f"Gen {generation}: {best} | Fitness: {fitness(best)}\n")

    next_gen = []
    for _ in range(POP_SIZE):
        parent1 = select(population)
        parent2 = select(population)
        child = crossover(parent1, parent2)
        child = mutate(child)
        next_gen.append(child)
    population = next_gen

population = [random_individual() for _ in range(POP_SIZE)]
fitness_table = [0 for _ in range(POP_SIZE)]
while True:
    update_table(population, fitness_table)
    update_population(population, fitness_table)