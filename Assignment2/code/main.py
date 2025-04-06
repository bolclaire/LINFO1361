import random_agent
import mcts_agent2 as agent
from game_manager import *

win = 0
total = 0

while True:
    res = TextGameManager(agent_1=agent.MCTS(1), agent_2=random_agent.RandomAgent(-1), display=False).play()
    if res[0] == 1:
        win += 1
    total += 1
    print(f"{win}/{total}")
