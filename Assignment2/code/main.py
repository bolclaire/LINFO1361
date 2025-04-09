from mcts import MCTS
from alphabeta import AlphaBetaAgent, HeuristicCoeffs, Coeff
from fenix import FenixAction
from visual_game_manager import *
from game_manager import *
from some_heuristics import H2

red_win = 0
black_win = 0
# while True:
p1 = [HeuristicCoeffs(has_king=Coeff(coeff=82.1812244688934, dir=1), has_king_adv=Coeff(coeff=49.02570372606518, dir=-1), has_general=Coeff(coeff=96.29911199857814, dir=1), has_general_adv=Coeff(coeff=16.849241994145125, dir=-1), has_soldier=Coeff(coeff=18.874887430839326, dir=1), has_soldier_adv=Coeff(coeff=21.711743707167408, dir=-1), has_token=Coeff(coeff=78.79578596927323, dir=1), has_token_adv=Coeff(coeff=26.769807461295827, dir=-1), could_create_king=Coeff(coeff=33.702606842400094, dir=1), could_create_king_adv=Coeff(coeff=74.53718168242607, dir=-1), could_create_general=Coeff(coeff=13.581855888621474, dir=1), could_create_general_adv=Coeff(coeff=74.93814014535623, dir=-1), protected_king=Coeff(coeff=8.490477715523326, dir=1), protected_king_adv=Coeff(coeff=96.72066631265544, dir=-1), protected_general=Coeff(coeff=57.54660755432145, dir=1), protected_general_adv=Coeff(coeff=46.50246207916735, dir=-1), endangered=Coeff(coeff=27.156887495630365, dir=1), endangered_adv=Coeff(coeff=54.62372226120063, dir=-1), mobile_general=Coeff(coeff=75.5170835721448, dir=1), mobile_general_adv=Coeff(coeff=9.972974012835733, dir=-1)), [FenixAction(start=(3, 2), end=(3, 1), removed=frozenset()), FenixAction(start=(4, 1), end=(4, 0), removed=frozenset()), FenixAction(start=(1, 4), end=(1, 3), removed=frozenset()), FenixAction(start=(0, 0), end=(0, 1), removed=frozenset()), FenixAction(start=(1, 1), end=(0, 1), removed=frozenset())]]

# l2 = [46.046469647000386, 94.48714339813093, 79.4955626207432, 76.44007403640273, 66.18995590317242, 98.0832138409852, 66.61007544327292, 9.00519233295477, 70.07474352562446, 58.573260970574836, 48.30829004007373, 3.1259980829838163, 46.98683661715272, 17.55253568900841, 15.563383951759258, 52.315741596660445, 46.218948392758904, 18.044262367733698, 25.02497081625067, 77.34369811909755, 5.2132358935237715, 69.37360710821481, 9.25759323923806, 34.90141812425562]
# coeffs2 = HeuristicCoeffs(*[Coeff(l2[i], 1-2*(i%2)) for i in range(len(l2))])

VisualGameManager(red_agent=AlphaBetaAgent(1, p1[0], p1[1]),
                  black_agent=MCTS(-1, 1.4142)).play()
# Rwin, Bwin = TextGameManager(agent_1=agent.MCTS(1, c_param = 1), agent_2=agent.MCTS(-1, c_param = 1.4142), display=False).play()
# red_win += 1 if Rwin == 1 else 0
# black_win += 1 if Bwin == 1 else 0
# print(f"{red_win}/{black_win}")
