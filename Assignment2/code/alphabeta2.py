from agent import Agent
from fenix import FenixState, FenixAction
from observed import ObsFenixState
import random
import time

depth = 5
def evaluate(state: ObsFenixState, player: int):
    return dummy_heuristic(state, player)

def dummy_heuristic(state:ObsFenixState, player) :
    p = player
    a = 5
    b = 100
    c = 0
    d = -100
    e = 10000
    f = 10000
    value =  a * (1/state.diffusion_factor(p)) \
        + b * state.has_piece(p)\
        + c * state.diffusion_factor(-p)\
        + d * state.has_piece(-p)\
        + e * state.has_king(p)\
        + f * (state.has_king(-p) == False)
    
    # generaux et roi proches du bord
    return value

def minimax(depth: int, state: ObsFenixState, player: int, is_maxing: bool, alpha, beta) -> tuple[FenixAction, float]:
    if depth == 0 or state.is_terminal():
        return None, evaluate(state, player) if is_maxing else evaluate(state, -player)
    
    if is_maxing:
        max_eval = -float("inf")
        best_move = None
        for action in state.actions():
            child_board = state.result(action)

            _, eval = minimax(depth-1, child_board, player, not is_maxing, alpha, beta)

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

            _, eval = minimax(depth-1, child_board, player, not is_maxing, alpha, beta)
            
            if eval < min_eval:
                min_eval = eval
                best_move = action

            beta = min(beta, eval)
            if beta <= alpha:
                break

        return best_move, min_eval

class AlphaBetaAgent(Agent):
    def act(self, state:FenixState, remaining_time):
        start = time.time()
        state = ObsFenixState(state)

        if state.turn < 10:
            return random.choice(state.actions())
        action, _ = minimax(3, ObsFenixState(state), self.player, True, -float("inf"), float("inf"))
        print(time.time() - start)
        return action
