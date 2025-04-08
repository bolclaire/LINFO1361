from utils import *

agent = lambda p : [RandomAgent(p), AlphaBetaAgent(p, H0, None, depth=3)]
n = 2

agent1 = agent(1)
agent2 = agent(-1)
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