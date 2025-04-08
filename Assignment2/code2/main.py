import mcts
import alphabeta
from fenix import FenixAction
from visual_game_manager import *
from game_manager import *

red_win = 0
black_win = 0
# while True:
l1 = [99.543787436251124, 79.3385853692131, 46.079367221239444, 6.904992705715718, 91.62524215350562, 15.406646819410275, 28.67630624830364, 79.34432967920961, 58.2728511119195, 62.7110088690252, 2.3517504625701235, 52.32354657126979, 91.03349863883973, 37.97383474526717, 34.539488418966336, 29.914033425014676, 52.73385434133494, 12.191930361298231, 6.585715520292013, 6.572799042541422, 24.460297043781253, 28.1093497290153, 32.10443965059325, 36.653557758343155]
coeffs1 = alphabeta.HeuristicCoeffs(*[alphabeta.Coeff(l1[i], 1-2*(i%2)) for i in range(len(l1))])

l2 = [46.046469647000386, 94.48714339813093, 79.4955626207432, 76.44007403640273, 66.18995590317242, 98.0832138409852, 66.61007544327292, 9.00519233295477, 70.07474352562446, 58.573260970574836, 48.30829004007373, 3.1259980829838163, 46.98683661715272, 17.55253568900841, 15.563383951759258, 52.315741596660445, 46.218948392758904, 18.044262367733698, 25.02497081625067, 77.34369811909755, 5.2132358935237715, 69.37360710821481, 9.25759323923806, 34.90141812425562]
coeffs2 = alphabeta.HeuristicCoeffs(*[alphabeta.Coeff(l2[i], 1-2*(i%2)) for i in range(len(l2))])

VisualGameManager(red_agent=alphabeta.AlphaBetaAgent(1, coeffs1, [FenixAction((4, 1), (4, 0), frozenset()), FenixAction((0, 0), (0, 1), frozenset()), FenixAction((3, 2), (3, 1), frozenset()), FenixAction((2, 1), (1, 1), frozenset()), FenixAction((1, 0), (1, 1), frozenset())]),
                  black_agent=alphabeta.AlphaBetaAgent(-1, coeffs2, [FenixAction((4, 1), (4, 0), frozenset()), FenixAction((0, 0), (0, 1), frozenset()), FenixAction((3, 2), (3, 1), frozenset()), FenixAction((2, 1), (1, 1), frozenset()), FenixAction((1, 0), (1, 1), frozenset())])).play()
# Rwin, Bwin = TextGameManager(agent_1=agent.MCTS(1, c_param = 1), agent_2=agent.MCTS(-1, c_param = 1.4142), display=False).play()
# red_win += 1 if Rwin == 1 else 0
# black_win += 1 if Bwin == 1 else 0
# print(f"{red_win}/{black_win}")
