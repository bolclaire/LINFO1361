from alphabeta import AlphaBetaAgent
from some_heuristics import H2 as H
from fenix import FenixAction
from visual_game_manager import VisualGameManager

# defined for player 1
starting_policy =     [FenixAction((0,0), (0,1), None)]
starting_policy.append(FenixAction((1,0), (2,0), None))
starting_policy.append(FenixAction((0,2), (0,1), None))
starting_policy.append(FenixAction((2,3), (2,4), None))
starting_policy.append(FenixAction((2,1), (1,1), None))

""""
To know about starting policy : 
-> a starting policy is by default for the red agent (top left corner)
-> transpose is always from the top left corner (red agent) to the bottom right corner (black agent)
-> a filtering is applied (is the action valid ?), if not, a random valid action will be selected
-> transpose is done inside the AlphaBetaAgent class when player == -1
"""

agent1 = AlphaBetaAgent(1, H, starting_policy=starting_policy)
agent2 = AlphaBetaAgent(-1, H, starting_policy=starting_policy)

NewGame = VisualGameManager(agent1, agent2)
NewGame.play()