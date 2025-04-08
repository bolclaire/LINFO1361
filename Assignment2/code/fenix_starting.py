from fenix import FenixAction
import random

"""
!!! dim is assumed (7,8) !!!
"""
dim = (7,8)

def transpose(Action) :
    """
    Transforme une action ou liste d'actions d'un joueur en son symétrique pour le joueur adverse.
    Utile pour la starting_policy.
    Attention : ne traite pas les captures (nouvelle liste vide).
    """
    if (type(Action) == FenixAction) :
        return _transpose(Action)
    if (type(Action) == list) :
        new = []
        for action in Action :
            new.append(_transpose(action))
        return new

def _transpose(action : FenixAction) :
    """
    Transforme une action d'un joueur en son symétrique pour le joueur adverse.
    Utile pour la starting_policy.
    Attention : ne traite pas les captures (nouvelle liste vide).
    """
    start = (dim[0]-1-action.start[0], dim[1]-1-action.start[1])
    end   = (dim[0]-1-action.end  [0], dim[1]-1-action.end  [1])
    removed = None
    return FenixAction(start, end, removed)

def filter(action : FenixAction, actions : list[FenixAction]) :
    for valid_action in actions :
        if (valid_action.start == action.start and valid_action.end == action.end) :
            return valid_action
    print(1)
    return random.choice(actions)