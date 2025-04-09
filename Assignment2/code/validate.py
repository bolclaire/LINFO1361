from game_manager import TextGameManager

from random_agent import RandomAgent
from mcts import MCTS

from alphabeta import AlphaBetaAgent
from final_heuristics import Heuristic, Policy

from final_heuristics import H0

def tournoi(agent1, agent2, contestants = None, n_iter = 100) :
    print("Tournoi !")
    print(contestants)
    print("=================")

    n = len(agent1)

    counts = [0]*n
    wins = [0]*n

    for _ in range(n_iter) :
        for i in range(n) :
            for j in range(n) :
                if (i!=j) :
                    l = [-1]*n
                    l[i] = 1
                    l[j] = 2
                    print("Match: " + str(l))
                    v,w = TextGameManager(agent1[i], agent2[j], display=False).play()
                    counts[i] += 1
                    counts[j] += 1
                    wins[i] += (v+1)==2
                    wins[j] += (w+1)==2
                    print("Games: " + str(counts))
                    print("Wins : " + str(wins))
                    print("=================")


my_alphabeta = AlphaBetaAgent(1, Heuristic, starting_policy=Policy)
my_random = RandomAgent(-1)
my_mcts = MCTS(-1, 1.4142)

import numpy as np
time = []
n_iter = 10
for i in range(n_iter) :
    print("Alpha vs Random")
    v,w = TextGameManager(my_alphabeta, my_random, display=False).play()
    time.append(my_alphabeta.time/my_alphabeta.n)
    print(f"{my_alphabeta.n} tours, t_tot = {my_alphabeta.time}")
    my_alphabeta.n = 0
    my_alphabeta.time = 0
moy = np.sum(time)/n_iter
sigma = np.sqrt(np.var(time))
print(f"Temps moyen d'un tour = {moy}, ecart-type = {sigma}")

alpha_contre_mcts = [0,0]
n_iter = 3

for i in range(n_iter) :
    print("Alpha vs MCTS")
    v,w = TextGameManager(my_alphabeta, my_mcts, display=False).play()
    alpha_contre_mcts[0] += (v==1)
    alpha_contre_mcts[1] += (w==1)
    print(alpha_contre_mcts)