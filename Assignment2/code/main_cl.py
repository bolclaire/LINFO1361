from game_manager import TextGameManager

from random_agent import RandomAgent
from mcts import MCTS

from alphabeta import AlphaBetaAgent
from some_heuristics import H0, starting_policy

check1 = lambda p : [RandomAgent(p), AlphaBetaAgent(p, H0, starting_policy, depth=3, max_depth=3)]
check1_str = "[Random, Dummy AlphaBeta]"

def tournoi(agents, contestants = None) :
    print("Tournoi !")
    print(contestants)
    print("=================")

    agent1 = agents(1)
    agent2 = agents(-1)
    n = len(agent1)

    counts = [0]*n
    wins = [0]*n

    while True:
        for i in range(n) :
            for j in range(n) :
                if j != i :
                    l = [0]*n
                    l[i] = 1
                    l[j] = 1
                    print("Match: " + str(l))
                    v,w = TextGameManager(agent1[i], agent2[j], display=False).play()
                    counts[i] += 1
                    counts[j] += 1
                    wins[i] += (v+1)==2
                    wins[j] += (w+1)==2
                    print("Games: " + str(counts))
                    print("Wins : " + str(wins))
                    print("=================")