import random
from collections import namedtuple
from agent import Agent
from fenix import FenixState, FenixAction

# group 150:
# Claire Boland
# Ioannis Chrissantakis

Coeff = namedtuple('Coeff',['coeff','dir'])
HeuristicCoeffs = namedtuple('HeuristicCoeffs',
                                [
                                'has_king', 'has_king_adv', 
                                'has_general', 'has_general_adv', 
                                'has_soldier', 'has_soldier_adv', 
                                'has_token', 'has_token_adv',
                                'could_create_king', 'could_create_king_adv',
                                'could_create_general', 'could_create_general_adv',
                                'protected_king', 'protected_king_adv',
                                'protected_general', 'protected_general_adv',
                                'endangered', 'endangered_adv',
                                'mobile_general', 'mobile_general_adv'
                                ]
                            )


class ObsFenixState:
    """
    Represents the (deducible) game state from a Fenix state.
    """
    def __init__(self, state:FenixState):
        """
        Initializes a new ObsFenixState with the configuration of the given state and additional computations.
        """
        self.parent                   = state
        self.dim                      = state.dim
        self.pieces                   = state.pieces
        self.turn                     = state.turn
        self.current_player           = state.current_player
        self.can_create_general       = state.can_create_general
        self.can_create_king          = state.can_create_king
        self.precomputed_hash         = state.precomputed_hash
        self.history_boring_turn_hash = state.history_boring_turn_hash
        self.boring_turn              = state.boring_turn

        # inherited from FenixState (pre-computation)
        self.is_terminal              = state.is_terminal()
        self.actions                  = state.actions()

        # scores compris entre 0 et 1
        # value[0] concerne le player (1), value[1] concerne le player(-1)
        self._utility                  = [state.utility(1), state.utility(-1)]
        self._has_king                 = [0,0]
        self._has_general              = [0,0]
        self._has_soldier              = [0,0]
        self._has_token                = [0,0]
        self._could_create_king        = [0,0]
        self._could_create_general     = [0,0]
        self._protected_king           = [0,0]
        self._protected_general        = [0,0]
        self._endangered               = [0,0]
        self._mobile_general           = [0,0]
        
        self.compute()
    
    def utility(self, p) :
        """the utilitity associated to the player in a terminal state"""
        return self._utility[(p+1)==0]
    
    def has_king(self, p) :
        """1 if true or 0 if false"""
        return self._has_king[(p+1)==0]
    def has_general(self, p) :
        """the number of generals divided by its maximum number: 1, 2/3, 1/3 or 0"""
        return self._has_general[(p+1)==0]
    def has_soldier(self, p) :
        """the number of sodier divided by its maximum number: 1, 11/12, 10/12... or 0"""
        return self._has_general[(p+1)==0]
    def has_token(self, p) :
        """the number of tokens divided by its maximum number: 1, 20/21, 19/21... or 0"""
        return self._has_general[(p+1)==0]
    
    def could_create_king(self, p) :
        """1 if true or 0 if false"""
        return self._could_create_king[(p+1)==0]
    def could_create_general(self, p) :
        """1 if true or 0 if false """
        return self._could_create_general[(p+1)==0]
    
    def protected_king(self, p) :
        """
        score of a king:
        protected on a line 0.4
        protected on a diagonal 0.1
        """
        return self._protected_king[(p+1)==0]
    def protected_general(self, p) :
        """
        score of a general :
        protected on a line 0.4
        protected on a diagonal 0.1
        score = sum/3
        """
        return self._protected_general[(p+1)==0]
    
    def endangered(self,p) :
        """1 if the following action results in piece removal, 0 otherwise"""
        return self._endangered[(p+1)==0]
    
    def mobile_general(self, p) :
        """the number of possible moves by a general divided by its maximum"""
        return self._mobile_general[(p+1)==0]
    
    def sorting_weight(self, action: FenixAction):
        """
        associates each action with a value to allow easy sorting of the actions
        """
        if action.removed: # no sorting for capture moves
            return 0
        if abs(self.parent.pieces.get(action.start, 0)) == 1:
            if abs(self.parent.pieces.get(action.end, 0)) == 1:
                return 3
            if abs(self.parent.pieces.get(action.end, 0)) == 2:
                return 4
            return 0
        if abs(self.parent.pieces.get(action.start, 0)) == 2:
            return 2 + (abs(action.end[0] - action.start[0]) + abs(action.end[1] - action.start[1]))/10
        if abs(self.parent.pieces.get(action.start, 0)) == 3:
            return 1
        return 0
    
    def compute(self) :
        """all the calculations needed by the heureristics"""
        self.actions.sort(key = self.sorting_weight, reverse=True)
        
        if (not self.is_terminal) and (len(self.actions[0].removed) > 0) :
            self._endangered[-self.current_player] = 1

        for pos1 in self.pieces :
            i = 0
            p1 = self.pieces[pos1]
            if (p1 < 0):
                i = 1
            self._has_token  [i] += abs(p1)
            self._has_soldier[i] += (abs(p1)==1)
            self._has_general[i] += (abs(p1)==2)
            self._has_king   [i] += (abs(p1)==3)

            for pos2 in self.pieces :
                p2 = self.pieces[pos2]
                if (abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1]) == 1) :  # pos1 and pos2 are adjacent
                    if (p1*p2 == 1) :
                        self._could_create_general[i] = 1
                    if (p1*p2 == 2) :
                        self._could_create_king   [i] = 1

            if (abs(p1) == 2 or abs(p1) == 3) :
                x,y = pos1[0],pos1[1]
                adj = [[(x-1,y),(x+1,y)],
                       [(x,y-1),(x,y+1)]]
                diag = [[(x+1,y+1),(x-1,y-1)],
                        [(x+1,y-1),(x-1,y+1)]]
                for a in adj :
                    if ((a[0] in self.pieces and self.pieces[a[0]]*p1 > 0) or (a[1] in self.pieces and self.pieces[a[1]]*p1 > 0)) or not self._is_inside(a[0]) or not self._is_inside(a[1]) :
                        self._protected_general[i] += 0.4*(abs(p1)==2)
                        self._protected_king   [i] += 0.4*(abs(p1)==3)
                for d in diag :
                    if ((d[0] in self.pieces and self.pieces[d[0]]*p1 > 0) or (d[1] in self.pieces and self.pieces[d[1]]*p1 > 0)) or not self._is_inside(d[0]) or not self._is_inside(d[1]) :
                        self._protected_general[i] += 0.1*(abs(p1)==2)
                        self._protected_king   [i] += 0.1*(abs(p1)==3)
                if (abs(p1) == 2) :
                    for action in self.actions :
                        if (action.start == pos1) :
                            self._mobile_general[i] += 1
        
        for i in range(2) :
            self._has_token  [i] = self._has_token  [i] / 21, 1
            self._has_soldier[i] = min(self._has_soldier[i] / 12, 1)
            self._has_general[i] = min(self._has_general[i] / 3, 1)
            self._protected_general[i] = min(self._protected_general[i] / 3, 1)
            self._mobile_general[i] = self._mobile_general[i] / (3*13)
        
        return self
    
    def talk(self) :
        """a printing of all the calculated information contained in the state"""
        print('ObsFenixState')
        print('current_player:', self.current_player)
        print('players       :', [1,-1])
        print('has_king      :', self._has_king)
        print('has_general   :', self._has_general)
        print('has_soldier   :', self._has_soldier)
        print('has_token     :', self._has_token)
        print('could_create_king   :', self._could_create_king)
        print('could_create_general:', self._could_create_general)
        print('protected_king      :', self._protected_king)
        print('protected_general   :', self._protected_general)
        print('endangered          :', self._endangered)
        print('mobile_general:', self._mobile_general)
        
    def _is_inside(self, position):
        return 0 <= position[0] < self.dim[0] and 0 <= position[1] < self.dim[1]
    
    def result(self, action):
        return ObsFenixState(self.parent.result(action))

    def __str__(self):
        s = '-' * (self.dim[1] * 5 + 1) + '\n'
        for i in range(0, self.dim[0]):
            local_s = '|'
            for j in range(0, self.dim[1]):
                if (i, j) in self.pieces:
                    local_s += f' {self.pieces[(i, j)]:2} |'
                else:
                    local_s += '    |'
            s += local_s + '\n'
            s += '-' * (self.dim[1] * 5 + 1) + '\n'
        return s

##########################################################################################
##########################################################################################
##########################################################################################

def transpose(action_list: list[FenixAction]) -> list[FenixAction]:
    """
    transforms the setup actions of the red player into ones of the black player and vice-versa
    """
    if (action_list == None) :
        return None
    corner = (6,7) # dim = (7,8)
    return [FenixAction((corner[0]-action.start[0], corner[1]-action.start[1]), (corner[0]-action.end[0], corner[1]-action.end[1]), frozenset()) for action in action_list]

def init_coeffs() :
    """
    initiates a HeuristicsCoeffs with all of its values set to None 
    """
    return HeuristicCoeffs._make([None]*len(HeuristicCoeffs._fields))

def mod_coeffs(coeffs:HeuristicCoeffs, dict) :
    """
    dict is a dictionary with entries key -> value : 
    field_to_update:string -> new_coeff:HeuristicCoeff
    """
    return coeffs._replace(**dict)

def sanitycheck_coeffs(coeffs:HeuristicCoeffs) :
    """
    checks if the coeffs are in the right format
    """
    for el in coeffs :
        if (el != None) :
            if (el.coeff > 100 or el.coeff < 0) :
                raise ValueError("Heuristic coefficients should be in [0,100]")
            if (abs(el.dir) != 1) :
                raise ValueError("Heuristic coefficients directions should be (1) or (-1)")
    return ('OK : ' + str(coeffs))

##########################################################################################
##########################################################################################
##########################################################################################

def heuristic(coeffs : HeuristicCoeffs, state : ObsFenixState, p : int) :
    """
    returns an evaluation of the advantage of the state given 
    the weighting of the small heuristics and the current state
    """
    if (state.is_terminal) :
        return (1001*state.utility(p))
    res = 0
    N = 0
    list = [
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
        (coeffs.endangered               , state.endangered            (p) ),
        (coeffs.endangered_adv           , state.endangered           (-p) ),
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
            N += (coeff != 0)
            res += coeff * score
    return res/N

class AlphaBetaAgent(Agent):
    def __init__(self,
                 player,
                 coeffs:HeuristicCoeffs = HeuristicCoeffs(has_king=Coeff(coeff=80.12188716475654, dir=1), has_king_adv=Coeff(coeff=85.59443623550513, dir=-1), has_general=Coeff(coeff=52.333004654395324, dir=1), has_general_adv=Coeff(coeff=16.849241994145125, dir=-1), has_soldier=Coeff(coeff=18.874887430839326, dir=1), has_soldier_adv=Coeff(coeff=32.078369148632746, dir=-1), has_token=Coeff(coeff=88.07926433613996, dir=1), has_token_adv=Coeff(coeff=26.769807461295827, dir=-1), could_create_king=Coeff(coeff=33.702606842400094, dir=1), could_create_king_adv=Coeff(coeff=9.624691120971995, dir=-1), could_create_general=Coeff(coeff=13.795532670542087, dir=1), could_create_general_adv=Coeff(coeff=74.93814014535623, dir=-1), protected_king=Coeff(coeff=2.7883226514197945, dir=1), protected_king_adv=Coeff(coeff=96.72066631265544, dir=-1), protected_general=Coeff(coeff=57.54660755432145, dir=1), protected_general_adv=Coeff(coeff=49.353569262848595, dir=-1), endangered=Coeff(coeff=27.156887495630365, dir=1), endangered_adv=Coeff(coeff=28.155754601907734, dir=-1), mobile_general=Coeff(coeff=10.210648463990257, dir=1), mobile_general_adv=Coeff(coeff=60.424551710019834, dir=-1)),
                 starting_policy:list[FenixAction] = [FenixAction(start=(3, 2), end=(3, 1), removed=frozenset()), FenixAction(start=(4, 1), end=(4, 0), removed=frozenset()), FenixAction(start=(1, 4), end=(1, 3), removed=frozenset()), FenixAction(start=(0, 0), end=(0, 1), removed=frozenset()), FenixAction(start=(1, 1), end=(0, 1), removed=frozenset())],
                 depth=4,
                 max_depth=7
                ):
        """
        the initialisation of the AlphaBetaAgent
        """
        Agent.__init__(self, player)
        self.init_depth = depth
        self.max_depth = max_depth
        self.coeffs = coeffs
        if (player == 1):
            self.starting_policy = starting_policy
        else:
            self.starting_policy = transpose(starting_policy)
        self.heuristic = lambda state : heuristic(self.coeffs, state, self.player)
        
    def act(self, base_state: FenixState, remaing_time):
        """
        given a state, returns the action 
        """
        state = ObsFenixState(base_state)
        if state.turn < 10 and self.starting_policy != None :
            return self.setup_turns(state)
        elif len(state.actions) == 1:
            return state.actions[0]
        else:
            action, _ = self.minimax(self.max_depth, state, True, float("-inf"), float("inf"))
            return action
    
    def setup_turns(self, state:ObsFenixState):
        """
        returns the action for the setup turns if defined, or a random move if not
        """
        action = self.starting_policy[state.turn//2]
        for state_action in state.actions:
            if action.start == state_action.start and action.end == state_action.end:
                return state_action
        return random.choice(state.actions)

    def minimax(self, depth: int, state: ObsFenixState, is_maxing: bool, alpha, beta) -> tuple[FenixAction, float]:
        """
        a pure implementation of the minimax algorithm with alpha-beta pruning
        """

        if state.is_terminal :
            return None, self.heuristic(state)

        if depth <= self.max_depth - self.init_depth :
            if not state.actions[0].removed:
                depth = 0

        if depth == 0:
            return None, self.heuristic(state)
        
        if is_maxing:
            max_eval = float("-inf")
            best_move = None
            for action in state.actions:
                child_board = state.result(action)

                _, eval = self.minimax(depth-1, child_board, False, alpha, beta)

                if eval > max_eval:
                    max_eval = eval
                    best_move = action
                
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break
            
            return best_move, max_eval
        
        else:
            min_eval = float("inf")
            best_move = None
            for action in state.actions:
                child_board = state.result(action)

                _, eval = self.minimax(depth-1, child_board, True, alpha, beta)
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = action

                beta = min(beta, eval)
                if alpha >= beta:
                    break

            return best_move, min_eval