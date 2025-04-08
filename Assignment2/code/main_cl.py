from random_agent import RandomAgent
from mcts import MCTS
from alphabeta import AlphaBetaAgent
from visual_game_manager import VisualGameManager
from game_manager import TextGameManager
from some_heuristics import H1, H2, H3

agent1 = [AlphaBetaAgent(1, H2), AlphaBetaAgent(1, H3), MCTS(1, 1.414213)]
agent2 = [AlphaBetaAgent(-1, H2), AlphaBetaAgent(-1, H3), MCTS(-1, 1.414213)]

n = 3
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