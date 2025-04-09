from mcts import MCTS
from groupe_150 import AlphaBetaAgent, HeuristicCoeffs, Coeff
from fenix import FenixAction
from visual_game_manager import *
from game_manager import *
from some_heuristics import H2

red_win = 0
black_win = 0
# while True:
# l2 = [46.046469647000386, 94.48714339813093, 79.4955626207432, 76.44007403640273, 66.18995590317242, 98.0832138409852, 66.61007544327292, 9.00519233295477, 70.07474352562446, 58.573260970574836, 48.30829004007373, 3.1259980829838163, 46.98683661715272, 17.55253568900841, 15.563383951759258, 52.315741596660445, 46.218948392758904, 18.044262367733698, 25.02497081625067, 77.34369811909755, 5.2132358935237715, 69.37360710821481, 9.25759323923806, 34.90141812425562]
# coeffs2 = HeuristicCoeffs(*[Coeff(l2[i], 1-2*(i%2)) for i in range(len(l2))])

VisualGameManager(red_agent=AlphaBetaAgent(1),
                  black_agent=MCTS(-1, 1.4142)).play()
# Rwin, Bwin = TextGameManager(agent_1=agent.MCTS(1, c_param = 1), agent_2=agent.MCTS(-1, c_param = 1.4142), display=False).play()
# red_win += 1 if Rwin == 1 else 0
# black_win += 1 if Bwin == 1 else 0
# print(f"{red_win}/{black_win}")
