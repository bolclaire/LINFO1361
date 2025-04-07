from alphabeta import *

H1 = init_coeffs()
h1 = {\
    'has_king'        : Coeff(100,1),\
    'has_king_adv'    : Coeff(100,-1),\
    'has_general'     : Coeff(80,1),\
    'has_general_adv' : Coeff(70,-1),\
    'has_soldier'     : Coeff(50,1),\
    'has_soldier_adv' : Coeff(60,-1),\
    'has_token'       : Coeff(0,1),\
    'has_token_adv'   : Coeff(0,-1)\
    }
H1 = mod_coeffs(H1, h1)


H2 = init_coeffs()
h2 = {\
    'has_king'        : Coeff(100,1),\
    'has_king_adv'    : Coeff(100, -1),\
    'has_general'     : Coeff(80,1),\
    'has_soldier'     : Coeff(50,1)\
    }
H2 = mod_coeffs(H2, h2)