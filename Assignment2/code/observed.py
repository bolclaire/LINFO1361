from fenix import FenixState, FenixAction

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
        # self._endang_king              = [0,0]
        # self._endang_general           = [0,0]
        # self._endang_soldier           = [0,0]
        
        self.compute()
    
    def utility(self, p) :
        """1 ou -1"""
        return self._utility[(p+1)==0]
    
    def has_king(self, p) :
        """1 ou 0"""
        return self._has_king[(p+1)==0]
    def has_general(self, p) :
        """1, 2/3, 1/3 ou 0"""
        return self._has_general[(p+1)==0]
    def has_soldier(self, p) :
        """1, 11/12, 10/12... ou 0"""
        return self._has_general[(p+1)==0]
    def has_token(self, p) :
        """1, 20/21, 19/21... ou 0"""
        return self._has_general[(p+1)==0]
    
    def could_create_king(self, p) :
        """1 ou 0"""
        return self._could_create_king[(p+1)==0]
    def could_create_general(self, p) :
        """1 ou 0"""
        return self._could_create_general[(p+1)==0]
    
    def protected_king(self, p) :
        """
        Protégé sur une ligne 0.4
        Protégé sur une diagonale 0.1
        """
        return self._protected_king[(p+1)==0]
    def protected_general(self, p) :
        """
        Score d'un général :
        Protégé sur une ligne 0.4
        Protégé sur une diagonale 0.1
        score = sum/3
        """
        return self._protected_general[(p+1)==0]
    
    def endangered(self,p) :
        return self._endangered[(p+1)==0]
    
    def mobile_general(self, p) :
        return self._mobile_general[(p+1)==0]
    
    # def endang_king(self, p) :
    #     """1 ou 0"""
    #     return self._endang_king[(p+1)==0]
    # def endang_general(self, p) :
    #     """1, 2/3, 1/3 ou 0"""
    #     return self._endang_general[(p+1)==0]
    # def endang_soldier(self, p) :
    #     """1 ou 0"""
    #     return self._endang_soldier[(p+1)==0]
    
    def sorting_weight(self, action: FenixAction):
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
            self._mobile_general[i] = self._mobile_general[i] / 13
        
        return self
    
    def talk(self) :
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
        # print('endang_king:', self._endang_king)
        # print('endang_general:', self._endang_general)
        # print('endang_soldier:', self._endang_soldier)

    def _is_inside(self, position):
        return 0 <= position[0] < self.dim[0] and 0 <= position[1] < self.dim[1]
    
    def result(self, action):
        return ObsFenixState(self.parent.result(action))

    def __str__(self): #TOEV
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