from agent import Agent
import random
from math import log, sqrt
from fenix import FenixState, FenixAction
from copy import deepcopy
import time

class MCTS_Tree:
    """
    The tree structure that is used in the exploration of the game tree using mcts
    to store the wins and total game obtained from descending in that direction
    """
    def __init__(self, state: FenixState, c_param = 1.4142, parent = None):
        self.state: FenixState = state
        self.actions: list[FenixAction] = state.actions()
        self.len = len(self.actions)
        self.childs: list[MCTS_Tree|None] = [None] * self.len
        self.parent: MCTS_Tree = parent
        self.win = 0
        self.total = 0
        self.is_fully_extended = False
        self.is_terminal: bool = self.state.is_terminal()
        self.c_param = c_param
    
    def best_child(self, c_param = 1.4142) -> int:
        """
        a function that gives the next node to explore using the basic MCTS logic

        Args:
            c_param (float, optional): the c variable in MCTS where c describes the likelyhood to explore or exploit a certain path. Defaults to 1.4142.

        Returns:
            int: the index of the choosed action to follow
        """
        best_index = 0
        best_score = 0
        for i in range(len(self.childs)):
            child = self.childs[i]
            if child == None:
                return i
            else:
                score = (child.win / child.total) + self.c_param * sqrt(log(self.total) / child.total)
                if score > best_score:
                    best_index = i
                    best_score = score
        
        return best_index
    
    def __str__(self):
        return f"{self.win}/{self.total} : [{len(self.actions)}]"

def defaul_descend(root_state: FenixState, player: int) -> bool:
    """
    a simple loop to find a terminal state to then 

    Args:
        root_state (FenixState): the starting state to start descending the game tree
        player (int): 1 if red player, -1 if black player 

    Returns:
        bool: True if the final state is winning and false otherwise
    """
    state = deepcopy(root_state)
    while not state.is_terminal():
        actions = state.actions()
        # state = state.result(random.choice(actions))
        in_place_result(state, random.choice(actions)) # "IndexError: Cannot choose from an empty sequence" ?????????
    
    return state.utility(player) == 1

def extend(node: MCTS_Tree, player: int) -> bool:
    """
    Changes "node" to add to it a new child while returning the result from the descend of "default_descend"

    Args:
        node (MCTS_Tree): the node to extend
        player (int): 1 if red player, -1 if black player

    Returns:
        bool: True if the final state from "default_descend" is winning and false otherwise
    """
    if node.is_terminal:
        return node.state.utility(player) == 1
    index = node.childs.index(None)
    child = MCTS_Tree(node.state.result(node.actions[index]), node.c_param, node)
    if index+1 == node.len:
        node.is_fully_extended = True
    child.total = 1

    try:
        result = defaul_descend(child.state, player)
    except:
        result = False
    if result:
        child.win = 1
    node.childs[index] = child
    return result

def back_propagation(node: MCTS_Tree, did_win: bool):
    """
    updates all nodes parent from "node" depending on the final result of "default_descend"

    Args:
        node (MCTS_Tree): the leaf node to start the propagation of the result
        did_win (bool): true if the state from "default_descend" was winning, false otherwise
    """
    if did_win:
        while node.parent != None:
            node.win += 1
            node.total += 1
            node = node.parent
        node.win += 1
        node.total += 1
    else:
        while node.parent != None:
            node.total += 1
            node = node.parent
        node.total += 1

def mcts(node: MCTS_Tree, player: int):
    """
    basic logic of the MCTS algorithm

    Args:
        node (MCTS_Tree): the root node
        player (int): 1 if red player, -1 if black player
    """
    while node.is_fully_extended:
        node = node.childs[node.best_child()]
    
    result = extend(node, player)
    back_propagation(node, result)

def in_place_result(state: FenixState, action: FenixAction):
    """
    a pure copy of "FenixState.result" without the copy
    """
    h = hash(state._flatten())

    start = action.start
    end = action.end
    removed = action.removed

    state.pieces[end] = state.pieces.get(end, 0) + state.pieces[start]
    state.pieces.pop(start)

    state.can_create_general = False
    state.can_create_king = False
    for removed_piece in removed:
        removed_piece_type = abs(state.pieces[removed_piece])
        if removed_piece_type == 2:
            state.can_create_general = True
        elif removed_piece_type == 3:
            state.can_create_king = True
        state.pieces.pop(removed_piece)

    state.turn += 1
    state.current_player = -state.current_player

    state.precomputed_hash = None

    if len(removed) > 0:
        state.boring_turn = 0
        state.history_boring_turn_hash = []
    elif state.turn > 10:
        state.boring_turn += 1
        state.history_boring_turn_hash.append(h)

    return state

class MCTS(Agent):
    def __init__(self, player, c_param):
        super().__init__(player)
        self.tree: MCTS_Tree = None
        self.last_hashed_states = []
        self.c_param = c_param
        
    def act(self, state: FenixState, remaining_time):
        try:
            self.tree = self.tree.childs[self.last_hashed_states.index(hash(state._flatten()))]
        except:
            self.tree = MCTS_Tree(state, self.c_param)
            # print("oops, not recovered previous mcts")

        start = time.time()
        count = 0
        while time.time() - start < 1.5:
            mcts(self.tree, self.player)
            count += 1

        # print(count)

        action_index = self.tree.childs.index(max(self.tree.childs, key= lambda child: child.win/child.total))
        action = self.tree.actions[action_index]

        self.tree = self.tree.childs[action_index]
        self.last_hashed_states = [None] * self.tree.len
        for i in range(self.tree.len):
            if self.tree.childs[i] != None:
                self.last_hashed_states[i] = hash(self.tree.childs[i].state._flatten())

        return action
