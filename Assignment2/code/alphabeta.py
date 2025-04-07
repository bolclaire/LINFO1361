from agent import Agent
from fenix import FenixState, FenixAction
from observed import ObsFenixState
import random
import time
from collections import namedtuple
from fenix_starting import transpose, filter

depth = 3

Coeff = namedtuple('Coeff',['coeff','dir'])
HeuristicCoeffs = namedtuple('HeuristicCoeffs',\
                                [\
                                'has_king', 'has_king_adv', \
                                'has_general', 'has_general_adv', \
                                'has_soldier', 'has_soldier_adv', \
                                'has_token', 'has_token_adv',\
                                'could_create_king', 'could_create_king_adv',\
                                'could_create_general', 'could_create_general_adv',\
                                'protected_king', 'protected_king_adv',\
                                'protected_general', 'protected_general_adv',\
                                'endang_king', 'endang_king_adv',\
                                'endang_general', 'endang_general_adv',\
                                'endang_soldier', 'endang_soldier_adv',\
                                'mobile_general', 'mobile_general_adv'\
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
    return ('OK : ' + str(coeffs))

def heuristic(coeffs : HeuristicCoeffs, state : ObsFenixState, player : int) :
    p = player
    if (state.utility(p) == 1) :
        return 100
    if (state.utility(p) == -1) :
        return 0
    res = 0
    N = 0
    list = [\
        (coeffs.has_king                 , state.has_king              (p) ),    
        (coeffs.has_king_adv             , state.has_king             (-p) ),    
        (coeffs.has_general              , state.has_general           (p) ),    
        (coeffs.has_general_adv          , state.has_general          (-p) ),    
        (coeffs.has_soldier              , state.has_soldier           (p) ),    
        (coeffs.has_soldier_adv          , state.has_soldier          (-p) ),    
        (coeffs.has_token                , state.has_token             (p) ),    
        (coeffs.has_token_adv            , state.has_token            (-p) ),    
        (coeffs.could_create_king        , state.could_create_king     (p) ),   
        (coeffs.could_create_king_adv    , state.could_create_king    (-p) ),   
        (coeffs.could_create_general     , state.could_create_general  (p) ),   
        (coeffs.could_create_general_adv , state.could_create_general (-p) ),   
        (coeffs.protected_king           , state.protected_king        (p) ),   
        (coeffs.protected_king_adv       , state.protected_king       (-p) ),   
        (coeffs.protected_general        , state.protected_general     (p) ),   
        (coeffs.protected_general_adv    , state.protected_general    (-p) ),   
        (coeffs.endang_king              , state.endang_king           (p) ),   
        (coeffs.endang_king_adv          , state.endang_king          (-p) ),   
        (coeffs.endang_general           , state.endang_general        (p) ),   
        (coeffs.endang_general_adv       , state.endang_general       (-p) ),   
        (coeffs.endang_soldier           , state.endang_soldier        (p) ),   
        (coeffs.endang_soldier_adv       , state.endang_soldier       (-p) ),   
        (coeffs.mobile_general           , state.mobile_general        (p) ),   
        (coeffs.mobile_general_adv       , state.mobile_general       (-p) )    
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
        for action in state.actions:
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
        for action in state.actions:
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

    def __init__(self, player, coeffs:HeuristicCoeffs, starting_policy:list[FenixAction] = None) :
        Agent.__init__(self, player)
        self.coeffs = coeffs
        self.starting_policy = starting_policy
        if (player == -1) :
            self.starting_policy = transpose(self.starting_policy)

    def local_heuristic(self, state, player) :
        return heuristic(self.coeffs, state, player)

    def act(self, state:FenixState, remaining_time):
        # start = time.time()
        if state.turn < 10:
            if (self.starting_policy != None and len(self.starting_policy) == 5) :
                return filter(self.starting_policy[state.turn//2], state.actions())
            return random.choice(state.actions())
        action, _ = minimax(depth, ObsFenixState(state), self.player, True, -float("inf"), float("inf"), self.local_heuristic)
        # print(time.time() - start)
        return action
