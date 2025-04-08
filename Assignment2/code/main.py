from mcts import MCTS
from alphabeta import AlphaBetaAgent, HeuristicCoeffs, Coeff
from fenix import FenixAction
from visual_game_manager import *
from game_manager import *
from some_heuristics import H2

red_win = 0
black_win = 0
# while True:
p1 = [HeuristicCoeffs(has_king=Coeff(coeff=98.97015270098784, dir=1), has_king_adv=Coeff(coeff=90.24755918524377, dir=-1), has_general=Coeff(coeff=26.4118840340106, dir=1), has_general_adv=Coeff(coeff=91.60985325675675, dir=-1), has_soldier=Coeff(coeff=66.03196141650939, dir=1), has_soldier_adv=Coeff(coeff=97.3074182032409, dir=-1), has_token=Coeff(coeff=85.04899553014418, dir=1), has_token_adv=Coeff(coeff=9.040164787865635, dir=-1), could_create_king=Coeff(coeff=53.771769652841996, dir=1), could_create_king_adv=Coeff(coeff=99.66698048550036, dir=-1), could_create_general=Coeff(coeff=11.760564497117354, dir=1), could_create_general_adv=Coeff(coeff=29.67039546094593, dir=-1), protected_king=Coeff(coeff=15.023760456655399, dir=1), protected_king_adv=Coeff(coeff=51.057662893842334, dir=-1), protected_general=Coeff(coeff=72.0919145613403, dir=1), endangered=Coeff(coeff=0.2511022759517645, dir=1), endangered_adv=Coeff(coeff=0.2511022759517645, dir=-1), protected_general_adv=Coeff(coeff=0.2511022759517645, dir=-1), mobile_general=Coeff(coeff=59.655342414043055, dir=1), mobile_general_adv=Coeff(coeff=51.19732747689507, dir=-1)), [FenixAction(start=(3, 0), end=(2, 0), removed=frozenset()), FenixAction(start=(4, 1), end=(3, 1), removed=frozenset()), FenixAction(start=(1, 1), end=(1, 0), removed=frozenset()), FenixAction(start=(1, 3), end=(0, 3), removed=frozenset()), FenixAction(start=(0, 4), end=(0, 3), removed=frozenset())]]

l2 = [46.046469647000386, 94.48714339813093, 79.4955626207432, 76.44007403640273, 66.18995590317242, 98.0832138409852, 66.61007544327292, 9.00519233295477, 70.07474352562446, 58.573260970574836, 48.30829004007373, 3.1259980829838163, 46.98683661715272, 17.55253568900841, 15.563383951759258, 52.315741596660445, 46.218948392758904, 18.044262367733698, 25.02497081625067, 77.34369811909755, 5.2132358935237715, 69.37360710821481, 9.25759323923806, 34.90141812425562]
coeffs2 = HeuristicCoeffs(*[Coeff(l2[i], 1-2*(i%2)) for i in range(len(l2))])

VisualGameManager(red_agent=AlphaBetaAgent(1, H2, p1[1]),
                  black_agent=MCTS(-1, 1.4142)).play()
# Rwin, Bwin = TextGameManager(agent_1=agent.MCTS(1, c_param = 1), agent_2=agent.MCTS(-1, c_param = 1.4142), display=False).play()
# red_win += 1 if Rwin == 1 else 0
# black_win += 1 if Bwin == 1 else 0
# print(f"{red_win}/{black_win}")
