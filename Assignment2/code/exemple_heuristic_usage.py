from alphabeta2 import Coeff, HeuristicCoeffs, init_coeffs, mod_coeffs, sanitycheck_coeffs
from alphabeta2 import AlphaBetaAgent
from game_manager import TextGameManager

H1 = init_coeffs()
some_modification = {'has_king' : Coeff(80, 1), 'has_token' : Coeff(20, 1), 'has_general_adv' : Coeff(50, -1)}
H1 = mod_coeffs(H1, some_modification)
resp = sanitycheck_coeffs(H1)
# print(resp)

myagent = AlphaBetaAgent(1, H1)

some_modification = {'has_general' : Coeff(60, 1)}
H2 = mod_coeffs(H1, some_modification)
resp = sanitycheck_coeffs(H2)
# print(resp)

myotheragent = AlphaBetaAgent(-1, H2)

NewGame = TextGameManager(myagent, myotheragent)
NewGame.play()