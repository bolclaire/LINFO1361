import random_agent
import mcts_agent as agent
import alphabeta as agentab
from visual_game_manager import *
from game_manager import *

red_win = 0
black_win = 0
# while True:
VisualGameManager(red_agent=agent.MCTS(1, c_param = 1), black_agent=agentab.AlphaBetaAgent(-1)).play()
# Rwin, Bwin = TextGameManager(agent_1=agent.MCTS(1, c_param = 1), agent_2=agent.MCTS(-1, c_param = 1.4142), display=False).play()
red_win += 1 if Rwin == 1 else 0
black_win += 1 if Bwin == 1 else 0
print(f"{red_win}/{black_win}")
