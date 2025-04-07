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

def update_table(table: list[int], list):
    red_players = [AlphaBetaAgent(1, ) for i in ]

population = [random_individual() for _ in range(POP_SIZE)]
fitness_table = [0 for _ in range(POP_SIZE)]
while True:
    update_table(fitness_table, population)