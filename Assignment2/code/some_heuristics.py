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
H3 = HeuristicCoeffs(has_king=Coeff(coeff=98.97015270098784, dir=1), has_king_adv=Coeff(coeff=90.24755918524377, dir=-1), has_general=Coeff(coeff=26.4118840340106, dir=1), has_general_adv=Coeff(coeff=91.60985325675675, dir=-1), has_soldier=Coeff(coeff=66.03196141650939, dir=1), has_soldier_adv=Coeff(coeff=97.3074182032409, dir=-1), has_token=Coeff(coeff=85.04899553014418, dir=1), has_token_adv=Coeff(coeff=9.040164787865635, dir=-1), could_create_king=Coeff(coeff=53.771769652841996, dir=1), could_create_king_adv=Coeff(coeff=99.66698048550036, dir=-1), could_create_general=Coeff(coeff=11.760564497117354, dir=1), could_create_general_adv=Coeff(coeff=29.67039546094593, dir=-1), protected_king=Coeff(coeff=15.023760456655399, dir=1), protected_king_adv=Coeff(coeff=51.057662893842334, dir=-1), protected_general=Coeff(coeff=72.0919145613403, dir=1), protected_general_adv=Coeff(coeff=0.2511022759517645, dir=-1), mobile_general=Coeff(coeff=59.655342414043055, dir=1), mobile_general_adv=Coeff(coeff=51.19732747689507, dir=-1), endangered=None, endangered_adv=None)