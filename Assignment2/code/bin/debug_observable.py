from stash.observed import ObsFenixState
from random_agent import RandomTalkativeAgent
from game_manager import TextGameManager

NewGame = TextGameManager(RandomTalkativeAgent(1), RandomTalkativeAgent(-1))
NewGame.play()