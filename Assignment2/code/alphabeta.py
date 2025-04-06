from agent import Agent
import random
from fenix import FenixState, FenixAction
from observed import ObsFenixState

class AlphaBetaAgent(Agent):

    depth = 3

    def act(self, state:FenixState, remaining_time):
        best_action = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        state = ObsFenixState(state)  
        # make it full of deductions

        ###
        if state.turn < 10 :
            return state.actions()[0]
        ###

        for action in state.actions() :
            value = self.min_value(state.result(action), alpha, beta, self.depth - 1)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, value)

        return best_action

    def min_value(self, state:ObsFenixState, alpha, beta, depth):
        if state.is_terminal() or depth == 0:
            return self.evaluate(state)

        value = float('inf')
        for action in state.actions():
            value = min(value, self.max_value(state.result(action), alpha, beta, depth - 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def max_value(self, state:ObsFenixState, alpha, beta, depth):
        if state.is_terminal() or depth == 0:
            return self.evaluate(state)

        value = float('-inf')
        for action in state.actions():
            value = max(value, self.min_value(state.result(action), alpha, beta, depth - 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def evaluate(self, state:ObsFenixState):
        return self.dummy_heuristic(state)
    
    def random_heuristic(self, state:ObsFenixState) :
        return random.randint(-10,10)
    
    def dummy_heuristic(self, state:ObsFenixState) :
        p = self.player
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