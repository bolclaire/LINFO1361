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
Win_Table = {}

def list_to_coeffs(l: list[float]) -> HeuristicCoeffs:
    l = [Coeff(l[i], 1-2*(i%2)) for i in range(COEFFS_NUMBER)]
    base_tuple = HeuristicCoeffs(*l)

    # print(base_tuple)
    return base_tuple

def base_coeff() -> float:
    return 100*random.random()

def random_action_general() -> FenixAction:
    start_choices = [(i,j) for i in range(6) for j in range(0,i+1)]
    start = random.choice(start_choices)
    end_choices = [(start[0]+1, start[1]), (start[0], start[1]+1), (start[0]-1, start[1]), (start[0], start[1]-1)]
    end = random.choice(end_choices)
    while 0 > end[0] or end[0] > 5 or (0 > end[1]) or (end[1] > 5):
        end = random.choice(end_choices)
    
    return FenixAction(start, end, frozenset())

def random_action_king() -> tuple[FenixAction, FenixAction]:
    end_choices = [(i,j) for i in range(5) for j in range(0,i+1)]
    end = random.choice(end_choices)

    start_choices = [(end[0]+1, end[1]), (end[0], end[1]+1), (end[0]-1, end[1]), (end[0], end[1]-1)]
    start1 = random.choice(start_choices)
    while (0 > start1[0]) or (0 > start1[1]):
        start1 = random.choice(start_choices)
    
    start2 = random.choice(start_choices)
    while (0 > start1[0]) or (0 > start1[1]) or (start1 == start2):
        start2 = random.choice(start_choices)
    
    return FenixAction(start1, end, frozenset()), FenixAction(start2, end, frozenset())

def is_compatible(action: FenixAction, list: list[FenixAction|None]) -> bool:
    for item in list:
        if item == None:
            return True
        if action.start == item.start or action.end == item.start or action.start == item.end or action.end == item.end:
            return False
    return True

# Generate a random string
def random_individual() -> list[float|FenixAction]:
    res = [base_coeff() for _ in range(COEFFS_NUMBER)]
    actions: list[FenixAction|None] = [None] * (ACTION_NUMBER-2)
    for i in range(ACTION_NUMBER-2):
        new_action = random_action_general()
        while not is_compatible(new_action, actions):
            new_action = random_action_general()
        actions[i] = new_action

    
    king_actions = random_action_king()
    while not is_compatible(king_actions[0], actions) and not is_compatible(king_actions[1], actions):
        king_actions = random_action_king()

    return res + actions + list(king_actions)

# Fitness: number of characters that match the target
def fitness(individual):
    return Win_Table[tuple(individual)]

# Selection: pick 2 individuals via tournament
def select(population):
    return max(random.sample(population, 3), key=fitness)

# Crossover: mix two parents
def crossover(parent1, parent2):
    point = random.randint(0, COEFFS_NUMBER-1)
    return parent1[:point] + parent2[point:]

# Mutation: randomly change some characters
def mutate(individual):
    for i in range(COEFFS_NUMBER):
        if random.random() < MUTATION_RATE:
            individual[i] = base_coeff()
            
    for i in range(ACTION_NUMBER-2):
        if random.random() < MUTATION_RATE:
            new_action = random_action_general()
            while not is_compatible(new_action, individual[COEFFS_NUMBER:]):
                new_action = random_action_general()
            individual[COEFFS_NUMBER+i] = new_action
    
    # if random.random() < MUTATION_RATE:
    new_actions = random_action_king()
    while not is_compatible(new_actions, individual[COEFFS_NUMBER:COEFFS_NUMBER+ACTION_NUMBER-1]):
        new_actions = random_action_king()
    individual[COEFFS_NUMBER+ACTION_NUMBER-2] = new_actions[0]
    individual[COEFFS_NUMBER+ACTION_NUMBER-1] = new_actions[1]

    return individual
    

# Run it!
population = [random_individual() for _ in range(POP_SIZE)]
for generation in range(GENERATIONS):

    Win_Table = {tuple(individual): 0 for individual in population}
    p1_agents = [AlphaBetaAgent(1, list_to_coeffs(population[i]), population[i][COEFFS_NUMBER:]) for i in range(POP_SIZE)]
    p2_agents = [AlphaBetaAgent(-1, list_to_coeffs(population[i]), population[i][COEFFS_NUMBER:]) for i in range(POP_SIZE)]
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

with open("best_individual.txt", "a") as file:
    file.write("\n")