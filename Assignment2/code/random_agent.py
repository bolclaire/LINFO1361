from agent import Agent
import random
import fenix
from observed import ObsFenixState

class RandomAgent(Agent):
    def act(self, state, remaining_time):
        actions = state.actions()
        if len(actions) == 0:
            raise Exception("No action available.")
        return random.choice(actions)

class RandomTalkativeAgent(Agent):
    def act(self, state, remaining_time):
        actions = state.actions()
        if len(actions) == 0:
            raise Exception("No action available.")
        print(ObsFenixState(state).talk())
        input("Press Enter to continue.")
        return random.choice(actions)