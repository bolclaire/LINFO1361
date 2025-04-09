from alphabeta import *

Heuristic = HeuristicCoeffs(has_king=Coeff(coeff=82.1812244688934, dir=1), has_king_adv=Coeff(coeff=49.02570372606518, dir=-1), has_general=Coeff(coeff=96.29911199857814, dir=1), has_general_adv=Coeff(coeff=16.849241994145125, dir=-1), has_soldier=Coeff(coeff=18.874887430839326, dir=1), has_soldier_adv=Coeff(coeff=21.711743707167408, dir=-1), has_token=Coeff(coeff=78.79578596927323, dir=1), has_token_adv=Coeff(coeff=26.769807461295827, dir=-1), could_create_king=Coeff(coeff=33.702606842400094, dir=1), could_create_king_adv=Coeff(coeff=74.53718168242607, dir=-1), could_create_general=Coeff(coeff=13.581855888621474, dir=1), could_create_general_adv=Coeff(coeff=74.93814014535623, dir=-1), protected_king=Coeff(coeff=8.490477715523326, dir=1), protected_king_adv=Coeff(coeff=96.72066631265544, dir=-1), protected_general=Coeff(coeff=57.54660755432145, dir=1), protected_general_adv=Coeff(coeff=46.50246207916735, dir=-1), endangered=Coeff(coeff=27.156887495630365, dir=1), endangered_adv=Coeff(coeff=54.62372226120063, dir=-1), mobile_general=Coeff(coeff=75.5170835721448, dir=1), mobile_general_adv=Coeff(coeff=9.972974012835733, dir=-1))
Policy = [FenixAction(start=(3, 2), end=(3, 1), removed=frozenset()), FenixAction(start=(4, 1), end=(4, 0), removed=frozenset()), FenixAction(start=(1, 4), end=(1, 3), removed=frozenset()), FenixAction(start=(0, 0), end=(0, 1), removed=frozenset()), FenixAction(start=(1, 1), end=(0, 1), removed=frozenset())]

H0 = init_coeffs()
H0 = mod_coeffs(H0, {'has_king' : Coeff(100,1)})