from game_manager import TextGameManager

from random_agent import RandomAgent
from mcts import MCTS

from alphabeta import AlphaBetaAgent
from some_heuristics import *

def tournoi(agent1, agent2, contestants = None) :
    print("Tournoi !")
    print(contestants)
    print("=================")

    n = len(agent1)

    counts = [0]*n
    wins = [0]*n

    while True:
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


my_alphabeta = lambda p,h : AlphaBetaAgent(p, h, starting_policy, depth=3, max_depth=5)
agent1 = []
agent2 = []
for my_heuristic in [H3, H4, H7, H15]:
    agent1.append(my_alphabeta(1, my_heuristic))
    agent2.append(my_alphabeta(-1, my_heuristic))
agent1.append(MCTS(1,1.4142))
agent2.append(MCTS(-1,1.4142))
contestants = "[AlphaBeta-H3, AlphaBeta-H4, AlphaBeta-H7, AlphaBeta-H15, MCTS]"

tournoi(agent1, agent2, contestants)