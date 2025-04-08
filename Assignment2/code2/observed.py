from fenix import FenixState, FenixAction

class ObsFenixState:
    def __init__(self, state:FenixState):
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

        # scores compris entre 0 et 1
        # value[0] concerne le player (1), value[1] concerne le player(-1)
        self._has_king                 = [0,0]
        self._has_general              = [0,0]
        self._has_soldier              = [0,0]
        self._has_token                = [0,0]
        self._could_create_king        = [0,0]
        self._could_create_general     = [0,0]
        self._protected_king           = [0,0]
        self._protected_general        = [0,0]
        self._endang_king              = [0,0]
        self._endang_general           = [0,0]
        self._endang_soldier           = [0,0]
        self._mobile_general           = [0,0]
        
        # (peux pas être mentionné avant définition, donc -> #)
        # self.actions
        
        self.compute()
    
    def has_king(self, p):
        return self._has_king[(p+1)==0]
    def has_general(self, p):
        return self._has_general[(p+1)==0]
    def has_soldier(self, p):
        return self._has_general[(p+1)==0]
    def has_token(self, p):
        return self._has_general[(p+1)==0]
    
    def could_create_king(self, p):
        return self._could_create_king[(p+1)==0]
    def could_create_general(self, p):
        return self._could_create_general[(p+1)==0]
    
    def protected_king(self, p):
        return self._protected_king[(p+1)==0]
    def protected_general(self, p):
        return self._protected_general[(p+1)==0]
    
    def endang_king(self, p):
        return self._endang_king[(p+1)==0]
    def endang_general(self, p):
        return self._endang_general[(p+1)==0]
    def endang_soldier(self, p):
        return self._endang_soldier[(p+1)==0]
    
    def mobile_general(self, p):
        return self._mobile_general[(p+1)==0]
    
    # "i" should be in for loop 
    def compute(self) :
        self.actions = self.parent.actions()
        for pos1 in self.pieces :
            i = 0
            piece = self.pieces[pos1]
            if (piece < 0):
                i = 1
                piece = -piece
            self._has_token[i] += piece
            self._has_soldier[i] += (piece==1)
            self._has_general[i] += (piece==2)
            self._has_king   [i] += (piece==3)
        
        for i in range(2) :
            self._has_token  [i] = self._has_token  [i] / 21
            self._has_soldier[i] = self._has_soldier[i] / 12
            self._has_general[i] = self._has_general[i] / 3
            self._has_king   [i] = self._has_king   [i] / 1

        return self
    
    def result(self, action):
        """
        Returns the state that results from applying a given action.

        Args:
            action (FenixAction): The action to apply.

        Returns:
            FenixState: The new game state after the action.
        """
        return ObsFenixState(self.parent.result(action))
    
    def is_terminal(self):
        """
        Determines if the game has reached a terminal state.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.parent.is_terminal()

    def utility(self, player):
        """
        Computes the utility value for the given player.

        Args:
            player (int): The player for whom to calculate the utility (1 or -1).

        Returns:
            int: 1 if the player wins, -1 if the player loses, 0 for a draw or ongoing game.
        """
        return self.parent.utility(player)
    
    def diffusion_factor(self, player) :
        d = 0
        mypos = set()
        for pos in self.pieces :
            if (self.pieces[pos] * player > 0) :
                mypos.add(pos)
        for pos1 in mypos :
            d += min(pos1[0],pos1[1])
            for pos2 in mypos :
                d += abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])
        return d

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