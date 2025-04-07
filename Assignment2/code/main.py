import random_agent
import mcts_agent as agent
import alphabeta as agentab
from visual_game_manager import *
from game_manager import *

red_win = 0
black_win = 0
# while True:
l = [70.59303712922738, 76.91004499220043, 14.609115765518233, 35.82213382182533, 46.19763187555361, 75.19539794541124, 40.839966583315956, 83.41675795806043]
coeffs = agentab.HeuristicCoeffs(agentab.Coeff(l[0],-1),
                                 agentab.Coeff(l[1], 1),
                                 agentab.Coeff(l[2],-1),
                                 agentab.Coeff(l[3], 1),
                                 agentab.Coeff(l[4],-1),
                                 agentab.Coeff(l[5], 1),
                                 agentab.Coeff(l[6],-1),
                                 agentab.Coeff(l[7], 1))

VisualGameManager(red_agent=agentab.AlphaBetaAgent(1, coeffs), black_agent=agent.MCTS(-1, 1.4142)).play()
# Rwin, Bwin = TextGameManager(agent_1=agent.MCTS(1, c_param = 1), agent_2=agent.MCTS(-1, c_param = 1.4142), display=False).play()
# red_win += 1 if Rwin == 1 else 0
# black_win += 1 if Bwin == 1 else 0
# print(f"{red_win}/{black_win}")
