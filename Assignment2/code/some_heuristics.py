from alphabeta import *

H1 = init_coeffs()
h1 = {
    'has_king'        : Coeff(100,1),
    'has_king_adv'    : Coeff(100,-1),
    'has_general'     : Coeff(80,1),
    'has_general_adv' : Coeff(70,-1),
    'has_soldier'     : Coeff(50,1),
    'has_soldier_adv' : Coeff(60,-1),
    'has_token'       : Coeff(0,1),
    'has_token_adv'   : Coeff(0,-1)
    }
H1 = mod_coeffs(H1, h1)


H2 = init_coeffs()
h2 = {
    'has_king'        : Coeff(100,1),
    'has_king_adv'    : Coeff(100, -1),
    'has_general'     : Coeff(80,1),
    'has_soldier'     : Coeff(50,1)
    }
H2 = mod_coeffs(H2, h2)


# stolen from best_individuals.txt
l = [73.53883823978077, 23.913397441385687, 61.83680266821058, 62.930308662035, 42.317541779535595, 59.98406148162106, 47.07590897054057, 19.724589301871788]
H3 = init_coeffs()
modif = {}
modif['has_king']           = Coeff(l[0], 1)
modif['has_king_adv']       = Coeff(l[1],-1)
modif['has_general']        = Coeff(l[2], 1)
modif['has_general_adv']    = Coeff(l[3],-1)
modif['has_soldier']        = Coeff(l[4], 1)
modif['has_soldier_adv']    = Coeff(l[5],-1)
modif['has_token']          = Coeff(l[6], 1)
modif['has_token_adv']      = Coeff(l[7],-1)

H3 = mod_coeffs(H3, modif)