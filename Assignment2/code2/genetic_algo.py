import random
from game_manager import *
from alphabeta import *
from mcts import MCTS

# Parameters
POP_SIZE = 50
MUTATION_RATE = 0.02
GENERATIONS = 10000
COEFFS_NUMBER = 24
ACTION_NUMBER = 5
FIGHT_NUMBER = 10
MCTS_AGENT = MCTS(1, 1.4142)
Win_Table = []

def base_coeff() -> float:
    return 100*random.random()

def random_action_general() -> FenixAction:
    start_choices = [(i,j) for i in range(6) for j in range(6-i)]
    start = random.choice(start_choices)
    end_choices = [(start[0]+1, start[1]), (start[0], start[1]+1), (start[0]-1, start[1]), (start[0], start[1]-1)]
    end = random.choice(end_choices)
    while (0 > end[0]) or (0 > end[1]) or (end[0] + end[1] > 5):
        end = random.choice(end_choices)
    
    return FenixAction(start, end, frozenset())

def random_action_king() -> tuple[FenixAction, FenixAction]:
    end_choices = [(i,j) for i in range(5) for j in range(5-i)]
    end = random.choice(end_choices)

    start_choices = [(end[0]+1, end[1]), (end[0], end[1]+1), (end[0]-1, end[1]), (end[0], end[1]-1)]
    start1 = random.choice(start_choices)
    while (0 > start1[0]) or (0 > start1[1]) or (start1[0]+start1[1] > 5):
        start1 = random.choice(start_choices)
    
    start2 = random.choice(start_choices)
    while (0 > start2[0]) or (0 > start2[1]) or (start2[0]+start2[1] > 5) or (start1 == start2):
        start2 = random.choice(start_choices)

    # if start1[0] < 0 or start1[1] < 0 or start2[0] < 0 or start2[1] < 0 or end[0] < 0 or end[1] < 0:
    #     print(start1, start2, end)
    
    return [FenixAction(start1, end, frozenset()), FenixAction(start2, end, frozenset())]

def is_compatible(action: FenixAction, list: list[FenixAction|None]) -> bool:
    for item in list:
        if item == None:
            continue
        if action.start == item.start or action.end == item.start or action.start == item.end or action.end == item.end:
            return False
    return True

def random_individual() -> list[HeuristicCoeffs,list[FenixAction]]:
    l = [Coeff(base_coeff(), 1-2*(i%2)) for i in range(COEFFS_NUMBER)]
    res = HeuristicCoeffs(*l)
    
    actions: list[FenixAction|None] = [None] * (ACTION_NUMBER-2)
    for i in range(ACTION_NUMBER-2):
        new_action = random_action_general()
        while not is_compatible(new_action, actions):
            new_action = random_action_general()
        actions[i] = new_action

    
    king_actions = random_action_king()
    while not is_compatible(king_actions[0], actions) or not is_compatible(king_actions[1], actions):
        king_actions = random_action_king()

    return [res, actions + king_actions]

def fitness(i):
    return Win_Table[i]

def select(i: list[int]):
    return max(random.sample(i, 3), key=fitness)

def crossover(parent1, parent2):
    return [HeuristicCoeffs(*[random.choice([parent1[0][i], parent2[0][i]]) for i in range(COEFFS_NUMBER)]), random.choice([parent1[1], parent2[1]])]

# Mutation: randomly change some characters
def mutate(individual) -> list[HeuristicCoeffs,list[FenixAction]]:
    coeffs = [None] * COEFFS_NUMBER
    for i in range(COEFFS_NUMBER):
        if random.random() < MUTATION_RATE:
            coeffs[i] = Coeff(base_coeff(), 1-2*(i%2))
        else:
            coeffs[i] = individual[0][i]
    
    actions = [None] * ACTION_NUMBER
    for i in range(ACTION_NUMBER-2):
        if random.random() < MUTATION_RATE:
            new_action = random_action_general()
            while not is_compatible(new_action, individual[COEFFS_NUMBER:]):
                new_action = random_action_general()
            actions[i] = new_action
        else:
            actions[i] = individual[1][i]
    
    if random.random() < MUTATION_RATE:
        new_actions = random_action_king()
        while not is_compatible(new_actions[0], individual[1]) \
                or not is_compatible(new_actions[1], individual[1]):
            new_actions = random_action_king()
        actions[ACTION_NUMBER-2] = new_actions[0]
        actions[ACTION_NUMBER-1] = new_actions[1]
    else:
        actions[ACTION_NUMBER-2] = individual[1][ACTION_NUMBER-2]
        actions[ACTION_NUMBER-1] = individual[1][ACTION_NUMBER-1]

    return [HeuristicCoeffs(*coeffs), actions]
    

# Run it!
population: list[list[HeuristicCoeffs, list[FenixAction]]] = [random_individual() for _ in range(POP_SIZE)]
for generation in range(GENERATIONS):

    Win_Table = [0 for _ in population]
    p1_agents = [AlphaBetaAgent(1, population[i][0], population[i][1]) for i in range(POP_SIZE)]
    p2_agents = [AlphaBetaAgent(-1, population[i][0], population[i][1]) for i in range(POP_SIZE)]
    for i in range(POP_SIZE):

            for _ in range(FIGHT_NUMBER):
                j = random.randint(0, POP_SIZE-1)
                while i == j:
                    j = random.randint(0, POP_SIZE-1)

                win_p1, win_p2 = TextGameManager(agent_1=p1_agents[i], agent_2=p2_agents[j], display=False).play()
                if win_p1 == 1:
                    Win_Table[i] += 1

                win_p1, win_p2 = TextGameManager(agent_1=p1_agents[j], agent_2=p2_agents[i], display=False).play()
                if win_p2 == 1:
                    Win_Table[i] += 1
            
            # win_p1, win_p2 = TextGameManager(agent_1=MCTS_AGENT, agent_2=p2_agents[i], display=False).play()
            # if win_p2 == 1:
            #     Win_Table[tuple(population[i])] += 8
    
    sorted_indexes = sorted(range(POP_SIZE), key=fitness, reverse=True)
    best = population[sorted_indexes[0]]
    print(f"Gen {generation}: {best} | Fitness: {fitness(sorted_indexes[0])}")
    with open("best_individual.txt", "a") as file:
        file.write(f"Gen {generation}: {best} | Fitness: {fitness(sorted_indexes[0])}\n")
    with open("last_population.txt", "w") as file:
        for individual in population:
            file.write(str(individual) + "\n")

    next_gen = [None] * POP_SIZE
    for i in range(POP_SIZE):
        parent1 = population[select(range(POP_SIZE))]
        parent2 = population[select(range(POP_SIZE))]
        child = crossover(parent1, parent2)
        child = mutate(child)
        next_gen[i] = child
    population = next_gen

with open("best_individual.txt", "a") as file:
    file.write("\n")
