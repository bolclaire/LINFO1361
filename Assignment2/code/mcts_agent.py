from agent import Agent
import random
from math import log, sqrt
from fenix import FenixState, FenixAction
import time

sqrt2 = sqrt(2.)

def random_explore(state: FenixState, player) -> bool:
    while not state.is_terminal():
        actions = state.actions()
        state = state.result(random.choice(actions)) # should change result
    
    return state.utility(player) == 1

# def flatten(state: FenixState):
#     board = [0] * (state.dim[0] * state.dim[1])
#     for position, value in state.pieces.items():
#         board[position[0] * state.dim[1] + position[1]] = value
#     return tuple(board)

class MCTS_Tree:
    def __init__(self, state: FenixState):
        self.state: FenixState = state
        self.actions: list[FenixAction] = state.actions()
        self.childs: list[MCTS_Tree|None] = [None for _ in self.actions]
        self.win = 0
        self.total = 0
    
    def best_child(self, c_param: float = sqrt2) -> int:
        if self.total == 0:
            return 0
        best_index = 0
        best_score = 0

        for i in range(len(self.childs)):
            child = self.childs[i]
            if child == None:
                return i
            else:
                score = (child.win / child.total) + c_param * sqrt(log(self.total) / child.total)
                if score > best_score:
                    best_index = i
                    best_score = score
        
        return best_index
    
    def explore(self, player: int) -> bool:
        best_index = self.best_child()
        if self.childs[best_index] == None:
            self.childs[best_index] = MCTS_Tree(self.state.result(self.actions[best_index]))
            best_child = self.childs[best_index]

            best_child.total += 1
            if random_explore(best_child.state, player):
                best_child.win += 1
                return True
            return False
        else:
            self.total += 1
            if self.childs[best_index].explore(player):
                self.win += 1
                return True
            return False
    
    def best_action(self) -> int:
        action = -1
        max_value = 0
        for i in range(len(self.actions)):
            if self.childs[i] != None:
                value = self.childs[i].win / self.childs[i].total
                if max_value < value:
                    action = i
                    max_value = value
        
        return action
    
    def __str__(self):
        return f"{self.win}/{self.total} : [{len(self.actions)}]"

class MCTS(Agent):
    def __init__(self, player):
        super().__init__(player)
        self.tree: MCTS_Tree = None
        self.last_search_state_list: FenixState = []
        
    def act(self, state: FenixState, remaining_time):
        self.tree = MCTS_Tree(state)
        # if self.tree == None:
        # else:
            # self.tree = self.tree.childs[find_state(self.last_search_hash_list.index())]

        count = 0
        start = time.time()
        while time.time() - start < 5.:
            self.tree.explore(self.player)
            count += 1
        
        print(count)
        # for child in self.tree.childs:
        #     print(child)

        choice_index = self.tree.best_action()
        action = self.tree.actions[choice_index]

        # self.tree = self.tree.childs[choice_index]
        # self.last_search_hash_list = [child.state for child in self.tree.childs]
        return action