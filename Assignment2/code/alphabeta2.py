from agent import Agent
from fenix import FenixState, FenixAction
from observed import ObsFenixState
import time
from collections import namedtuple

depth = 5

Coeff = namedtuple('Coeff',['coeff','dir'])
HeuristicCoeffs = namedtuple('HeuristicCoeffs',\
                                [\
                                'has_king', 'has_king_adv', \
                                'has_general', 'has_general_adv', \
                                'has_soldier', 'has_soldier_adv', \
                                'has_token', 'has_token_adv'\
                                ]\
                            )

def init_coeffs() :
    return HeuristicCoeffs._make([None]*len(HeuristicCoeffs._fields))

def mod_coeffs(coeffs:HeuristicCoeffs, dict) :
    """
    dict is a dictionary with entries key -> value : 
    field_to_update:string -> new_coeff:HeuristicCoeff
    """
    return coeffs._replace(**dict)

def sanitycheck_coeffs(coeffs:HeuristicCoeffs) :
    for el in coeffs :
        if (el != None) :
            if (el.coeff > 100 or el.coeff < 0) :
                raise ValueError("Heuristic coefficients should be in [0,100]")
            if (abs(el.dir) != 1) :
                raise ValueError("Heuristic coefficients directions should be (1) or (-1)")
    return('OK : ' + str(coeffs))

def heuristic(coeffs : HeuristicCoeffs, state : ObsFenixState, player : int) :
    p = player
    if (state.utility(p) == 1) :
        return 100
    if (state.utility(p) == -1) :
        return 0
    res = 0
    N = 0
    list = [\
        (coeffs.has_king         , state.has_king    (p)),    \
        (coeffs.has_king_adv     , state.has_king   (-p)),    \
        (coeffs.has_general      , state.has_general (p)),    \
        (coeffs.has_general_adv  , state.has_general(-p)),    \
        (coeffs.has_soldier      , state.has_soldier (p)),    \
        (coeffs.has_soldier_adv  , state.has_soldier(-p)),    \
        (coeffs.has_token        , state.has_token   (p)),    \
        (coeffs.has_token_adv    , state.has_token  (-p)),    \
        ]
    for el in list :
        if (el[0] != None) :
            coeff = el[0].coeff
            dir   = el[0].dir
            score = el[1]
            if (dir == -1) :
                score = 1 - score
            N += 1
            res += coeff * score
    return res/N

def minimax(depth: int, state: ObsFenixState, player: int, is_maxing: bool, alpha, beta, evaluate) -> tuple[FenixAction, float]:
    if depth == 0 or state.is_terminal():
        return None, evaluate(state, player) if is_maxing else evaluate(state, -player)
    
    if is_maxing:
        max_eval = -float("inf")
        best_move = None
        for action in state.actions():
            child_board = state.result(action)

            _, eval = minimax(depth-1, child_board, player, not is_maxing, alpha, beta, evaluate)

            if eval > max_eval:
                max_eval = eval
                best_move = action
            
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        return best_move, max_eval
    
    else:
        min_eval = float("inf")
        best_move = None
        for action in state.actions():
            child_board = state.result(action)

            _, eval = minimax(depth-1, child_board, player, not is_maxing, alpha, beta, evaluate)
            
            if eval < min_eval:
                min_eval = eval
                best_move = action

            beta = min(beta, eval)
            if beta <= alpha:
                break

        return best_move, min_eval

class AlphaBetaAgent(Agent):

    def __init__(self, player, coeffs:HeuristicCoeffs) :
        Agent.__init__(self, player)
        self.coeffs = coeffs

    def local_heuristic(self, state, player) :
        return heuristic(self.coeffs, state, player)

    def act(self, state:FenixState, remaining_time):
        start = time.time()
        if state.turn < 10:
            return state.actions()[0]
        move, _ = minimax(3, ObsFenixState(state), self.player, True, -float("inf"), float("inf"), self.local_heuristic)
        print(time.time() - start)
        return move
