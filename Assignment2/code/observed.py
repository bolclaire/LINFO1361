from fenix import FenixState, FenixAction

class ObsFenixState:
    """
    Represents the (deducible) game state from a Fenix state. All parameters are >=0 and <=1.

    Attributes:

    """
    def __init__(self, state:FenixState):
        """
        Initializes a new ObsFenixState with the configuration of the given state.
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

        # scores compris entre 0 et 1
        # value[0] concerne le player (1), value[1] concerne le player(-1)
        self.has_king                 = [0,0]
        self.has_general              = [0,0]
        self.has_soldier              = [0,0]
        self.has_token                = [0,0]
        self.could_create_general     = [0,0]
        self.could_create_king        = [0,0]
        self.protected_king           = [0,0]
        self.protected_general        = [0,0]
        self.mobile_general           = [0,0]
    
    @staticmethod
    def _get(score, player):
        return score[(player+1)==0]

    def compute(self) :
        i = 0
        for pos1 in self.pieces :
            piece = self.pieces[pos1]
            if (piece < 0):
                i = 1
                piece = -piece
            self.has_token[i] += piece
            self.has_soldier[i] += (piece==1)
            self.has_general[i] += (piece==2)
            self.has_king   [i] += (piece==3)

        #    for pos2 in self.pieces :

        
        for i in range(2) :
            self.has_token  [i] = self.has_token  [i] / 21
            self.has_soldier[i] = self.has_soldier[i] / 12
            self.has_general[i] = self.has_general[i] / 3
            self.has_king   [i] = self.has_king   [i] / 1

        return self
    

    def setup_actions(self): #UL
        actions = []
        for position, value in self.pieces.items():
            if value != self.current_player:
                continue
            for direction_i, direction_j in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                neighbor_position = (position[0] + direction_i, position[1] + direction_j)
                if neighbor_position not in self.pieces:
                    continue
                neighbor_type = self.pieces[neighbor_position]
                if ((neighbor_type == self.current_player and self.count_generals(self.current_player) < 4) or
                    (neighbor_type == 2*self.current_player and not self.has_king(self.current_player))):
                    actions.append(FenixAction(position, neighbor_position, frozenset()))
        return actions

    def get_neighbors_soldier(self, start, end, removed, captured_units): #TOEV
        neighbors = []
        for dir_i, dir_j in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            neighbor_position = (end[0]+dir_i, end[1]+dir_j)
            if not self.is_inside(neighbor_position):
                continue
            if neighbor_position in removed:
                continue
            next_neighbor_position = (neighbor_position[0]+dir_i, neighbor_position[1]+dir_j)
            if (self.pieces.get(neighbor_position, 0) * self.current_player < 0 and
                self.is_inside(next_neighbor_position) and
                next_neighbor_position not in self.pieces):
                neighbors.append((start, next_neighbor_position, removed.union([neighbor_position]), captured_units + abs(self.pieces[neighbor_position])))
                continue
            if captured_units == 0:
                if ((neighbor_position not in self.pieces) or
                    (self.can_create_general and self.pieces[neighbor_position] == self.current_player) or
                    (self.can_create_king and self.pieces[neighbor_position] == 2*self.current_player)):
                    neighbors.append((start, neighbor_position, removed, captured_units))
        return neighbors

    def get_neighbors_general(self, start, end, removed, captured_units): #TOEV
        neighbors = []
        for dir_i, dir_j in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            jumped = False
            jumped_piece = None
            for dist in range(1, 9):
                neighbor_position = (end[0]+(dist*dir_i), end[1]+(dist*dir_j))
                if not self.is_inside(neighbor_position):
                    break
                if (neighbor_position in self.pieces) and (self.pieces[neighbor_position] * self.current_player > 0):
                    break
                if (neighbor_position in removed):
                    break

                if not jumped:
                    if (neighbor_position not in self.pieces) and (captured_units == 0):
                        neighbors.append((start, neighbor_position, removed, captured_units))
                    elif (neighbor_position in self.pieces) and (self.pieces[neighbor_position] * self.current_player < 0):
                        jumped = True
                        jumped_piece = neighbor_position
                else:
                    if (neighbor_position not in self.pieces):
                        neighbors.append((start, neighbor_position, removed.union([jumped_piece]), captured_units + abs(self.pieces[jumped_piece])))
                    elif (neighbor_position in self.pieces) and (self.pieces[neighbor_position] * self.current_player < 0):
                        break
        return neighbors

    def get_neighbors_king(self, start, end, removed, captured_units): #TOEV
        neighbors = []
        for dir_i, dir_j in [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
            neighbor_position = (end[0]+dir_i, end[1]+dir_j)
            if not self.is_inside(neighbor_position):
                continue
            if neighbor_position in removed:
                continue
            next_neighbor_position = (neighbor_position[0]+dir_i, neighbor_position[1]+dir_j)
            if (self.pieces.get(neighbor_position, 0) * self.current_player < 0 and
                self.is_inside(next_neighbor_position) and
                next_neighbor_position not in self.pieces):
                neighbors.append((start, next_neighbor_position, removed.union([neighbor_position]), captured_units + abs(self.pieces[neighbor_position])))
                continue
            if captured_units == 0:
                if neighbor_position not in self.pieces:
                    neighbors.append((start, neighbor_position, removed, captured_units))
        return neighbors

    def get_neighbors(self, start, end, removed, captured_units): #TOEV
        start_type = abs(self.pieces[start])
        if start_type == 1:
            return self.get_neighbors_soldier(start, end, removed, captured_units)
        elif start_type == 2:
            return self.get_neighbors_general(start, end, removed, captured_units)
        elif start_type == 3:
            return self.get_neighbors_king(start, end, removed, captured_units)

    def to_move(self): #UL (redundant)
        """
        Returns the player whose turn it is to move.

        Returns:
            int: The player whose turn it is (1 or -1).
        """
        return self.parent.to_move()

    def actions(self) -> list[FenixAction]: ## personal modification : state specified
        """
        Returns the list of legal actions available in the current state.

        Returns:
            list of FenixAction: The available actions.
        """
        return self.parent.actions()

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

    def _flatten(self): #TOEV
        board = [0 for _ in range(self.dim[0] * self.dim[1])]
        for position, value in self.pieces.items():
            board[position[0] * self.dim[1] + position[1]] = value
        return tuple(board)

    def _hash(self): #TOEV
        if self.precomputed_hash is None:
            self.precomputed_hash = hash(self._flatten())
        return self.precomputed_hash

    class _ActionContainer: #TOEV
        def __init__(self):
            self.actions = []
            self.max_captured_units = 0

        def add(self, action, captured_units):
            if captured_units > self.max_captured_units:
                self.max_captured_units = captured_units
                self.actions = [action]
            elif captured_units == self.max_captured_units:
                self.actions.append(action)

        def get_actions(self):
            return self.actions